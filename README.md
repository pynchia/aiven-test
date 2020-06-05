# Test for Aiven

Build a complete project to distribute website monitoring data to consumers via Aiven Kafka and store to Aiven PostgreSQL.

Producer -> broker -> Consumer -> DB

## Execution

1. Unzip the `certs.zip` archive and place the "certs" folder in the main directory (aiven-test).

2. In the main directory, build the docker image with
 `docker build --no-cache -t aiven:v1 .`

3. Finally, run docker-compose to execute the whole system (producer and consumer) with
 `KAFKA='the-kafka-uri' PG='the-postreSQL-uri' docker-compose up`
