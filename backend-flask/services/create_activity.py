import uuid
from datetime import datetime, timedelta, timezone
from lib.db import db


class CreateActivity:

  def run(message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }


    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      expires_at = (now + ttl_offset).isoformat()
      object_json = CreateActivity.create_activity(handle_user=user_handle,message=message,expires_at=expires_at)
      model['data'] = object_json
      import pdb;pdb.set_trace()
    return model

  @classmethod
  def create_activity(cls,handle_user,message, expires_at):
    sql = f"""
      INSERT INTO public.activities (user_uuid,message,expires_at) 
      VALUES (
        (SELECT uuid FROM public.users WHERE users.handle = %(handle_user)s LIMIT 1) ,%(message)s,%(expires_at)s) RETURNING uuid
    """
    uuid = db.query_commit_return_id(sql=sql,handle_user=handle_user,message=message,expires_at=expires_at)
    import pdb;pdb.set_trace()
    return CreateActivity.query_object_activity(uuid)

  @classmethod
  def query_object_activity(cls,uuid):

    sql = f"""
      SELECT * FROM public.activities 
      where uuid = %(uuid)s
    """

    object = db.query_object(sql,{
      'uuid': uuid
    })
    import pdb;pdb.set_trace()
