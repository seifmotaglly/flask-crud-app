# Flask CRUD Application

This project is a Flask-based CRUD application that utilizes JWT authentication and MongoDB for data storage. The application is containerized using Docker for ease of deployment and uses Redis for caching.

## Technologies Used

- **Flask**: Web framework for building the application.
- **MongoDB**: NoSQL database for data storage.
- **Redis**: In-memory data structure store, used for caching.
- **Docker**: Containerization platform for deploying the application.
- **JWT**: JSON Web Tokens for authentication.


## Setup

### Prerequisites

- Python 3.8+
- Docker (optional, for containerization)
- MongoDB
- Redis

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/seifmotaglly/flask-crud-app.git
    cd flask-crud-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    ```

5. Run the application:
    ```sh
    flask run
    ```

### Using Docker

1. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

### The application will be available at http://0.0.0.0:8080 or http://localhost:8080.

## Configuration

Configuration settings are managed in `config.py`. Adjust the settings as needed.

## Endpoints

### Authentication

- `POST /signup` - Register a new user

  *Request:*
  ```json
  {
    "name":"your name",
    "email": "your email;",
    "password": "your password"
  }
  ```
  *Response:*
  ```json
  {
    "msg": "User registered successfully"
  }
  ```
- `POST /login` - Log in and receive an access token and refresh token
  
  *Request:*
  ```json
  {
    "email": "your email",
    "password": "your password"
  }
  ```
  *Response:*
  ```json
  {
    "access_token": "your JWT",
    "refresh_token": "your refresh token"
  }
  ```
- `POST /refresh-token` - Refresh the refresh token

  *Request:*
  ```json
  {
   "refresh_token": "your refresh token"
  }
  ```
   *Response:*
  ```json
  {
    "access_token": "your JWT",
    "refresh_token": "your refresh token",
    "msg": "tokens refreshed"
  }
  ```


### Protected Routes

- `POST /organization` - Create a new organization (requires JWT)

  *Request:*
  ```json
  {
   "name": "organization name",
   "description": "organization description"
  }
  ```
  *Response:*
  ```json
  {
    "organization_id": "your organization id"
  }
  ```
- `GET /organization` - Retrieve all organizations (requires JWT)

  *Response:*
  ```json
  [
    {
      "_id": "organization id",
      "name": "organization name",
      "description": "organization description.",
      "organization_members": [
        {
          "access_level": "admin",
          "email": "email",
          "name": "name"
        }
      ]
    }, ...
  ]
  ```
- `GET /organization/<id>` - Retrieve a specific organization by ID (requires JWT)

  *Response:*
  ```json
  {
    "_id": "organization id",
    "name": "organization name",
    "description": "organization description.",
    "organization_members": [
      {
        "access_level": "admin",
        "email": "email",
        "name": "name"
      }
    ]
  }
  ```
- `POST /organization/<organization_id>/invite` - Invite a user (requires JWT)

  *Request:*
  ```json
  {
   "email": "email to invite"
  }
  ```
  *Response:*
  ```json
  {
    "msg": "User invited successfully"
  }
  ```
- `PUT /organization/<organization_id>` - Update a specific organization by ID (requires JWT)

  *Request:*
  ```json
  {
   "name": "updated organization name",
   "description": "updated organization description."
  }
  ```
  *Response:*
  ```json
  {
    "msg": "Organization updated successfully"
  }
  ```

- `DELETE /organization/<id>` - Delete a specific organization by ID (requires JWT)

  *Response:*
  ```json
  {
    "msg": "Organization deleted successfully"
  }
  ```
- `POST /revoke-refresh-token` - Revoke a refresh token (requires JWT)

  *Request:*
  ```json
  {
   "refresh_token": "your refresh token"
  }
  ```
  *Response:*
  ```json
  {
    "msg": "Refresh token successfully revoked"
  }
  ```


## Running Tests

To run the tests, use the following command:
```sh
pytest tests/tests.py
