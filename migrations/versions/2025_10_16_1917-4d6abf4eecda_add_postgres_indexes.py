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
    # PostgreSQL-specific performance indexes
    
    # Index on users.email for fast lookup (already unique, but explicit index)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    
    # Index on cases.status for filtering active/closed cases
    op.create_index('ix_cases_status', 'cases', ['status'], unique=False)
    
    # Index on junior_logs.timestamp for chronological queries
    op.create_index('ix_junior_logs_timestamp', 'junior_logs', ['timestamp'], unique=False)
    
    # PostgreSQL GIN index for full-text search on research_queries.query_text
    # Note: This uses PostgreSQL-specific GIN index with to_tsvector
    # Will be ignored/adapted in SQLite
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_research_queries_query_text_fts 
        ON research_queries USING gin(to_tsvector('english', query_text))
    """)
    
    # Additional composite indexes for common query patterns
    op.create_index('ix_clients_lawyer_id', 'clients', ['lawyer_id'], unique=False)
    op.create_index('ix_cases_client_id', 'cases', ['client_id'], unique=False)
    op.create_index('ix_inference_logs_query_id', 'inference_logs', ['query_id'], unique=False)


def downgrade() -> None:
    # Drop indexes in reverse order
    
    op.drop_index('ix_inference_logs_query_id', table_name='inference_logs')
    op.drop_index('ix_cases_client_id', table_name='cases')
    op.drop_index('ix_clients_lawyer_id', table_name='clients')
    
    # Drop PostgreSQL-specific GIN index
    op.execute("DROP INDEX IF EXISTS ix_research_queries_query_text_fts")
    
    op.drop_index('ix_junior_logs_timestamp', table_name='junior_logs')
    op.drop_index('ix_cases_status', table_name='cases')
    op.drop_index('ix_users_email', table_name='users')
