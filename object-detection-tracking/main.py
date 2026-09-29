import argparse
import time
import cv2

from src.video_input import open_video_source, get_video_properties
from src.detector import Detector
from src.tracker import Tracker
from src.utils import draw_track, draw_fps

def parse_args():
    parser = argparse.ArgumentParser(description="Object detection and tracking")
    parser.add_argument("--source", default="input/mixed.mp4",
                        help="video file path, or 0 for a webcam")
    parser.add_argument("--output", default="output/result.mp4")
    parser.add_argument("--model", default="models/yolov8n.pt")
    parser.add_argument("--conf", type=float, default=0.3)
    parser.add_argument("--max-frames", type=int, default=0,
                        help="stop after this many frames (0 = whole video)")
    parser.add_argument("--show", action="store_true",
                        help="open a live window (needs a screen, not for Codespaces)")
    return parser.parse_args()


def main():
    args = parse_args()

    source = int(args.source) if args.source.isdigit() else args.source
    cap = open_video_source(source)
    width, height, fps = get_video_properties(cap)

    writer = cv2.VideoWriter(
        args.output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    detector = Detector(args.model, conf=args.conf)
    tracker = Tracker()

    frame_count = 0
    while True:
        start = time.time()

        ok, frame = cap.read()
        if not ok:
            break

        detections = detector.detect(frame)
        tracks = tracker.update(detections, frame)

        for track_id, x1, y1, x2, y2, name in tracks:
            draw_track(frame, track_id, x1, y1, x2, y2, name)

        draw_fps(frame, 1.0 / max(time.time() - start, 1e-6))
        writer.write(frame)

        if args.show:
            cv2.imshow("Object Detection and Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames...")
        if args.max_frames and frame_count >= args.max_frames:
            break

    cap.release()
    writer.release()
    if args.show:
        cv2.destroyAllWindows()

    print(f"Done. {frame_count} frames saved to {args.output}")


if __name__ == "__main__":
    main()