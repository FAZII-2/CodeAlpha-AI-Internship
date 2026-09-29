from collections import Counter, defaultdict
from deep_sort_realtime.deepsort_tracker import DeepSort


class Tracker:
    
    def __init__(self, max_age=30, n_init=3):
        self.tracker = DeepSort(max_age=max_age, n_init=n_init)
        self.label_votes = defaultdict(Counter)

    def update(self, detections, frame):
        tracks = self.tracker.update_tracks(detections, frame=frame)

        results = []
        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 0:
                continue

            left, top, right, bottom = track.to_ltrb()
            track_id = track.track_id

            self.label_votes[track_id][track.get_det_class()] += 1
            label = self.label_votes[track_id].most_common(1)[0][0]

            results.append((
                track_id,
                int(left), int(top), int(right), int(bottom),
                label,
            ))

        return results