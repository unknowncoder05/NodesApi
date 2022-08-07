DOCKER_COMPOSE_FILE = docker-compose.yml

up:
	docker-compose up

build:
	docker-compose build

down:
	docker-compose down

manualm:
	echo docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web python manage.py migrate

m:
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web python manage.py migrate

mm:# Make Migrations
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web python manage.py makemigrations $(app)

mnm:# Make and migrate
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web bash -c "python manage.py makemigrations $(app) && python manage.py migrate"

me:# Make empty migration
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web python manage.py makemigrations --empty $(app)

admin:
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm web  python manage.py createsuperuser

c:
	docker-compose config

ps:
	docker-compose ps
