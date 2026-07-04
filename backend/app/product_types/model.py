from sqlalchemy import Integer, String, ForeignKey, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class ProductType(Base):

    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    subcategory = relationship("SubCategory")
