from datetime import datetime, timedelta, timezone

from lib.ddb import Ddb
from lib.db import db

class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    sql = """
    SELECT 
    users.uuid
    FROM public.users
    WHERE 
    users.cognito_user_id = %(cognito_user_id)s
    """

    my_user_uuid = db.query_object(sql,cognito_user_id=cognito_user_id)
    print(f"UUID: {my_user_uuid}")

    ddb = Ddb.client()
    data = Ddb.list_message_groups(ddb, my_user_uuid['uuid'])
    print("list_message_groups:",data)

    model['data'] = data
    return 