import os
import sys
import tempfile
import time
import zipfile
from fastapi import File, HTTPException, UploadFile, status
from PyPDF2 import PdfReader, PdfWriter
from core.infrastructure.repositories.event import EventRepository
from core.infrastructure.repositories.paper import PaperRepository
from api.services.file_handler import FileHandlerService
from api.contracts.responses.file_handler import PutObjectResponse
from api.utils.progress_checker import ProgressChecker


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
        self._papers_registered: list[str] = []
        self._papers_not_founded: list[str] = []

    async def merge_pdf_files(
        self, event_id: int, file: UploadFile = File(...)
    ) -> PutObjectResponse:
        event = self._event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if event.merged_papers_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Papers already merged for this event",
            )

        if self._paper_repo.count_papers_by_event_id(event_id) == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Papers not found for this event",
            )

        s3_folder_name = str(event.s3_folder_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            merged_papers_pdf_writer = await self._process_zip_file(
                temp_dir, file, event_id
            )

            if (papers_length := len(self._papers_not_founded)) > 0:
                detail = f"{papers_length} papers not found on zip: {', '.join(self._papers_not_founded)}"
                self._papers_not_founded = []
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=detail,
                )

            merged_papers_path = os.path.join(temp_dir, "merged_papers.pdf")
            return self._upload_merged_papers_to_s3_event_folder(
                merged_papers_path, merged_papers_pdf_writer, s3_folder_name
            )

    async def _process_zip_file(
        self, temp_dir: str, file: UploadFile, event_id: int
    ) -> PdfWriter:
        zip_file_path = await self._add_zip_file_to_temp_dir(temp_dir, file)
        pdf_writer = PdfWriter()
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            current_file = 1
            start_time = time.time()

            event_areas = self._paper_repo.get_areas_by_event_id(event_id)
            for area in event_areas:
                papers = self._paper_repo.get_papers_by_area(area)
                for paper in papers:
                    self._proccess_pdf_file(
                        event_id,
                        zip_ref,
                        pdf_writer,
                        temp_dir,
                        f"{paper.pdf_id}.pdf",
                        current_file,
                        start_time,
                    )
                    current_file += 1

        self._papers_registered = []

        return pdf_writer

    async def _add_zip_file_to_temp_dir(self, temp_dir: str, file: UploadFile) -> str:
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

        zip_file_path = os.path.join(temp_dir, file.filename)
        with open(zip_file_path, "wb") as buffer:
            buffer.write(await file.read())

        return zip_file_path

    def _proccess_pdf_file(
        self,
        event_id: int,
        zip_ref: zipfile.ZipFile,
        pdf_writer: PdfWriter,
        temp_dir: str,
        filename: str,
        current_file: int,
        start_time: float,
    ) -> None:
        try:
            zip_ref.extract(f"{zip_ref.namelist()[0]}{filename}", path=temp_dir)
        except KeyError:
            self._papers_not_founded.append(filename)
            return

        self._add_paper_pages_to_pdf_writer(zip_ref, pdf_writer, temp_dir, filename)

        # self._upload_paper_to_s3_event_folder(
        #     zip_ref, s3_folder_name, filename
        # )

        self._update_paper_from_pdf(event_id, zip_ref, temp_dir, filename)
        ProgressChecker.get_progress(
            "Progresso do cadastro",
            current_file,
            len(zip_ref.namelist()),
            start_time,
        )

    def _add_paper_pages_to_pdf_writer(
        self,
        zip_ref: zipfile.ZipFile,
        pdf_writer: PdfWriter,
        temp_dir: str,
        filename: str,
    ):
        pdf_reader = PdfReader(
            os.path.join(temp_dir, f"{zip_ref.namelist()[0]}{filename}")
        )
        for page_num in range(0, len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            pdf_writer.add_page(page_obj)

    def _upload_paper_to_s3_event_folder(
        self, zip_ref: zipfile.ZipFile, event_folder: str, filename: str
    ) -> None:
        with zip_ref.open(filename) as pdf_file:
            self._file_handler_service.put_object(
                pdf_file.read(),
                f"{event_folder}",
                filename,
            )

    def _update_paper_from_pdf(
        self, event_id: int, zip_ref: zipfile.ZipFile, temp_dir: str, filename: str
    ) -> None:
        pdf_id = os.path.splitext(os.path.basename(filename))[0]
        pdf_reader = PdfReader(
            os.path.join(temp_dir, f"{zip_ref.namelist()[0]}{filename}")
        )
        total_pages = len(pdf_reader.pages)

        if pdf_id.split()[0] not in self._papers_registered:
            self._paper_repo.update_paper_pages(event_id, pdf_id, total_pages)
            self._papers_registered.append(pdf_id)

    def _upload_merged_papers_to_s3_event_folder(
        self, merged_papers_path: str, pdf_writer: PdfWriter, event_folder: str
    ) -> PutObjectResponse:
        with open(merged_papers_path, "wb+") as output_file:
            start_time = time.time()
            pdf_writer.write(merged_papers_path)
            pdf_writer.close()
            sys.stdout.write(
                f"\nTempo para criação do Merged papers PDF local: {time.time() - start_time:.2f} seconds\n"
            )

            return self._file_handler_service.put_object(
                output_file.read(),
                event_folder,
                "merged_papers.pdf",
            )
