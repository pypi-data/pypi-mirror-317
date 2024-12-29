from requests import request
import json
from pathlib import Path
from enum import Enum
from loguru import logger
import re


class Business(Enum):
    """
    reply - 评论区
    dynamic - 动态
    """

    REPLY = 0
    DYNAMIC = 1


class Emoji:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    def __init__(
        self,
        proxies: dict = {},
        business: Business = Business.REPLY,
        cookie: str = "",
    ) -> None:
        """_summary_

        Args:
            proxies (dict): 代理
            business (Business, optional): _description_. REPLY或者DYNAMIC.
            cookie (str, optional): _description_. 登录信息，默认为"".
        """
        self.__get_all_url = "https://api.bilibili.com/x/emote/setting/panel"
        self.__get_certain_url = "https://api.bilibili.com/x/emote/package"
        self.business: Business = business
        self.proxies = proxies
        self.header: dict = {}
        self.cookie = cookie
        self.set_header()

    def set_header(self):
        """设置请求头"""
        if self.cookie == "":
            self.header = {"user-agent": self.user_agent}
        else:
            self.header = {"user-agent": self.user_agent, "cookie": self.cookie}

        logger.success(f"self.header: {self.header}")

    def certain_emoji(
        self,
        ids: int,
    ) -> dict:
        """获取特定表情包信息

        Args:
            ids (int): 表情包ID（必须）

        Returns:
            dict: 响应数据
        """
        response = request(
            "GET",
            self.__get_certain_url,
            headers=self.header,
            # proxies=self.proxies,
            params={"business": self.business.name.upper(), "ids": ids},
        )

        logger.info(f"id:{ids} get success")
        return response.json()

    def all_emoji(self, cookie: str) -> dict:
        """_summary_

        Args:
            cookie (str): 登录状态（必须）

        Returns:
            dict: 响应数据
        """

        if cookie == "":
            raise ValueError("cookie为空不合法")

        if "cookie" not in self.header:
            self.header["cookie"] = cookie
            print(f"header upper:{self.header}")

        response = request(
            "GET",
            self.__get_all_url,
            headers=self.header,
            params={"business": self.business.name.lower()},
        )

        logger.info(f"all emoji get success")
        return response.json()

    def save_json(self, data: dict, path: Path) -> None:
        """保存json数据到特定的路径

        Args:
            data (dict): 响应数据
            path (Path): 保存路径 特定emoji请写入文件夹名 全部emoji请直接给出文件名
        """

        if path.is_dir() == True:
            if not path.exists():
                path.mkdir()
            logger.warning(f"{path} is created")

            # 替换可能的非法字符做文件名
            emoji_name = self.sanitize_filename(data["data"]["packages"][0]["text"])
            save_name = Path.joinpath(path, emoji_name + ".json")

            with open(save_name, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))

            logger.success(f"{emoji_name} is saved in {save_name}")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def sanitize_filename(self, filename: str) -> str:
        """将文件名中的非法字符换为_

        Args:
            filename (str): 文件名

        Returns:
            str: 替换后的文件名
        """
        # 定义Windows不允许的字符
        invalid_chars = r'[<>:"/\\|?*，。！？]'
        # 使用下划线替换非法字符
        sanitized_filename = re.sub(invalid_chars, " ", filename)
        return sanitized_filename