#!/bin/bash

set -eo pipefail

cd /opt/star-burger/

git pull

docker build -t star_burger .

docker-compose up -d

source .env

COMMIT_HASH=$(git rev-parse HEAD)

curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "'"$COMMIT_HASH"'"}'
