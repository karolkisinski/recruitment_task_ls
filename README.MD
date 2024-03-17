
# Recruitment task LS

This application was created as part of an application to the LS company

**Tech stack:**
 - Django
 - Django Rest Framework
 - PostgreSQL

**For testing:**
 - Pytest
 - Django.test

To run this application:

 - clone repository
 - make two files - .env and .db.env (from template)
 - from location when docker-compose file exists run:
 
  ```
  docker-compose up --build
  ```
  Application will be running on ```localhost:8000```



## API Reference

Documentation is available after starting the application and entering url:

  ```localhost:8000/docs```


#### To make any request application needs an Token in header.

For testing purposes admin account will be created automatically(from .env variables).

To obtain token make a POST request to:

```
localhost:8000/auth/token/

payload

{
  "username": "admin",
  "password": "admin"
}

```


Then copy Access Token value and put in headers like this:

``` Authorization: Bearer token_value```

#### Get refresh and access token

```http
  POST /auth/token/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Obtain new access token

```http
  POST /auth/token/refresh/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `refresh` | `string` | **Required**. Your refresh token |

#### Get systems list

```http
  GET /system/
```

#### Create new system
```http
  POST /system/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `system_name` | `string` | **Required**. System name |
| `description` | `string` | **Optional**. System description |

#### Get specific system info by id
```http
  POST /system/id/
```

#### Update specific system info by id
```http
  PATCH /system/id/

  example payload:
  {
    "system_name": "System Updated"
  }

```


#### Delete specific system info by id
```http
  DELETE /system/id/
```

#### Get measurements for specific system by id

```http
  GET /measurements/system_id/
```

#### Add new measurement for specific system by id

```http
  POST /measurements/system_id/add/

  example payload

  {
    "ph": 3.5,
    "water_temperature": 30.0,
    "tds": 3.5
  }
```

#### Get last 10 measurements for specific system by id

```http
  GET /measurements/system_id/last10/
```

## Running Tests

To run tests, enter container with the following command

```bash
  docker exec -it recruitment_api sh
```

And run
```bash
  pytest
```

