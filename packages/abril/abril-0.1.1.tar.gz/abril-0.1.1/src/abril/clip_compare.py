import os
import torch
import clip
from PIL import Image
import numpy as np
from typing import Union, List, Tuple
from pathlib import Path


class ClipComparer:
    """Main class for comparing text and images using CLIP."""

    def __init__(self, model_name: str = "ViT-B/32", device: str = None):
        """
        Initialize the CLIP model.

        Args:
            model_name: CLIP model variant to use
            device: Device to run the model on ('cuda' or 'cpu')
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=device)

    def compare_text_with_image(
        self, text: Union[str, List[str]], image: Union[str, Path, Image.Image]
    ) -> Union[float, List[float]]:
        """
        Compare text with an image using CLIP.

        Args:
            text: Single text string or list of strings to compare
            image: Path to image file or PIL Image object

        Returns:
            Similarity score(s) between 0 and 1
        """
        # Prepare text input
        if isinstance(text, str):
            text = [text]

        # Prepare image input
        if isinstance(image, (str, Path)):
            image = Image.open(str(image))
        image = self.preprocess(image).unsqueeze(0).to(self.device)

        # Encode inputs
        with torch.no_grad():
            text_features = self.model.encode_text(clip.tokenize(text).to(self.device))
            image_features = self.model.encode_image(image)

        # Normalize features
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        # Calculate similarity
        similarity = (100.0 * text_features @ image_features.T).softmax(dim=-1)

        return similarity.cpu().numpy().tolist()[0]

    def find_best_match(
        self, texts: List[str], image: Union[str, Path, Image.Image]
    ) -> Tuple[str, float]:
        """
        Find the text that best matches the image.

        Args:
            texts: List of text strings to compare
            image: Path to image file or PIL Image object

        Returns:
            Tuple of (best matching text, similarity score)
        """
        scores = self.compare_text_with_image(texts, image)
        best_idx = np.argmax(scores)
        return texts[best_idx], scores[best_idx]
