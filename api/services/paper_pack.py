import os
import tempfile
import zipfile
from fastapi import File, HTTPException, UploadFile, status
from PyPDF2 import PdfMerger
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
        if file.filename and not file.filename.lower().endswith(".zip"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="The file must be a zip file",
            )

        s3_folder_name = str(
            self._event_repository.get_event_by_id(event_id).s3_folder_name
        )

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file_path = os.path.join(temp_dir, file.filename)  # type: ignore
                with open(zip_file_path, "wb") as buffer:
                    buffer.write(await file.read())

                merger = PdfMerger(False, "merged_papers.pdf")

                with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                    for filename in zip_ref.namelist():
                        if filename.lower().endswith(".pdf"):
                            with zip_ref.open(filename) as pdf_file:
                                # self._file_handler_service.put_object(
                                #     pdf_file.read(),
                                #     f"{s3_folder_name}",
                                #     filename,
                                # )
                                merger.append(pdf_file)
                merged_papers_path = os.path.join(temp_dir, "merged_papers.pdf")
                with open(merged_papers_path, "wb+") as output_file:
                    merger.write(output_file)
                    merger.close()
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
