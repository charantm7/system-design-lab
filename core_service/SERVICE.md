## Phase 1 Observation

### Database Failure Scenarios

- When Postgres is down, and hit '/data' endpoint
- FastAPI returns the 500 Internal Server Error
- The Error saying that the database connection is closed
- This error appears suddenly when database is unavailable

> Error Type: 500 Internal Server Error
> Error Message: sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SSL connection has been closed unexpectedly
> Response Time: 19ms

### Implementation Observtion

- Expected Behaviour:

  - When all components are running, the API should accept the request and return the response
  - The '/health' endpoint should confirm that the service is Up or Down
  - The '/data' endpoint should process the request and interacts with the database

- Actual Behaviour:

  - If both APP and the postgres server is running the endpoints respond correctly
  - The '/data' endpoint return the data from the DB correctly
  - Everything works good under normal condition

- What break when database is down:

  - When Postgres is down, and hit '/data' endpoint
  - FastAPI returns the 500 Internal Server Error
  - The Error saying that the database connection is closed
  - This error appears suddenly when database is unavailable

- What break when service is down:

  - When client sends the request, there is no service running on that endpoint
  - so the request couldn't connect

- learned:
  - The database is the importance dependency for the '/data' endpoints
  - If database is not available, the service is not able to proces the request
  - This raw failures helps to understand where the resilience mechanism is needed later

## Phase 2 - Horizonatal scaling

### Implementation

- created Dockerfile and added the service like system-design, db and nginx.
- Build the docker file and the system-design image is created
- The composing the docker-compose.yml like docker compose up and with 3 instances
- The docker starts the 3 instance at a time
- Then added the nginx as the load balancer for the instances

### Workflow

- When the request is sent to server the nginx route the request to instances
- The request is routed to all the instances one by one using round robin.
- The request is accepted by all the instances one by one
- The response is delevered to the client

### Observation

> First observation

- now 100 request are sent to only single instance and it took
- Requests per second: 1337.42/sec
- Time per request: 7.477ms

> Second observation

- now 100 request are sent to all 3 instances and i took
- Requests per second: 2179.60/sec
- Time per request: 4.588ms

> Total observation

- Here we can observe that how the horizontal scalling reduce the overload on single instance
- And reduce the latency and increase the accepatance of the request
- The Request per second from 1337/s --> 2179/s its approx 1.6x times request rate is increased
- And latency is reduced from 7.477ms --> 4.588ms per request

## Added Caching

- implemented caching layers using redis
- it is the in memory caching that stores in the ram of the local system

### observation

- If the data is not stored in the cache, initially the data is queried from the DB
- once the data is returned from the DB at the same time the data is stored in the cache also
- In the next request the cache return the data if the were requested for the same data

### pros

- It reduces the load on the database
- it reduces the response latency
- It increase the performance of the application

---

## Timeout, Retries and backpressure

- implement all this features on the postgres and redis
- The timeout is applided to both postgres and redis
- But the retries is applied to only the redis
- And backpressure is allowed for only 100 concurrent request

### Observation

- Added timeout so when the query took more time to respose
- It will fall back to the exception
- And the retries are added for the redis for 2 times
- If the redis is down at the first time and it retries for the 2nd time to get the data
- For only 100 concurrent request are allowed to the service if more it backpressure the request

- If the redis is down the request is automatically fallback to the database
- and if the database is down and the data is in the cache it return the data from cache
- if the data is not cached and DB is down then the request return the 503 service unavailable
- That particular service is not been processed
