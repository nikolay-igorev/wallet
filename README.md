# Приложение работы с кошельками

Использовался Django Rest Framework.

* Получение баланса кошелька;
* Операция по изменению баланса кошелька (снятие и пополнение).

### Документация Swagger:

`http://127.0.0.1:8000/api/v1/swagger/`<br>

## Установка с помощью Docker

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://username:password@localhost:5432/db_name
DATABASE_URL_DOCKER=postgres://postgres:postgres@db:5432/postgres
```

Выполните команду:

```bash
docker-compose up -d --build
```

Запустите миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создайте суперюзера:

```bash
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000/`<br>

Чтобы посмотреть вывод логов:

```bash
 docker-compose logs -f 'web'
```

Чтобы запустить тесты:

```bash
docker-compose exec web python manage.py test
```

Чтобы остановить все контейнеры:

```bash
docker-compose down
```