import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from pathlib import Path

def run_inference(image_path):
	MODEL_PATH = str(
		Path(__file__).resolve().parent / "model_visdrone_yolov8n_car.tflite"
	)

	CONF_TH = 0.35
	IOU_TH = 0.45

	CLASS_NAMES = {
    		0: "car",
    		1: "van",
    		2: "truck"
	}

	interpreter = Interpreter(model_path=MODEL_PATH)
	interpreter.allocate_tensors()

	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()

	input_shape = input_details[0]["shape"]
	height = input_shape[1]
	width = input_shape[2]

	img = cv2.imread(str(image_path))
	if img is None:
	    raise FileNotFoundError(f"Immagine non trovata: {image_path}")

	orig_h, orig_w = img.shape[:2]

	resized = cv2.resize(img, (width, height))
	rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

	input_data = np.expand_dims(rgb, axis=0).astype(np.float32) / 255.0

	input_dtype = input_details[0]["dtype"]

	if input_dtype != np.float32:
	    scale, zero_point = input_details[0]["quantization"]
	    input_data = input_data / scale + zero_point
	    input_data = input_data.astype(input_dtype)

	interpreter.set_tensor(input_details[0]["index"], input_data)
	interpreter.invoke()

	output = interpreter.get_tensor(output_details[0]["index"])

	out_scale, out_zero = output_details[0]["quantization"]
	if out_scale != 0:
	    output = (output.astype(np.float32) - out_zero) * out_scale

	output = np.squeeze(output)

	if output.shape[0] < output.shape[1]:
	    output = output.T

	boxes = []
	scores = []
	classes = []

	for pred in output:
	    x, y, w, h = pred[0:4]

	    cls_scores = pred[4:]
	    cls_id = int(np.argmax(cls_scores))
	    conf = float(np.max(cls_scores))

	    if conf < CONF_TH:
	        continue

	    # Coordinate YOLO normalizzate 0-1
	    x1 = int((x - w / 2) * orig_w)
	    y1 = int((y - h / 2) * orig_h)
	    x2 = int((x + w / 2) * orig_w)
	    y2 = int((y + h / 2) * orig_h)

	    x1 = max(0, min(x1, orig_w - 1))
	    y1 = max(0, min(y1, orig_h - 1))
	    x2 = max(0, min(x2, orig_w - 1))
	    y2 = max(0, min(y2, orig_h - 1))

	    bw = x2 - x1
	    bh = y2 - y1

	    if bw <= 0 or bh <= 0:
	        continue

	    boxes.append([x1, y1, bw, bh])
	    scores.append(conf)
	    classes.append(cls_id)

	indices = cv2.dnn.NMSBoxes(
	    boxes,
	    scores,
	    CONF_TH,
	    IOU_TH
	)

	count = 0

	if len(indices) > 0:
	    for i in indices.flatten():
	        count += 1

	        x, y, w, h = boxes[i]
	        cls_id = classes[i]
	        conf = scores[i]

	        label = f"{CLASS_NAMES.get(cls_id, cls_id)} {conf:.2f}"

	        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
	        cv2.putText(
	            img,
	            label,
	            (x, max(y - 5, 20)),
	            cv2.FONT_HERSHEY_SIMPLEX,
	            0.6,
	            (255, 0, 0),
	            2
	        )

	print(f"VEICOLI_RILEVATI={count}")

	image_path = Path(image_path)
	output_path = image_path.with_name(
		f"{image_path.stem}_detected{image_path.suffix}"
	)

	cv2.imwrite(output_path, img)

	return count, str(output_path)
	
