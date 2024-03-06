# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Создайте маршрут для удаления информации о пользователе (метод DELETE).
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []

for i in range(1, 11):
    user = User(id=i, name=f"User {i}", email=f"user{i}@mail.ru", password=f"password{i}{i}{i}")
    users.append(user)


@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})



@app.post("/add")
async def add_user(request: Request,name: str = Form(), email: str = Form(), password: str = Form()):
    user = User(id=len(users) + 1, name=name, email=email, password=password)
    users.append(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put("/update/{user_id}")
async def update_user(user_id: int, user: User):
    for u in users:
        if u.id == user_id:
            u.name = user.name
            u.email = user.email
            u.password = user.password
            return u
    return {"message": "User not found"}


@app.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    for u in users:
        if u.id == user_id:
            users.remove(u)
            return u
    return {"message": "User not found"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
