from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    sku: Mapped[str] = mapped_column(String(255), unique=True)

    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id"))

    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_types.id"))

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    uom_id: Mapped[int] = mapped_column(ForeignKey("units_of_measure.id"))

    purchase_price: Mapped[float] = mapped_column(Float)

    selling_price: Mapped[float] = mapped_column(Float)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    deactivated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    reactivated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    supplier = relationship("Supplier")
    category = relationship("Category")
    subcategory = relationship("SubCategory")
    product_type = relationship("ProductType")

    brand = relationship("Brand")
    uom = relationship("UnitOfMeasure")
