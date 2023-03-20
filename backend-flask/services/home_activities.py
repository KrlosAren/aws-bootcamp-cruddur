from datetime import datetime, timedelta, timezone
# from opentelemetry import trace

# import logging

# tracer = trace.get_tracer('home.activities')
from lib.db import db

class HomeActivities:
  def run(cognito_user_id = None ):
    # logger.info('HomeActivities')
    # with tracer.start_as_current_span('http-handler'):
    #   span = trace.get_current_span()
    now = datetime.now(timezone.utc).astimezone()

    if not cognito_user_id :
      return []
    
    sql = """
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      where public.users.uuid  = %s
      ORDER BY activities.created_at DESC
      """

    result = db.query_array(sql,uuid=cognito_user_id)

    return result
    # span.set_attribute("app.time", now.isoformat())