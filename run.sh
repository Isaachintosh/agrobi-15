#!/bin/bash
docker login

cd ./15.0

docker-compose up -d

docker ps