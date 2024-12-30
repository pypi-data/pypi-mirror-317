# -*- coding:utf-8 -*-
import httpx
import os.path

from urllib.parse import unquote
from sandbox_func.common.request.CybotronClient import CybotronClient
from sandbox_func.common.lang.async_requests import AsyncRequests


class LTFileManager:
    """
    多维表文件相关接口
    """

    def __init__(self, app_code, table_code):
        self.app_code = app_code
        self.table_code = table_code
        self.client = CybotronClient()
        self.async_client = AsyncRequests()

    async def __send_request(self, url: str, data=None, files=None, json=None):
        """
        :param url: 接口地址
        :param data:
        :param files:
        :param json:
        :return: 接口返回的result
        """
        response = await self.client.post(url=url, data=data, files=files, json=json)
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]

    async def upload_table_file(self, data_id: str, column_code: str, file_path: str) -> dict:
        """
        上传多维表附件
        :param data_id: 数据id
        :param column_code: 列编码
        :param file_path: 文件路径
        :return:
        """
        # 读取文件内容
        with open(file_path, 'rb') as f:
            files = {"file": f}
            data = {
                "dataId": data_id,
                "columnCode": column_code
            }
            api_url = '/cbn/api/v1/file2/{}/{}/upload'.format(self.app_code, self.table_code)
            result = await self.__send_request(api_url, data=data, files=files)
            return result

    async def delete_table_file(self, data_id: str, column_code: str, file_id: str) -> dict:
        """
        删除多维表附件
        :param data_id: 数据id
        :param column_code: 列编码
        :param file_id: 文件id
        :return:
        """
        params_data = {
            "fileId": file_id,
            "dataId": data_id,
            "columnCode": column_code
        }
        api_url = '/cbn/api/v1/file2/{}/{}/delete'.format(self.app_code, self.table_code)
        result = await self.__send_request(api_url, json=params_data)
        return result

    async def upload_file(self, file_path: str) -> str:
        """
        上传文件
        :param file_path: 文件路径
        :return:
        """
        # 读取文件内容
        with open(file_path, 'rb') as f:
            files = {"file": f}
            result = await self.__send_request('/cbn/api/v1/file2/uploadTmp', files=files)
            return result['url']

    async def download_file(self, url, save_path) -> str:
        """
        下载文件
        :param url: 文件地址
        :param save_path: 本地存储路径
        :return:
        """
        try:
            req = self.async_client.build_request("GET", url, timeout=60.0)
            response = await self.async_client.send(req)
            response.raise_for_status()  # 检查是否成功响应
            save_path = os.path.join(save_path, unquote(url.split('/')[-1]))
            with open(save_path, "wb") as file:
                file.write(response.content)
            return save_path
        except httpx.RequestError as exc:
            raise Exception(f"文件下载请求失败: {exc}")
        except httpx.HTTPStatusError as exc:
            raise Exception(f"文件下载HTTP错误: {exc.response.status_code} - {exc.response.text}")