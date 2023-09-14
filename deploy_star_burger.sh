#!/bin/bash

set -e

if [ -f .env ]; then
    source .env
fi

if [ -z "$ROLLBAR_TOKEN" ]; then
    echo "Переменная окружения ROLLBAR_TOKEN не установлена."
    exit 1
fi


if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Установите его перед запуском скрипта."                
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "npm не установлен. Установите его перед запуском скрипта."
    exit 1
fi

working_directory=$(pwd)

echo "Переходим в каталог /opt/Star-burger/"
cd /opt/Star-burger/

echo "Забирает изменения - git pull"
git pull

echo "Устанавливаем зависимости"
venv/bin/pip install -r requirements.txt

echo "Устанавливаем node"
npm ci --dev

echo "Собираем js код"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo "Собираем статику"
venv/bin/python manage.py collectstatic --noinput

echo "Выполняем миграцию"
venv/bin/python manage.py migrate

echo "Перезапускаем systemd"
systemctl restart starburger.service
systemctl restart postgresql.service

echo "Предупреждаем Rollbar о деплое"
sha=$(git rev-parse HEAD)
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header "X-Rollbar-Access-Token: ${ROLLBAR_TOKEN}" \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{
  "environment": "production",
  "revision": "'${sha}'"
}'

echo "Проект успешно задеплоен!!!"