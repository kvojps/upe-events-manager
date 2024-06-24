"""add initial events

Revision ID: b59d8aadf84c
Revises: 9ad42850aec4
Create Date: 2024-06-19 11:23:03.524739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b59d8aadf84c'
down_revision: Union[str, None] = '9ad42850aec4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        INSERT INTO events (id, name, initial_date, final_date, promoted_by, s3_folder_name, summary_filename, merged_papers_filename, anal_filename)
        VALUES
            (1, 'MOSTRA PIBIC', '2024-01-01', '2024-01-02', 'Universidade de Pernambuco', 'folder_s3_mostra_pibic', 'summary_file_mostra_pibic.txt', 'merged_papers_mostra_pibic.pdf', 'anal_mostra_pibic.txt'),
            (2, 'SECAP', '2024-02-01', '2024-02-02', 'Universidade de Pernambuco', 'folder_s3_secap', 'summary_file_secap.txt', 'merged_papers_secap.pdf', 'anal_secap.txt'),
            (3, 'Semana de Engenharia', '2024-03-01', '2024-03-05', 'Universidade de Pernambuco', 'folder_s3_semana_engenharia', 'summary_file_semana_engenharia.txt', 'merged_papers_semana_engenharia.pdf', 'anal_semana_engenharia.txt'),
            (4, 'Hackathon UPE', '2024-04-10', '2024-04-12', 'Universidade de Pernambuco', 'folder_s3_hackathon', 'summary_file_hackathon.txt', 'merged_papers_hackathon.pdf', 'anal_hackathon.txt'),
            (5, 'Feira de Robótica', '2024-05-15', '2024-05-17', 'Universidade de Pernambuco', 'folder_s3_feira_robotica', 'summary_file_feira_robotica.txt', 'merged_papers_feira_robotica.pdf', 'anal_feira_robotica.txt'),
            (6, 'Semana de Ciência da Computação', '2024-06-20', '2024-06-24', 'Universidade de Pernambuco', 'folder_s3_semana_cc', 'summary_file_semana_cc.txt', 'merged_papers_semana_cc.pdf', 'anal_semana_cc.txt'),
            (7, 'Workshop de Inteligência Artificial', '2024-07-10', '2024-07-12', 'Universidade de Pernambuco', 'folder_s3_workshop_ia', 'summary_file_workshop_ia.txt', 'merged_papers_workshop_ia.pdf', 'anal_workshop_ia.txt'),
            (8, 'Conferência de Big Data', '2024-08-01', '2024-08-03', 'Universidade de Pernambuco', 'folder_s3_conferencia_big_data', 'summary_file_conferencia_big_data.txt', 'merged_papers_conferencia_big_data.pdf', 'anal_conferencia_big_data.txt'),
            (9, 'Fórum de Segurança da Informação', '2024-09-15', '2024-09-17', 'Universidade de Pernambuco', 'folder_s3_forum_seguranca', 'summary_file_forum_seguranca.txt', 'merged_papers_forum_seguranca.pdf', 'anal_forum_seguranca.txt'),
            (10, 'Seminário de Redes de Computadores', '2024-10-10', '2024-10-12', 'Universidade de Pernambuco', 'folder_s3_seminario_redes', 'summary_file_seminario_redes.txt', 'merged_papers_seminario_redes.pdf', 'anal_seminario_redes.txt'),
            (11, 'Simpósio de Software Livre', '2024-11-01', '2024-11-03', 'Universidade de Pernambuco', 'folder_s3_simposio_software_livre', 'summary_file_simposio_software_livre.txt', 'merged_papers_simposio_software_livre.pdf', 'anal_simposio_software_livre.txt'),
            (12, 'Encontro de Empreendedorismo Tecnológico', '2024-12-10', '2024-12-12', 'Universidade de Pernambuco', 'folder_s3_encontro_empreendedorismo', 'summary_file_encontro_empreendedorismo.txt', 'merged_papers_encontro_empreendedorismo.pdf', 'anal_encontro_empreendedorismo.txt'),
            (13, 'Colóquio de Tecnologias Emergentes', '2024-01-20', '2024-01-22', 'Universidade de Pernambuco', 'folder_s3_coloquio_tecnologias', 'summary_file_coloquio_tecnologias.txt', 'merged_papers_coloquio_tecnologias.pdf', 'anal_coloquio_tecnologias.txt'),
            (14, 'Maratona de Programação', '2024-02-15', '2024-02-17', 'Universidade de Pernambuco', 'folder_s3_maratona_programacao', 'summary_file_maratona_programacao.txt', 'merged_papers_maratona_programacao.pdf', 'anal_maratona_programacao.txt'),
            (15, 'Expo UPE', '2024-03-25', '2024-03-27', 'Universidade de Pernambuco', 'folder_s3_expo_upe', 'summary_file_expo_upe.txt', 'merged_papers_expo_upe.pdf', 'anal_expo_upe.txt'),
            (16, 'Semana de Inovação', '2024-04-15', '2024-04-17', 'Universidade de Pernambuco', 'folder_s3_semana_inovacao', 'summary_file_semana_inovacao.txt', 'merged_papers_semana_inovacao.pdf', 'anal_semana_inovacao.txt'),
            (17, 'Jornada de Pesquisa', '2024-05-05', '2024-05-07', 'Universidade de Pernambuco', 'folder_s3_jornada_pesquisa', 'summary_file_jornada_pesquisa.txt', 'merged_papers_jornada_pesquisa.pdf', 'anal_jornada_pesquisa.txt');        
        SELECT setval('events_id_seq', 17, true);
        """
    )

def downgrade():
    op.execute(
        """
        DELETE FROM events WHERE is IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17);        
        SELECT setval('events_id_seq', 1, true);
        """
    )
