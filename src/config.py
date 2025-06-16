import os
from pathlib import Path

# UI config
GENERATED_IMAGE_SIZE = (512, 512)

# path configuration
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, 'dataset')
DATA_DIR = os.path.join(DATASET_DIR, 'data')
DOWNLOADS_DIR = os.path.join(DATASET_DIR, 'downloads')
DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
AUGMENTED_DATASET_PATH = os.path.join(DATA_DIR, 'augmented_dataset.csv')
ATTRIBUTE_DATA_PATH = os.path.join(DATA_DIR, 'image_attributes.csv')