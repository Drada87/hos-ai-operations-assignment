"""Data models for the flight recommendation engine.

These dataclasses define the structured objects passed between the parser,
candidate generator, constraint validator, scoring engine, and ranking stages.
They contain no business logic—only typed fields and documentation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time


@dataclass
class Layover:
    """A scheduled connection stop on a multi-segment flight option."""

    airport: str
    """IATA airport code where the traveler changes planes."""

    duration_minutes: int
    """Scheduled ground time between arrival and the next departure."""


@dataclass
class Flight:
    """A single bookable flight option within an itinerary."""

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
    """Segment fare in USD."""

    fare_class: str
    is_nonstop: bool
    layovers: list[Layover] = field(default_factory=list)
    """Connection stops; empty when ``is_nonstop`` is True."""

    red_eye: bool = False
    """True when the flight departs late at night or arrives early morning."""


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
    acceptable_home_airports: list[str] = field(default_factory=list)
    legs: list[TripLeg] = field(default_factory=list)

    budget_max_usd: float | None = None
    budget_flexibility_usd: float | None = None
    prefer_nonstop: bool = True
    min_connection_savings_usd: float | None = None
    layover_min_minutes: int | None = None
    layover_max_minutes: int | None = None
    preferred_airlines: list[str] = field(default_factory=list)
    excluded_fare_classes: list[str] = field(default_factory=list)
    carry_on_only: bool = False
    preferred_seat: str | None = None
    avoid_departures_before: time | None = None


@dataclass
class Recommendation:
    """Final output returned by the decision engine."""

    best_itinerary: list[Flight]
    runner_up_itinerary: list[Flight]
    recommendation_reason: str
    """One-sentence explanation of why the best option beat the runner-up."""

    tradeoffs: list[str] = field(default_factory=list)
    unsatisfied_constraints: list[str] = field(default_factory=list)
    total_price: float = 0.0
    total_duration_minutes: int = 0
    scoring_summary: str = ""
    """Human-readable summary of how competing factors were weighted."""
