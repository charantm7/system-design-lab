# system-design-lab

## Phase 1 - System Working

### Request Flow

- The Client sends the HTTP request to the API Gateway
- The API Gateway receives the request and validate client authenticates
- The API Gateway forward the request to the core services
- The services recieves the request and perform the operationa and execute the bussines logics
- The Core services returns the response to the API Gateway
- Finally the API Gateway returns the response to the client

### API Communication Boundaries

- Client can only communicate with the API Gateway
- API Gateway sends and receives request and response from core services
- Services communicate with the Database to execute the commands
- Databases does not expose themself to the API Gateways or the client

### What breaks if core service is down?

- API Gateway receives the request from the client.
- Gateway try to forward the request to the services
- Due to services are unavilable, the request is failed
- The API Gateway returns error status 50X status code that might be a bad request or service unavailable

### What breaks if database stops?

- The API gateway forwards the reques to the service
- The service try to access the database
- Due to database is unavailable, the service fails to execute the command
- The service returns the bad request Error to the API Gateway
- The API Gateway forward the error status to the client

### Bottleneck Identification

- core service is single point of failure there is no backup.
- Database is the single shared dependency
- Any increase in the traffic leads to the increase load on the core services

### Non Goals

- No Horizontal scaling
- No caching
- No asychronous processing
- No fault tolerance

---

## Phase 2 - Horizontal scale

![alt text](scaling.png)

### How Horizontal scaling works

- Due to increase in traffics single instance can't handle all request
- Now increase the number of instance
- So the load on the single instance is reduced and distributed on other instance
- By increasing the number of same services which can handle request easly

### Architecture of Horizontal scaling

- Client sends the HTTP request to API gateway
- The API gateway also acts as a loadbalancer
- This gateway redirects the request to all instance equally
- The core service process the request and return the response to the gateway
- The gateway sends the response to the client

### Failure scenarios: One Instance is down

- API gateway still starts to receive the request
- The down Instance is skipped
- The other instance starts to serve the request
- Client may experince the little downtime or the no DTM

### Bottleneck scenarios

- Still the API gateway is the single point of failure
- client may experience some latency due to laod balance
- Database remains shared dependency
