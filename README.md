# scrapy-sqlite-item-exporter

Export items to sqlite3 database.

**Requires:**

* python >= 3.5

**Tested on:**

* scrapy == 1.7.3

## How to use

1. Place `exporters.py` in your scrapy project directory
2. In settings.py add:

    ```python
    FEED_EXPORTERS = {
        'sqlite': '<script directory>.exporters.SqliteItemExporter',
    }
    ```

3. In a terminal execute the crawl:

```console
$ scrapy crawl <spider name> -o sqlite.db -t sqlite
```

## Extra features


### primary key
By default the primary key is chosen more or less at random, since the order of
keys in the dictionary is not guaranteed.

To hint to the exporter which field should be a primary key define your Item
class with a field containing `primary_key` key with a value of `True`.


See example.

### Column Type

By default all fields are created as `TEXT` columns. Hint to the exporter which
column a field should be by specifying `sql_type`.

See example.

### Examples

```python
class CheeseItem(scrapy.Item):
  id = scrapy.Field(primary_key=True)
  name = scrapy.Field()
  stinkyness = scrapy.Field(serializer=int)
  crawled_at = scrapy.Field(sql_type="timestamp")
```


This item class produces the following schema:

```sql
CREATE TABLE [CheeseItem] ([name] text, [id] text, [crawled_at] timestamp, [stinkyness] text, primary key (id));
```
