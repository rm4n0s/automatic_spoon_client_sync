import httpx

from .schemas import ImageSchema


class ImageCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_images(self) -> list[ImageSchema]:
        resp = httpx.get(self._host + "/api/v1/images")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return [ImageSchema(**item) for item in json_data]

    def get_image(self, id: int) -> ImageSchema:
        resp = httpx.get(self._host + "/api/v1/images/" + str(id))
        _ = resp.raise_for_status()
        json_data = resp.json()
        return ImageSchema.model_validate(json_data)

    def download_image(self, id: int, file_path: str) -> None:
        with httpx.Client() as client:
            with client.stream(
                "GET", self._host + "/api/v1/images/" + str(id) + "/show"
            ) as response:
                response.raise_for_status()  # Raise an error for bad status codes (e.g., 404)
                with open(file_path, "wb") as f:
                    for chunk in response.iter_bytes(
                        chunk_size=8192
                    ):  # Adjust chunk_size as needed
                        f.write(chunk)
