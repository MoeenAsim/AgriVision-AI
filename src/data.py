from pathlib import Path
import shutil
import random

# -----------------------------
# Configuration
# -----------------------------

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

CLASSES = {
    "Wheat___Brown_Rust": "brown_rust",
    "Wheat___Healthy": "healthy",
    "Wheat___Yellow_Rust": "yellow_rust",
}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

random.seed(SEED)


# -----------------------------
# Create directories
# -----------------------------

for split in ["train", "validation", "test"]:
    for class_name in CLASSES.values():
        (PROCESSED_DIR / split / class_name).mkdir(
            parents=True,
            exist_ok=True
        )


# -----------------------------
# Process each class
# -----------------------------

for raw_class, processed_class in CLASSES.items():

    source_dir = RAW_DIR / raw_class

    images = list(source_dir.glob("*.jpg"))

    random.shuffle(images)

    total = len(images)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    splits = {
        "train": train_images,
        "validation": val_images,
        "test": test_images,
    }

    for split, split_images in splits.items():

        destination = PROCESSED_DIR / split / processed_class

        for image in split_images:
            shutil.copy2(
                image,
                destination / image.name
            )

    print(
        f"{processed_class}: "
        f"train={len(train_images)}, "
        f"validation={len(val_images)}, "
        f"test={len(test_images)}"
    )


print("\nDataset processing completed.")