import os
import shutil
import uuid
from io import BytesIO
import pdfkit # type: ignore
from fastapi import HTTPException, status
from PyPDF2 import PdfReader
from api.contracts.responses.summary import SummaryPdfResponse
from core.domain.dto.summary import SummaryDTO
from core.infrastructure.repositories.event import EventRepository
from core.infrastructure.repositories.paper import PaperRepository


class SummaryService:
    def __init__(
        self,
        paper_repo: PaperRepository,
        event_repo: EventRepository,
    ):
        self._paper_repo = paper_repo
        self._event_repo = event_repo

    def create_summary_pdf(
        self, event_id: int, summary_dto: SummaryDTO
    ) -> SummaryPdfResponse:
        event = self._event_repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )

        if event.summary_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Summary already exists for this event",
            )

        event_areas = self._paper_repo.get_areas_by_event_id(event_id)
        if len(event_areas) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No papers found for this event",
            )

        paper = self._paper_repo.get_first_paper()
        if not paper.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Papers cannot have empty fields to generate the summary",
            )

        html_bytes_summary_without_pages_description = self._create_html_summary(
            event_areas, 0, 0
        )
        summary_pages_length = self._count_pdf_summary_pages(
            html_bytes_summary_without_pages_description
        )
        html_bytes_summary = self._create_html_summary(
            event_areas, summary_dto.cover_pages_length, summary_pages_length
        )
        pdf_bytes_summary = self._create_pdf_summary(html_bytes_summary)

        return SummaryPdfResponse(
            summary_pdf_folder=str(event.s3_folder_name),
            summary_pdf_filename=f"{str(event.name).lower().replace(' ', '_')}_summary.pdf",
            summary_pdf=pdf_bytes_summary,
        )

    def _create_html_summary(
        self, event_areas: list[str], cover_pages_length: int, summary_pages_length: int
    ) -> bytes:
        buffer = BytesIO()

        content = ""
        pages = cover_pages_length + summary_pages_length + 1
        for area in event_areas:
            content += f"""
                <h1 class="h1-section">{area}</h1>
                <ul>
            """
            papers = self._paper_repo.get_papers_by_area(area)
            for paper in papers:
                content += f"""
                    <li>
                        <p>
                            <strong>{(str(paper.title)).capitalize()}</strong>
                        </p>
                        <div class="div-autores-pagina">
                            <p class="p-autores">
                                {str(paper.authors)}
                                <span>{pages}</span>
                            </p>
                        </div>
                    </li>
                """
                pages += int(paper.total_pages)

            content += "</ul>"

        template_html = """
            <!doctype html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Summary</title>
                    <style>
                        body {
                            font-family: "Times New Roman";
                            margin: 0;
                            padding: 0;
                            background-color: #f7f7f7;
                            text-align: justify;
                            text-justify: inter-word;
                        }
                        .container {
                            max-width: 800px;
                            margin: 20px auto;
                            padding: 20px;
                            background-color: #fff;
                            border-radius: 5px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }
                        p {
                            font-size: 16px;
                            margin: 4px;
                            width: 95%;
                        }
                        .p-autores {
                            font-style: italic;
                        }
                        ul {
                            list-style-type: none;
                        }
                        li {
                            padding: 4px;
                        }
                        .div-autores-pagina {
                            width: 95%;
                            span {
                            font-size: 18px;
                            float: right;
                            }
                        }
                        .separator {
                            border-top: 1px solid #ccc;
                            margin-top: 10px;
                            margin-bottom: 10px;
                        }
                        .h1-title {
                            padding-bottom: 32px;
                        }
                        .h1-section {
                            padding-bottom: 24px;
                        }
                    </style>
                </head>""" + (
            f"""
                <body>
                    <div class="container">
                        <div class="separator"></div>
                        <h1 class="h1-title">Sumário</h1>
                        {content}
                    </div>
                </body>
            </html> """
        )

        buffer.write(template_html.encode("UTF-8"))

        return buffer.getvalue()

    def _count_pdf_summary_pages(self, html_bytes_summary: bytes) -> int:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        session_id = uuid.uuid4()

        temp_html_file_path = f"{temp_dir}/{session_id}__summary.html"
        with open(temp_html_file_path, "wb") as file:
            file.write(html_bytes_summary)

        temp_pdf_file_path = f"{temp_dir}/{session_id}__summary.pdf"
        pdfkit.from_file(temp_html_file_path, temp_pdf_file_path)

        pdf_reader = PdfReader(temp_pdf_file_path)
        pages_length = len(pdf_reader.pages)

        shutil.rmtree(temp_dir)

        return pages_length

    def _create_pdf_summary(self, html_bytes_summary: bytes) -> bytes:
        buffer = BytesIO()

        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        session_id = uuid.uuid4()

        temp_html_file_path = f"{temp_dir}/{session_id}__summary.html"
        with open(temp_html_file_path, "wb") as file:
            file.write(html_bytes_summary)

        temp_pdf_file_path = f"{temp_dir}/{session_id}__summary.pdf"
        pdfkit.from_file(temp_html_file_path, temp_pdf_file_path)

        buffer.write(open(temp_pdf_file_path, "rb").read())

        shutil.rmtree(temp_dir)

        return buffer.getvalue()
