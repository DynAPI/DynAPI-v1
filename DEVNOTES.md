# Development Notes

## Endpoints

```bash
/
/redoc
/swagger
/openapi
/docs/*
/api/*
/api/db/{schema}/{table}

/api/meta/{schema}/{table}/columns
/api/meta/
=> schemas
/api/meta/{schama}/
=> tables
/api/db
```

```
/api
=> schemas []
/api/{schema}
=> table []
/api/{schema}?meta
/api/{schema}/{table}/
/api/{schema}/{table}/column
```

```bash
/list-tables
# [customer,setup,system]
/list-columns/{schema}/{table}
# [id,name,created]
/list-table-meta
# {"customer": [id,name,created]}
/select/{schema}/{table}?name=SSW&__resolved__=true&__max__=100
# []
/select/{schema}/{table}/{id}
# {}
```
172.20.13.183 / 184
## Meta and Documentation

```
/status
/openapi
/redoc
/swagger
```

## Background

```sql
SELECT * FROM pg_catalog.pg_tables;
```

```sql
SELECT *
  FROM information_schema.columns
 WHERE table_schema = 'your_schema'
   AND table_name   = 'your_table'
```


# Body

```json5
{
  "resolve_depth": 0,
  "columns": ["string"],
  "filter": [
    [
      ["key", "op", "value"]
    ]
  ],
  "object": {
    "key": "any"
  },
  "affected": 1,  // 
}
```


```json
filters=[["id", "==", "0"], "or", [[["id", "==", "0"], "and", [["id", "==", "0"]]]]]
```
