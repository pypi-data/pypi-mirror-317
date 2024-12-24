import json
import os
from urllib.parse import urlparse

import requests

from .check_func import CheckValue


class ColabLoad(CheckValue):

    @staticmethod
    async def __get_url_id(url):
        return urlparse(url).path.rstrip("/").split("/")[-1]

    async def load_file_s(self, url: str, save_dir: str, file_name: str):
        return await self.load_file_single(url, save_dir, file_name)

    async def load_file_single(self, url: str, save_dir: str = None, file_name: str = None):
        """
        :param url: url
        :param save_dir: The folder where the files will be saved
        :return:
        """
        if save_dir:
            save_dir = self._check_dir(save_dir)
        file_name = file_name if file_name.endswith(".ipynb") else file_name + ".ipynb"

        url = self._check_url(url)
        url_id = await self.__get_url_id(url)

        response = requests.get(
            f'https://drive.usercontent.google.com/download?id={url_id}',
        )
        if response.status_code != 200:
            return {"error": True,
                    "msg": f"Ошибка - {url}!",
                    "file_path": None,
                    # "response_text": response.text,
                    "status_code": response.status_code
                    }

        if save_dir:
            file_path = os.path.join(save_dir, file_name)
        else:
            file_path = file_name

        try:
            data = json.loads(response.content)
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            return {"error": True,
                    "exe": e,
                    "msg": f"No access - {url}",
                    "file_path": None,
                    # "response_text": response.text,
                    "status_code": response.status_code}

        return {"error": False,
                "msg": f"File save to - {file_path}",
                "file_path": file_path,
                # "response_text": None,
                "status_code": response.status_code
                }
