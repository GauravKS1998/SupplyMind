from sqlalchemy import Integer, String, Float, ForeignKey, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    sku: Mapped[str] = mapped_column(String(255), unique=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id"))

    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_types.id"))

    price: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    supplier = relationship("Supplier")
    category = relationship("Category")
    subcategory = relationship("SubCategory")
    product_type = relationship("ProductType")
