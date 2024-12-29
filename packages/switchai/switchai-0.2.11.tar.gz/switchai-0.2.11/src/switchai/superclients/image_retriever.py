from typing import Optional, List, Union

from PIL.Image import Image

from .. import SwitchAI


class ImageRetriever:
    def __init__(
        self,
        client: SwitchAI,
        images_folder_path: str,
        batch_size: Optional[int] = 32,
        embeddings_path: Optional[str] = None,
    ):
        pass

    def retrieve_images(self, query: Union[str, Image]) -> List[str]:
        pass
