from pydantic import BaseModel


class SummaryPdfResponse(BaseModel):
    summary_pdf_folder: str
    summary_pdf_filename: str
    summary_pdf: bytes