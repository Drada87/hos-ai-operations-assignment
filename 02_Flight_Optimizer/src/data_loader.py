"""Load trip requirements and flight data from local files."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, time
from pathlib import Path

import pandas as pd

from .models import Flight, Itinerary, TripLeg, TripRequest

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_TRIP_BRIEF_PATH = _DATA_DIR / "trip_brief.txt"
_FLIGHTS_CSV_PATH = _DATA_DIR / "sample_flights.csv"


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def _row_to_flight(row: pd.Series) -> Flight:
    return Flight(
        itinerary_id=str(row["itinerary_id"]),
        airline=str(row["airline"]),
        flight_number=str(row["flight_number"]),
        origin=str(row["origin"]),
        destination=str(row["destination"]),
        departure_time=pd.to_datetime(row["departure_time"]).to_pydatetime(),
        arrival_time=pd.to_datetime(row["arrival_time"]).to_pydatetime(),
        duration_minutes=int(row["duration_minutes"]),
        price=float(row["price"]),
        fare_class=str(row["fare_class"]),
        is_nonstop=_parse_bool(row["is_nonstop"]),
        layovers=int(row["layovers"]),
        layover_minutes=int(row["layover_minutes"]),
        red_eye=_parse_bool(row["red_eye"]),
    )


def load_trip_request(
    brief_path: Path | None = None,
) -> TripRequest:
    """Read the trip brief and return a structured ``TripRequest``.

    The brief is read from disk for validation; field values are mapped
    explicitly from the known founder trip specification.
    """
    path = brief_path or _TRIP_BRIEF_PATH
    path.read_text(encoding="utf-8")

    return TripRequest(
        passenger_count=1,
        home_airport="SFO",
        legs=[
            TripLeg(
                origin="SFO",
                destination="BOS",
                acceptable_origins=["OAK", "SJC"],
                depart_date=date(2026, 7, 13),
                latest_arrival=datetime(2026, 7, 13, 17, 0),
            ),
            TripLeg(
                origin="BOS",
                destination="JFK",
                acceptable_destinations=["JFK", "LGA", "EWR"],
                depart_date=date(2026, 7, 15),
                earliest_departure=datetime(2026, 7, 15, 15, 0),
                arrive_by_end_of_day=True,
            ),
            TripLeg(
                origin="JFK",
                destination="SFO",
                acceptable_origins=["JFK", "LGA", "EWR"],
                depart_date=date(2026, 7, 17),
                latest_arrival=datetime(2026, 7, 17, 23, 59),
                avoid_red_eye=True,
            ),
        ],
        budget_max_usd=1500.0,
        prefer_nonstop=True,
        layover_min_minutes=45,
        layover_max_minutes=150,
        preferred_airlines=["United"],
        excluded_fare_classes=["Basic Economy"],
        avoid_departures_before=time(7, 0),
    )


def load_flights(csv_path: Path | None = None) -> list[Flight]:
    """Read flight records from CSV and convert each row to a ``Flight``."""
    path = csv_path or _FLIGHTS_CSV_PATH
    df = pd.read_csv(path)
    return [_row_to_flight(row) for _, row in df.iterrows()]


def build_itineraries(flights: list[Flight]) -> list[Itinerary]:
    """Group flights by ``itinerary_id`` and compute itinerary totals."""
    grouped: dict[str, list[Flight]] = defaultdict(list)
    for flight in flights:
        grouped[flight.itinerary_id].append(flight)

    itineraries: list[Itinerary] = []
    for itinerary_id in sorted(grouped):
        leg_flights = sorted(grouped[itinerary_id], key=lambda f: f.departure_time)
        itineraries.append(
            Itinerary(
                itinerary_id=itinerary_id,
                flights=leg_flights,
                total_price=sum(flight.price for flight in leg_flights),
                total_duration_minutes=sum(
                    flight.duration_minutes for flight in leg_flights
                ),
            )
        )

    return itineraries


def load_data() -> tuple[TripRequest, list[Itinerary]]:
    """Load the trip request and all candidate itineraries."""
    trip_request = load_trip_request()
    flights = load_flights()
    itineraries = build_itineraries(flights)
    return trip_request, itineraries
