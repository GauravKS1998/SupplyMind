from datetime import date

from sqlalchemy.orm import Session

from app.common.document_number.enums import DocumentType
from app.common.document_number.model import DocumentSequence


def find_document_sequence_for_update(
    db: Session,
    document_type: DocumentType,
    sequence_date: date,
):
    return (
        db.query(DocumentSequence)
        .filter(
            DocumentSequence.document_type == document_type,
            DocumentSequence.sequence_date == sequence_date,
        )
        .with_for_update()  # for row locking to accomodate mutiple users
        .first()
    )


def save_document_sequence(
    db: Session,
    document_sequence: DocumentSequence,
):
    db.add(document_sequence)
    db.flush()

    return document_sequence
