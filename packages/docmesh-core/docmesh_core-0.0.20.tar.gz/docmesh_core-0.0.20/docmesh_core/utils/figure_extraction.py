import os
import requests

from io import BytesIO
from PIL import Image
from retry import retry


@retry(tries=3)
def extract_figures(img: Image.Image, threshold: float = 0.85) -> list[Image.Image]:
    url = os.getenv("FIGURE_EXTRACTION_URL")

    if url is None:
        raise ValueError("FIGURE_EXTRACTION_URL is not set.")
    else:
        figures = []
        with BytesIO() as buffer:
            img.save(buffer, format="PNG")

            files = [("img", ("image.png", buffer.getvalue(), "image/png"))]
            rsp = requests.request("POST", url, files=files)
            rsp.raise_for_status()

        for data in rsp.json():
            if data["score"] >= threshold:
                figures.append(img.crop(data["box"]))

        return figures
