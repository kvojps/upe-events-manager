"""add papers to MOSTRA PIBIC

Revision ID: beb92ade6c78
Revises: b59d8aadf84c
Create Date: 2024-06-24 17:12:42.563654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beb92ade6c78'
down_revision: Union[str, None] = 'b59d8aadf84c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO papers (id, pdf_id, area, title, authors, is_ignored, total_pages, event_id)
        VALUES
        (1, 'pdf_1', 'Engenharia', 'Paper Title 1', 'Author 1, Author 2', false, 10, 1),
        (2, 'pdf_2', 'Ciência da Computação', 'Paper Title 2', 'Author 3, Author 4', false, 12, 1),
        (3, 'pdf_3', 'Física', 'Paper Title 3', 'Author 5, Author 6', false, 8, 1),
        (4, 'pdf_4', 'Matemática', 'Paper Title 4', 'Author 7, Author 8', false, 15, 1),
        (5, 'pdf_5', 'Química', 'Paper Title 5', 'Author 9, Author 10', false, 20, 1),
        (6, 'pdf_6', 'Biologia', 'Paper Title 6', 'Author 11, Author 12', false, 18, 1),
        (7, 'pdf_7', 'Medicina', 'Paper Title 7', 'Author 13, Author 14', false, 22, 1),
        (8, 'pdf_8', 'Engenharia', 'Paper Title 8', 'Author 15, Author 16', false, 10, 1),
        (9, 'pdf_9', 'Ciência da Computação', 'Paper Title 9', 'Author 17, Author 18', false, 12, 1),
        (10, 'pdf_10', 'Física', 'Paper Title 10', 'Author 19, Author 20', false, 8, 1),
        (11, 'pdf_11', 'Matemática', 'Paper Title 11', 'Author 21, Author 22', false, 15, 1),
        (12, 'pdf_12', 'Química', 'Paper Title 12', 'Author 23, Author 24', false, 20, 1),
        (13, 'pdf_13', 'Biologia', 'Paper Title 13', 'Author 25, Author 26', false, 18, 1),
        (14, 'pdf_14', 'Medicina', 'Paper Title 14', 'Author 27, Author 28', false, 22, 1),
        (15, 'pdf_15', 'Engenharia', 'Paper Title 15', 'Author 29, Author 30', false, 10, 1),
        (16, 'pdf_16', 'Ciência da Computação', 'Paper Title 16', 'Author 31, Author 32', false, 12, 1),
        (17, 'pdf_17', 'Física', 'Paper Title 17', 'Author 33, Author 34', false, 8, 1),
        (18, 'pdf_18', 'Matemática', 'Paper Title 18', 'Author 35, Author 36', false, 15, 1),
        (19, 'pdf_19', 'Química', 'Paper Title 19', 'Author 37, Author 38', false, 20, 1),
        (20, 'pdf_20', 'Biologia', 'Paper Title 20', 'Author 39, Author 40', false, 18, 1),
        (21, 'pdf_21', 'Medicina', 'Paper Title 21', 'Author 41, Author 42', false, 22, 1),
        (22, 'pdf_22', 'Engenharia', 'Paper Title 22', 'Author 43, Author 44', false, 10, 1),
        (23, 'pdf_23', 'Ciência da Computação', 'Paper Title 23', 'Author 45, Author 46', false, 12, 1),
        (24, 'pdf_24', 'Física', 'Paper Title 24', 'Author 47, Author 48', false, 8, 1),
        (25, 'pdf_25', 'Matemática', 'Paper Title 25', 'Author 49, Author 50', false, 15, 1),
        (26, 'pdf_26', 'Química', 'Paper Title 26', 'Author 51, Author 52', false, 20, 1),
        (27, 'pdf_27', 'Biologia', 'Paper Title 27', 'Author 53, Author 54', false, 18, 1),
        (28, 'pdf_28', 'Medicina', 'Paper Title 28', 'Author 55, Author 56', false, 22, 1),
        (29, 'pdf_29', 'Engenharia', 'Paper Title 29', 'Author 57, Author 58', false, 10, 1),
        (30, 'pdf_30', 'Ciência da Computação', 'Paper Title 30', 'Author 59, Author 60', false, 12, 1),
        (31, 'pdf_31', 'Física', 'Paper Title 31', 'Author 61, Author 62', false, 8, 1),
        (32, 'pdf_32', 'Matemática', 'Paper Title 32', 'Author 63, Author 64', false, 15, 1),
        (33, 'pdf_33', 'Química', 'Paper Title 33', 'Author 65, Author 66', false, 20, 1),
        (34, 'pdf_34', 'Biologia', 'Paper Title 34', 'Author 67, Author 68', false, 18, 1),
        (35, 'pdf_35', 'Medicina', 'Paper Title 35', 'Author 69, Author 70', false, 22, 1),
        (36, 'pdf_36', 'Engenharia', 'Paper Title 36', 'Author 71, Author 72', false, 10, 1),
        (37, 'pdf_37', 'Ciência da Computação', 'Paper Title 37', 'Author 73, Author 74', false, 12, 1),
        (38, 'pdf_38', 'Física', 'Paper Title 38', 'Author 75, Author 76', false, 8, 1),
        (39, 'pdf_39', 'Matemática', 'Paper Title 39', 'Author 77, Author 78', false, 15, 1),
        (40, 'pdf_40', 'Química', 'Paper Title 40', 'Author 79, Author 80', false, 20, 1),
        (41, 'pdf_41', 'Biologia', 'Paper Title 41', 'Author 81, Author 82', false, 18, 1),
        (42, 'pdf_42', 'Medicina', 'Paper Title 42', 'Author 83, Author 84', false, 22, 1),
        (43, 'pdf_43', 'Engenharia', 'Paper Title 43', 'Author 85, Author 86', false, 10, 1),
        (44, 'pdf_44', 'Ciência da Computação', 'Paper Title 44', 'Author 87, Author 88', false, 12, 1),
        (45, 'pdf_45', 'Física', 'Paper Title 45', 'Author 89, Author 90', false, 8, 1)
        """
    )
    op.execute(
        """
        SELECT setval('papers_id_seq', 45, false);
        """
    )

def downgrade() -> None:
    op.execute(
        """
        DELETE FROM papers WHERE event_id = 1;
        """
    )
    op.execute(
        """
        SELECT setval('papers_id_seq', 1, true);
        """
    )
