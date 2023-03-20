from psycopg_pool import ConnectionPool
import os
import sys
import re

import logging

logging.basicConfig(level=logging.INFO,format='%(levelname)s:%(message)s',)
logger = logging.getLogger(__name__)

class Db:
  def __init__(self):
    self.init_pool()
    
  def init_pool(self):
    self.connection_url = os.getenv('CONNECTION_URL')
    self.pool = ConnectionPool(self.connection_url)
  
  def print_psycopg_err(self,err):
    
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno

    print("\npsycopg2 ERROR:", err, "on line number:" , line_num)
    print("psycopg2 traceback:", traceback, "--- type:" , err_type)
  
  def query_wrap_object(self,template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def query_wrap_array(self,template):
    sql = f"""
      (
        SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) 
        FROM ({template}) array_row
      );
    """
    return sql

  def query_array(self,sql,*args, **kwargs):
    wrapped_sql = self.query_wrap_array(sql)
    try:
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,kwargs)
          json = cur.fetchone()
          return json[0]
    except Exception as error:
      self.print_psycopg_err(error)
      return []

  def query_object(self,sql):
    wrapped_sql = self.query_wrap_object(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        json = cur.fetchone()
      
        return json[0]

  def query_commit_return_id(self, sql,*args,**kwargs):
    print('-SQL STATEMENT')

    pattern = r'\bRETURNING\b'
    match = bool(re.search(pattern, sql))
    returning_id = None

    try:
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql, kwargs)

          if match:
            returning_id = cur.fetchone()[0]
          
          conn.commit()
          return returning_id

    except Exception as error:
      self.print_psycopg_err(error)


  def query_commit(self,sql,*args):
    try:
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          conn.commit(sql)
    except Exception as error:
      self.print_psycopg_err(error)


db = Db()