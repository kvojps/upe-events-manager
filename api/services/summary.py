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
        self._y_position = 750
        self.page_iterator = 0

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

        buffer = BytesIO()
        summary_pdf = canvas.Canvas(buffer, pagesize=letter)
        summary_pdf.setFont("Helvetica-Bold", 12)

        for area in event_areas:
            self._write_area_on_pdf(summary_pdf, area)
            papers = self._paper_repo.get_papers_by_area(area)
            for paper in papers:
                self._write_title_on_pdf(summary_pdf, str(paper.title))
                self._write_authors_on_pdf(summary_pdf, str(paper.authors), int(paper.total_pages))

        summary_pdf.save()
        self.page_iterator = 0

        return SummaryPdfResponse(
            summary_pdf_folder=str(event.s3_folder_name),
            summary_pdf_filename=f"{str(event.name).lower().replace(' ', '_')}_summary.pdf",
            summary_pdf=buffer.getvalue(),
        )

    def _write_area_on_pdf(self, summary_pdf: canvas.Canvas, area: str):
        summary_pdf.setFont("Helvetica-Bold", 16)
        if self._y_position < 60:
            summary_pdf.showPage()
            self._y_position = 750
        summary_pdf.drawString(100, self._y_position, f"Área: {area}")
        self._y_position -= 20

    def _write_title_on_pdf(self, summary_pdf: canvas.Canvas, title: str):
        summary_pdf.setFont("Helvetica-Bold", 12)
        title_lines = simpleSplit(
            "* " + str(title).capitalize(),
            summary_pdf._fontname,
            summary_pdf._fontsize,
            400,
        )
        for line in title_lines:
            if self._y_position < 50:
                summary_pdf.showPage()
                self._y_position = 750
                summary_pdf.setFont("Helvetica-Bold", 12)
            summary_pdf.drawString(165, self._y_position, line)
            self._y_position -= 20

    def _write_authors_on_pdf(self, summary_pdf: canvas.Canvas, authors: str, pages: int):
        summary_pdf.setFont("Helvetica-Bold", 10)
        authors_lines = simpleSplit(
            f"Autores: {authors}",
            summary_pdf._fontname,
            summary_pdf._fontsize,
            400,
        )
        for line in authors_lines:
            pagination_text = str(self.page_iterator + 1)
            if self._y_position < 50:
                summary_pdf.showPage()
                self._y_position = 750
                summary_pdf.setFont("Helvetica-Bold", 10)
            summary_pdf.drawString(165, self._y_position, line)

            if (len(authors_lines) - authors_lines.index(line)) < 2:
                summary_pdf.drawRightString(600, self._y_position, pagination_text)
                self.page_iterator += pages
            self._y_position -= 20
