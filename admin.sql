BEGIN;
UPDATE users
SET role = 'admin'
WHERE email = 'test@gmail.com';
COMMIT;

