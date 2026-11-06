import unittest

from telemetry import calculate_haversine_distance, compute_telemetry_metrics


class HaversineDistanceTests(unittest.TestCase):
    def test_same_coordinate_has_zero_distance(self):
        self.assertAlmostEqual(
            calculate_haversine_distance(23.3441, 85.3096, 23.3441, 85.3096),
            0.0,
            places=10,
        )

    def test_one_degree_of_latitude_is_about_111_km(self):
        distance = calculate_haversine_distance(0, 0, 1, 0)
        self.assertAlmostEqual(distance, 111.195, delta=0.01)

    def test_distance_is_symmetric(self):
        forward = calculate_haversine_distance(23.3441, 85.3096, 23.3451, 85.3106)
        reverse = calculate_haversine_distance(23.3451, 85.3106, 23.3441, 85.3096)
        self.assertAlmostEqual(forward, reverse, places=10)


class TelemetryMetricsTests(unittest.TestCase):
    def test_empty_and_single_point_tracks_have_no_segments(self):
        self.assertEqual(compute_telemetry_metrics([]), (0.0, []))
        self.assertEqual(compute_telemetry_metrics([(0, 0, 0)]), (0.0, []))

    def test_track_sums_distance_and_returns_segment_metrics(self):
        track = [(0, 0, 0), (0, 0.01, 3600)]
        total_distance, segments = compute_telemetry_metrics(track)

        self.assertAlmostEqual(total_distance, 1.11195, delta=0.001)
        self.assertEqual(len(segments), 1)
        self.assertAlmostEqual(segments[0]["distance_km"], total_distance)
        self.assertAlmostEqual(segments[0]["speed_kmh"], total_distance)
        self.assertAlmostEqual(segments[0]["pace"], 60.0)

    def test_non_positive_time_is_excluded_from_segments(self):
        track = [(0, 0, 10), (0, 0.01, 10), (0, 0.02, 5)]
        total_distance, segments = compute_telemetry_metrics(track)

        self.assertGreater(total_distance, 2.0)
        self.assertEqual(segments, [])


if __name__ == "__main__":
    unittest.main()
