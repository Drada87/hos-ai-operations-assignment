from .models import (
    Itinerary,
    Recommendation,
    TripRequest,
)


def _has_red_eye(itinerary: Itinerary) -> bool:
    return any(flight.red_eye for flight in itinerary.flights)


def _uses_excluded_fare_class(
    itinerary: Itinerary,
    request: TripRequest,
) -> bool:
    if not request.excluded_fare_classes:
        return False

    excluded = set(request.excluded_fare_classes)
    return any(flight.fare_class in excluded for flight in itinerary.flights)


def _has_early_departure(
    itinerary: Itinerary,
    request: TripRequest,
) -> bool:
    if request.avoid_departures_before is None:
        return False

    cutoff = request.avoid_departures_before
    return any(
        flight.departure_time.time() < cutoff for flight in itinerary.flights
    )


def _layover_violations(
    itinerary: Itinerary,
    request: TripRequest,
) -> list[str]:
    violations: list[str] = []

    for flight in itinerary.flights:
        if flight.is_nonstop and flight.layovers == 0:
            continue

        if (
            request.layover_min_minutes is not None
            and flight.layover_minutes < request.layover_min_minutes
        ):
            violations.append("Includes a short layover")

        if (
            request.layover_max_minutes is not None
            and flight.layover_minutes > request.layover_max_minutes
        ):
            violations.append("Includes a long layover")

    return violations


def _uses_preferred_airline(
    itinerary: Itinerary,
    request: TripRequest,
) -> bool:
    if not request.preferred_airlines:
        return True

    preferred = set(request.preferred_airlines)
    return any(flight.airline in preferred for flight in itinerary.flights)


def _is_all_nonstop(itinerary: Itinerary) -> bool:
    return all(flight.layovers == 0 for flight in itinerary.flights)


def find_unsatisfied_constraints(
    itinerary: Itinerary,
    request: TripRequest,
) -> list[str]:
    """Identify which founder preferences were not satisfied."""
    violations: list[str] = []

    if request.budget_max_usd is not None:
        flexible_budget = request.budget_max_usd + 400
        if itinerary.total_price > flexible_budget:
            violations.append("Exceeds flexible budget")
        elif itinerary.total_price > request.budget_max_usd:
            violations.append("Exceeds stated budget")

    if request.prefer_nonstop and not _is_all_nonstop(itinerary):
        violations.append("Includes connecting flights")

    if not _uses_preferred_airline(itinerary, request):
        violations.append("Does not use a preferred airline")

    if _uses_excluded_fare_class(itinerary, request):
        violations.append("Uses Basic Economy")

    if _has_red_eye(itinerary):
        violations.append("Includes a red-eye flight")

    if _has_early_departure(itinerary, request):
        violations.append("Has an early departure")

    for layover_issue in _layover_violations(itinerary, request):
        if layover_issue not in violations:
            violations.append(layover_issue)

    return violations


def build_tradeoffs(
    best: Itinerary,
    runner_up: Itinerary,
) -> list[str]:
    """Explain the key differences between the top two itineraries."""
    tradeoffs: list[str] = []

    price_diff = best.total_price - runner_up.total_price
    duration_diff = best.total_duration_minutes - runner_up.total_duration_minutes
    best_red_eye = _has_red_eye(best)
    runner_up_red_eye = _has_red_eye(runner_up)
    best_nonstop = _is_all_nonstop(best)
    runner_up_nonstop = _is_all_nonstop(runner_up)

    if price_diff > 0 and not best_red_eye and runner_up_red_eye:
        tradeoffs.append("Costs more but avoids a red-eye.")
    elif price_diff < 0 and not best_nonstop and runner_up_nonstop:
        tradeoffs.append("Cheaper but includes a connection.")
    elif price_diff > 0:
        tradeoffs.append(
            f"Costs ${price_diff:.0f} more than the runner-up."
        )
    elif price_diff < 0:
        tradeoffs.append(
            f"Costs ${abs(price_diff):.0f} less than the runner-up."
        )

    if duration_diff < 0:
        tradeoffs.append("Saves travel time.")
    elif duration_diff > 0:
        tradeoffs.append(
            f"Adds {duration_diff} minutes of total travel time."
        )

    if not best_red_eye and runner_up_red_eye and "red-eye" not in " ".join(
        tradeoffs
    ).lower():
        tradeoffs.append("Avoids a red-eye flight included in the runner-up.")

    if not best_nonstop and runner_up_nonstop and "connection" not in " ".join(
        tradeoffs
    ).lower():
        tradeoffs.append("Includes a connection while the runner-up is nonstop.")

    if best_nonstop and not runner_up_nonstop:
        tradeoffs.append("Uses nonstop flights while the runner-up includes connections.")

    if (
        "Includes a preferred airline" in best.reasons
        and "Includes a preferred airline" not in runner_up.reasons
    ):
        tradeoffs.append("Uses the preferred airline.")

    if best.score > runner_up.score:
        tradeoffs.append(
            f"Higher overall score ({best.score:.0f} vs {runner_up.score:.0f})."
        )

    return tradeoffs


def build_recommendation_reason(
    best: Itinerary,
    runner_up: Itinerary,
) -> str:
    """Generate a one-sentence recommendation summary."""

    if best.itinerary_id == runner_up.itinerary_id:
        return (
            "Recommended because it is the highest-scoring available itinerary "
            "for this trip."
        )

    return (
    "Recommended because it offers the best overall balance of "
    "cost, travel time, and traveler preferences."
)


def _build_scoring_summary(itinerary: Itinerary) -> str:
    if not itinerary.reasons:
        return f"Final score: {itinerary.score:.0f}"

    return "\n".join(itinerary.reasons)


def recommend(
    request: TripRequest,
    itineraries: list[Itinerary],
) -> Recommendation:
    """Select the best itinerary and build the final recommendation."""
    if not itineraries:
        raise ValueError("At least one scored itinerary is required.")

    best = itineraries[0]
    runner_up = itineraries[1] if len(itineraries) > 1 else itineraries[0]

    tradeoffs = build_tradeoffs(best, runner_up)
    constraints = find_unsatisfied_constraints(best, request)
    reason = build_recommendation_reason(best, runner_up)

    return Recommendation(
        best_itinerary=best,
        runner_up_itinerary=runner_up,
        tradeoffs=tradeoffs,
        unsatisfied_constraints=constraints,
        recommendation_reason=reason,
        scoring_summary=_build_scoring_summary(best),
    )
