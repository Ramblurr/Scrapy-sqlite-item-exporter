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

By default the primary key is chosen more or less at random, since the order of
keys in the dictionary is not guaranteed.

To hint to the exporter which field should be a primary key define your Item
class with a field containing `primary_key` key with a value of `True.


**Example:**

```python
class CheeseItem(scrapy.Item):

  id = scrapy.Field(primary_key=True)
  name = scrapy.Field()
  stinkyness = scrapy.Field(serializer=int)


```
