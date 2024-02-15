from io import BytesIO
from math import ceil
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
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

        y_position = 750  # Posição inicial Y

        for area in event_areas:
            # Escreva o título da área
            summary_pdf.setFont("Helvetica-Bold", 16)
            summary_pdf.drawString(100, y_position, f"Área: {area}")
            y_position -= 20  # Atualize a posição Y

            papers = self._paper_repo.get_papers_by_area(area)
            for paper in papers:
                # Escreva o título do paper
                summary_pdf.setFont("Helvetica-Bold", 12)
                summary_pdf.drawString(165, y_position, str(paper.title))
                y_position -= 20  # Atualize a posição Y

                # Escreva os autores
                summary_pdf.setFont("Helvetica", 12)
                summary_pdf.drawString(165, y_position, f"Autores: {', '.join(paper.authors)}")
                y_position -= 20  # Atualize a posição Y

                if y_position < 50:
                    summary_pdf.showPage()
                    y_position = 750  # Reinicie a posição Y para a próxima página

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
