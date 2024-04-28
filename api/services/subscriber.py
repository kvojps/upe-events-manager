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
from api.config.dynaconf import settings
from api.models.event import Event
from api.models.subscriber import Subscriber
from api.ports.event import EventRepository
from api.ports.subscriber import SubscriberRepository
from api.services.responses.subscriber import (
    BatchSubscribersErrorResponse,
    BatchSubscribersResponse,
    SubscribersPaginatedResponse,
)
from api.utils.user_validator import validate_cpf, validate_email


class SubscriberService:
    def __init__(
        self, subscriber_repo: SubscriberRepository, event_repo: EventRepository
    ):
        self._subscriber_repo = subscriber_repo
        self._event_repo = event_repo

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

        csv_reader = csv.DictReader(decoded_content, delimiter=";")
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

    def _get_certificate_html(self, event: Event, subscriber: Subscriber):
        buffer = BytesIO()

        template_html = """
            <!DOCTYPE html>
            <html lang=en">
            <head>
                <title>Certificado SECAP</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link
                    href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
                    rel="stylesheet">
                <style>
                    body {
                        margin: 0;
                    }
                    main {
                        font-family: Poppins;
                    }
                    header {
                        background-color: #050973;
                        height: 200px;
                    }
                    h2 {
                        margin: 0px;
                        padding-top: 84px;
                    }
                    p {
                        margin: 0;
                    }
                    .div-titulo {
                        height: 200px;
                        font-size: 32px;
                        text-align: center;
                    }
                    .div-desc {
                        height: 100px;
                        text-align: center;

                        p {
                            padding: 0px 12px 0px 12px;
                        }
                    }
                    .div-assinaturas {
                        position: relative;
                        height: 200px;
                        padding-bottom: 40px;
                        text-align: center;

                    }
                    .img-assinatura {
                        position: absolute;
                        top: 15px;
                        right: 45%;
                    }
                    footer {
                        position: absolute;
                        margin: 0 2.5%;
                        width: 95%;

                        .div-parceiros {
                            align-items: center;
                            gap: 25px;
                        }
                    }
                    .parceiros {
                        margin: 0px 5px;
                    }
                    .secap {
                        right: 0%;
                        position: absolute;
                        justify-self: end;
                        margin-top: -40px;
                    }
                </style>
            </head>""" + (
            f"""
            <body>
                <main>
                    <header>
                    </header>
                    <div class="div-titulo">
                        <h1>CERTIFICADO</h1>
                    </div>
                    <div class="div-desc">
                        <p>
                            CERTIFICAMOS QUE <strong> {subscriber.name}</strong> PARTICIPOU COMO <strong>OUVINTE</strong> NA
                            <strong> {event.name}</strong>,
                            PROMOVIDA PELA {event.promoted_by}, DE {event.initial_date} A {event.final_date}, COM CARGA HORÁRIA DE
                            <strong>{subscriber.workload} </strong>HORAS.
                        </p>

                    </div>
                    <div class="div-assinaturas">
                        <img class="img-assinatura" style="width: 180px;" src="{settings.S3_BASE_URL}resources/higor_signature.png" alt="">
                        <h2>HIGOR RICARDO MONTEIRO SANTOS</h2>
                        <p>Coordenador Setorial de Extensão e Cultura da UPE Garanhuns</p>
                    </div>
                    <footer>
                        <div class="div-parceiros">
                            <img class="parceiros" style="width: 80px"
                                src="{settings.S3_BASE_URL}resources/upe_icon.png"
                                alt="">
                            <img class="parceiros" style="width: 60px"
                                src="{settings.S3_BASE_URL}resources/ufape_icon.png"
                                alt="">
                            <img class="parceiros" style="width: 90px"
                                src="{settings.S3_BASE_URL}resources/ifpe_icon.png"
                                alt="">
                            <img class="parceiros" style="width: 90px"
                                src="{settings.S3_BASE_URL}resources/aesga_icon.png" alt="">
                        </div>
                        <div class="secap">
                            <img class="secap" style="width: 120px"
                                src="{settings.S3_BASE_URL}resources/secap_icon.png"
                                alt="">
                        </div>
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

        csv_reader = csv.DictReader(decoded_content, delimiter=";")
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
        except Exception as e:
            batch_subscribers_errors.append(
                BatchSubscribersErrorResponse(
                    id=subscriber_to_update.email if subscriber_to_update.email else "No id available",  # type: ignore
                    message=f"Exception creating subscriber: {str(e)}",
                )
            )
