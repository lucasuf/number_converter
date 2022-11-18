# Number to English Words
This is a Django application that **exposes two endpoints for converting a given number to words in english**.
## Demo
The application is deployed under the following link on heroku for public access:
```
https://number-converter.herokuapp.com/docs/
```
## Installation & Run
```bash
# Download the project
git clone https://github.com/lucasuf/trellis_converter.git
```
For running the API, you can use the `docker-compose.yml` file or run it locally.
### Docker
```bash
# Build and Run
make dev-up
# API Endpoint : http://localhost:8000
```

## Structure
```
├── converter_app
│   ├── migrations
│   ├── tests          // Our API tests
│   │   ├── test_views.py    // Tests for the endpoints
│   ├── apps.py          
│   ├── converters.py   // Converter classes used to read a number
│   ├── urls.py     
│   └── views.py        // Class based view contanint the endpoint used on the application
├── trellis_converter
├── Dockerfile
├── Makefile                  // File containing instructions for running the application
└── docker-compose.yml
```

## Documentation
The full swagger documentation can be found under:
```bash
http://localhost:8000/docs
```
## REST API
___
### GET (Example)

`GET /number_to_english?number=12`

    curl -X 'GET' 'http://localhost:8000/number_to_english?number=12' -H 'accept: application/json'

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Content-Type: application/json
    	
    Response body:
    {
      "status": "ok",
      "number_in_english": "twelve"
    }
____

### POST (Example)

`POST /number_to_english`
```
curl -X 'POST' \
  'http://127.0.0.1:8050/number_to_english' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "number": 10000000000
}'
```
### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Content-Type: application/json

    Response body:
    {
      "status": "ok",
      "number_in_english": "ten billion"
    }



## Requirements

- [x] Support endpoints requirements for converting numbers.
- [x] Implement conversion class.
- [x] Add limit of 12 characters.
- [x] Add Dockerfile, docker-compose.yml and Makefile
- [x] Write tests for the view class.
- [x] Add API throttling (has we do not have auth, use API throttling to prevent production issues).
- [x] Add /docs with Swagger.
- [x] Deploy application to heroku.