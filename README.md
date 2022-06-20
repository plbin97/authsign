# Authsign

![](https://github.com/plbin97/authsign/actions/workflows/test.yml/badge.svg)
![](https://github.com/plbin97/authsign/actions/workflows/staging.yml/badge.svg)


This repository is a flask blueprint for user management required by Keith Williams for his IS 218 and IS 690 classes.

Keith Williams is a good professor; If you can understand everything in this repository, you will get an "A."

### API documentation

API documentation are managed by swagger
[Click me](https://plbin97.github.io/authsign/)

### Stage server

[https://authsign.teenet.me/authsign](https://authsign.teenet.me/authsign)

### Run the this app by Docker

Run docker from Docker hub
```shell
docker pull plbin97/authsign:master && docker run -d plbin97/authsign
```

Or, you can build docker by yourself
```shell
docker build -t authsign . && docker run -d authsign
```

