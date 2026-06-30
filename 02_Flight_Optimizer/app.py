from src.data_loader import load_data
from src.scorer import score_itineraries
from src.recommender import recommend


def main():
    print("=== Flight Recommendation Engine ===\n")

    request, itineraries = load_data()

    scored = score_itineraries(itineraries, request)

    recommendation = recommend(request, scored)

    print(f"Best itinerary: {recommendation.best_itinerary.itinerary_id}")
    print(f"Runner-up: {recommendation.runner_up_itinerary.itinerary_id}")
    print(f"Score: {recommendation.best_itinerary.score}")
    print(
    f"Runner-up price: "
    f"${recommendation.runner_up_itinerary.total_price:.0f}"
    )
    print(f"Total price: ${recommendation.best_itinerary.total_price:.0f}")
    print(
        f"Total duration: "
        f"{recommendation.best_itinerary.total_duration_minutes} minutes"
    )

    print("\nRecommendation")
    print(recommendation.recommendation_reason)

    print("\nTradeoffs")
    for item in recommendation.tradeoffs:
        print(f"- {item}")

    print("\nUnsatisfied constraints")
    if recommendation.unsatisfied_constraints:
        for item in recommendation.unsatisfied_constraints:
            print(f"- {item}")
    else:
        print("None")

    print("\nScoring summary")
    print(recommendation.scoring_summary)


if __name__ == "__main__":
    main()