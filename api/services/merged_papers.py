import os
import tempfile
import zipfile
from fastapi import File, HTTPException, UploadFile, status
from PyPDF2 import PdfReader, PdfWriter
from api.models.dto.paper import PaperDTO
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository
from api.services.file_handler import FileHandlerService, PutObjectResponse


class MergedPapersService:
    def __init__(
        self,
        file_handler_service: FileHandlerService,
        event_repo: EventRepository,
        paper_repo: PaperRepository,
    ):
        self._file_handler_service = file_handler_service
        self._event_repo = event_repo
        self._paper_repo = paper_repo

    async def merge_pdf_files(
        self, event_id: int, file: UploadFile = File(...)
    ) -> PutObjectResponse:
        event = self._event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )

        if event.merged_papers_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Papers already merged for this event",
            )

        if self._paper_repo.count_papers_by_event_id(event_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Papers already created for this event",
            )

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The file must have a name",
            )

        if not file.filename.lower().endswith(".zip"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="The file must be a zip file",
            )

        s3_folder_name = str(event.s3_folder_name)

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file_path = os.path.join(temp_dir, file.filename)
                with open(zip_file_path, "wb") as buffer:
                    buffer.write(await file.read())

                pdf_writer = PdfWriter()
                with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                    papers_registered: list[str] = []
                    for filename in zip_ref.namelist():
                        zip_ref.extract(filename, path=temp_dir)

                        self._add_paper_pages_to_pdf_writer(
                            pdf_writer, temp_dir, filename
                        )
                        # self._upload_paper_to_s3_event_folder(
                        #     zip_ref, s3_folder_name, filename
                        # )
                        self._create_paper_from_pdf(
                            papers_registered, temp_dir, filename
                        )
                merged_papers_path = os.path.join(temp_dir, "merged_papers.pdf")
                return self._upload_merged_papers_to_s3_event_folder(
                    merged_papers_path, pdf_writer, s3_folder_name
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while processing the file: {str(e)}",
            )

    def _add_paper_pages_to_pdf_writer(
        self, pdf_writer: PdfWriter, temp_dir: str, filename: str
    ):
        pdf_reader = PdfReader(os.path.join(temp_dir, filename))
        for page_num in range(0, len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            pdf_writer.add_page(page_obj)

    def _upload_paper_to_s3_event_folder(
        self, zip_ref: zipfile.ZipFile, event_folder: str, filename: str
    ):
        with zip_ref.open(filename) as pdf_file:
            self._file_handler_service.put_object(
                pdf_file.read(),
                f"{event_folder}",
                filename,
            )

    def _create_paper_from_pdf(
        self, papers_registered: list[str], temp_dir: str, filename: str
    ):
        pdf_id = os.path.splitext(os.path.basename(filename))[0]
        pdf_reader = PdfReader(os.path.join(temp_dir, filename))
        total_pages = len(pdf_reader.pages)

        if pdf_id not in papers_registered:
            self._paper_repo.create_paper(
                PaperDTO(
                    pdf_id=pdf_id,
                    area=None,
                    title=None,
                    authors=None,
                    is_ignored=None,
                    total_pages=total_pages,
                    event_id=None,
                )
            )
            papers_registered.append(pdf_id)

    def _upload_merged_papers_to_s3_event_folder(
        self, merged_papers_path: str, pdf_writer: PdfWriter, event_folder: str
    ) -> PutObjectResponse:
        with open(merged_papers_path, "wb+") as output_file:
            pdf_writer.write(merged_papers_path)
            pdf_writer.close()

            return self._file_handler_service.put_object(
                output_file.read(),
                event_folder,
                "merged_papers.pdf",
            )
