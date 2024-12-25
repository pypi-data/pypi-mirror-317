import sys
from pathlib import Path
import os

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_path))

import pytest
from PIL import Image
import numpy as np
from urllib.request import urlretrieve

# Import from local source instead of installed package
from abril.clip_compare import ClipComparer


def get_test_image():
    """Download a test image if it doesn't exist."""
    test_image_path = os.path.join(os.path.dirname(__file__), "data", "test_image.jpg")
    os.makedirs(os.path.dirname(test_image_path), exist_ok=True)

    if not os.path.exists(test_image_path):
        print(f"Downloading test image to {test_image_path}...")
        url = "https://raw.githubusercontent.com/openai/CLIP/main/CLIP.png"
        urlretrieve(url, test_image_path)

    return test_image_path


def test_clip_comparer_initialization():
    comparer = ClipComparer()
    assert comparer is not None
    print("Initialization test passed")


def test_compare_text_with_image():
    comparer = ClipComparer()
    test_image_path = get_test_image()

    # Test with single text
    print("\nTesting single text comparison...")
    score = comparer.compare_text_with_image("a photo of a dog", test_image_path)
    print(f"Single text score: {score}")
    print(f"Score type: {type(score)}")
    assert isinstance(score, float), f"Expected float, got {type(score)}"
    assert 0 <= score <= 1, f"Score {score} not in range [0,1]"
    print("Single text test passed")

    # Test with multiple texts
    print("\nTesting multiple text comparison...")
    scores = comparer.compare_text_with_image(
        ["a photo of a dog", "a photo of a cat", "a photo of a car"], test_image_path
    )
    print(f"Multiple text scores: {scores}")
    print(f"Scores type: {type(scores)}")
    assert isinstance(scores, list), f"Expected list, got {type(scores)}"
    assert all(isinstance(s, float) for s in scores), "All scores should be floats"
    assert all(0 <= s <= 1 for s in scores), "All scores should be in range [0,1]"
    print("Multiple text test passed")


def test_find_best_match():
    comparer = ClipComparer()
    test_image_path = get_test_image()
    texts = ["a photo of a dog", "a photo of a cat", "a photo of a car", "a landscape photo"]

    print("\nTesting best match...")
    best_text, score = comparer.find_best_match(texts, test_image_path)
    print(f"Best match: {best_text}, score: {score}")
    assert best_text in texts
    assert isinstance(score, float)
    assert 0 <= score <= 1
    print("Best match test passed")


if __name__ == "__main__":
    print("Starting tests...")
    test_clip_comparer_initialization()
    test_compare_text_with_image()
    test_find_best_match()
    print("\nAll tests passed successfully!")
