import os

from datasets import load_from_disk, Image as DatasetImage
from src import config
from src.dataloaders import diffDB_loader
from src.utils import generate_projections

class Dataset:
    data = None
    count = None

    @staticmethod
    def load():
        if Dataset.data is not None:
            print("Dataset already loaded.")
            return

        print("Loading dataset...")
        if not os.path.exists(config.AUGMENTED_DATASET_PATH):
            dataset = diffDB_loader.load()
            print(dataset['train'][0])  # Print the first entry as a sample
            generate_projections(dataset)

        Dataset.data = load_from_disk(config.AUGMENTED_DATASET_PATH)
        Dataset.data = Dataset.data.cast_column("image", DatasetImage(decode=True))
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
        return os.path.exists(config.AUGMENTED_DATASET_PATH) and os.path.exists(config.DATASET_PATH)
