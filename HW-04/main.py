from sqlalchemy import Column, String, ForeignKey, Boolean, Numeric, Integer, create_engine, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)

category_electronics = Category(name="Электроника", description="Гаджеты и устройства.")
category_books = Category(name="Книги", description="Печатные книги и электронные книги.")
category_clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([category_electronics, category_books, category_clothing])
session.commit()

session.add_all([
    Product(name="Смартфон", price=299.99, in_stock=True, category=category_electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=category_electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=category_books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=category_clothing),
    Product(name="Футболка", price=20.00, in_stock=True, category=category_clothing),
])
session.commit()

# 1. Извлекаем все категории и их продукты
all_categories = session.query(Category).all()
for category in all_categories:
    print(f"Категория: {category.name}")
    for product in category.products:
        print(f"  - {product.name}: {product.price}$")
    print()

# 2. Находим первый продукт и обновляем цену
smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()

# Проверяем изменение цены
smartphone = session.query(Product).filter_by(name="Смартфон").first()
print(f"Обновленный смартфон: {smartphone.name}, новая цена: {smartphone.price}$")

# 3. Подсчет продуктов по каждой категории
category_counts = (
    session.query(Category.name, func.count(Product.id).label("count"))
    .join(Product)
    .group_by(Category.id)
    .all()
)
print("\nКоличество продуктов в каждой категории:")
for category_name, count in category_counts:
    print(f"{category_name}: {count} продуктов")

# 4. Категории где больше одного
categories_with_multiple_products = (
    session.query(Category.name)
    .join(Product)
    .group_by(Category.id)
    .having(func.count(Product.id) > 1)
    .all()
)
print("\nКатегории с более чем одним продуктом:")
for category_name in categories_with_multiple_products:
    print(category_name[0])




