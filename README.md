## Setup

To run the project you need `Docker` and `Docker Compose` on your machine.

Open your terminal and type in required commands:

```
$ git clone git@github.com:lolekgk/sample-project-api.git
$ cd sample-project-api
```

Fill in provided `.env.sample` file with the required values and save as `.env`.

```
$ docker-compose build
$ docker-compose up
$ docker exec -it sample_project bash
```

Visit [localhost:8000/redoc/](http://localhost:8000/redoc/) in the browser to see all available endpoints and their details.
