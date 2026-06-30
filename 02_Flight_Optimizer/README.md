# Flight Recommendation Engine

A Python-based flight recommendation tool that evaluates complete multi-city itineraries and recommends the best option based on business rules, traveler preferences, and weighted scoring.

This project was developed as part of the HOS AI Operations assignment.

---

## Overview

The application reads a structured trip request together with a set of candidate itineraries, evaluates each option against hard constraints and weighted preferences, ranks every itinerary, and returns the best recommendation.

The recommendation includes:

- Best itinerary
- Runner-up itinerary
- Tradeoffs between the top two options
- Unsatisfied constraints
- Scoring summary

The scoring logic is reusable for future trip requests without changing the recommendation engine.

---



## Project Structure

```

02_Flight_Optimizer/

├── [app.py](http://app.py)

├── test_[pipeline.py](http://pipeline.py)

├── [README.md](http://README.md)

│

├── data/

│   ├── trip_brief.txt

│   └── sample_flights.csv

│

└── src/

    ├── [models.py](http://models.py)

    ├── data_[loader.py](http://loader.py)

    ├── [scorer.py](http://scorer.py)

    └── [recommender.py](http://recommender.py)

```

---



## Architecture

The application follows a modular pipeline.

```

Trip Brief

      │

      ▼

Data Loader

      │

      ▼

Trip Request

      │

      ▼

Scoring Engine

      │

      ▼

Recommendation Engine

      │

      ▼

Final Recommendation

```



### Components



### [models.py](http://models.py)

Defines the application's data structures.

- Flight
- Itinerary
- TripRequest
- Recommendation

---



### data_[loader.py](http://loader.py)

Responsible for:

- Loading the trip brief
- Reading the sample flight dataset
- Building itinerary objects

---



### [scorer.py](http://scorer.py)

Evaluates every itinerary using weighted business rules.

Current scoring considers:

- Budget
- Flexible budget allowance
- Preferred airline
- Nonstop preference
- Fare class restrictions
- Red-eye penalties
- Early departure penalties
- Layover duration validation

Each itinerary receives:

- Final score
- Human-readable scoring reasons

---



### [recommender.py](http://recommender.py)

Ranks scored itineraries and generates:

- Best itinerary
- Runner-up
- Recommendation explanation
- Tradeoffs
- Unsatisfied constraints
- Scoring summary

---



## Scoring Logic

The recommendation engine combines multiple traveler preferences using weighted scoring.

| Rule | Weight |

|------|-------:|

| Within budget | +25 |

| Flexible budget | +5 |

| Preferred airline | +10 |

| Nonstop itinerary | +20 |

| Connection | -15 |

| Basic Economy | -100 |

| Red-eye | -40 |

| Early departure | -20 |

| Invalid layover | -50 |

Some assignment requirements were intentionally simplified.

For example, the "$400 flexible budget only if it avoids a red-eye or saves more than three hours" rule is currently implemented as a simplified flexible-budget bonus. The scoring engine was designed so additional business rules can be incorporated without changing the overall architecture.

---



## Running the Project

Install dependencies:

```bash

pip install pandas

```

Run the application:

```bash

python [app.py](http://app.py)

```

For a verbose execution showing all candidate itineraries:

```bash

python test_[pipeline.py](http://pipeline.py)

```

---



## Sample Output

```

=== Flight Recommendation Engine ===

Best itinerary: ITIN-001

Runner-up: ITIN-002

Score: 55

Recommendation:

Recommended because it offers the best overall balance of cost, travel time, and traveler preferences.

Tradeoffs

- Costs $100 more than the runner-up.

- Saves travel time.

- Uses the preferred airline.

Scoring summary

Final score: 55

Total price is within budget

Includes a preferred airline

All flights are nonstop

```

---



## Future Improvements

Possible enhancements include:

- Live flight search API integration
- Airline alliance support
- Dynamic scoring configuration
- Interactive web interface
- Unit and integration tests
- Support for additional traveler preferences

---



## Design Principles

This project emphasizes:

- Modular architecture
- Separation of responsibilities
- Readable and maintainable code
- Explainable recommendation logic
- Reusable scoring engine

