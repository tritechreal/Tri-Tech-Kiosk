from picamera2.devices.imx500 import IMX500

# This must be called before instantiation of Picamera2
imx500 = IMX500(model_file)

class Detection:
    def __init__(self, coords, category, conf, metadata):
        """Create a Detection object, recording the bounding box, category and confidence."""
        self.category = category
        self.conf = conf
        obj_scaled = imx500.convert_inference_coords(coords, metadata, picam2)
        self.box = (obj_scaled.x, obj_scaled.y, obj_scaled.width, obj_scaled.height)

def draw_detections(request, detections, stream="main"):
    """Draw the detections for this request onto the ISP output."""
    labels = get_labels()
    with MappedArray(request, stream) as m:
        for detection in detections:
            x, y, w, h = detection.box
            label = f"{labels[int(detection.category)]} ({detection.conf:.2f})"
            cv2.putText(m.array, label, (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 0, 255, 0))
        if args.preserve_aspect_ratio:
            b = imx500.get_roi_scaled(request)
            cv2.putText(m.array, "ROI", (b.x + 5, b.y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.rectangle(m.array, (b.x, b.y), (b.x + b.width, b.y + b.height), (255, 0, 0, 0))

def parse_detections(request, stream='main'):
    """Parse the output tensor into a number of detected objects, scaled to the ISP output."""
    outputs = imx500.get_outputs(request.get_metadata())
    boxes, scores, classes = outputs[0][0], outputs[1][0], outputs[2][0]
    detections = [ Detection(box, category, score, metadata)
                   for box, score, category in zip(boxes, scores, classes) if score > threshold]
    draw_detections(request, detections, stream)