#!/bin/bash
cd ..
docker build --no-cache -t cicd:jenad .
docker tag cicd:jenad registry:5000/jenad:$VERSION
docker push registry:5000/jenad:$VERSION
docker rmi cicd:jenad
