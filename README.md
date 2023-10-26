# ONCEO-test-task

##Створення користувача

```sh
python wsgi.py create_user --username your_username --password your_password
```

##Запуск в контейнерах
```sh
docker-compose up --build
```


##створення замовлення

```sh
/create_order
```
Привклад:
```sh
{
  "items": [
    {"id": "1", "count": 2},
  ],
  "addresses": [
    "123 First St, Cityville",
    "456 Market St, Cityville",
  ]
}
```

##отримання замовлення

```sh
/get_order/<string:order_uuid>
```

##адмін панель
```sh
/admin
```

##авторизація
```sh
/login
```

JSONRPC login
```sh
{
    "jsonrpc": "2.0",
    "method": "App.login",
    "params": {
        "username": "login",
        "password": "pass"
    },
    "id": 1
}
```