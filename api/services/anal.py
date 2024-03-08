import os
import tempfile
from fastapi import File, HTTPException, UploadFile, status
from PyPDF2 import PdfReader, PdfWriter
from api.ports.event import EventRepository
from api.services.file_handler import FileHandlerService, PutObjectResponse


class AnalService:
    def __init__(
        self,
        file_handler_service: FileHandlerService,
        event_repo: EventRepository,
    ):
        self._file_handler_service = file_handler_service
        self._event_repo = event_repo

    async def create_anal_pdf(
        self, event_id: int, cover: UploadFile = File(...)
    ) -> PutObjectResponse:
        event = self._event_repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if not event.summary_filename:
            raise HTTPException(status_code=404, detail="Summary file not found")

        if not event.merged_papers_filename:
            raise HTTPException(status_code=404, detail="Merged papers file not found")

        if not cover.filename:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The file must have a name",
            )

        if not cover.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="The file must be a pdf file",
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_writer = PdfWriter()

            cover_file_path = os.path.join(temp_dir, cover.filename)
            with open(cover_file_path, "wb") as buffer:
                buffer.write(await cover.read())
            self._add_pdf_pages_to_pdf_writer(pdf_writer, cover_file_path)

            summary_file_path = f"{temp_dir}/summary.pdf"
            self._file_handler_service.download_object(
                str(event.summary_filename), summary_file_path
            )
            self._add_pdf_pages_to_pdf_writer(pdf_writer, summary_file_path)

            merged_papers_file_path = f"{temp_dir}/merged_papers.pdf"
            self._file_handler_service.download_object(
                str(event.merged_papers_filename), merged_papers_file_path
            )
            self._add_pdf_pages_to_pdf_writer(pdf_writer, merged_papers_file_path)

            anal_file_path = os.path.join(temp_dir, f"{temp_dir}/anal.pdf")
            with open(anal_file_path, "wb+") as output_file:
                pdf_writer.write(anal_file_path)
                pdf_writer.close()

                return self._file_handler_service.put_object(
                    output_file.read(),
                    str(event.s3_folder_name),
                    "anal.pdf",
                )

    def _add_pdf_pages_to_pdf_writer(self, pdf_writer: PdfWriter, file_path: str):
        pdf_reader = PdfReader(file_path)

        for page_num in range(0, len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            pdf_writer.add_page(page_obj)
