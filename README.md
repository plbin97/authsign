# Authsign

[![](https://github.com/plbin97/authsign/actions/workflows/test.yml/badge.svg)](https://github.com/plbin97/authsign/actions/workflows/test.yml)
[![](https://github.com/plbin97/authsign/actions/workflows/deploy.yml/badge.svg)](https://github.com/plbin97/authsign/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/plbin97/authsign/branch/master/graph/badge.svg?token=EBTANVG4WE)](https://codecov.io/gh/plbin97/authsign)


This repository is a flask blueprint for user management required by Keith Williams for his IS 218 and IS 690 classes.

BTW, Keith Williams is a good professor; If you can understand everything in this repository, you will get an "A."

### API documentation

API documentation are managed by swagger
[Click me](https://plbin97.github.io/authsign/)

### Stage server

[https://authsign.teenet.me/authsign](https://authsign.teenet.me/authsign)

### Deploy by Docker

from Docker hub
```shell
docker pull plbin97/authsign:master && docker run -d plbin97/authsign
```

Or, you can build docker by yourself
```shell
docker build -t authsign . && docker run -d authsign
```

### Run this app locally

Prerequisite: ```python 3.8+```

Install dependency

```shell
pip3 install -r requirements.txt
```

Do database migration

```shell
flask db upgrade
```

Run the app

```shell
python3 app.py
```