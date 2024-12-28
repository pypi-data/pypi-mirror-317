import os
import uuid
import tempfile
from io import BytesIO
import numpy as np
from PIL import Image


def save_image_to_temp(image):
    random_filename = f"cfimg_{uuid.uuid4().hex}.png"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, random_filename)

    try:

        if isinstance(image, bytes):
            image = BytesIO(image)

        if isinstance(image, BytesIO):
            image = Image.open(image)

        if isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        if isinstance(image, Image.Image):
            image.save(file_path, format="PNG")
        else:
            raise ValueError("Unsupported image type provided.")

    except Exception as e:
        raise ValueError(f"Failed to save image: {e}")

    return file_path
