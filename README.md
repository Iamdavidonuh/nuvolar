# nuvolar
Nuvolar Python developer take home test

[![Nuvolar Tests](https://github.com/Iamdavidonuh/nuvolar/actions/workflows/test.yml/badge.svg)](https://github.com/Iamdavidonuh/nuvolar/actions/workflows/test.yml)

# Table of contents
1. [Installation](#Installation)
2. [Navigation](#Navigation)
3. [Endpoints](#Endpoints)
4. [Note](#Note)



## Installation

- Install virtualenv for creating virtual environments

        pip3 install virtualenv

- Set up virtual environment

        virtualenv -p python3.8 .virtualenv 

- Activate virutalenv

        source .virtualenv/bin/activate

- Install requirements

        pip3 install -r requirements.txt


- Run migrations before starting the server.

        python manage.py migrate

- Load Dummy Data.

        python manage.py loaddata fleet/fixtures/sample.json

- Start the server

        python manage.py runserver

- Run Tests

        python manage.py test


## Navigation:

You can navigate the application using:

- ### Django Rest APi root

    on your browser, go to ``127.0.0.1:8000``

- ### Using Swagger UI

    go to ``127.0.0.1:8000/swagger/``    


## Endpoints


- # Aircrafts

     - Create an aircraft

        ``` POST "http://localhost:8000/aircraft" ```
        
        ```
        {
            "serial_number": "123ABC89",
            "manufacturer": "Boeing"
        }
        ```
        
        ```
        response:
        
            {
                "id": 1,
                "serial_number": "123ABC89",
                "manufacturer": "Boeing"
            }
        ```

    - Get all aircrafts

        ``` GET "http://localhost:8000/aircraft" ```
        ```
        response:
        
        [
            {
                "id": 1,
                "serial_number": "123ABC89",
                "manufacturer": "Boeing"
            },
            {
                "id": 2,
                "serial_number": "404AE365",
                "manufacturer": "Fly Emirates"
            }
        ]
        ```
    - Get an Aircraft by ID

        ``` GET "http://localhost:8000/aircraft/1/" ```
        ```
        Response

            {
                    "id": 1,
                    "serial_number": "123ABC89",
                    "manufacturer": "Boeing"
            }
        ``` 
    - Update Aircraft

        ``` PUT "http://localhost:8000/aircraft/1/" ```
        ```
        example payload:

            {
                    "serial_number": "123909",
                    "manufacturer": "GX360"
            }

        ```
        ```
        Response

            {
                    "id": 1,
                    "serial_number": "123909",
                    "manufacturer": "GX360"
            }
        ``` 


    - DELETE an aircraft 

        ``` DELETE "http://localhost:8000/aircraft/1/"```
        ```
        Response
        

            {}
        ```

- # Airport

    ``127.0.0.1:8000/airport/``

    - Create an airport

        ``` POST "http://localhost:8000/airport" ```
        
        ```
        example payload:

        {
            "icao_code": "OMAA"
        }
        ```
        
        ```
        response:
        
            {
                "id": 1,
                "icao_code": "OMAA"
            }
        ```

    - Get all Airports

        ``` GET "http://localhost:8000/airport" ```
        ```
        response:
        
        [
            {
                "id": 1,
                "icao_code": "OMAA"
            },
            {
                "id": 2,
                "icao_code": "GCXO"
            },
            {
                "id": 3,
                "icao_code": "OMNK"
            }
        ]
        ```
    - Get an Airport by ID

        ``` GET "http://localhost:8000/airport/1/" ```
        ```
        Response

            {
                "id": 1,
                "icao_code": "OMAA"
            }
        ``` 
    - Update Airport

        ``` PUT "http://localhost:8000/airport/1/" ```
        ```
        example payload:
        
            {
                "icao_code": "GLXU"
            }

        ```
        ```
        Response

            {
                    "id": 1,
                    "icao_code": "GLXU"
            }
        ``` 


    - DELETE an airport 

        ``` DELETE "http://localhost:8000/airport/1/"```
        ```
        Response
        

            {}
        ```










- # Flight


    ``127.0.0.1:8000/flight/``

    - Create a flight

        ``` POST "http://localhost:8000/flight" ```
        
        ```Date format: "%Y-%m-%d %H:%M:%S"```

        ```
        example payload:

        {
            "departure_date": "2022-02-01 11:22:00",
            "arrival_date": "2022-02-02 04:22:00",
            "departure_airport": 1,
            "arrival_airport": 2,
            "aircraft": 1
        }
        ```
        
        ```
        response:
        
            {
                "departure_date": "2022-02-01 11:22:00",
                "arrival_date": "2022-02-02 04:22:00",
                "departure_airport": 1,
                "arrival_airport": 2,
                "aircraft": 1
            }
        ```

    - Get all flights

        ``` GET "http://localhost:8000/flight" ```
        ```
        response:
        
        [
            {
                "id": 1,
                "departure_date": "2022-01-30 15:30:00",
                "arrival_date": "2022-01-30 22:40:00",
                "departure_airport": 1,
                "arrival_airport": 2,
                "aircraft": 1
            },
            {
                "id": 2,
                "departure_date": "2022-02-01 11:22:00",
                "arrival_date": "2022-02-02 04:22:00",
                "departure_airport": 1,
                "arrival_airport": 2,
                "aircraft": 1
            }
        ]

        ```
    - Get a flight by ID

        ``` GET "http://localhost:8000/flight/1/" ```
        ```
        Response

            {
                "id": 1,
                "departure_date": "2022-01-30 15:30:00",
                "arrival_date": "2022-01-30 22:40:00",
                "departure_airport": 1,
                "arrival_airport": 2,
                "aircraft": 1
            }
        ``` 
    - Search Flight by departure and arrival airport

        ``` GET "http://localhost:8000/flight/?departure_airport=1&arrival_airport=2" ```
        ```
        Response

            {
                "id": 1,
                "departure_date": "2022-01-30 15:30:00",
                "arrival_date": "2022-01-30 22:40:00",
                "departure_airport": 1,
                "arrival_airport": 2,
                "aircraft": 1
            }
        ``` 
    - Search Flight by departure time range

        ``` GET "http://localhost:8000/flight/?start=09:30:00&end=13:30:00" ```

        ``` Time format: H:M:S```
        ```
        Response

            [
                {
                    "id": 2,
                    "departure_date": "2022-02-01 11:22:00",
                    "arrival_date": "2022-02-02 04:22:00",
                    "departure_airport": 1,
                    "arrival_airport": 2,
                    "aircraft": 1
                }
            ]
        ``` 
    - Update flight

        ``` PUT "http://localhost:8000/flight/2/" ```
        ```
        example payload:
        
            {
                "departure_date": "2022-02-01 11:22:00",
                "arrival_date": "2022-02-02 04:22:00",
                "departure_airport": 2,
                "arrival_airport": 3,
                "aircraft": 1
            }

        ```
        ```
        Response

            {
                "departure_date": "2022-02-01 11:22:00",
                "arrival_date": "2022-02-02 04:22:00",
                "departure_airport": 2,
                "arrival_airport": 3,
                "aircraft": 1
            }
        ``` 


    - DELETE a flight 

        ``` DELETE "http://localhost:8000/flight/1/"```
        ```
        Response
        

            {}
        ```

- # Reports

    ```127.0.0.1:8000/reports/```

    - Get Reports without any request parameters

        ``` GET "http://localhost:8000/reports" ```
        
        ```
            response:
            
            {
                "OMAA": {
                    "flights": 2,
                    "aircrafts": {
                        "123ABC89": {
                            "inflight_time": 430.0,
                            "average": 215.0
                        }
                    }
                }
            }

        ```
    - Get request with request params: departure_date and arrival_date
    
        ``` GET "http://localhost:8000/reports/?departure_date=2022-01-30 2015:30:00&arrival_date=2022-02-02 2004:22:00" ```

        ```
        response
            {
                "OMAA": {
                    "flights": 2,
                    "aircrafts": {
                        "123ABC89": {
                            "inflight_time": 430.0,
                            "average": 215.0
                        }
                    }
                }
            }
        ```


# Note

- ``Date format: "%Y-%m-%d %H:%M:%S"``

- ``Time Format: "%H:%M:%S"``