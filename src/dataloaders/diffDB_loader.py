from datasets import load_dataset, Image as DatasetImage
from src import config

import os
import re


def extract_paths():
    extracted_path = os.path.join(config.DATASET_DIR, 'downloads/extracted')
    hash_dirs = [d for d in os.listdir(extracted_path) if os.path.isdir(os.path.join(extracted_path, d))]

    config_entries = []
    for hash_dir in hash_dirs:
        full_path = os.path.join(extracted_path, hash_dir)
        for fname in os.listdir(full_path):
            match = re.match(r'part-(\d+)\.json', fname)
            if not match:
                continue

            config_entries.append({
                'hash': hash_dir,
                'part': fname,
                'path': os.path.join(full_path, fname)
            })

    return config_entries


def load():
    dataset = load_dataset('poloclub/diffusiondb', 'large_random_1k', cache_dir=config.DATASET_DIR, trust_remote_code=True).cast_column("image", DatasetImage(decode=False))
    cache_dir = dataset.cache_files['train'][0]['filename'].split('/')
    augmented_cache_dir = os.path.join(cache_dir[7], 'augmented_' + cache_dir[8], cache_dir[9])

    if not os.path.exists(augmented_cache_dir):
        config_entries = extract_paths()

        lines = []
        lines.append("\n\n# Auto-generated DiffusionDB cache config")
        lines.append(f"DATA_DIR = os.path.join(DATASET_DIR, 'downloads/extracted/{config_entries[0]['hash']}')")
        lines.append(f"DATASET_PATH = os.path.join(DATA_DIR, '{config_entries[0]['part']}')")
        lines.append(f"AUGMENTED_DATASET_PATH = os.path.join(DATASET_DIR, '{augmented_cache_dir}')")

        with open("src/config.py", "a") as f:
            f.write("\n".join(lines) + "\n")

    return dataset
