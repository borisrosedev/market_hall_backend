"""Add trigger for carts id

Revision ID: 4935abcbbab0
Revises: eadcd7e65123
Create Date: 2025-09-17 13:06:26.297533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4935abcbbab0'
down_revision: Union[str, Sequence[str], None] = 'eadcd7e65123'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("DROP TRIGGER IF EXISTS set_carts_id_trigger ON carts;")
    op.execute("DROP FUNCTION IF EXISTS set_carts_id();")
    op.execute("""
    CREATE OR REPLACE FUNCTION set_carts_id()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.id IS NULL THEN
            NEW.id = gen_random_uuid();
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER set_carts_id_trigger
    BEFORE INSERT ON carts
    FOR EACH ROW
    EXECUTE FUNCTION set_carts_id();
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS set_carts_id_trigger ON carts;")
    op.execute("DROP FUNCTION IF EXISTS set_carts_id();")
    