from datasets import load_dataset, Image as DatasetImage
from src import config

import json
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


def save_runtime_config(entries, augmented_cache_dir):
    data_dirs = [
        os.path.join(config.DATASET_DIR, "downloads", "extracted", entry['hash'])
        for entry in entries
    ]

    dataset_paths = [
        os.path.join(config.DATASET_DIR, "downloads", "extracted", entry['hash'], entry['part'])
        for entry in entries
    ]

    augmented_dataset_path = os.path.join(config.DATASET_DIR, augmented_cache_dir)

    runtime_config = {
        "DATA_DIRS": data_dirs,
        "DATASET_PATHS": dataset_paths,
        "AUGMENTED_DATASET_PATH": augmented_dataset_path
    }

    with open(config.RUNTIME_CONFIG_PATH, 'w') as f:
        json.dump(runtime_config, f, indent=2)


def load():
    dataset = load_dataset('poloclub/diffusiondb', 'large_first_10k', cache_dir=config.DATASET_DIR, trust_remote_code=True).cast_column("image", DatasetImage(decode=False))
    cache_dir = dataset.cache_files['train'][0]['filename'].split('/')
    augmented_cache_dir = os.path.join(cache_dir[7], 'augmented_' + cache_dir[8], cache_dir[9])

    if not os.path.exists(augmented_cache_dir):
        config_entries = extract_paths()
        save_runtime_config(config_entries, augmented_cache_dir)

    return dataset
