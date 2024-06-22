from typing import Optional
from sqlalchemy import or_
from core.domain.dto.paper import PaperDTO
from core.domain.paper import Paper
from core.infrastructure.repositories.paper import PaperRepository
from core.infrastructure.settings.db_connection import get_session


class PaperAdapter(PaperRepository):
    def create_paper(self, paper: PaperDTO) -> Paper:
        with get_session() as session:
            paper_data = Paper(
                pdf_id=paper.pdf_id,
                area=paper.area,
                title=paper.title,
                authors=paper.authors,
                is_ignored=paper.is_ignored,
                total_pages=paper.total_pages,
                event_id=paper.event_id,
            )

            session.add(paper_data)
            session.commit()
            session.refresh(paper_data)

            return paper_data

    def get_papers(
        self,
        search: Optional[str] = None,
        area: Optional[str] = None,
        event_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Paper]:
        with get_session() as session:
            papers = (
                session.query(Paper)
                .filter(
                    (
                        or_(
                            Paper.title.ilike(f"%{search}%"),
                            Paper.authors.ilike(f"%{search}%"),
                            Paper.pdf_id == search,
                        )
                        if search
                        else True
                    ),
                    Paper.area.ilike(area) if area else True,
                    Paper.event_id == event_id if event_id else True,
                )
                .order_by(Paper.title)
                .limit(page_size)
                .offset((page - 1) * page_size)
                .all()
            )

            return papers

    def get_paper_by_id(self, paper_id: int) -> Paper:
        with get_session() as session:
            return session.query(Paper).filter(Paper.id == paper_id).first()

    def get_papers_by_area(self, area: str) -> list[Paper]:
        with get_session() as session:
            return (
                session.query(Paper)
                .filter(Paper.area == area)
                .order_by(Paper.title)
                .all()
            )

    def get_paper_by_pdf_id(self, pdf_id: str) -> Paper:
        with get_session() as session:
            return session.query(Paper).filter(Paper.pdf_id == pdf_id).first()

    def get_first_paper(self) -> Paper:
        with get_session() as session:
            return session.query(Paper).first()

    def count_papers(
        self,
        search: Optional[str] = None,
        area: Optional[str] = None,
        event_id: Optional[int] = None,
    ) -> int:
        with get_session() as session:
            return (
                session.query(Paper)
                .filter(
                    (
                        or_(
                            Paper.title.ilike(f"%{search}%"),
                            Paper.authors.ilike(f"%{search}%"),
                            Paper.pdf_id == search,
                        )
                        if search
                        else True
                    ),
                    Paper.area.ilike(area) if area else True,
                    Paper.event_id == event_id if event_id else True,
                )
                .count()
            )

    def count_papers_by_event_id(self, event_id: int) -> int:
        with get_session() as session:
            return session.query(Paper).filter(Paper.event_id == event_id).count()

    def get_areas(self) -> list[str]:
        with get_session() as session:
            areas = (
                session.query(Paper.area)
                .filter(Paper.area.isnot(None))
                .distinct()
                .all()
            )

            return [area[0] for area in areas]

    def get_areas_by_event_id(self, event_id: int) -> list[str]:
        with get_session() as session:
            areas = (
                session.query(Paper.area)
                .filter(Paper.event_id == event_id)
                .distinct()
                .all()
            )

            return [area[0] for area in areas]

    def update_paper_pages(self, event_id: int, pdf_id: str, pages: int) -> Paper:
        with get_session() as session:
            paper_data = (
                session.query(Paper)
                .filter(Paper.event_id == event_id, Paper.pdf_id == pdf_id)
                .first()
            )

            paper_data.total_pages = pages

            session.commit()
            session.refresh(paper_data)

            return paper_data
