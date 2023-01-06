from pydantic import BaseModel, Field, validator


class NewTask(BaseModel):
    task: int = Field(...,
                      description="Task ID. Идентификатор задания, в зависимости от него будут создаваться разные "
                                  "типы заданий: 1 - квартиры, 2 - юр. лица, 3 - частные дома, 4 - WTTX, "
                                  "41 - Подключение IPTV")
    fio: str = Field(None, description="FIO of customer")
    phone: str = Field(..., exclude=["", ''], description="Phone must be in format 7*********")
    address: str = Field(None, description="Address of customer")
    tariff: str = Field(None, description="Tariff that customer want")

    @validator('task')
    def check_id(cls, task_id):
        if task_id not in [1, 2, 3, 4, 41]:
            raise ValueError("Task with such ID not exist!")
        return task_id

    @validator('phone')
    def check_phone(cls, phone):
        if len(phone) == 0:
            raise ValueError("Phone can't be empty!")
        return phone

    # @validator('phone')
    # def check_number(cls, phone: str):
    #     if re.match(r'7[0-9]{10}', phone) is None:
    #         raise ValueError("Phone format is wrong")
    #     return phone
