import logging
import requests
import hashlib
import datetime
import base64
import aiohttp

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

from os.path import join, dirname, abspath, basename, exists
from os import makedirs
from .types import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLakeSDK:
    # def __init__(self, url="https://aidc-us.anker-in.com/api"):
    def __init__(self, url="https://aidc-dev.anker-in.com/api"):
        self.url = url
        self.logger = logging.getLogger(__name__)

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()

    def _get_file_meta(self, file_path: str) -> FileMeta:
        """获取文件的宽度和高度，如果是视频，还返回时长"""
        try:
            # Check if the file is an image or video based on the file extension
            supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.mkv')
            if not file_path.lower().endswith(supported_extensions):
                print(f"Non video or image file for _get_file_meta")
                return FileMeta(resolution=Resolution(width=0, height=0), tokenLength=0, duration=0)

            # Use hachoir to parse the file
            parser = createParser(file_path)
            if not parser:
                raise ValueError(f"Unable to parse file {file_path}")
            metadata = extractMetadata(parser)
            if not metadata:
                raise ValueError(f"Unable to extract metadata from file {file_path}")

            # Extract width and height
            width = metadata.get("width")
            height = metadata.get("height")
            if width is None or height is None:
                print(f"File {file_path} has no width and height")

            resolution = Resolution(width=width, height=height)

            # Extract duration if available
            duration = metadata.get("duration").seconds if metadata.has("duration") else 0
            if duration is None:
                print(f"File {file_path} has no duration")

            return FileMeta(resolution=resolution, tokenLength=0, duration=duration)
        except Exception as e:
            # If it fails, return a default FileMeta and log the error
            print(f"Error reading file {file_path}: {e}")
            return None

    def _upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        # get upload url
        try:
            url = f"{self.url}/lakeapi/data/sync/getUploadLink"
            file_name = basename(file_path)
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
                # 'Authorization': f'Bearer {self.token}'  # Use the token dynamically
            }
            if not directory:
                directory = datetime.datetime.now().strftime("%Y-%m-%d")

            data = {
                "fileName": file_name,
                "directory": directory
            }
            object_name = f"{directory}/{file_name}"
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Check for HTTP errors
            response = response.json()
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            print(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
        except Exception as e:
            print(f"An error occurred while getting upload URL: {e}")
            raise Exception(f"An error occurred while getting upload URL: {e}")

        # upload file by url
        try:
            upload_url = response.get("data")  # Get the upload URL from the response
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # Calculate the file's MD5
            file_meta = self._get_file_meta(file_path)  # Get the file's metadata
            # Then put to this path
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # Check for HTTP errors
                return UploadFileResponse(
                    url=upload_url,
                    object_name=object_name,
                    uid=file_md5,
                    meta=file_meta
                )
        except requests.exceptions.RequestException as e:
            detail = None
            if res is not None:
                try:
                    detail = res.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading file: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")

    async def async_upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        # get upload url
        try:
            url = f"{self.url}/lakeapi/data/sync/getUploadLink"
            file_name = basename(file_path)
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            if not directory:
                directory = datetime.datetime.now().strftime("%Y-%m-%d")

            data = {
                "fileName": file_name,
                "directory": directory
            }
            object_name = f"{directory}/{file_name}"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
        except aiohttp.ClientError as e:
            detail = None
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            print(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
        except Exception as e:
            print(f"An error occurred while getting upload URL: {e}")
            raise Exception(f"An error occurred while getting upload URL: {e}")

        # upload file by url
        try:
            upload_url = response_json.get("data")  # Get the upload URL from the response
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # Calculate the file's MD5
            file_meta = self._get_file_meta(file_path)  # Get the file's metadata
            # Then put to this path
            async with aiohttp.ClientSession() as session:
                async with session.put(upload_url, data=open(file_path, "rb")) as res:
                    res.raise_for_status()
                    return UploadFileResponse(
                        url=upload_url,
                        object_name=object_name,
                        uid=file_md5,
                        meta=file_meta
                    )
        except aiohttp.ClientError as e:
            detail = None
            if res is not None:
                try:
                    detail = await res.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading file: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")


    def _upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/lakeapi/data/sync"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'            
            }
            print(f"upload raw_data: {raw_data}")
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response_json = response.json()
            if response_json.get("ok") is not True:
                print(f"Failed to upload raw data: {response_json.get('msg', 'No detail provided')}")
            return UploadRawDataResponse(
                raw_data_id=raw_data.get("uid", "")
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading raw data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")

    async def async_upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/lakeapi/data/sync"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'            
            }
            print(f"upload raw_data: {raw_data}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=raw_data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    if response_json.get("ok") is not True:
                        print(f"Failed to upload raw data: {response_json.get('msg', 'No detail provided')}")
                    return UploadRawDataResponse(
                        raw_data_id=raw_data.get("uid", "")
                    )
        except aiohttp.ClientError as e:
            detail = None
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading raw data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")


    def upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadFileWithInfoResponse:
        try:
            # 上传文件
            upload_file_response = self._upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name}

            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "personal-data"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0 if raw_data.get('meta') is not None else 1

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            if raw_data.get("category") is None:
                if raw_data.get("bg") == "Appliances":
                    raw_data["category"] = "clean"
                elif raw_data.get("bg") == "ZhixinSmartIOT":
                    raw_data["category"] = "security"
                else:
                    raw_data["category"] = "anker"

            upload_info_response = self._upload_raw_data(raw_data)
            return UploadFileWithInfoResponse(
                url=upload_file_response.url,
                object_name=upload_file_response.object_name,
                uid=upload_file_response.uid,
                raw_data_id=upload_info_response.raw_data_id,
                meta=upload_file_response.meta
            )
            # print(f"Raw data uploaded with file: {raw_data}")
            # return upload_info_response
        except requests.exceptions.RequestException as e:
            detail = None
            if e.response is not None:
                try:
                    detail = e.response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading data with info: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {str(e)}")

    async def async_upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadFileWithInfoResponse:
        try:
            # 上传文件
            upload_file_response = await self.async_upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name}

            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "personal-data"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0 if raw_data.get('meta') is not None else 1

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            if raw_data.get("category") is None:
                if raw_data.get("bg") == "Appliances":
                    raw_data["category"] = "clean"
                elif raw_data.get("bg") == "ZhixinSmartIOT":
                    raw_data["category"] = "security"
                else:
                    raw_data["category"] = "anker"

            upload_info_response = await self.async_upload_raw_data(raw_data)
            return UploadFileWithInfoResponse(
                url=upload_file_response.url,
                object_name=upload_file_response.object_name,
                uid=upload_file_response.uid,
                raw_data_id=upload_info_response.raw_data_id,
                meta=upload_file_response.meta
            )
        except aiohttp.ClientError as e:
            detail = None
            if e.response is not None:
                try:
                    detail = await e.response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading data with info: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {str(e)}")


    def upload_annotated_data(self, annotated_data: dict, version: str = None) -> UploadAnnotationDataResponse:
        try:
            url = f"{self.url}/lakeapi/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'            
            }
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
            # print(f"annotation response: {response_json}")

            if response_json.get("ok") is True and response_json.get("data") is not None and len(response_json.get("data")) > 0:
                annotation_data_id = response_json.get("data")[0]
            else:
                raise Exception(f"Failed to upload annotated data: {response_json.get('msg', 'No detail provided')}")

            if version is not None:
                if annotation_data_id is not None:
                    self._link_to_annotation_version(annotation_data_id, version)
                else:
                    raise Exception("Failed to link {annotation_data_id} to {version}: {}")

            return UploadAnnotationDataResponse(annotation_data_id=annotation_data_id)
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading annotated data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")

    async def async_upload_annotated_data(self, annotated_data: dict, version: str = None) -> UploadAnnotationDataResponse:
        try:
            url = f"{self.url}/lakeapi/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'            
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=annotated_data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    if response_json.get("ok") is True and response_json.get("data") is not None and len(response_json.get("data")) > 0:
                        annotation_data_id = response_json.get("data")[0]
                    else:
                        raise Exception(f"Failed to upload annotated data: {response_json.get('msg', 'No detail provided')}")

                    if version is not None:
                        if annotation_data_id is not None:
                            await self.async_link_to_annotation_version(annotation_data_id, version)
                        else:
                            raise Exception("Failed to link {annotation_data_id} to {version}: {}")

                    return UploadAnnotationDataResponse(annotation_data_id=annotation_data_id)
        except aiohttp.ClientError as e:
            detail = None
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading annotated data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")


    def _link_to_annotation_version(self, annotation_data_id: str, version: str):
        try:
            url = f"{self.url}/lakeapi/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'            
            }
            link_data = {
                "annotationVersionId": version,
                "annotationIds": [
                    annotation_data_id
                ]
            }
            response = requests.post(url, headers=headers, json=link_data)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
            if response_json.get("ok") is True:
                return True
            else:
                raise Exception(f"Failed to link {annotation_data_id} to {version}: {response_json.get('msg', 'No detail provided')}")
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while linking to annotation version: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking to annotation version: {e}")

    async def async_link_to_annotation_version(self, annotation_data_id: str, version: str):
        try:
            url = f"{self.url}/lakeapi/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'            
            }
            link_data = {
                "annotationVersionId": version,
                "annotationIds": [
                    annotation_data_id
                ]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=link_data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    if response_json.get("ok") is True:
                        return True
                    else:
                        raise Exception(f"Failed to link {annotation_data_id} to {version}: {response_json.get('msg', 'No detail provided')}")
        except aiohttp.ClientError as e:
            detail = None
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while linking to annotation version: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking to annotation version: {e}")


    def query_origin_data(self, query_origin_data: dict) -> dict:
        try:
            url = f"{self.url}/lakeapi/data/sync/queryOriginData"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=query_origin_data)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
            return response_json
        except requests.exceptions.RequestException as e:
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
                raise Exception(f"HTTP error occurred while querying origin data: {detail or str(e)}")
            else:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")

    async def async_query_origin_data(self, query_origin_data: dict) -> dict:
        try:
            url = f"{self.url}/lakeapi/data/sync/queryOriginData"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=query_origin_data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    return response_json
        except aiohttp.ClientError as e:
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
                raise Exception(f"HTTP error occurred while querying origin data: {detail or str(e)}")
            else:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")


    def query_annotation_data(self, query_annotation_data: dict) -> dict:
        try:
            url = f"{self.url}/lakeapi/data/annotation/query"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=query_annotation_data)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
            return response_json
        except requests.exceptions.RequestException as e:
            if response is not None:
                try:
                    detail = response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
                raise Exception(f"HTTP error occurred while querying annotation data: {detail or str(e)}")
            else:
                raise Exception(f"HTTP error occurred while querying annotation data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying annotation data: {e}")

    async def async_query_annotation_data(self, query_annotation_data: dict) -> dict:
        try:
            url = f"{self.url}/lakeapi/data/annotation/query"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=query_annotation_data) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    return response_json
        except aiohttp.ClientError as e:
            if response is not None:
                try:
                    detail = await response.json().get("msg", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
                raise Exception(f"HTTP error occurred while querying annotation data: {detail or str(e)}")
            else:
                raise Exception(f"HTTP error occurred while querying annotation data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying annotation data: {e}")


    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            url = f"{self.url}/lakeapi/data/sync/getLakeDownloadLink"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            params = {
                "uid": uid
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        if response_json is None:
            raise Exception("No response received from the server.")

        try:
            is_ok = response_json.get("ok")
            if not is_ok:
                raise Exception(f"Failed to get download URL: {response_json.get('msg', 'No detail provided')}")
            download_url = response_json.get("data")  # Get the download URL from the response
            if not download_url:
                raise Exception("No download URL found in the response.")

            response = requests.get(download_url)
            response.raise_for_status()  # Check for HTTP errors
            if response is None:
                raise Exception("No response received from the download URL.")

            # Save to local
            save_path = join(directory, uid)
            # Check if directory exists
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")

    async def async_download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            url = f"{self.url}/lakeapi/data/sync/getLakeDownloadLink"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            params = {
                "uid": uid
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    response_json = await response.json()
        except aiohttp.ClientError as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        if response_json is None:
            raise Exception("No response received from the server.")

        try:
            is_ok = response_json.get("ok")
            if not is_ok:
                raise Exception(f"Failed to get download URL: {response_json.get('msg', 'No detail provided')}")
            download_url = response_json.get("data")  # Get the download URL from the response
            if not download_url:
                raise Exception("No download URL found in the response.")

            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    response.raise_for_status()
                    if response is None:
                        raise Exception("No response received from the download URL.")

                    # Save to local
                    save_path = join(directory, uid)
                    # Check if directory exists
                    if not exists(dirname(save_path)):
                        makedirs(dirname(save_path))
                    with open(save_path, "wb") as f:
                        f.write(await response.read())
                    return save_path
        except aiohttp.ClientError as e:
            raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")


    def get_imagebase64_by_uid(self, uid: str, bg_confirm: str=None) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self.query_origin_data(query_origin_data)
        except Exception as e:
            print(f"Failed to query origin data: {e}")
            raise Exception(f"Failed to query origin data: {e}")

        try:
            if origin_data is None or origin_data.get('data') is None:
                raise Exception("No origin data found for the given UID.")
            data = origin_data.get('data')
            records = data.get("records") if data is not None else None

            if records is None or len(records) == 0:
                raise Exception("No origin data found for the given UID.")

            record = records[0]
            get_uid = record.get("uid") if record is not None else None
            file_type = record.get("type") if record is not None else None
            bg = record.get("bg") if record is not None else None

            if get_uid is None or get_uid != uid:
                raise Exception("UID mismatch.")

            if file_type is None or file_type != "image":
                raise Exception("The file is not an image.")

            if bg_confirm is not None:
                if bg is None or bg != bg_confirm:
                    raise Exception(f"The file bg {bg} is not matched with bg_confirm {bg_confirm}.")

            storage = record.get("storage")
            object_name = storage.get("objectName") if storage is not None else None
            if object_name is None:
                raise Exception("Missing object_name in origin data.")
        except Exception as e:
            print(f"Error occurred while processing origin data: {e}")
            raise Exception(f"Error occurred while processing origin data: {e}")

        try:
            url = f"{self.url}/lakeapi/data/sync/getLakeDownloadLink"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            params = {
                "uid": uid
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Check for HTTP errors
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred while getting download URL: {e}")
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            print(f"An error occurred while getting download URL: {e}")
            raise Exception(f"An error occurred while getting download URL: {e}")

        if response_json is None:
            raise Exception("No response received from the server.")

        try:
            is_ok = response_json.get("ok")
            if not is_ok:
                raise Exception(f"Failed to get download URL: {response_json.get('msg', 'No detail provided')}")
            download_url = response_json.get("data")  # Get the download URL from the response
            if not download_url:
                raise Exception("No download URL found in the response.")

            response = requests.get(download_url)
            response.raise_for_status()  # Check for HTTP errors
            if response is None:
                raise Exception("No response received from the download URL.")

            # Encode the file content to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred while downloading file: {e}")
            raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            print(f"An error occurred while downloading file: {e}")
            raise Exception(f"An error occurred while downloading file: {e}")

    async def async_get_imagebase64_by_uid(self, uid: str, bg_confirm: str=None) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = await self.async_query_origin_data(query_origin_data)
        except Exception as e:
            print(f"Failed to query origin data: {e}")
            raise Exception(f"Failed to query origin data: {e}")

        try:
            if origin_data is None or origin_data.get('data') is None:
                raise Exception("No origin data found for the given UID.")
            data = origin_data.get('data')
            records = data.get("records") if data is not None else None

            if records is None or len(records) == 0:
                raise Exception("No origin data found for the given UID.")

            record = records[0]
            get_uid = record.get("uid") if record is not None else None
            file_type = record.get("type") if record is not None else None
            bg = record.get("bg") if record is not None else None

            if get_uid is None or get_uid != uid:
                raise Exception("UID mismatch.")

            if file_type is None or file_type != "image":
                raise Exception("The file is not an image.")

            if bg_confirm is not None:
                if bg is None or bg != bg_confirm:
                    raise Exception(f"The file bg {bg} is not matched with bg_confirm {bg_confirm}.")

            storage = record.get("storage")
            object_name = storage.get("objectName") if storage is not None else None
            if object_name is None:
                raise Exception("Missing object_name in origin data.")
        except Exception as e:
            print(f"Error occurred while processing origin data: {e}")
            raise Exception(f"Error occurred while processing origin data: {e}")

        try:
            url = f"{self.url}/lakeapi/data/sync/getLakeDownloadLink"
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
            }
            params = {
                "uid": uid
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    response_json = await response.json()
        except aiohttp.ClientError as e:
            print(f"HTTP error occurred while getting download URL: {e}")
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            print(f"An error occurred while getting download URL: {e}")
            raise Exception(f"An error occurred while getting download URL: {e}")

        if response_json is None:
            raise Exception("No response received from the server.")

        try:
            is_ok = response_json.get("ok")
            if not is_ok:
                raise Exception(f"Failed to get download URL: {response_json.get('msg', 'No detail provided')}")
            download_url = response_json.get("data")  # Get the download URL from the response
            if not download_url:
                raise Exception("No download URL found in the response.")

            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    response.raise_for_status()
                    if response is None:
                        raise Exception("No response received from the download URL.")

                    # Encode the file content to base64
                    image_base64 = base64.b64encode(await response.read()).decode('utf-8')
                    return image_base64
        except aiohttp.ClientError as e:
            print(f"HTTP error occurred while downloading file: {e}")
            raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            print(f"An error occurred while downloading file: {e}")
            raise Exception(f"An error occurred while downloading file: {e}")