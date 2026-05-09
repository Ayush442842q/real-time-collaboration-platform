# README-backend.md
## Project Description
The Real-Time Collaboration Platform is a backend application that provides a set of API endpoints for managing teams, users, and real-time collaboration features. The platform uses a JWT Bearer token authentication scheme to secure its endpoints.

## Tech Stack Used
The following technologies are used in this project:
* Node.js as the runtime environment
* Express.js as the web framework
* MongoDB as the database
* JSON Web Tokens (JWT) for authentication

## Setup Instructions
To set up the project, follow these steps:
1. **Clone the repository**: Clone the repository using `git clone https://github.com/your-username/real-time-collaboration-platform.git`
2. **Install dependencies**: Install the dependencies using `npm install`
3. **Create a MongoDB database**: Create a new MongoDB database and add a `users` and `teams` collection
4. **Create a `.env` file**: Create a new file named `.env` in the root of the project and add the following environment variables:
	* `DB_URI`: The MongoDB database URI
	* `JWT_SECRET`: The secret key for signing JWT tokens
	* `PORT`: The port number to run the application on

## Environment Variables Needed
The following environment variables are required:
* `DB_URI`: The MongoDB database URI (e.g. `mongodb://localhost:27017/real-time-collaboration-platform`)
* `JWT_SECRET`: The secret key for signing JWT tokens (e.g. `your-secret-key`)
* `PORT`: The port number to run the application on (e.g. `3000`)

## API Endpoints Overview
The following API endpoints are available:
* `POST /api/v1/users`: Create a new user
* `GET /api/v1/users`: Get a list of all users
* `POST /api/v1/teams`: Create a new team

## How to Run Locally
To run the application locally, follow these steps:
1. **Start the MongoDB database**: Start the MongoDB database using `mongod`
2. **Start the application**: Start the application using `npm start`
3. **Access the API**: Access the API using `http://localhost:3000/api/v1`

## How to Run Tests
To run the tests, follow these steps:
1. **Install the testing dependencies**: Install the testing dependencies using `npm install --only=dev`
2. **Run the tests**: Run the tests using `npm test`
Note: The tests are written using Jest and are located in the `tests` directory.

## API Contract
The API contract is documented in the [API Contract](#real-time-collaboration-platform-api-contract) section.

### Real-Time Collaboration Platform API Contract
#### Introduction
The Real-Time Collaboration Platform API provides a set of endpoints for managing teams, users, and real-time collaboration features. This API contract outlines the endpoints, request and response formats, and error handling mechanisms for the platform.

#### Base URL and Versioning Strategy
The base URL for the API is `https://api.collaboration-platform.com/v1`. The API uses a versioning strategy based on the URL path, where `v1` represents the first version of the API.

#### Authentication Scheme
The API uses a JWT Bearer token authentication scheme. Clients must include a valid JWT token in the `Authorization` header of each request.

#### Global Error Format
The API returns errors in the following format:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string"
  }
}
```
#### Rate Limiting Policy
The API has a rate limiting policy of 100 requests per minute per client. Exceeding this limit will result in a `429 Too Many Requests` error.

#### Endpoints

##### 1. POST /api/v1/users
###### Description
Create a new user.
###### Authentication
Required: JWT Bearer token
###### Request Body
```json
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```
###### Success Response
```json
{
  "id": "integer",
  "username": "string",
  "email": "string"
}
```
###### Error Responses
* `400 Bad Request`: Invalid request body
* `409 Conflict`: Username already exists
###### Example Request/Response
```bash
POST /api/v1/users HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "username": "john",
  "password": "password",
  "email": "john@example.com"
}

HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "username": "john",
  "email": "john@example.com"
}
```

##### 2. GET /api/v1/users
###### Description
Get a list of all users.
###### Authentication
Required: JWT Bearer token
###### Request Body
None
###### Success Response
```json
[
  {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
]
```
###### Error Responses
* `401 Unauthorized`: Invalid JWT token
###### Example Request/Response
```bash
GET /api/v1/users HTTP/1.1
Authorization: Bearer <token>

HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  {
    "id": 2,
    "username": "jane",
    "email": "jane@example.com"
  }
]
```

##### 3. POST /api/v1/teams
###### Description
Create a new team.
###### Authentication
Required: JWT Bearer token
###### Request Body
```json
{
  "name": "string",
  "description": "string"
}
```
###### Success Response
```json
{
  "id": "integer",
  "name": "string",
  "description": "string"
}
```
###### Error Responses
* `400 Bad Request`: Invalid request body
* `409 Conflict`: Team name already exists
###### Example Request/Response
```bash
POST /api/v1/teams HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Team 1",
  "description": "This is team 1"
}

HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "name": "Team 1",
  "description": "This is team 1"
}
```