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


# Пересоздаем таблицы
Base.metadata.create_all(engine)

# Добавляем категории и сразу получаем их объекты
category_electronics = Category(name="Электроника", description="Гаджеты и устройства.")
category_books = Category(name="Книги", description="Печатные книги и электронные книги.")
category_clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([category_electronics, category_books, category_clothing])
session.commit()

# Добавляем продукты
session.add_all([
    Product(name="Смартфон", price=299.99, in_stock=True, category=category_electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=category_electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=category_books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=category_clothing),
    Product(name="Футболка", price=20.00, in_stock=True, category=category_clothing),
])
session.commit()

# 2. Чтение данных
# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.
# Задание 3. Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
# Задание 4. Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
# Задание 5. Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.

all_categories = session.query(Category).all()
print(all_categories)

update_price = session.query(Category).get(1)
if update_price:
    update_price.price = 349.99
    session.commit()

update_price = session.query(Category).get(1)
print(update_price)

count_products = session.query(Product.id).func.count().label('count').group_by(Product.name).all()
print(count_products)






