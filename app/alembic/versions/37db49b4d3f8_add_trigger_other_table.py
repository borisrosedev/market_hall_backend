"""add trigger other table

Revision ID: 37db49b4d3f8
Revises: 4935abcbbab0
Create Date: 2025-09-17 14:55:33.971205

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "37db49b4d3f8"
down_revision: Union[str, Sequence[str], None] = "4935abcbbab0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Supprimer le trigger et la fonction s'ils existent
    op.execute("DROP TRIGGER IF EXISTS set_products_id_trigger ON products;")
    op.execute("DROP FUNCTION IF EXISTS set_products_id();")

    # Créer la fonction et le trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION set_products_id()
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
    CREATE TRIGGER set_products_id_trigger
    BEFORE INSERT ON products
    FOR EACH ROW
    EXECUTE FUNCTION set_products_id();
    """)

    op.execute("DROP TRIGGER IF EXISTS set_orders_id_trigger ON orders;")
    op.execute("DROP FUNCTION IF EXISTS set_orders_id();")
    op.execute("""
    CREATE OR REPLACE FUNCTION set_orders_id()
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
    CREATE TRIGGER set_orders_id_trigger
    BEFORE INSERT ON orders
    FOR EACH ROW
    EXECUTE FUNCTION set_orders_id();
    """)

    # Supprimer le trigger et la fonction s'ils existent
    op.execute("DROP TRIGGER IF EXISTS set_tags_id_trigger ON tags;")
    op.execute("DROP FUNCTION IF EXISTS set_tags_id();")

    # Créer la fonction et le trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION set_tags_id()
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
    CREATE TRIGGER set_tags_id_trigger
    BEFORE INSERT ON tags
    FOR EACH ROW
    EXECUTE FUNCTION set_tags_id();
    """)

    # Supprimer le trigger et la fonction s'ils existent
    op.execute("DROP TRIGGER IF EXISTS set_order_addresses_id_trigger ON order_addresses;")
    op.execute("DROP FUNCTION IF EXISTS set_order_addresses_id();")

    # Créer la fonction et le trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION set_order_addresses_id()
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
    CREATE TRIGGER set_order_addresses_id_trigger
    BEFORE INSERT ON order_addresses
    FOR EACH ROW
    EXECUTE FUNCTION set_order_addresses_id();
    """)

    # Supprimer le trigger et la fonction s'ils existent
    op.execute("DROP TRIGGER IF EXISTS set_order_items_id_trigger ON order_items;")
    op.execute("DROP FUNCTION IF EXISTS set_order_items_id();")

    # Créer la fonction et le trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION set_order_items_id()
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
    CREATE TRIGGER set_order_items_id_trigger
    BEFORE INSERT ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION set_order_items_id();
    """)

    op.alter_column(
        "orders",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.func.now(),
    )
    op.alter_column(
        "products",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.func.now(),
    )
    op.alter_column(
        "products",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        nullable=True,
    )

    op.alter_column(
        "tags",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.func.now(),
    )
    op.alter_column(
        "tags",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        nullable=True,
    )

    op.alter_column(
        "order_items",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.func.now(),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS set_products_id_trigger ON products;")
    op.execute("DROP FUNCTION IF EXISTS set_products_id();")
    op.execute("DROP TRIGGER IF EXISTS set_orders_id_trigger ON orders;")
    op.execute("DROP FUNCTION IF EXISTS set_orders_id();")
    op.execute("DROP TRIGGER IF EXISTS set_tags_id_trigger ON tags;")
    op.execute("DROP FUNCTION IF EXISTS set_tags_id();")
    op.execute("DROP TRIGGER IF EXISTS set_order_addresses_id_trigger ON order_addresses;")
    op.execute("DROP FUNCTION IF EXISTS set_order_addresses_id();")
    op.execute("DROP TRIGGER IF EXISTS set_order_items_id_trigger ON order_items;")
    op.execute("DROP FUNCTION IF EXISTS set_order_items_id();")

    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        server_default=None,
    )
    op.alter_column(
        "products",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        nullable=False,
    )
    op.alter_column(
        "products",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        server_default=None,
    )
    op.alter_column(
        "tags",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        nullable=False,
    )
    op.alter_column(
        "tags",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        server_default=None,
    )
    op.alter_column(
        "order_items",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        server_default=None,
    )
