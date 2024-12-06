import datetime
from typing import Annotated, Optional
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Order(BaseModel):
    number : int
    startDate : datetime.date
    device : str
    model : str
    description : str
    client : str
    phone_number : str
    status : str
    master : Optional[str] = "Не назначен"
    comments : Optional[list] = []

class UpdateOrderDTO(BaseModel):
    number : int
    status : Optional[str] = ""
    description : Optional[str] = ""
    master : Optional[str] = ""
    comment : Optional[str] = str

message = ""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

repo = [
    Order(
        number = 1,
        startDate = "2020-12-10",
        device = "Принтер",
        model = "3000",
        description = "Сломался",
        client = "Иванов Иван Иванович",
        phone_number = "+79573759836",
        status = "новая заявка"
    )
]

@app.get("/orders")
def get_orders(param = None):
    global message
    buffer = message
    message = ""
    if(param):
        return {"repo" : [o for o in repo if o.number == int(param)], "message" : buffer}
    return {"repo" : repo, "message" : buffer}

@app.post("/orders")
def create_orders(dto : Annotated[Order, Form()]):
    repo.append(dto)

@app.post("/update")
def update_orders(dto : Annotated[UpdateOrderDTO, Form()]):
    for o in repo:
        if o.number == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
                message += f"Статус заявки №{o.number} изменён\n"
            if dto.description != "":
                o.description = dto.description
            if o.master != "":
                o.master = dto.master
            if dto.comment != None and dto.comment != "":
                o.comments.append(dto.comment)
            return o 
    return "Не найдено"    

def complete_count():
    return len([o for o in repo if o.status == "завершена"])