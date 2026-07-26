from datetime import date

from sqlalchemy.orm import Session

from .enums import DocumentType
from .model import DocumentSequence
from .repository import (
    find_document_sequence_for_update,
    save_document_sequence,
)


def get_next_document_number(db: Session, document_type: DocumentType):
    today = date.today()

    document_sequence = find_document_sequence_for_update(
        db=db, document_type=document_type, sequence_date=today
    )

    if not document_sequence:

        document_sequence = DocumentSequence(
            document_type=document_type, sequence_date=today, last_sequence=0
        )

        save_document_sequence(db, document_sequence)

    document_sequence.last_sequence += 1

    return _format_document_number(
        document_type=document_type,
        sequence_date=today,
        sequence=document_sequence.last_sequence,
    )


def _format_document_number(
    document_type: DocumentType, sequence_date: date, sequence: int
):
    return (
        f"{document_type.value}-"
        f"{sequence_date.strftime('%y%m%d')}-"
        f"{sequence:04d}"
    )
