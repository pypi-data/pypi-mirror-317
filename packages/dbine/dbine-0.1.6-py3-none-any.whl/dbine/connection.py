from enum import Enum
from pydantic import BaseModel
import psycopg
import mysql.connector
import sqlite3
import graspgraph as gg
from pyemon.path import *
import yaml

class Type(Enum):
  PostgreSQL = 1
  MySQL = 2
  SQLite = 3

  @classmethod
  def from_name(cls, name):
    for type in Type:
      if type == name or type.name == name:
        return type
    return Type.PostgreSQL

  @classmethod
  def from_value(cls, value):
    for type in Type:
      if type == value or type.value == value:
        return type
    return Type.PostgreSQL

class ConnectionConfig(BaseModel):
  Type: Type
  DatabaseName: str
  UserName: str = ""
  Password: str = ""
  Host: str = "localhost"
  Port: int = 0

  def update(self):
    match self.Type:
      case Type.PostgreSQL:
        if self.Port == 0:
          self.Port = 5432
      case Type.MySQL:
        if self.Port == 0:
          self.Port = 3306
    return self

  def to_options(self):
    match self.Type:
      case Type.PostgreSQL:
        return " ".join([
          """dbname={}""".format(self.DatabaseName),
          """host={}""".format(self.Host),
          """port={}""".format(self.Port),
          """user={}""".format(self.UserName),
          """password={}""".format(self.Password),
        ])
      case Type.MySQL:
        return {
          "database": self.DatabaseName,
          "host": self.Host,
          "port": self.Port,
          "user": self.UserName,
          "password": self.Password,
        }
      case Type.SQLite:
        return self.DatabaseName
    return None

  def to_string(self):
    options = self.to_options()
    if type(options) is str:
      return options
    return str(options)

  def __str__(self):
    return self.to_string()

  def load(self, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      connectionConfig = ConnectionConfig.from_yaml(file)
      self.Type = connectionConfig.Type
      self.DatabaseName = connectionConfig.DatabaseName
      self.UserName = connectionConfig.UserName
      self.Password = connectionConfig.Password
      self.Host = connectionConfig.Host
      self.Port = connectionConfig.Port
    return self

  def save(self, filePath):
    Path.from_file_path(filePath).makedirs()
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      connectionConfig = self.model_dump()
      connectionConfig["Type"] = connectionConfig["Type"].name
      yaml.dump(connectionConfig, file, sort_keys = False, default_flow_style = False, allow_unicode = True)
    return self

  @classmethod
  def default_dict(cls, type = None, databaseName = ""):
    if type is None:
      type = Type.PostgreSQL
    return {"Type": type, "DatabaseName": databaseName}

  @classmethod
  def from_yaml(cls, stream):
    connectionConfig = yaml.safe_load(stream) or ConnectionConfig.default_dict()
    connectionConfig["Type"] = Type.from_name(connectionConfig["Type"])
    return ConnectionConfig(**connectionConfig)

  @classmethod
  def from_file_path(cls, filePath):
    return ConnectionConfig(**ConnectionConfig.default_dict()).load(filePath)

class Connection:
  def __init__(self, connectionConfig):
    self.__Connections = []
    self.open(connectionConfig)

  @property
  def Cursor(self):
    if len(self.__Connections) == 0:
      return None
    return self.__Connections[0]

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.close()

  def open(self, connectionConfig):
    self.close()
    connectionConfig.update()
    match connectionConfig.Type:
      case Type.PostgreSQL:
        connection = psycopg.connect(connectionConfig.to_options())
        self.__Connections = [connection.cursor(), connection]
      case Type.MySQL:
        connection = mysql.connector.connect(**connectionConfig.to_options())
        self.__Connections = [connection.cursor(), connection]
      case Type.SQLite:
        connection = sqlite3.connect(connectionConfig.to_options())
        self.__Connections = [connection.cursor(), connection]
    self.ConnectionConfig = connectionConfig
    return self

  def close(self):
    if 0 < len(self.__Connections):
      for connection in self.__Connections:
        connection.close()
      self.__Connections = []
    return self

  def get_database(self):
    database = gg.Database()
    match self.ConnectionConfig.Type:
      case Type.PostgreSQL:
        cursor = self.Cursor
        cursor.execute("SELECT schemaname, tablename FROM pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
        for tableDefinitions in cursor.fetchall():
          table = gg.DatabaseTable(**{"Namespace": """{}.{}""".format(self.ConnectionConfig.DatabaseName, tableDefinitions[0]), "Name": tableDefinitions[1]})
          cursor.execute("""SELECT pg_description.description FROM pg_class JOIN pg_description ON pg_class.oid = pg_description.objoid WHERE pg_class.relname = '{}' AND pg_description.objsubid = 0""".format(tableDefinitions[1]))
          if cursor.rowcount == 1:
            table.Comment = cursor.fetchone()[0]
          cursor.execute("""SELECT column_name, data_type, character_maximum_length, ordinal_position FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}'""".format(*tableDefinitions))
          for columnDefinitions in cursor.fetchall():
            column = gg.DatabaseColumn(**{"Name": columnDefinitions[0], "Type": columnDefinitions[1].upper()})
            if columnDefinitions[2] is not None:
              column.Type = """{}({})""".format(column.Type, columnDefinitions[2])
            cursor.execute("""SELECT pg_description.description FROM pg_class JOIN pg_description ON pg_class.oid = pg_description.objoid WHERE pg_class.relname = '{}' AND pg_description.objsubid = {}""".format(tableDefinitions[1], columnDefinitions[3]))
            if cursor.rowcount == 1:
              column.Comment = cursor.fetchone()[0]
            cursor.execute("""SELECT constraint_type FROM information_schema.table_constraints JOIN information_schema.constraint_column_usage ON information_schema.table_constraints.constraint_name = information_schema.constraint_column_usage.constraint_name WHERE information_schema.constraint_column_usage.table_catalog = '{}' AND information_schema.constraint_column_usage.table_schema = '{}' AND information_schema.constraint_column_usage.table_name = '{}' AND information_schema.constraint_column_usage.column_name = '{}'""".format(self.ConnectionConfig.DatabaseName, tableDefinitions[0], tableDefinitions[1], columnDefinitions[0]))
            if cursor.rowcount == 1 and cursor.fetchone()[0] == "PRIMARY KEY":
              column.Caption = "PK"
            table.Columns.append(column)
          database.Tables.append(table)
      case Type.MySQL:
        cursor = self.Cursor
        cursor.execute("SHOW TABLE STATUS")
        for tableDefinitions in cursor.fetchall():
          table = gg.DatabaseTable(**{"Namespace": self.ConnectionConfig.DatabaseName, "Name": tableDefinitions[0], "Comment": tableDefinitions[-1]})
          cursor.execute("""SHOW FULL COLUMNS FROM {}""".format(tableDefinitions[0]))
          for columnDefinitions in cursor.fetchall():
            caption = ""
            if columnDefinitions[4] == "PRI":
              caption = "PK"
            table.Columns.append(gg.DatabaseColumn(**{"Name": columnDefinitions[0], "Type": columnDefinitions[1].upper(), "Comment": columnDefinitions[-1], "Caption": caption}))
          database.Tables.append(table)
      case Type.SQLite:
        cursor = self.Cursor
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        for tableDefinitions in cursor.fetchall():
          table = gg.DatabaseTable(**{"Namespace": Path.from_file_path(self.ConnectionConfig.DatabaseName).File, "Name": tableDefinitions[0]})
          cursor.execute("""PRAGMA TABLE_INFO({})""".format(tableDefinitions[0]))
          for columnDefinitions in cursor.fetchall():
            caption = ""
            if columnDefinitions[5] == 1:
              caption = "PK"
            table.Columns.append(gg.DatabaseColumn(**{"Name": columnDefinitions[1], "Type": columnDefinitions[2].upper(), "Caption": caption}))
          database.Tables.append(table)
    return database
