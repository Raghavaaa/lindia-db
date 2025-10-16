"""add_postgres_indexes

Revision ID: 4d6abf4eecda
Revises: 04bd3fd5e6c2
Create Date: 2025-10-16 19:17:31.999035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d6abf4eecda'
down_revision = '04bd3fd5e6c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Additional composite indexes for common query patterns
    op.create_index('ix_clients_lawyer_id', 'clients', ['lawyer_id'], unique=False)
    op.create_index('ix_cases_client_id', 'cases', ['client_id'], unique=False)
    op.create_index('ix_inference_logs_query_id', 'inference_logs', ['query_id'], unique=False)
    
    # PostgreSQL GIN index for full-text search on research_queries.query_text
    # Only runs on PostgreSQL (SQLite will skip this)
    from sqlalchemy import inspect
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("""
            CREATE INDEX IF NOT EXISTS ix_research_queries_query_text_fts 
            ON research_queries USING gin(to_tsvector('english', query_text))
        """)


def downgrade() -> None:
    # Drop PostgreSQL-specific GIN index first
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("DROP INDEX IF EXISTS ix_research_queries_query_text_fts")
    
    # Drop composite indexes
    op.drop_index('ix_inference_logs_query_id', table_name='inference_logs')
    op.drop_index('ix_cases_client_id', table_name='cases')
    op.drop_index('ix_clients_lawyer_id', table_name='clients')
