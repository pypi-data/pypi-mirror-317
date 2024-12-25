from __future__ import annotations

import logging
import torch
import open_clip  # Changed to open_clip for explicit reference
import numpy as np
from PIL import Image
from typing import Union, List, Tuple, Optional
from pathlib import Path
from PIL.Image import Image as PILImage

# Configure logging
logger = logging.getLogger(__name__)


class ClipComparer:
    """
    A class to compare images and text using OpenAI's CLIP model.

    This class provides functionality to:
    1. Compare text descriptions with images
    2. Find the best matching text for a given image
    3. Calculate similarity scores between text and images
    """

    def __init__(self, model_name: str = "ViT-B-32", device: Optional[str] = None) -> None:
        """
        Initialize the CLIP model with specified parameters.

        Args:
            model_name (str): Name of the CLIP model to use (default: "ViT-B-32")
            device (Optional[str]): Device to run the model on (default: None, will use CUDA if available)

        Raises:
            RuntimeError: If model loading fails
        """
        try:
            # Set device (CUDA if available, else CPU)
            self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Loading CLIP model '{model_name}' on {self.device}")

            # Initialize model and preprocessor
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                model_name, device=self.device, pretrained="openai"
            )
            self.model_name = model_name
            self.tokenizer = open_clip.get_tokenizer(model_name)

            # Set model to evaluation mode
            self.model.eval()
            logger.info("CLIP model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise RuntimeError(f"Failed to load CLIP model '{model_name}': {e}")

    def compare_text_with_image(
        self, text: Union[str, List[str]], image: Union[str, Path, PILImage]
    ) -> Union[float, List[float]]:
        """
        Compare text descriptions with an image using CLIP.

        Args:
            text (Union[str, List[str]]): Single text string or list of text strings to compare
            image (Union[str, Path, PILImage]): Image to compare (file path or PIL Image)

        Returns:
            Union[float, List[float]]: Similarity score(s) between 0 and 1

        Raises:
            FileNotFoundError: If image file not found
            ValueError: If image loading fails
            Exception: For other processing errors
        """
        try:
            # Handle single text input
            single_text = isinstance(text, str)
            texts = [text] if single_text else text

            # Load image if path provided
            if isinstance(image, (str, Path)):
                try:
                    image_path = Path(image)
                    if not image_path.exists():
                        raise FileNotFoundError(f"Image file not found: {image_path}")
                    image = Image.open(image_path).convert("RGB")
                except Exception as e:
                    raise ValueError(f"Failed to load image from path: {e}")

            # Preprocess image for model input
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            # Process through CLIP
            with torch.no_grad():
                # Tokenize and encode text
                text_tokens = self.tokenizer(texts).to(self.device)

                # Get text and image features
                text_features = self.model.encode_text(text_tokens)
                image_features = self.model.encode_image(image_input)

                # Normalize features
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)

                # Calculate cosine similarity
                similarity = (text_features @ image_features.T).squeeze(1)

                # Convert to standard Python floats
                raw_scores = similarity.cpu().numpy().tolist()
                if isinstance(raw_scores, float):
                    raw_scores = [raw_scores]

                # Convert similarity scores to 0-1 range
                scores = [(score + 1) / 2 for score in raw_scores]

                return scores[0] if single_text else scores

        except Exception as e:
            logger.error(f"Error in compare_text_with_image: {e}")
            raise

    def find_best_match(
        self, texts: List[str], image: Union[str, Path, PILImage]
    ) -> Tuple[str, float]:
        """
        Find the text description that best matches the image.

        Args:
            texts (List[str]): List of text descriptions to compare
            image (Union[str, Path, PILImage]): Image to compare against

        Returns:
            Tuple[str, float]: Best matching text and its similarity score

        Raises:
            Exception: If comparison fails
        """
        try:
            scores = self.compare_text_with_image(texts, image)
            best_idx = np.argmax(scores)
            return texts[best_idx], float(scores[best_idx])
        except Exception as e:
            logger.error(f"Error in find_best_match: {e}")
            raise

    def __repr__(self) -> str:
        """Return string representation of the ClipComparer instance."""
        return f"ClipComparer(model='{self.model_name}', device='{self.device}')"
