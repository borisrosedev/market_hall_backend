-- CREATE VIEW ecommerce.table_structure AS 
SELECT 
	table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'ecommerce' 
ORDER BY table_name, ordinal_position;
SELECT * FROM ecommerce.table_structure WHERE table_name = 'notifications';

