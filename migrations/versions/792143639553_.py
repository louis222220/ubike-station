"""empty message

Revision ID: 792143639553
Revises: 
Create Date: 2018-11-08 15:40:17.694015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '792143639553'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('station_no', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'favorite_stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('station_id', sa.Integer(), nullable=True),
        sa.Column('created_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_stations')
    op.drop_table('stations')
    # ### end Alembic commands ###
