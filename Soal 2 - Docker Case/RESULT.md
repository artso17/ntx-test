# Result of Soal 2-Docker Case

In this case, I realize that the services api container and etl container are running independently. As the result, at the first running, the etl service cannot connect the api service because the api service did not finished its starting process. Also I found that there are scripts in Dockerfile which not best practice.

## Steps to Solve The Problem
- Run default `docker-compose.yml` to know how the services act and errors compared to the expected `output.jpg` image.
- Changed CMD command to ENTRYPOINT command in files `api/Dockerfile` and `etl/Dockerfile` since the command should not be overriden and also for meet the best practice
- Added `healthcheck` declaration in api container as the trigger for other services 
- Added `depends_on` declaration in etl container that depends on api container with `condition: service_healthy` to start the service
- Added networks in each containers explicitely and instantiated the network with name `api_etl`
- Restart the containers by running command `docker compose up --build`
- Captured the success logs

