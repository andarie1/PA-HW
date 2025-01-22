"""
Задача
Создать класс, который принимает данные пользователя в формате JSON и валидирует их на уровне типов данных.
Данные включают имя пользователя, возраст, email и адрес, состоящий из города, улицы и номера дома.
"""

from pydantic import BaseModel, EmailStr, field_validator

# class Address(BaseModel):
#     city: str
#     street: str
#     building: str | int
#
#
# class User(BaseModel):
#     name: str
#     age: int
#     email: EmailStr
#     address: Address
#
# if __name__ == '__main__':
#     json_string = """
#     {
#         "name": "John Doe",
#         "age": 22,
#         "email": "john.doe@example.com",
#         "address": {
#             "city": "New York",
#             "street": "5th Avenue",
#             "building": 123
#         }
#     }
#     """
#     user = User.model_validate_json(json_string, strict=True)
#     print(user)
#     print(user.model_dump_json(indent=4))


"""Задача
Создать систему для управления учетными записями пользователей, где необходимо:
Валидировать что email оканчивается на .com.
Проверить, что имя пользователя содержит только буквы."""
class User(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, username):
        if not username.isalpha():
            raise ValueError("Имя пользователя может содержать только буквы.")
        return username

    @field_validator("email")
    def validate_email(cls, email):
        if not email.endswith(".com"):
            raise ValueError("Email должен оканчиваться на '.com'.")
        return email

user = User(email="mybox@gmail.com")
print(user)

