# Flight Recommendation Engine Design

## Objective

This project implements a reusable recommendation engine that evaluates complete flight itineraries based on hard constraints and weighted traveler preferences.

The goal is not to build a flight search engine, but to provide a modular decision engine that can be reused with different trip requests.

---

## Architecture

Trip Brief (TXT)
↓
Data Loader
↓
Trip Request
↓
Scoring Engine
↓
Recommendation Engine

### Data Loader

Loads the trip brief and flight dataset from local files.

### Trip Request

Represents the traveler requirements as structured domain objects.

### Scoring Engine

Applies business rules and weighted preferences to evaluate every itinerary.

### Recommendation Engine

Ranks candidate itineraries and generates:

- Best itinerary
- Runner-up
- Tradeoffs
- Unsatisfied constraints

---



## Design Principles

- Single Responsibility Principle
- Modular architecture
- Python dataclasses
- Type hints where appropriate
- Separation of concerns
- Readability over clever code
- Avoid unnecessary abstractions
- PEP 8 compliance

---



## Module Responsibilities



### [models.py](http://models.py)

Defines domain models.

### data_loader.py

Loads input data.

### [scorer.py](http://scorer.py)

Evaluates itineraries.

### [recommender.py](http://recommender.py)

Generates ranked recommendations.

### [app.py](http://app.py)

Presentation layer only.