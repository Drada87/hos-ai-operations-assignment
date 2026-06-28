# # Current Task

## Objective

Create the file:

data/sample_flights.csv

---

## Context

This dataset will be used by the Flight Recommendation Engine.

The goal is to evaluate a recommendation algorithm, not to simulate every possible flight.

The CSV should contain realistic flight options for the founder's three-leg business trip.

Trip:

- San Francisco → Boston

- Boston → New York

- New York → San Francisco

---

## Required Columns

airline

flight_number

origin

destination

departure_time

arrival_time

duration_minutes

price

fare_class

is_nonstop

layovers

red_eye

---

## Requirements

Generate realistic flight options.

Include multiple alternatives for every leg.

Include:

- United

- Delta

- American

- JetBlue

Create meaningful trade-offs.

Examples:

- cheaper but longer flights

- expensive nonstop flights

- one or two red-eye options

- flights that violate preferences

- flights that satisfy every requirement

Use realistic prices and flight durations.

Return ONLY the CSV.