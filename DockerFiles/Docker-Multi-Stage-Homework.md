# Docker Multi-Stage Build Homework

**Name:** Dhruv Soni

**Enrollment Number:** `[24BCS10205]`

## Task 1: Multi-stage Dockerfile

The application is in `multi-stage-dockerfile/` and uses separate `builder` and `production` stages. It serves on port `8080`.

### Build

```bash
docker build -t hello-multi-stage ./multi-stage-dockerfile
```

![docker build — multi-stage](ss/image.png)

Both stages complete: `builder` installs all deps, `production` copies only the runtime files. Final line: `naming to docker.io/library/hello-multi-stage:latest`.

### Run and verify the application

```bash
docker run -d --name hello-multi-stage -p 8080:8080 hello-multi-stage
curl http://localhost:8080/
docker ps
```

![docker run, curl and docker ps](ss/image-1.png)

`curl` returns `<h1>Hello World from Docker multi-stage build</h1>` and `docker ps` shows the container Up with `0.0.0.0:8080->8080/tcp`.

### Browser verification

![Browser showing Hello World at localhost:8080](ss/image-3.png)

The page loads at `localhost:8080` and displays **Hello World**.

## Task 3: Docker application deployments

The repository contains these independently runnable Docker applications:

| Application | Folder | Build command | Run command | Port |
|---|---|---|---|---:|
| Node.js multi-stage | `multi-stage-dockerfile` | `docker build -t hello-multi-stage ./multi-stage-dockerfile` | `docker run -d -p 8080:8080 hello-multi-stage` | 8080 |
| Python | `python-app` | `docker build -t ms-python ./python-app` | `docker run -d -p 8082:8000 ms-python` | 8082 |
| Java | `java-app` | `docker build -t ms-java ./java-app` | `docker run -d -p 8081:8081 ms-java` | 8081 |

### Java app build and run

![Java app — docker build and curl](ss/image-4.png)

Build completes in 25 s. `curl http://localhost:8081` returns `Hello World from Docker Java app`.

### Python app build and run

![Python app — docker build, curl and docker ps](ss/image-5.png)

`curl http://localhost:8082` returns `Hello World from Docker Python app`. Final `docker ps` shows all three containers running simultaneously.

## Cleanup

```bash
docker rm -f hello-multi-stage ms-python ms-java
```
