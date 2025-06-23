import os
from pathlib import Path

# UI config
GENERATED_IMAGE_SIZE = (512, 512)
MAX_IMAGES_IN_ZOOM = 100

# path configuration
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, 'dataset')
MODEL_DIR = os.path.join(DATASET_DIR, 'models')
GENERATED_IMAGE_DIR = os.path.join(DATASET_DIR, 'generated')

RUNTIME_CONFIG_PATH = os.path.join(ROOT_DIR, 'src/config.json')