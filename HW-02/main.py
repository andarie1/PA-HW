import json
from pydantic import BaseModel, Field, field_validator, EmailStr


class Address(BaseModel):
    city: str = Field(..., min_length=2, max_length=50)
    street: str = Field(..., min_length=3, max_length=50)
    house_number: str = Field(..., min_length=1, max_length=10)


class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, pattern=r'^[A-Za-z]+$')
    age: int = Field(..., ge=0, le=120)
    email: EmailStr = Field(..., min_length=10, max_length=50)
    is_employed: bool = Field(default=False)
    address: Address

    @field_validator('is_employed')
    def validate_is_employed(cls, v, info):
        if v and (info.data['age'] < 18 or info.data['age'] > 65):
            raise ValueError("Only individuals between 18 and 65 years old can be employed.")
        return v


valid_json_data = json.dumps({
    "name": "JohnDoe",
    "age": 30,
    "email": "johndoe@example.com",
    "is_employed": True,
    "address": {
        "city": "NewYork",
        "street": "MainStreet",
        "house_number": "123"
    }
})

invalid_age_json_data = json.dumps({
    "name": "JaneDoe",
    "age": 17,
    "email": "janedoe@example.com",
    "is_employed": True,
    "address": {
        "city": "NewYork",
        "street": "MainStreet",
        "house_number": "123"
    }
})

try:
    valid_user = User(**json.loads(valid_json_data))
    print("Valid data processed successfully:")
    print(valid_user.model_dump_json())
except ValueError as e:
    print(f"Error processing valid data: {e} (should not occur)")

try:
    invalid_user = User(**json.loads(invalid_age_json_data))
    print("Invalid data processed successfully (should fail):")
    print(invalid_user.model_dump_json())
except ValueError as e:
    print(f"Error processing invalid data (expected behavior): {e}")