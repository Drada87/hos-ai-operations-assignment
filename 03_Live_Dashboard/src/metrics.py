import pandas as pd

EMPTY_TOP_COUNTRIES = pd.DataFrame(
    columns=["origin_country", "aircraft_count"]
)

EMPTY_GROUND_DISTRIBUTION = pd.DataFrame(
    columns=["status", "count"]
)

EMPTY_SERIES = pd.Series(dtype=float)


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate dashboard KPIs and chart-ready datasets.

    Parameters
    ----------
    df : pd.DataFrame
        Clean aircraft state data.

    Returns
    -------
    dict
        Dictionary containing dashboard KPIs and chart-ready data.
    """

    if df.empty:
        return {
            "kpis": {
                "total_aircraft": 0,
                "airborne_aircraft": 0,
                "ground_aircraft": 0,
                "countries_represented": 0,
                "highest_speed": 0.0,
                "highest_altitude": 0.0,
            },
            "charts": {
                "top_countries": EMPTY_TOP_COUNTRIES,
                "ground_distribution": EMPTY_GROUND_DISTRIBUTION,
                "altitude_distribution": EMPTY_SERIES,
                "speed_distribution": EMPTY_SERIES,
            },
        }

    total_aircraft = len(df)

    airborne_aircraft = int(df["on_ground"].eq(False).sum())
    ground_aircraft = int(df["on_ground"].eq(True).sum())

  # Remove unrealistic speed values (>350 m/s ≈ 1260 km/h)
    valid_speeds = df.loc[
        df["velocity"].between(0, 350),
        "velocity",
    ]

    highest_speed_value = valid_speeds.max()
    highest_altitude_value = df["geo_altitude"].max()

    top_countries = (
        df["origin_country"]
        .value_counts(dropna=True)
        .head(10)
        .reset_index()
    )
    top_countries.columns = [
        "origin_country",
        "aircraft_count",
    ]

    ground_distribution = pd.DataFrame(
        {
            "status": ["Airborne", "On Ground"],
            "count": [airborne_aircraft, ground_aircraft],
        }
    )

    return {
        "kpis": {
            "total_aircraft": total_aircraft,
            "airborne_aircraft": airborne_aircraft,
            "ground_aircraft": ground_aircraft,
            "countries_represented": int(
                df["origin_country"].nunique(dropna=True)
            ),
            "highest_speed": (
                float(highest_speed_value)
                if pd.notna(highest_speed_value)
                else 0.0
            ),
            "highest_altitude": (
                float(highest_altitude_value)
                if pd.notna(highest_altitude_value)
                else 0.0
            ),
        },
        "charts": {
            "top_countries": top_countries,
            "ground_distribution": ground_distribution,
            "altitude_distribution": (
                df["geo_altitude"]
                .dropna()
                .reset_index(drop=True)
            ),
        "speed_distribution": (
                valid_speeds
                .dropna()
                .reset_index(drop=True)
            ),
        },
    }