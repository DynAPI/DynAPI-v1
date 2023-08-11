#!/usr/bin/env bash
########################################################################################################################
# This plugin-manager is a limited version of the dynapi-plugin-manager and is meant for simple automated control over #
# the plugins on a deployed dynapi-build. It is recommended to use the standard plugin-manager and create a customised #
# build for your specific needs. Otherwise use the [plugins] section in api.conf to control which plugins are loaded.  #
########################################################################################################################
set -e
THIS="$(realpath "$(dirname "$(realpath "$0")")")"
cd "$THIS"

# ensure the folders are present
mkdir -p plugins
mkdir -p plugins-disabled

FGR="\e[31m"
FGY="\e[33m"
FG="\e[39m"

function error() {
    echo -e -n "${FGR}Error:${FG} "
    echo "$@"
}

function warn() {
    echo -e -n "${FGY}Warning:${FG} "
    echo "$@"
}

function enable_plugin() {
  plugin="${1////_}"
  if [ ! -d plugins-disabled/"$plugin" ]; then
    if [ ! -d plugins/"$plugin" ]; then
      error "Plugin '$plugin' doesn't exist"
      return 1
    else
      warn "Plugin '$plugin' is already enabled"
      return 0
    fi
  fi
  mv plugins-disabled/"$plugin" plugins/"$plugin"
  echo "Plugin '$plugin' was enabled"
}

function disable_plugin() {
  plugin="${1////_}"
  if [ ! -d plugins/"$plugin" ]; then
    if [ ! -d plugins-disabled/"$plugin" ]; then
      error "Plugin '$plugin' doesn't exist"
      return 1
    else
      warn "Plugin '$plugin' is already disabled"
      return 0
    fi
  fi
  mv plugins/"$plugin" plugins-disabled/"$plugin"
  echo "Plugin '$plugin' was disabled"
}

function print_help() {
  echo "plugin-manager {help,enable,disable}"
  echo "plugin-manager help"
  echo "    shows this message"
  echo "plugin-manager enable <plugin-name>"
  echo "    enable a plugin to be loaded"
  echo "plugin-manager disable <plugin-name>"
  echo "    disable a plugin to be loaded"
}

case "$1" in
"enable")
  enable_plugin "${@:2}"
;;
"disable")
  disable_plugin "${@:2}"
;;
"help" | "--help")
  print_help "${@:2}"
;;
*)
  warn "Unknown command '$1'"
  print_help
  exit 1
;;
esac
