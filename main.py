from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

login_realy = "Ustym"
password_realy = "password"

def read(url):
    with open(url, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data    

def write(f, objct):
    with open(f, 'w', encoding='utf-8') as file:
        json.dump(objct, file, ensure_ascii=False, indent=4)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://alilujko.github.io'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class Register(BaseModel):
    login: str
    password: str

class Change_data(BaseModel):
    old_name: str
    new_name: str
    new_image: str
    new_price: int

@app.get('/')
def main():
    return {"message":"Вітаю вас на потужному сервер"}

@app.get('/get_menu')
def get_menu():
    menu = read('database.json')
    return menu

@app.post('/register')
def reg(data: Register):
    if data.login == login_realy and data.password == password_realy:
        return {"message":"true"}
    else:
        return {"message":"false"}

@app.post('/change_data')
def change_data(data: Change_data):
    menu = read('database.json')

    key = data.old_name
    if key not in menu:
        key = next((k for k, item in menu.items() if item.get("name") == data.old_name), None)
        if key is None:
            return {"message": "товар не знайдено"}

    item = menu.pop(key)
    item["name"] = data.new_name
    item["image"] = data.new_image
    item["price"] = data.new_price
    menu[data.new_name] = item

    write("database.json", menu)

    return {"message":"добре пройшло"}

if __name__ == '__main__':
    uvicorn.run(app)