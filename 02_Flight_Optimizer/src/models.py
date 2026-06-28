"""
Data models used by the Flight Recommendation Engine.

These dataclasses define the core entities exchanged between the data loader,
scoring engine, and recommendation engine.

They contain no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time


@dataclass
class Flight:
    """A single bookable flight option within an itinerary."""

    itinerary_id: str
    airline: str
    flight_number: str

    origin: str
    """IATA airport code for departure."""

    destination: str
    """IATA airport code for arrival."""

    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int

    price: float
    """Flight price in USD."""

    fare_class: str
    is_nonstop: bool

    # Number of layovers in the itinerary segment.
    layovers: int = 0

    red_eye: bool = False
    """True when the flight departs late at night or arrives early morning."""


@dataclass
class Itinerary:
    """
    Complete travel option composed of one or more flights.

    The scoring engine evaluates itineraries rather than individual flights.
    """

    flights: list[Flight]
    total_price: float
    total_duration_minutes: int

    score: float = 0.0
    """Calculated by the scoring engine."""

    ranking_reason: str = ""
    """Explanation of why this itinerary received its ranking."""


@dataclass
class TripLeg:
    """Travel requirements for one segment of a multi-city trip."""

    origin: str
    destination: str

    acceptable_origins: list[str] = field(default_factory=list)
    """Alternate departure airports accepted for this leg."""

    acceptable_destinations: list[str] = field(default_factory=list)
    """Alternate arrival airports accepted for this leg."""

    depart_date: date | None = None
    latest_arrival: datetime | None = None
    earliest_departure: datetime | None = None
    arrive_by_end_of_day: bool = False
    avoid_red_eye: bool = False


@dataclass
class TripRequest:
    """Structured travel requirements extracted from a trip brief."""

    passenger_count: int
    home_airport: str
    legs: list[TripLeg] = field(default_factory=list)

    budget_max_usd: float | None = None
    prefer_nonstop: bool = True
    layover_min_minutes: int | None = None
    layover_max_minutes: int | None = None
    preferred_airlines: list[str] = field(default_factory=list)
    excluded_fare_classes: list[str] = field(default_factory=list)
    avoid_departures_before: time | None = None


@dataclass
class Recommendation:
    """Final output returned by the decision engine."""

    # Highest-ranked itinerary.
    best_itinerary: Itinerary

    # Second-best alternative.
    runner_up_itinerary: Itinerary

    recommendation_reason: str
    """One-sentence explanation of why the best option beat the runner-up."""

    tradeoffs: list[str] = field(default_factory=list)
    unsatisfied_constraints: list[str] = field(default_factory=list)
    total_price: float = 0.0
    total_duration_minutes: int = 0

    scoring_summary: str = ""
    """Human-readable summary of how competing factors were weighted."""