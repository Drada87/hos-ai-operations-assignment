from src.data_loader import load_data
from src.scorer import score_itineraries
from src.recommender import recommend


def main():
    print("Loading data...")

    trip_request, itineraries = load_data()

    print(f"Loaded {len(itineraries)} itineraries")

    scored = score_itineraries(
        itineraries,
        trip_request,
    )

    print("\n==============================")
    print("ITINERARY RANKING")
    print("==============================")

    for itinerary in scored:

        print(f"\n{itinerary.itinerary_id}")
        print("-" * 40)

        print(f"Score: {itinerary.score}")
        print(f"Price: ${itinerary.total_price}")
        print(f"Duration: {itinerary.total_duration_minutes} minutes")

        print("\nReasons:")

        if itinerary.reasons:
            for reason in itinerary.reasons:
                print(f"  • {reason}")
        else:
            print("  • None")

        print("\nFlights:")

        for flight in itinerary.flights:
            print(
                f"  {flight.origin} -> {flight.destination}"
            )
            print(
                f"    Airline: {flight.airline}"
            )
            print(
                f"    Price: ${flight.price}"
            )
            print(
                f"    Fare: {flight.fare_class}"
            )
            print(
                f"    Nonstop: {flight.is_nonstop}"
            )
            print(
                f"    Layovers: {flight.layovers}"
            )
            print(
                f"    Red-eye: {flight.red_eye}"
            )

    recommendation = recommend(
        trip_request,
        scored,
    )

    print("\n==============================")
    print("FINAL RECOMMENDATION")
    print("==============================")

    print(f"Best itinerary: {recommendation.best_itinerary.itinerary_id}")
    print(f"Score: {recommendation.best_itinerary.score}")

    print("\nRecommendation reason:")
    print(recommendation.recommendation_reason)

    print("\nTradeoffs:")

    if recommendation.tradeoffs:
        for item in recommendation.tradeoffs:
            print(f"  • {item}")
    else:
        print("  • None")

    print("\nUnsatisfied constraints:")

    if recommendation.unsatisfied_constraints:
        for item in recommendation.unsatisfied_constraints:
            print(f"  • {item}")
    else:
        print("  • None")

    print("\nScoring summary:")
    print(recommendation.scoring_summary)


if __name__ == "__main__":
    main()