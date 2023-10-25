# ONCEO-test-task

Створення користувача

```sh
python wsgi.py create_user --username your_username --password your_password
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

##адмін панель
```sh
/admin
```

##авторизація
```sh
/login
```