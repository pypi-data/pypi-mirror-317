# Health Predictor

A Python package for health metric analysis and prediction.

## Installation

```bash
pip install healthpredictor
```

## Usage

```python
from healthpredictor import HealthAnalyzer

# Initialize analyzer
analyzer = HealthAnalyzer()

# Analyze health metrics
result = analyzer.analyze_metrics(
    condition="diabetes",
    metrics={
        "bloodGlucose": 120,
        "hba1c": 6.5,
        "bloodPressure": 130
    }
)

print(result)
```

## Features

- Health score calculation
- Risk level assessment
- Metric-specific analysis
- Confidence scoring
- Recommendation generation

## License

MIT License