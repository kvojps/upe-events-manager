from io import BytesIO
from fastapi import HTTPException, status
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
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

    def create_summary_pdf(self, event_id: int) -> SummaryPdfResponse:
        event = self._event_repo.get_event_by_id(event_id)

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

        buffer = BytesIO()
        summary_pdf = canvas.Canvas(buffer, pagesize=letter)
        summary_pdf.setFont("Helvetica-Bold", 12)

        y_position = 750

        for area in event_areas:
            summary_pdf.setFont("Helvetica-Bold", 16)
            if y_position < 60:
                summary_pdf.showPage()
                y_position = 750
            summary_pdf.drawString(100, y_position, f"Área: {area}")
            y_position -= 20
            papers = self._paper_repo.get_papers_by_area(area)
            for paper in papers:
                summary_pdf.setFont("Helvetica-Bold", 12)
                title_lines = simpleSplit(
                    "* " + str(paper.title).capitalize(),
                    summary_pdf._fontname,
                    summary_pdf._fontsize,
                    400,
                )
                for line in title_lines:
                    if y_position < 50:
                        summary_pdf.showPage()
                        y_position = 750
                        summary_pdf.setFont("Helvetica-Bold", 12)
                    summary_pdf.drawString(165, y_position, line)
                    y_position -= 20

                summary_pdf.setFont("Helvetica-Bold", 10)
                authors_lines = simpleSplit(
                    f"Autores: {paper.authors}",
                    summary_pdf._fontname,
                    summary_pdf._fontsize,
                    400,
                )
                for line in authors_lines:
                    if y_position < 50:
                        summary_pdf.showPage()
                        y_position = 750
                        summary_pdf.setFont("Helvetica-Bold", 10)
                    summary_pdf.drawString(165, y_position, line)
                    y_position -= 20

        summary_pdf.save()

        return SummaryPdfResponse(
            summary_pdf_folder=str(event.s3_folder_name),
            summary_pdf_filename=f"{str(event.name).lower().replace(' ', '_')}_summary.pdf",
            summary_pdf=buffer.getvalue(),
        )
