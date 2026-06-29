from .models import Itinerary, TripRequest

WEIGHTS = {
    ...
}
WEIGHTS = {
    # Budget
    "within_budget": 25,
    "budget_flexible": 5,
    "over_budget": -50,

    # Flight preferences
    "nonstop": 20,
    "connection": -15,
    "preferred_airline": 10,

    # Restrictions
    "basic_economy": -100,
    "red_eye": -40,
    "early_departure": -20,
    "invalid_layover": -50,
}

from .models import Itinerary, TripRequest

def score_budget(
    itinerary: Itinerary,
    request: TripRequest,
) -> tuple[int, str]:
    """Evaluate the itinerary against the founder's budget preferences."""
    if request.budget_max_usd is None:
        return (0, "")

    if itinerary.total_price <= request.budget_max_usd:
        return (WEIGHTS["within_budget"], "Total price is within budget")

    if itinerary.total_price <= request.budget_max_usd + 400:
        return (WEIGHTS["budget_flexible"], "Total price is within flexible budget")

    return (WEIGHTS["over_budget"], "Total price exceeds flexible budget")


def score_airline(
    itinerary: Itinerary,
    request: TripRequest,
) -> tuple[int, str]:
    """Evaluate the itinerary against the founder's airline preferences."""
    if not request.preferred_airlines:
        return (0, "")

    preferred = set(request.preferred_airlines)
    if any(flight.airline in preferred for flight in itinerary.flights):
        return (WEIGHTS["preferred_airline"], "Includes a preferred airline")

    return (0, "")


def score_nonstop(
    itinerary: Itinerary,
) -> tuple[int, str]:
    """Reward nonstop itineraries and penalize connections."""
    if all(flight.is_nonstop for flight in itinerary.flights):
        return (WEIGHTS["nonstop"], "All flights are nonstop")

    return (WEIGHTS["connection"], "Itinerary includes connecting flights")


def score_fare_class(
    itinerary: Itinerary,
    request: TripRequest,
) -> tuple[int, str]:
    """Evaluate fare class restrictions."""
    if not request.excluded_fare_classes:
        return (0, "")

    excluded = set(request.excluded_fare_classes)
    if any(flight.fare_class in excluded for flight in itinerary.flights):
        return (WEIGHTS["basic_economy"], "Includes an excluded fare class")

    return (0, "")


def score_red_eye(
    itinerary: Itinerary,
) -> tuple[int, str]:
    """Penalize red-eye flights."""
    if any(flight.red_eye for flight in itinerary.flights):
        return (WEIGHTS["red_eye"], "Includes a red-eye flight")

    return (0, "")


def score_departure_time(
    itinerary: Itinerary,
    request: TripRequest,
) -> tuple[int, str]:
    """Evaluate departure time preference."""
    if request.avoid_departures_before is None:
        return (0, "")

    cutoff = request.avoid_departures_before
    if any(
        flight.departure_time.time() < cutoff for flight in itinerary.flights
    ):
        return (WEIGHTS["early_departure"], "Includes an early-morning departure")

    return (0, "")


def score_layovers(
    itinerary: Itinerary,
    request: TripRequest,
) -> tuple[int, str]:
    """Validate layover duration constraints."""
    for flight in itinerary.flights:
        if flight.is_nonstop and flight.layovers == 0:
            continue

        if (
            request.layover_min_minutes is not None
            and flight.layover_minutes < request.layover_min_minutes
        ):
            return (WEIGHTS["invalid_layover"], "Layover duration is too short")

        if (
            request.layover_max_minutes is not None
            and flight.layover_minutes > request.layover_max_minutes
        ):
            return (WEIGHTS["invalid_layover"], "Layover duration is too long")

    return (0, "")


def score_itinerary(
    itinerary: Itinerary,
    request: TripRequest,
) -> Itinerary:
    """Calculate the final score for one itinerary."""
    components = [
        score_budget(itinerary, request),
        score_airline(itinerary, request),
        score_nonstop(itinerary),
        score_fare_class(itinerary, request),
        score_red_eye(itinerary),
        score_departure_time(itinerary, request),
        score_layovers(itinerary, request),
    ]

    itinerary.score = sum(points for points, _ in components)
    itinerary.reasons = [reason for _, reason in components if reason]
    return itinerary


def score_itineraries(
    itineraries: list[Itinerary],
    request: TripRequest,
) -> list[Itinerary]:
    """Score every itinerary in the candidate list."""
    scored = [score_itinerary(itinerary, request) for itinerary in itineraries]
    return sorted(scored, key=lambda itinerary: itinerary.score, reverse=True)