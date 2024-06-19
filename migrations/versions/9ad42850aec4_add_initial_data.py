"""add initial data

Revision ID: 9ad42850aec4
Revises: 
Create Date: 2024-06-19 11:19:24.099952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ad42850aec4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('initial_date', sa.DateTime(), nullable=True),
    sa.Column('final_date', sa.DateTime(), nullable=True),
    sa.Column('promoted_by', sa.String(), nullable=True),
    sa.Column('s3_folder_name', sa.String(), nullable=True),
    sa.Column('summary_filename', sa.String(), nullable=True),
    sa.Column('merged_papers_filename', sa.String(), nullable=True),
    sa.Column('anal_filename', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_events_name'), 'events', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pdf_id', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('authors', sa.String(), nullable=True),
    sa.Column('is_ignored', sa.Boolean(), nullable=True),
    sa.Column('total_pages', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_papers_id'), 'papers', ['id'], unique=False)
    op.create_index(op.f('ix_papers_pdf_id'), 'papers', ['pdf_id'], unique=False)
    op.create_table('subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('cpf', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('workload', sa.Float(), nullable=True),
    sa.Column('is_present', sa.Boolean(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribers_cpf'), 'subscribers', ['cpf'], unique=True)
    op.create_index(op.f('ix_subscribers_email'), 'subscribers', ['email'], unique=True)
    op.create_index(op.f('ix_subscribers_id'), 'subscribers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscribers_id'), table_name='subscribers')
    op.drop_index(op.f('ix_subscribers_email'), table_name='subscribers')
    op.drop_index(op.f('ix_subscribers_cpf'), table_name='subscribers')
    op.drop_table('subscribers')
    op.drop_index(op.f('ix_papers_pdf_id'), table_name='papers')
    op.drop_index(op.f('ix_papers_id'), table_name='papers')
    op.drop_table('papers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_events_name'), table_name='events')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
