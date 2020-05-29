# Test for Aiven

Build a complete project to distribute website monitoring data to consumers via Aiven Kafka and store to Aiven PostgreSQL.

Producer -> broker -> Consumer -> DB

## Execution

Launch both the producer and the consumer with the shell command:

 `KAFKA='the-kafka-uri' PG='the-postreSQL-uri' docker-compose up`
