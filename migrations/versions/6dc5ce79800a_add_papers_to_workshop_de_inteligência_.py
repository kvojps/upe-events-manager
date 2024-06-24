"""add papers to Workshop de Inteligência Artificial

Revision ID: 6dc5ce79800a
Revises: beb92ade6c78
Create Date: 2024-06-24 17:15:12.222082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc5ce79800a'
down_revision: Union[str, None] = 'beb92ade6c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Inserir novos registros na tabela `papers`
    op.execute(
        """
        INSERT INTO papers (id, pdf_id, area, title, authors, is_ignored, total_pages, event_id)
        VALUES
        (46, 'pdf_46', 'Inteligência Artificial', 'Aplicações de Redes Neurais em Reconhecimento de Imagens', 'Author 1, Author 2', false, 10, 7),
        (47, 'pdf_47', 'Inteligência Artificial', 'Machine Learning para Previsão de Séries Temporais', 'Author 3, Author 4', false, 12, 7),
        (48, 'pdf_48', 'Inteligência Artificial', 'Processamento de Linguagem Natural em Assistentes Virtuais', 'Author 5, Author 6', false, 8, 7),
        (49, 'pdf_49', 'Inteligência Artificial', 'Redes Neurais Convolucionais para Detecção de Objetos', 'Author 7, Author 8', false, 15, 7),
        (50, 'pdf_50', 'Inteligência Artificial', 'Aprendizado por Reforço em Jogos de Computador', 'Author 9, Author 10', false, 20, 7),
        (51, 'pdf_51', 'Inteligência Artificial', 'Sistemas de Recomendação Baseados em Inteligência Artificial', 'Author 11, Author 12', false, 18, 7),
        (52, 'pdf_52', 'Inteligência Artificial', 'Análise de Sentimentos em Redes Sociais usando NLP', 'Author 13, Author 14', false, 22, 7),
        (53, 'pdf_53', 'Inteligência Artificial', 'Detecção de Fraudes com Algoritmos de Machine Learning', 'Author 15, Author 16', false, 10, 7),
        (54, 'pdf_54', 'Inteligência Artificial', 'Desenvolvimento de Chatbots Inteligentes para Atendimento ao Cliente', 'Author 17, Author 18', false, 12, 7),
        (55, 'pdf_55', 'Inteligência Artificial', 'Segmentação de Imagens Médicas com Redes Neurais', 'Author 19, Author 20', false, 8, 7),
        (56, 'pdf_56', 'Inteligência Artificial', 'O Uso de Inteligência Artificial na Previsão do Tempo', 'Author 21, Author 22', false, 15, 7),
        (57, 'pdf_57', 'Inteligência Artificial', 'Transferência de Estilo Neural para Criação Artística', 'Author 23, Author 24', false, 20, 7),
        (58, 'pdf_58', 'Inteligência Artificial', 'Técnicas de Redução de Dimensionalidade em Big Data', 'Author 25, Author 26', false, 18, 7),
        (59, 'pdf_59', 'Inteligência Artificial', 'Análise de Dados de Sensores IoT com Machine Learning', 'Author 27, Author 28', false, 22, 7),
        (60, 'pdf_60', 'Inteligência Artificial', 'Algoritmos de Deep Learning para Tradução Automática', 'Author 29, Author 30', false, 10, 7),
        (61, 'pdf_61', 'Inteligência Artificial', 'Reconhecimento de Voz com Redes Neurais Recorrentes', 'Author 31, Author 32', false, 12, 7),
        (62, 'pdf_62', 'Inteligência Artificial', 'Aprendizado de Máquina para Diagnóstico Médico', 'Author 33, Author 34', false, 8, 7),
        (63, 'pdf_63', 'Inteligência Artificial', 'Detecção de Anomalias em Sistemas de Segurança', 'Author 35, Author 36', false, 15, 7),
        (64, 'pdf_64', 'Inteligência Artificial', 'O Impacto da Inteligência Artificial na Automação Industrial', 'Author 37, Author 38', false, 20, 7),
        (65, 'pdf_65', 'Inteligência Artificial', 'Algoritmos Evolutivos em Inteligência Artificial', 'Author 39, Author 40', false, 18, 7);
        """
    )
    op.execute(
        """
        SELECT setval('papers_id_seq', 65, false);
        """
    )

def downgrade():
    op.execute(
        """
        DELETE FROM papers WHERE event_id = 2 AND id BETWEEN 46 AND 65;
        """
    )
    op.execute(
        """
        SELECT setval('papers_id_seq', 46, true);
        """
    )