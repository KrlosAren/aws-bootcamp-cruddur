INSERT INTO public.users (display_name,email, handle, cognito_user_id)
VALUES
  ('Carlos Lopez', 'krlosaren@gmail.com', 'krlosaren' ,'MOCK'),
  ('Andrew Bayko', 'clopezzavarce@gmail.com', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'krlosaren' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )