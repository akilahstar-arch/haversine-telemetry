# Haversine Telemetry

A small, dependency-free Python utility for calculating GPS track distance and per-segment telemetry using the Haversine formula.

## Usage

Requires Python 3. Run the example with:

```bash
python telemetry.py
```

Import the functions in your own code:

```python
from telemetry import calculate_haversine_distance, compute_telemetry_metrics

track_data = [
    (23.3441, 85.3096, 0),
    (23.3451, 85.3106, 12),
    (23.3465, 85.3120, 25),
]

total_distance_km, segments = compute_telemetry_metrics(track_data)
print(f"Total distance: {total_distance_km:.3f} km")
```

Coordinates are `(latitude, longitude, timestamp_seconds)` tuples. The returned total distance is in kilometers. Each segment includes distance in kilometers, speed in kilometers per hour, and pace in minutes per kilometer. Segments with zero or negative elapsed time are excluded from the segment metrics.
