from io import BytesIO
from math import ceil
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository


class EventsPaginatedResponse(BaseModel):
    events: list[EventResponse]
    total_papers: int
    total_pages: int
    current_page: int


class EventService:
    def __init__(self, event_repo: EventRepository, paper_repo: PaperRepository):
        self._event_repo = event_repo
        self._paper_repo = paper_repo

    def create_event(self, event: EventDTO) -> EventResponse:
        event_data = self._event_repo.create_event(event)

        return EventResponse.from_event(event_data)

    def create_summary(self, event_id: int) -> bytes:
        event_areas = self._paper_repo.get_areas_by_event_id(event_id)

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
                    "* " + str(paper.title),
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

        return buffer.getvalue()

    def get_events(self, page: int = 1, page_size: int = 10) -> EventsPaginatedResponse:
        events_data = self._event_repo.get_events(page, page_size)
        events_response = [
            EventResponse.from_event(event_data) for event_data in events_data
        ]

        return EventsPaginatedResponse(
            events=events_response,
            total_papers=self._event_repo.count_events(),
            total_pages=ceil(self._event_repo.count_events() / page_size),
            current_page=page,
        )
