from fleet.models import Flight


def update_departure_data(inflight_time, flight: Flight, data: dict):
    """[summary]

    Args:
        inflight_time ([float]): [time in minutes for a flight in air]
        flight (Flight): [Flight model object]
        data (dict): [dictionary of aircraft data ]

    Returns:
        [dict]: [aircraft data]
    """
    aircraft = flight.aircraft
    if not aircraft.serial_number in data["aircrafts"].keys():
        data["aircrafts"][aircraft.serial_number] = {
            "inflight_time": inflight_time,
            "average": inflight_time,
        }
        return data
    data["aircrafts"][aircraft.serial_number]["inflight_time"] += inflight_time
    return data


def compute_average(flight: Flight, data: dict):
    """[summary]

    Args:
        flight (Flight): [Flight model object]
        data (dict): [dictionary of aircraft data]
    """

    number_of_flights = data[flight.departure_airport.icao_code]["flights"]
    intime_flights = data[flight.departure_airport.icao_code]["aircrafts"][
        flight.aircraft.serial_number
    ]["inflight_time"]

    data[flight.departure_airport.icao_code]["aircrafts"][
        flight.aircraft.serial_number
    ]["average"] = (intime_flights / number_of_flights)
    return data
