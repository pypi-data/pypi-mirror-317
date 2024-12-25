from __future__ import annotations

import logging
import torch
import clip
from PIL import Image
import numpy as np
from typing import Union, List, Tuple, Optional
from pathlib import Path
from PIL.Image import Image as PILImage

logger = logging.getLogger(__name__)


class ClipComparer:
    def __init__(self, model_name: str = "ViT-B/32", device: Optional[str] = None) -> None:
        """Initialize CLIP model."""
        try:
            self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Loading CLIP model '{model_name}' on {self.device}")
            self.model, self.preprocess = clip.load(model_name, device=self.device)
            self.model_name = model_name
            self.model.eval()
            logger.info("CLIP model loaded successfully")
        except RuntimeError as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise RuntimeError(f"Failed to load CLIP model '{model_name}': {e}")

    def compare_text_with_image(
        self, text: Union[str, List[str]], image: Union[str, Path, PILImage]
    ) -> Union[float, List[float]]:
        """Compare text with image using CLIP."""
        try:
            # Convert single text to list and track if we should return single value
            single_text = isinstance(text, str)
            texts = [text] if single_text else text

            # Load and preprocess image
            if isinstance(image, (str, Path)):
                try:
                    image_path = Path(image)
                    if not image_path.exists():
                        raise FileNotFoundError(f"Image file not found: {image_path}")
                    image = Image.open(image_path)
                except Exception as e:
                    raise ValueError(f"Failed to load image from path: {e}")

            # Preprocess image for CLIP
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            # Process through CLIP
            with torch.no_grad():
                # Tokenize and encode text
                text_tokens = clip.tokenize(texts).to(self.device)
                text_features = self.model.encode_text(text_tokens)
                image_features = self.model.encode_image(image_input)

                # Normalize features
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)

                # Calculate cosine similarity
                similarity = text_features @ image_features.T

                # Convert to Python floats (values will be between -1 and 1)
                raw_scores = [float(score) for score in similarity.cpu().numpy()]

                # Convert from cosine similarity (-1 to 1) to a more intuitive 0 to 1 scale
                scores = [(score + 1) / 2 for score in raw_scores]

                # Return single float if input was single string
                return scores[0] if single_text else scores

        except Exception as e:
            logger.error(f"Error in compare_text_with_image: {e}")
            raise

    def find_best_match(
        self, texts: List[str], image: Union[str, Path, PILImage]
    ) -> Tuple[str, float]:
        """Find the text that best matches the image."""
        try:
            scores = self.compare_text_with_image(texts, image)
            best_idx = np.argmax(scores)
            return texts[best_idx], float(scores[best_idx])
        except Exception as e:
            logger.error(f"Error in find_best_match: {e}")
            raise

    def __repr__(self) -> str:
        """Return string representation."""
        return f"ClipComparer(model='{self.model_name}', device='{self.device}')"
