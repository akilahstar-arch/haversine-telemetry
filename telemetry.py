import math


def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Compute the great-circle distance between two GPS coordinates in km."""
    earth_radius_km = 6371.0

    # Convert degrees to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    # Haversine core equation
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    # Clamp to protect sqrt from floating-point rounding near antipodal points.
    a = min(1.0, max(0.0, a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


def compute_telemetry_metrics(coord_history):
    """Compute total distance and per-segment speed and pace.

    Args:
        coord_history: Iterable of (latitude, longitude, timestamp_seconds) tuples.

    Returns:
        A tuple containing total distance in kilometers and a list of segment
        dictionaries. Each segment has distance_km, speed_kmh, and pace (minutes
        per kilometer). Segments with non-positive elapsed time are omitted.
    """
    total_distance = 0.0
    segments = []

    for i in range(1, len(coord_history)):
        lat1, lon1, t1 = coord_history[i - 1]
        lat2, lon2, t2 = coord_history[i]

        dist = calculate_haversine_distance(lat1, lon1, lat2, lon2)
        total_distance += dist

        time_delta_hours = (t2 - t1) / 3600.0
        if time_delta_hours > 0:
            speed_kmh = dist / time_delta_hours
            pace_min_km = 60.0 / speed_kmh if speed_kmh > 0.5 else 0.0
            segments.append(
                {
                    "distance_km": dist,
                    "speed_kmh": speed_kmh,
                    "pace": pace_min_km,
                }
            )

    return total_distance, segments


if __name__ == "__main__":
    # Example coordinates around Ranchi, India; timestamps are in seconds.
    track_data = [
        (23.3441, 85.3096, 0),
        (23.3451, 85.3106, 12),
        (23.3465, 85.3120, 25),
    ]

    total_dist, telemetry_log = compute_telemetry_metrics(track_data)
    print(f"Total Traversed Distance: {total_dist:.3f} km")
    print(f"Segment metrics: {telemetry_log}")
