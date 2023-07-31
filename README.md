# DynAPI
Dynamic API for (postgresql) Databases

> Please don't install/use this tool yet. It's not developed enough.

## Installation

### Archive (.tgz)

```bash
tar -xf dynapi-{x.x.x}.tgz
cd dynapi
cp api.conf.template api.conf
# edit api.conf
(opt) mv dynapi.service /etc/systemd/system/
./dynapi.run
```


## Documentation

```bash
./scripts/serve-docs
```

# Body
```json5
{
  "columns": ["string"],  // what columns to select in an GET request
  "filter": [
    [
      ["key", "operation", "value"],["key", "operation", "value"] //inner brackets == AND
    ],
    [
      ["[key]", "op", "[value]"] //inner brackets == AND
    ] //outer brackets==OR
  ],
  "object": {
    "[key]": "[value]" //used for PUT and POST columns + values
  },
  "affected": 1,  // checks number of objects affected, if not number or in range of numbers then fail the request
  // "affected": [5, 10],  // this format is also possible
}
```
# Valid Filter operators:
`==`, `=`, `eq`, `!=`, `not`, `>`, `>=`, `<`, `<=`, `glob`, `like`
