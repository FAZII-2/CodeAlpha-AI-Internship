import cv2

def get_color(track_id):
    track_id = int(track_id)
    return (
        (track_id * 37) % 200 + 55,
        (track_id * 91) % 200 + 55,
        (track_id * 153) % 200 + 55,
    )

def draw_track(frame, track_id, x1, y1, x2, y2, label):
    color = get_color(track_id)
    text = f"{label} #{track_id}"

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    (text_w, text_h), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

    top = max(y1 - text_h - baseline - 4, 0)
    cv2.rectangle(frame, (x1, top), (x1 + text_w + 6, top + text_h + baseline + 4), color, -1)
    cv2.putText(frame, text, (x1 + 3, top + text_h + 1),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)