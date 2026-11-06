# Haversine Telemetry

A small, dependency-free Python utility for calculating GPS track distance, overall average speed, and per-segment telemetry using the Haversine formula.

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

total_distance_km, segments, average_speed_kmh = compute_telemetry_metrics(track_data)
print(f"Total distance: {total_distance_km:.3f} km")
print(f"Average speed: {average_speed_kmh:.2f} km/h")
```

Coordinates are `(latitude, longitude, timestamp_seconds)` tuples. The function returns total distance in kilometers, a list of per-segment metrics, and overall average speed in kilometers per hour. Overall average speed is total track distance divided by the elapsed time between the first and last timestamps; it is `0.0` if elapsed time is not positive. Each segment includes distance in kilometers, speed in kilometers per hour, and pace in minutes per kilometer. Segments with zero or negative elapsed time are excluded from the segment metrics.
