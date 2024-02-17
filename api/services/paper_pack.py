import os
import tempfile
import zipfile
from fastapi import File, HTTPException, UploadFile, status
from PyPDF2 import PdfReader, PdfWriter
from api.ports.event import EventRepository
from api.services.file_handler import FileHandlerService, PutObjectResponse


class PaperPackService:
    def __init__(
        self,
        file_handler_service: FileHandlerService,
        event_repository: EventRepository,
    ):
        self._file_handler_service = file_handler_service
        self._event_repository = event_repository

    async def merge_pdf_files(
        self, event_id: int, file: UploadFile = File(...)
    ) -> PutObjectResponse:
        event = self._event_repository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )

        if event.all_papers_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Papers already merged for this event",
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
                    for filename in zip_ref.namelist():
                        if filename.lower().endswith(".pdf"):
                            zip_ref.extract(filename, path=temp_dir)
                            pdf_reader = PdfReader(os.path.join(temp_dir, filename))
                            for page_num in range(0, len(pdf_reader.pages)):
                                page_obj = pdf_reader.pages[page_num]
                                pdf_writer.add_page(page_obj)

                            with zip_ref.open(filename) as pdf_file:
                                self._file_handler_service.put_object(
                                    pdf_file.read(),
                                    f"{s3_folder_name}",
                                    filename,
                                )

                merged_papers_path = os.path.join(temp_dir, "merged_papers.pdf")
                with open(merged_papers_path, "wb+") as output_file:
                    pdf_writer.write(merged_papers_path)
                    pdf_writer.close()

                    put_object_response = self._file_handler_service.put_object(
                        output_file.read(),
                        s3_folder_name,
                        "merged_papers.pdf",
                    )

                return put_object_response
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while processing the file: {str(e)}",
            )
