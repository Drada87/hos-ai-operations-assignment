import pandas as pd
import requests

API_URL = "https://opensky-network.org/api/states/all"

STATE_COLUMNS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]

NUMERIC_COLUMNS = [
    "longitude",
    "latitude",
    "baro_altitude",
    "geo_altitude",
    "velocity",
    "vertical_rate",
    "true_track",
]


def fetch_states() -> pd.DataFrame:
    """
    Fetch the latest aircraft state vectors from the OpenSky API.

    Returns
    -------
    pd.DataFrame
        Clean DataFrame containing the latest aircraft states.

    Raises
    ------
    RuntimeError
        If the API request fails or the response is invalid.
    """

    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()

    except requests.RequestException:
        return pd.DataFrame(columns=STATE_COLUMNS)

    payload = response.json()
    states = payload.get("states")

    if not states:
        return pd.DataFrame(columns=STATE_COLUMNS)

    df = pd.DataFrame(states, columns=STATE_COLUMNS)

    # -----------------------
    # Basic cleanup
    # -----------------------

    df["callsign"] = (
        df["callsign"]
        .fillna("")
        .str.strip()
    )

    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    # Show the most recently updated aircraft first
    df = df.sort_values(
        by="last_contact",
        ascending=False,
    )

    return df