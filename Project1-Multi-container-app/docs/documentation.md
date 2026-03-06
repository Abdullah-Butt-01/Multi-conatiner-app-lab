# Project: Multi-Container App

## Objective

* Create a multi-container app using flask and redis

## Commands Practiced

* docker compose up - Start containers
	- -d - detached mode
* docker compose up --build - Build images first, then start containers
* docker compose down - Stop and remove containters


## What I did

* Created a flask app
* Created Dockerfile, requirement.txt and docker-compose_file
* Ran conatiners using docker compose
* Containers ran automatically
* Tested from host browser
* Updated docker compose file for persistent redis data (in database)
* Tested from browser
* Stopped containers
* Started again and tested from browser
* The counter continued from previous state

## Problems Faced

* Continuous error when using docker compose even after resetting docker
* Docker not working (disabled)
* Docker compose denied access of using image

## How I solved

* Used isolated environment:
	- curl -fsSL https://get.docker.com -o get-docker.sh
	- sudo sh get-docker.sh
* Started and enabled docker
* Updated docker compose file to use Dockerfile for image
