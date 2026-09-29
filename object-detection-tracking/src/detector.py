from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="models/yolov8n.pt", conf=0.4):
        self.model = YOLO(model_path)
        self.conf = conf
        self.names = self.model.names

    def detect(self, frame):
        result = self.model(frame, conf=self.conf, verbose=False)[0]

        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.names[class_id]

            detections.append(([x1, y1, x2 - x1, y2 - y1], confidence, class_name))

        return detections