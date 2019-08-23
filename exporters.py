"""
Item Exporters are used to export/serialize items into sqlite3 database.
"""

from scrapy.exporters import BaseItemExporter
import sqlite3


class SqliteItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.conn = sqlite3.connect(file.name)
        self.conn.text_factory = str
        self.created_tables = []

    def export_item(self, item):
        print(item.__class__)
        item_class_name = type(item).__name__

        if item_class_name not in self.created_tables:
            keys = None
            if hasattr(item, "keys"):
                sqlite_keys = list(item.keys())

            pk = None
            for field_name in item:
                field = {} if isinstance(item, dict) else item.fields[field_name]
                is_pk = field.get("primary_key", False)
                if is_pk:
                    pk = field_name
                    break

            self._create_table(
                item_class_name, pk, iter(item.fields.keys()), sqlite_keys
            )
            self.created_tables.append(item_class_name)

        field_list = []
        value_list = []
        for field_name in item.keys():
            field_list.append("[%s]" % field_name)
            field = item.fields[field_name]
            value_list.append(self.serialize_field(field, field_name, item[field_name]))

        sql = "insert or ignore into [%s] (%s) values (%s)" % (
            item_class_name,
            ", ".join(field_list),
            ", ".join(["?" for f in field_list]),
        )
        self.conn.execute(sql, value_list)
        self.conn.commit()

    def _create_table(self, table_name, pk, columns, keys=None):
        sql = "create table if not exists [%s] " % table_name

        column_define = ["[%s] text" % column for column in columns]
        print("type: %s" % type(keys))
        if pk is not None:
            primary_key = "primary key ({})".format(pk)
            column_define.append(primary_key)
        elif keys:
            if len(keys) > 0:
                primary_key = "primary key ({})".format(keys[0])
                column_define.append(primary_key)

            # for key in keys[1:]:
            # column_define.append('unique (%s)' % ', '.join(key))

        sql += "(%s)" % ", ".join(column_define)

        print("sql: %s" % sql)
        self.conn.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
