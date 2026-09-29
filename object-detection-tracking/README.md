# Object Detection and Tracking

**CodeAlpha AI Internship — Task 4**

Real-time object detection and multi-object tracking on video, built with a pre-trained YOLOv8 model and Deep SORT.

## Features

- Reads video from a file or a live webcam
- Detects objects in every frame using a pre-trained YOLOv8 model
- Tracks each object across frames with Deep SORT, giving it a persistent ID
- Draws bounding boxes, class labels, and tracking IDs on the video in real time
- Stabilizes labels per track using a majority-vote system, so a single object keeps one consistent label instead of flickering between guesses
- Filters out "ghost" boxes — predicted positions for objects Deep SORT has lost, rather than real detections
- Displays a live FPS counter
- Saves the final annotated video to disk

## Tech Stack

- **OpenCV** – video I/O, frame processing, drawing
- **Ultralytics YOLOv8** – pre-trained object detection
- **deep-sort-realtime** – multi-object tracking

## Project Structure

object-detection-tracking/
├── src/
│ ├── video_input.py # opens webcam or video file
│ ├── detector.py # loads YOLOv8, runs detection per frame
│ ├── tracker.py # Deep SORT wrapper, ID assignment, label voting
│ └── utils.py # drawing boxes, labels, FPS counter
├── input/ # source videos
├── output/ # saved result videos
├── models/ # YOLOv8 weight files
├── main.py # runs the full pipeline
├── requirements.txt
└── README.md


## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

```bash
python main.py --source input/street_road.mp4 --model models/yolov8s.pt --output output/street_result.mp4 --conf 0.4
```

**Arguments**

| Flag | Default | Description |
|---|---|---|
| `--source` | `input/mixed.mp4` | Video file path, or `0` for a webcam |
| `--model` | `models/yolov8n.pt` | Path to the YOLOv8 weights to use |
| `--output` | `output/result.mp4` | Where the annotated video is saved |
| `--conf` | `0.3` | Minimum detection confidence to keep a box |
| `--max-frames` | `0` (whole video) | Stop early after N frames, useful for quick tests |
| `--show` | off | Open a live preview window (needs a display, not for Codespaces) |

## How It Works

1. **Video input** — `open_video_source()` opens either a webcam index or a video file path through OpenCV's `VideoCapture`, so the rest of the pipeline doesn't need to know which one it's using.
2. **Detection** — Each frame is passed to a YOLOv8 model, which returns bounding boxes, class names, and confidence scores for every object it finds.
3. **Tracking** — Those detections are handed to Deep SORT, which matches them against objects seen in previous frames and assigns a consistent track ID. A majority-vote system remembers every label Deep SORT's underlying detections have given a track ID and displays the most common one, so a car briefly misclassified for a frame or two doesn't flicker between labels.
4. **Drawing and output** — Each tracked object is drawn as a box with its ID and label, an FPS counter is overlaid, and the frame is written to the output video.

## Results

- Model used: `[yolov8s.pt]`
- Test video: `[street_road.mp4, 18 seconds, street-level traffic]`
- Observed FPS: `[462]`
- An earlier test on an overhead parking-lot clip with yolov8n produced frequent mislabeling (cars tagged as buses/cell phones) and unstable IDs; switching to yolov8s and street-level footage resolved this.

## Limitations

- Overhead or unusual camera angles reduce detection accuracy, since YOLOv8 was trained mostly on eye-level/street-level imagery
- Runs on CPU by default; a GPU would allow real-time performance at higher resolutions
- Occasional ID switches can still occur during heavy occlusion (objects passing behind each other)

## Author

CodeAlpha AI Internship — Faizan Ali