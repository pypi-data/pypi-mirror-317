from requests import request
import json
from random import choice
from pathlib import Path
from loguru import logger
import re


class Dress:
    user_agent_pool = [
        # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.80",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.51",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.63",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.70",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.86",  # 2024.12
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.70 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.108 Safari/537.36",  # 2024.12
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.109 Safari/537.36",
        # Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",  # 2024.10
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",  # 2024.11
    ]
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    def __init__(self, proxies: dict = {}, cookie: str = "") -> None:
        """构造函数

        Args:
            proxies (dict, optional): _description_. 代理 默认为{}.
            cookie (str, optional): _description_. 登陆状态 默认为"".
        """
        self.__search_url = "https://api.bilibili.com/x/garb/v2/mall/home/search"
        self.__get_lottery_url = "https://api.bilibili.com/x/vas/dlc_act/act/basic"
        self.__get_certain_url = (
            "https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail"
        )
        self.proxies = proxies
        self.header: dict = {}
        self.cookie = cookie
        self.set_header()

    def set_header(self):
        """设置请求头"""
        if self.cookie == "":
            self.header = {"user-agent": choice(self.user_agent_pool)}
        else:
            self.header = {
                "user-agent": choice(self.user_agent_pool),
                "cookie": self.cookie,
            }

        logger.success(f"self.header: {self.header}")

    def search_dress(self, num: int, keyword: str = "") -> dict:
        """搜索装扮/收藏集信息

        Args:
            num (int): 需要展示的数量
            keyword (str, optional): 关键字. 默认是 "".

        Returns:
            dict: 响应数据
        """

        response = request(
            "GET",
            self.__search_url,
            headers=self.header,
            proxies=self.proxies,
            params={"key_word": keyword},
        )
        logger.info(f"keyword:{keyword} get success")

        self.show_head_info(num, response.json())
        return response.json()

    def show_head_info(self, num: int, data: dict) -> None:
        """展示前num个搜索结果

        Args:
            num(int): 展示结果的数量
            data (dict): 响应数据
        """
        for index, value in enumerate(data["data"]["list"]):
            if index == num:
                break
            print(f"NO.{index+1}:")
            print("name:    \t\t", value["name"])
            print("part_id:\t\t", value["part_id"])
            print("image_cover:\t\t", value["properties"]["image_cover"])
            if value["part_id"] == 0:
                print("dlc_act_id:\t\t", value["properties"]["dlc_act_id"])
                print("dlc_lottery_id:\t\t", value["properties"]["dlc_lottery_id"])
            print(
                "sale_bp_forever_raw:\t",
                float(value["properties"]["sale_bp_forever_raw"]) / 100,
            )
            print("--------------------")

    def certain_lottery(self, act_id: int, lottery_id: int) -> dict:
        """获取特定的收藏集信息

        Args:
            act_id (int): id1
            lottery_id (int): id2

        Returns:
            dict: 响应数据
        """
        response = request(
            "GET",
            self.__get_certain_url,
            headers=self.header,
            proxies=self.proxies,
            params={
                "act_id": act_id,
                "lottery_id": lottery_id,
            },
        )

        # print(response.json())
        logger.info(f"act_id:{act_id} get success")
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

            dress_name = data["data"]["name"]
            # 替换文件名中非法的部分
            dress_name = self.sanitize_filename(dress_name)
            save_name = Path.joinpath(path, dress_name + ".json")

            with open(save_name, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))

            logger.success(f"{dress_name} is saved in {save_name}")
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


