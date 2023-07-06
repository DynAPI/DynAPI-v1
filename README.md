# DynAPI
Dynamic API for (postgresql) Databases

## Todo
yaml files for routes.meta

## Endpoints

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
