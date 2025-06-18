import os
from pathlib import Path

# UI config
GENERATED_IMAGE_SIZE = (512, 512)

# path configuration
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, 'dataset')

RUNTIME_CONFIG_PATH = os.path.join(ROOT_DIR, 'src/config.json')