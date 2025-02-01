from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import pandas as pd

# Задача 1: Создаём экземпляр движка для подключения к SQLite базе данных в памяти.
engine = create_engine('sqlite:///:memory:', echo=False)

# Задача 2: Создаём базовый класс и сессию для взаимодействия с БД.
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# Задача 3: Определяем модель Product.
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric, nullable=False)
    in_stock = Column(Boolean, nullable=False, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', back_populates='products')

# Задача 4: Определяем модель Category.
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
.
    products = relationship('Product', back_populates='category')

# Задача 5: Создаём таблицы в базе данных.
Base.metadata.create_all(engine)

# Добавление данных в базу.
category = Category(name="Electronics", description="Electronic gadgets and devices")
session.add(category)  # Добавляем категорию в сессию.
session.commit()  # Сохраняем изменения.

# Добавляем продукты, связывая их с категорией.
product1 = Product(name="Smartphone", price=699.99, in_stock=True, category_id=category.id)
product2 = Product(name="Laptop", price=999.99, in_stock=True, category_id=category.id)

# Добавляем продукты в сессию и сохраняем.
session.add_all([product1, product2])
session.commit()

# Используем pandas для извлечения данных из базы и красивого вывода.
def query_to_dataframe(query):
    """Преобразует результат SQLAlchemy-запроса в pandas DataFrame."""
    return pd.DataFrame(
        [
            {
                "Product Name": product.name,
                "Price": float(product.price),
                "In Stock": product.in_stock,
                "Category Name": product.category.name,
                "Category Description": product.category.description,
            }
            for product in query
        ]
    )

# Выполняем запрос к таблице Product и преобразуем его в DataFrame.
query = session.query(Product).all()
df = query_to_dataframe(query)

# Выводим результат в красивом табличном формате.
print(df.to_string(index=False))




