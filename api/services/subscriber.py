import csv
from fastapi import File, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from validate_docbr import CPF  # type: ignore
from api.ports.event import EventRepository
from api.ports.subscriber import SubscriberRepository
from api.services.responses.subscriber import (BatchSubscribersErrorResponse,
                                               BatchSubscribersResponse)
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
                    id=cpf_row if cpf_row else "CPF not found",
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
