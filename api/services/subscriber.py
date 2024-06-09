import csv
import os
import shutil
import uuid
from io import BytesIO
from math import ceil
import pdfkit  # type: ignore
from fastapi import File, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from validate_docbr import CPF  # type: ignore
from core.infrastructure.settings.env_handler import settings
from api.models.event import Event
from api.models.subscriber import Subscriber
from core.infrastructure.shared.cloud.email_handler import EmailHandlerProvider
from core.infrastructure.repositories.event import EventRepository
from core.infrastructure.repositories.subscriber import SubscriberRepository
from api.services.responses.subscriber import (
    BatchSubscribersErrorResponse,
    BatchSubscribersResponse,
    SubscribersPaginatedResponse,
)
from api.utils.user_validator import validate_cpf, validate_email


class SubscriberService:
    def __init__(
        self,
        subscriber_repo: SubscriberRepository,
        event_repo: EventRepository,
        ses_adapter: EmailHandlerProvider,
    ):
        self._subscriber_repo = subscriber_repo
        self._event_repo = event_repo
        self._ses_adapter = ses_adapter

    async def batch_create_subscribers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> BatchSubscribersResponse:
        if not (event := self._event_repo.get_event_by_id(event_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are allowed",
            )

        content = await file.read()
        try:
            decoded_content = content.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Invalid CSV file: Format must be utf-8",
            )

        csv_reader = csv.DictReader(decoded_content, delimiter=",")
        batch_subscribers_errors: list[BatchSubscribersErrorResponse] = []
        cpf_validator = CPF()
        for row in csv_reader:
            self._create_subscriber_by_csv_row(
                row, int(event.id), batch_subscribers_errors, cpf_validator
            )

        return BatchSubscribersResponse(
            detail="Batch subscribers finished",
            errors=batch_subscribers_errors,
        )

    def _create_subscriber_by_csv_row(
        self,
        row,
        event_id: int,
        batch_subscribers_errors: list[BatchSubscribersErrorResponse],
        cpf_validator: CPF,
    ) -> None:
        try:
            cpf_row = str(row["cpf"])
            email_row = str(row["email"])

            validate_cpf(cpf_validator, cpf_row)
            validate_email(email_row)
            self._subscriber_repo.create_subscriber(
                cpf=cpf_row,
                email=email_row,
                event_id=event_id,
            )
        except KeyError as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id="Invalid CSV row",
                    message=f"Error creating subscriber: {str(e)}",
                )
            )
        except SQLAlchemyError as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id=f"cpf: {cpf_row} - email: {email_row}",
                    message=f"Subscriber already exists: CPF or email already registered",
                )
            )
        except ValueError as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id=f"cpf: {cpf_row} - email: {email_row}",
                    message=f"Error creating subscriber: {str(e)}",
                )
            )
        except Exception as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id=cpf_row if cpf_row else "CPF not found",
                    message=f"Exception creating subscriber: {str(e)}",
                )
            )

    def get_subscribers_by_event_id(
        self, event_id: int, page: int = 1, page_size: int = 10
    ) -> SubscribersPaginatedResponse:

        if not self._event_repo.get_event_by_id(event_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        subscribers_amount = self._subscriber_repo.count_subscribers_by_event_id(
            event_id
        )
        return SubscribersPaginatedResponse.from_subscribers(
            subscribers=self._subscriber_repo.get_subscribers(
                event_id, page, page_size
            ),
            total_subscribers=subscribers_amount,
            total_pages=ceil(subscribers_amount / page_size),
            current_page=page,
        )

    def get_subscriber_certificate(self, event_id: int, email: str) -> bytes:
        if not (event := self._event_repo.get_event_by_id(event_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if not (
            subscriber := self._subscriber_repo.get_event_subscriber_by_email(
                event_id, email
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscriber not found",
            )

        html_bytes_certificate = self._get_certificate_html(event, subscriber)
        return self._get_certficate_pdf(html_bytes_certificate)

    async def send_all_certificates(self, event_id: int):
        listeners = self._subscriber_repo.get_listeners(event_id)

        if listeners is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listeners not found",
            )

        for listener in listeners:
            certificate = self.get_subscriber_certificate(event_id, str(listener.email))
            self._ses_adapter.send_raw_email(certificate, listener)
            print(listener.email)

    def _get_certificate_html(self, event: Event, subscriber: Subscriber):
        buffer = BytesIO()

        initial_date = str(event.initial_date).replace("-", "/")
        final_date = str(event.final_date).replace("-", "/")

        template_html = """
            <!DOCTYPE html>
            <html lang=en">
            <head>
                <title>Certificado SECAP</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                @font-face {
                    font-family: 'Poppins';
                    src: url('https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap');
                }
            body {
                
                    margin: 0; 
                    width: 100%;
                    height: 100%;
                    font-family: Arial; 
                    background-color: #fef7ee
                }
            main {
                width: 1920px;
                margin: 0;
                height: 1080px;
            }
            header {
                width: 100%;
                height: 200px;
                position: relative;
                top: 0;
            }
            .div-titulo {
                text-align: center;
            }
            .div-desc {
                width: 85%;
                margin: 0 auto;
                padding-top: 100px;
                padding-bottom: 100px;
            }
            .div-desc p {
                font-size: 24px;
            }
            .div-assinaturas {
                width: 100%;
                height: 180px;
                text-align: center;
            }
            .div-assinaturas-content {
                display: inline-block;
                text-align: center;
            }
            footer {
                padding-top: 64px;
                margin-top: 9px;
                width: 100%;
                position: relative;
                bottom: 0;
                }
            
        }
      </style>
            </head>""" + (
            f"""
            <body>
                <main>
                    <header>
                        <img style="width: 100%" src="{settings.S3_BASE_URL}cabecalho_certificado.png"/>
                    </header>
                    <div class="div-titulo">
                        <img style="" src="{settings.S3_BASE_URL}titulo_certificado.png"/>
                    </div>
                    <div class="div-desc">
                        <p>
                            CERTIFICAMOS QUE <strong>{str(subscriber.name).upper()}</strong> PARTICIPOU COMO <strong>OUVINTE</strong> NA
                            <strong> {str(event.name).upper()}</strong>,
                            PROMOVIDA PELA {str(event.promoted_by).upper()}, DE <strong>{initial_date}</strong> A <strong>{final_date}</strong>, COM CARGA HORÁRIA DE
                            <strong>{subscriber.workload} </strong>HORA(S).
                        </p>

                    </div>
                    <div class="div-assinaturas">
                        <div class="div-assinaturas-content">
                            <img style="width: 70%" src="{settings.S3_BASE_URL}assinatura_certificado.png" alt="">
                        </div>
                    </div>
                    <footer >
                        <img src="{settings.S3_BASE_URL}rodape_certificado.png" style="width: 100%"/>
                    </footer>
                </main>
            </body>
            </html>"""
        )
        buffer.write(template_html.encode("UTF-8"))

        return buffer.getvalue()

    def _get_certficate_pdf(self, html_bytes_summary: bytes) -> bytes:
        buffer = BytesIO()

        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        session_id = uuid.uuid4()

        temp_html_file_path = f"{temp_dir}/{session_id}__summary.html"
        with open(temp_html_file_path, "wb") as file:
            file.write(html_bytes_summary)

        temp_pdf_file_path = f"{temp_dir}/{session_id}__summary.pdf"
        options = {
            "orientation": "Landscape",
            "page-size": "A4",
            "no-outline": None,
            "margin-top": "0",
            "margin-right": "0",
            "margin-bottom": "0",
            "margin-left": "0",
        }
        pdfkit.from_file(temp_html_file_path, temp_pdf_file_path, options=options)

        buffer.write(open(temp_pdf_file_path, "rb").read())

        shutil.rmtree(temp_dir)

        return buffer.getvalue()

    async def batch_update_subscribers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> BatchSubscribersResponse:
        if not (event := self._event_repo.get_event_by_id(event_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are allowed",
            )

        content = await file.read()
        try:
            decoded_content = content.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Invalid CSV file: Format must be utf-8",
            )

        csv_reader = csv.DictReader(decoded_content, delimiter=",")
        batch_subscribers_errors: list[BatchSubscribersErrorResponse] = []

        for row in csv_reader:
            self._update_subscriber_by_csv_row(
                row, int(event.id), batch_subscribers_errors
            )

        return BatchSubscribersResponse(
            detail="Batch subscribers finished",
            errors=batch_subscribers_errors,
        )

    def _update_subscriber_by_csv_row(
        self,
        row,
        event_id: int,
        batch_subscribers_errors: list[BatchSubscribersErrorResponse],
    ) -> None:
        try:
            if subscriber_to_update := self._subscriber_repo.get_event_subscriber_by_email(
                event_id, str(row["email"])
            ):
                subscriber_to_update.name = str(row["nome"])  # type: ignore
                subscriber_to_update.workload = float(row["ch"])  # type: ignore
                subscriber_to_update.is_present = True  # type: ignore

                self._subscriber_repo.update_subscriber(subscriber_to_update)
        except KeyError as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id="Invalid CSV row",
                    message=f"Error creating subscriber: {str(e)}",
                )
            )
        except Exception as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id=subscriber_to_update.email if subscriber_to_update.email else "No id available",  # type: ignore
                    message=f"Exception creating subscriber: {str(e)}",
                )
            )
