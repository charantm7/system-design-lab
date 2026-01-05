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
