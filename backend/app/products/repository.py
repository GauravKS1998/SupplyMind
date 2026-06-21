from sqlalchemy.orm import Session

from .model import Product


def find_all(db: Session):  # Similar to EntityManager/JpaRepository
    return db.query(Product).all()  # Similar to productRepository.findAll()


def find_by_id(db: Session, product_id: int):
    return (
        db.query(Product).filter(Product.id == product_id).first()
    )  # Similar to productRepository.findById(id)


def save(db: Session, product: Product):  # Similar to EntityManager/JpaRepository
    db.add(product)  # similar to repository.save(product)
    db.commit()  # Equivalent to transaction commit
    db.refresh(product)  # Equivalent to entityManager.refresh(entity)

    return product


def delete(db: Session, product: Product):
    db.delete(product)  # Similar to repository.delete(entity);
    db.commit()
