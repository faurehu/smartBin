import json
import MySQLdb

def singleton(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

@singleton
class DB:
  def __init__(self):
    with open('../config/database.json', 'r') as conf_json_f:
      conf_json = json.loads(conf_json_f.read())
      self.db = MySQLdb.connect(
        host = conf_json['host'],
        user = conf_json['user'],
        passwd = conf_json['pass'],
        db = conf_json['db']
      )
      self.cursor = self.db.cursor()
  def query(self, query, args = []):
    self.cursor.execute(query, args)
    return self.cursor
  def db(self):
    return self.db
  def cursor(self):
    return self.cursor

