#!/usr/bin/env bash
########################################################################################################################
# This plugin-manager is a limited version of the dynapi-plugin-manager and is meant for simple automated control over #
# the plugins on a deployed dynapi-build. It is recommended to use the standard plugin-manager and create a customised #
# build for your specific needs. Otherwise use the [plugins] section in api.conf to control which plugins are loaded.  #
########################################################################################################################
set -e
shopt -s nullglob  # dont return the glob-pattern if nothing found
THIS="$(realpath "$(dirname "$(realpath "$0")")")"
cd "$THIS"

# ensure the folders are present
mkdir -p plugins
mkdir -p plugins-disabled

FGG="\e[32m"
FGR="\e[31m"
FGY="\e[33m"
FG="\e[39m"

function get_width() {
  COLUMNS=$(tput cols)
  echo $((COLUMNS > 80 ? 80 : COLUMNS))
}

function print_centered() {
  COLS=$(get_width)
  padding="$(printf '%0.1s' ={1..500})"
  printf '%*.*s %s %*.*s\n' 0 "$(((COLS-2-${#1})/2))" "$padding" "$1" 0 "$(((COLS-1-${#1})/2))" "$padding"
}

function error() {
    echo -e -n "${FGR}Error:${FG} "
    echo "$@"
}

function warn() {
    echo -e -n "${FGY}Warning:${FG} "
    echo "$@"
}

function format_plugin_info() {
    folder=$(dirname "${1}")
    name="${folder#"${2}/"}"
    output=$"$(print_centered "${name}")\n"

    if [ -d plugins/"${name////_}" ]; then
      output+=$"Status: ${FGG}active${FG}\n"
    else
      output+=$"Status: ${FGR}inactive${FG}\n"
    fi

    if [ -f "$folder/description" ]; then
      output+=$"$(cat "${folder}/description")\n"
    fi

    if [ -f "$folder/dependencies" ]; then
      output+="
Dependencies:
$(sed 's/^/- /' "${folder}/dependencies")
"
    fi

    echo "$output"
}

function list_plugins() {
  listed=""

  for module in plugins/*/__init__.py; do
    output=$(format_plugin_info "$module" plugins)

    if [ "$1" ] && ! (echo "$output" | grep -iq "$1"); then
      continue
    fi

    listed+="
$(echo -e "$output" | fold -sw "$(get_width)" | grep --color=always -iE "$1|$")
"
  done

  for module in plugins-disabled/*/__init__.py; do
    output=$(format_plugin_info "$module" plugins-disabled)

    if [ "$1" ] && ! (echo "$output" | grep -iq "$1"); then
      continue
    fi

    listed+="
$(echo -e "$output" | fold -sw "$(get_width)" | grep --color=always -iE "$1|$")
"
  done

  echo "$listed" | less -R
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

function enable_all_plugins() {
  for plugin in plugins-disabled/*; do
    enable_plugin "$plugin"
  done
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

function disable_all_plugins() {
  for plugin in plugins/*; do
    disable_plugin "$plugin"
  done
}

function print_help() {
  echo "plugin-manager {help,enable,disable}"
  echo "plugin-manager help"
  echo "    shows this message"
  echo "plugin-manager list [query]"
  echo "    list plugins and their status"
  echo "plugin-manager enable <plugin-name>"
  echo "    enable a plugin to be loaded"
  echo "plugin-manager disable <plugin-name>"
  echo "    disable a plugin to be loaded"
}

case "$1" in
"list" | "list-plugins")
  list_plugins "${@:2}"
;;
"enable")
  enable_plugin "${@:2}"
;;
"enable-all")
  enable_all_plugins "${@:2}"
;;
"disable")
  disable_plugin "${@:2}"
;;
"disable-all")
  disable_all_plugins "${@:2}"
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
