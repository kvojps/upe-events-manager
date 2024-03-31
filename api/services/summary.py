from io import BytesIO
from fastapi import HTTPException, status
from pydantic import BaseModel
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository


class SummaryPdfResponse(BaseModel):
    summary_pdf_folder: str
    summary_pdf_filename: str
    summary_pdf: bytes


class SummaryService:
    def __init__(
        self,
        paper_repo: PaperRepository,
        event_repo: EventRepository,
    ):
        self._paper_repo = paper_repo
        self._event_repo = event_repo
        self._y_position = 750

    def create_summary_pdf(self, event_id: int) -> SummaryPdfResponse:
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

        html_bytes_summary = self._create_html_summary(event_areas)

        return SummaryPdfResponse(
            summary_pdf_folder=str(event.s3_folder_name),
            summary_pdf_filename=f"{str(event.name).lower().replace(' ', '_')}_summary.html",
            summary_pdf=html_bytes_summary,
        )

    def _create_html_summary(self, event_areas: list[str]) -> bytes:
        buffer = BytesIO()

        content = ""
        pages = 0
        for area in event_areas:
            content += f"""
                <h1>{area}</h1>
            """
            papers = self._paper_repo.get_papers_by_area(area)
            for paper in papers:
                pages += int(paper.total_pages)
                content += f"""
                    <p><strong>Título:</strong> {(str(paper.title)).capitalize()} - <strong>{pages}</strong></p>
                    <p><strong>Autores:</strong> {str(paper.authors)}</p>
                    <div class="separator"></div>
                """

        template_html = """
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Summary</title>
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
                <style>
                    body {
                        font-family: 'Roboto', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f7f7f7;
                    }

                    .container {
                        max-width: 800px;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }

                    h1 {
                        font-size: 24px;
                        color: #333;
                        margin-bottom: 30px;
                    }

                    p {
                        font-size: 16px;
                        color: #555;
                    }

                    .separator {
                        border-top: 1px solid #ccc;
                        margin-top: 10px;
                        margin-bottom: 10px;
                    }
                </style>
            </head>""" + (
            f"""
            <body>
                <div class="container">
                    {content}
                </div>
            </body>

            </html> """
        )

        buffer.write(template_html.encode("UTF-8"))

        return buffer.getvalue()
