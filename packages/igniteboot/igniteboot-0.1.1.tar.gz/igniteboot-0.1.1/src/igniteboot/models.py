from .db import create_database
from .config import load_settings_from_file

settings = load_settings_from_file()
db_instance = create_database(settings.DATABASE_URL)

class Field:
    def __init__(self, field_type=str, default=None, unique=False, index=False):
        self.field_type = field_type
        self.default = default
        self.unique = unique
        self.index = index

    def to_sql_type(self):
        if self.field_type == int:
            return "INTEGER"
        elif self.field_type == float:
            return "REAL"
        return "TEXT"

class Integer(Field):
    def __init__(self, default=0, unique=False, index=False):
        super().__init__(int, default, unique, index)

class String(Field):
    def __init__(self, default="", unique=False, index=False):
        super().__init__(str, default, unique, index)

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                del attrs[key]

        attrs["_fields"] = fields
        attrs["_table_name"] = name.lower()

        new_class = super().__new__(cls, name, bases, attrs)
        ModelMeta._create_table(new_class)
        return new_class

    @staticmethod
    def _create_table(model_class):
        table_name = model_class._table_name
        columns = []
        columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        for field_name, field_obj in model_class._fields.items():
            column_def = f"{field_name} {field_obj.to_sql_type()}"
            if field_obj.unique:
                column_def += " UNIQUE"
            columns.append(column_def)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        db_instance.execute(create_sql)

        for field_name, field_obj in model_class._fields.items():
            if field_obj.index:
                index_sql = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{field_name} ON {table_name} ({field_name})"
                db_instance.execute(index_sql)

class Model(metaclass=ModelMeta):
    @classmethod
    def create(cls, **kwargs):
        field_names = []
        placeholders = []
        values = []
        for field_name, field_obj in cls._fields.items():
            val = kwargs.get(field_name, field_obj.default)
            field_names.append(field_name)
            placeholders.append("?")
            values.append(val)
        sql = f"INSERT INTO {cls._table_name} ({', '.join(field_names)}) VALUES ({', '.join(placeholders)})"
        cursor = db_instance.execute(sql, tuple(values))
        return cursor.lastrowid

    @classmethod
    def all(cls):
        sql = f"SELECT * FROM {cls._table_name}"
        rows = db_instance.fetchall(sql)
        return rows

    @classmethod
    def filter(cls, **kwargs):
        conditions = []
        values = []
        for k, v in kwargs.items():
            conditions.append(f"{k} = ?")
            values.append(v)
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT * FROM {cls._table_name} WHERE {where_clause}"
        rows = db_instance.fetchall(sql, tuple(values))
        return rows
