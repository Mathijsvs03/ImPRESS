import os
import json

from datasets import load_from_disk, Image as DatasetImage
from src import config
from src.dataloaders import diffDB_loader
from src.utils import generate_projections

class Dataset:
    data = None
    count = None
    augmented_path = None

    @staticmethod
    def load():
        if Dataset.data is not None:
            print("Dataset already loaded.")
            return

        if os.path.exists(config.RUNTIME_CONFIG_PATH):
            with open(config.RUNTIME_CONFIG_PATH) as f:
                config_data = json.load(f)
                Dataset.augmented_path = config_data.get('AUGMENTED_DATASET_PATH', None)

        print("Loading dataset...")
        if not Dataset.files_exist():
            print("Starting download")
            dataset = diffDB_loader.load()
            print("loaded")
            with open(config.RUNTIME_CONFIG_PATH) as f:
                Dataset.augmented_path = json.load(f).get('AUGMENTED_DATASET_PATH')

            generate_projections(dataset)

        Dataset.data = load_from_disk(Dataset.augmented_path) if Dataset.augmented_path else None
        if Dataset.data is None:
            raise ValueError("Dataset could not be loaded. Please check the data source.")

        # Dataset.data = Dataset.data.cast_column("image", DatasetImage(decode=True)) # Uncomment if you want to load all images in memory
        Dataset.count = Dataset.data.num_rows
        print(f"Finished loading dataset with {Dataset.count} entries.")

    @staticmethod
    def get_data():
        if Dataset.data is None:
            raise ValueError("Dataset not loaded. Call Dataset.load() first.")
        return Dataset.data

    @staticmethod
    def get_count():
        if Dataset.count is None:
            raise ValueError("Dataset not loaded. Call Dataset.load() first.")
        return Dataset.count

    @staticmethod
    def files_exist():
        augmented_exists = Dataset.augmented_path is not None and os.path.exists(Dataset.augmented_path)
        return os.path.exists(config.RUNTIME_CONFIG_PATH) and augmented_exists
