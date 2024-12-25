import pytest
from abril import ClipComparer
from PIL import Image
import numpy as np


def test_clip_comparer_initialization():
    comparer = ClipComparer()
    assert comparer is not None


def test_compare_text_with_image(test_image_path):
    comparer = ClipComparer()

    # Test with single text
    score = comparer.compare_text_with_image("a photo of a dog", test_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 1

    # Test with multiple texts
    scores = comparer.compare_text_with_image(
        ["a photo of a dog", "a photo of a cat"], test_image_path
    )
    assert isinstance(scores, list)
    assert all(0 <= s <= 1 for s in scores)


def test_find_best_match(test_image_path):
    comparer = ClipComparer()
    texts = ["a photo of a dog", "a photo of a cat", "a photo of a car"]

    best_text, score = comparer.find_best_match(texts, test_image_path)
    assert best_text in texts
    assert 0 <= score <= 1
