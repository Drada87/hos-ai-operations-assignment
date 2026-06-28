# AI Context

## Project

Flight Recommendation Engine

This project is part of an AI Operations / Chief of Staff technical assessment.

The objective is NOT to build a flight search engine.

The objective is to build a reusable decision engine that recommends the best itinerary based on hard constraints and weighted preferences.

---

## Current Architecture

Trip Brief (TXT)

↓

Data Loader

↓

TripRequest

↓

Available Flights

↓

Scoring Engine

↓

Recommendation Engine

↓

Streamlit UI

---

## Project Structure

src/

    [models.py](http://models.py)

    data_[loader.py](http://loader.py)

    [scorer.py](http://scorer.py)

    [recommender.py](http://recommender.py)

data/

    trip_brief.txt

    sample_flights.csv

[app.py](http://app.py)

---

## Design Principles

- Keep business logic separated by module.

- Use Python dataclasses.

- Use type hints.

- Keep modules focused on a single responsibility.

- Prefer readability over clever code.

- Avoid unnecessary abstractions.

- Follow PEP 8.

---

## Module Responsibilities

[models.py](http://models.py)

Defines domain objects only.

No business logic.

---

data_[loader.py](http://loader.py)

Loads trip requests and flight datasets.

No scoring.

---

[scorer.py](http://scorer.py)

Evaluates itineraries.

No file access.

---

[recommender.py](http://recommender.py)

Ranks itineraries.

Builds explanations.

---

[app.py](http://app.py)

Presentation layer only.

No business logic.

---

## Important

This is a Minimum Viable Product.

Do not overengineer.

Do not introduce frameworks.

Do not redesign the architecture.