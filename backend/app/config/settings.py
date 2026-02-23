from platformdirs import user_data_dir
import os

# Model Exports Path
MODEL_EXPORTS_PATH = "app/models/ONNX_Exports"

# Microservice URLs
SYNC_MICROSERVICE_URL = "http://localhost:52124"

CONFIDENCE_PERCENT = 0.6
# Object Detection Models:
SMALL_OBJ_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Small.onnx"
NANO_OBJ_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Nano.onnx"
MEDIUM_OBJ_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Medium.onnx"

# Face Detection Models:
SMALL_FACE_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Small_Face.onnx"
NANO_FACE_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Nano_Face.onnx"
MEDIUM_FACE_DETECTION_MODEL = f"{MODEL_EXPORTS_PATH}/YOLOv11_Medium_Face.onnx"

# FaceNet Model to extract face embeddings:
DEFAULT_FACENET_MODEL = f"{MODEL_EXPORTS_PATH}/FaceNet_128D.onnx"

TEST_INPUT_PATH = "tests/inputs"
TEST_OUTPUT_PATH = "tests/outputs"
if os.getenv("GITHUB_ACTIONS") == "true":
    DATABASE_PATH = os.path.join(os.getcwd(), "test_db.sqlite3")
else:
    DATABASE_PATH = os.path.join(user_data_dir("PictoPy"), "database", "PictoPy.db")
THUMBNAIL_IMAGES_PATH = os.path.join(user_data_dir("PictoPy"), "thumbnails")
IMAGES_PATH = "./images"
# Shutdown protection settings
# If SHUTDOWN_TOKEN is set in environment, the shutdown endpoint requires the header
# 'X-Shutdown-Token' with the same value. By default remote shutdowns are not allowed
# unless ALLOW_REMOTE_SHUTDOWN is set to 'true' in the environment.
SHUTDOWN_TOKEN = os.getenv("SHUTDOWN_TOKEN")
ALLOW_REMOTE_SHUTDOWN = os.getenv("ALLOW_REMOTE_SHUTDOWN", "false").lower() == "true"
