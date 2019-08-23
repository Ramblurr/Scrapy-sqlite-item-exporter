"""
Item Exporters are used to export/serialize items into sqlite3 database.
"""

from scrapy.exporters import BaseItemExporter
import sqlite3


def get_field(item, field_name):
    return {} if isinstance(item, dict) else item.fields[field_name]


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
            self._create_table(item_class_name, item)
            self.created_tables.append(item_class_name)

        field_list = []
        value_list = []
        for field_name in item.keys():
            field_list.append("[%s]" % field_name)
            field = get_field(item, field_name)
            value_list.append(self.serialize_field(field, field_name, item[field_name]))

        sql = "insert or ignore into [%s] (%s) values (%s)" % (
            item_class_name,
            ", ".join(field_list),
            ", ".join(["?" for f in field_list]),
        )
        print("SQL: ", sql)
        print("VLIST", value_list)
        self.conn.execute(sql, value_list)
        self.conn.commit()

    def _create_table(self, table_name, item):
        sql = "create table if not exists [%s] " % table_name
        pk = None
        col_types = {}
        for field_name in item:
            field = get_field(item, field_name)
            is_pk = field.get("primary_key", False)
            if is_pk:
                pk = field_name
            sql_type = field.get("sql_type", "text")
            col_types[field_name] = sql_type
        column_define = [
            "[{}] {}".format(column, sql_type) for column, sql_type in col_types.items()
        ]
        if pk is not None:
            primary_key = "primary key ({})".format(pk)
            column_define.append(primary_key)
        else:
            keys = list(item.keys())
            if len(keys) > 0:
                primary_key = "primary key ({})".format(keys[0])
                column_define.append(primary_key)

        sql += "(%s)" % ", ".join(column_define)

        print("sql: %s" % sql)
        self.conn.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
