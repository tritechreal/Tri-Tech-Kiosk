import os

from tflite_model_maker import model_spec
from tflite_model_maker import object_detector
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.object_detector import DataLoader

train_data = DataLoader.from_pascal_voc(
    images_dir='/path/to/images', 
    annotations_dir='/path/to/annotations', 
    label_map={1: "your_label_1", 2: "your_label_2"}  # Update with your labels
)

train_data, validation_data = train_data.split(0.8)  # 80% for training

spec = model_spec.get('efficientdet_lite0')

model = object_detector.create(train_data, model_spec=spec, validation_data=validation_data, epochs=50, batch_size=8)  # Adjust epochs and batch_size as needed

model.evaluate(validation_data)
config = QuantizationConfig.for_float16()  # Or other quantization options
model.export(export_dir='.', tflite_filename='my_quantized_model.tflite', quantization_config=config)