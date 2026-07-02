
from src.api import fetch_states
from src.metrics import calculate_metrics
from src.dashboard import render_dashboard


def main() -> None:
    """Run the Live Air Traffic Dashboard."""

    df = fetch_states()

    metrics = calculate_metrics(df)

    render_dashboard(df, metrics)


if __name__ == "__main__":
    main()