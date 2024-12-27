import asyncio
import base64
import json
import logging
import os

import requests
import websockets
from websockets.exceptions import ConnectionClosedError

from ai_cloud_sdk_4pd import models as ai_cloud_sdk_4pd_models


class Client:
    def __init__(
        self,
        config: ai_cloud_sdk_4pd_models.Config,
    ):
        self._token = config.token
        self._call_token = config.call_token
        # self._endpoint = config.endpoint
        self._region = config.region
        self._http_endpoint = None
        self._websocket_endpoint = None
        self.blacklist_token = []
        self.blacklist_call_token = []

        # asr websocket
        self._ws_asr = None

        # 设置region和endpoint
        self._http_endpoint_map = {
            'China': 'http://172.26.1.45:8202',
            # 'China': 'localhost:8090/ai/cpp/api',
            'HongKong': 'https://Hongkong.com',
            'Other': 'https://Other.com',
        }
        self._websocket_endpoint_map = {
            'China': 'ws://172.26.1.45:8090',
            # 'China': 'ws://localhost:8090',
            # 'HongKong': 'https://Hongkong.com',
            # 'Other': 'https://Other.com',
        }
        self.__set_region_and_endpoint()
        self.__verify_tokens()

    def __set_region_and_endpoint(self) -> None:
        # 如果endpoint已给出且合法，则直接返回
        # if self._endpoint and self._endpoint in self._endpoint_map.values():
        #     self._region = [
        #         k for k, v in self._endpoint_map.items() if v == self._endpoint
        #     ][0]
        #     return

        # 如果endpoint未给出或不合法，且region存在且合法，则根据region确定endpoint
        if (
            self._region
            and self._region in self._http_endpoint_map.keys()
            and self._region in self._websocket_endpoint_map.keys()
        ):
            self._http_endpoint = self._http_endpoint_map[self._region]
            self._websocket_endpoint = self._websocket_endpoint_map[self._region]
            return

        # 如果endpoint未给出或不合法，且region不存在或不合法，则默认endpoint(China)
        self._region = 'China'
        self._http_endpoint = self._http_endpoint_map[self._region]
        self._websocket_endpoint = self._websocket_endpoint_map[self._region]
        return

    def __verify_tokens(self) -> None:
        # 如果token或call_token未给出，则抛出异常
        if self._token is None or self._call_token is None:
            raise ValueError('token and call_token is required')

    def audio_language_detection(
        self,
        request: ai_cloud_sdk_4pd_models.BaseRequest = None,
    ) -> ai_cloud_sdk_4pd_models.BaseResponse:

        # 如果token或call_token在黑名单中，则抛出异常
        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f'{self._http_endpoint}{request.api}'
        headers = {
            'token': self._token,
            'call_token': self._call_token,
            'content-type': request.content_type,
        }

        headers = {
            'token': self._token,
            'call_token': self._call_token,
        }
        payload = request.payload
        file_url = payload.get('audio')
        metadata = payload.get('metadata')
        choices = payload.get('choices')
        files = {'audio': (file_url, open(file_url, 'rb'))}
        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data={'metadata': metadata, 'choices': choices},
            files=files,
        )

        # 如果返回码为503，则将token和call_token加入黑名单
        if response.json().get('code', None) == 503:
            self.blacklist_token.append(self._token)
            self.blacklist_call_token.append(self._call_token)
            raise ValueError('token or call_token is invalid')

        return ai_cloud_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )

    async def asr(
        self,
        request: ai_cloud_sdk_4pd_models.ASRRequest = None,
        on_ready: callable = None,
        on_response: callable = None,
        on_completed: callable = None,
    ) -> None:

        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f"{self._websocket_endpoint}{request.api}"
        headers = {
            'token': self._token,
            'call_token': self._call_token,
        }
        # 设置 ping 的超时时间和 ping 的间隔
        ping_timeout = 120  # 秒
        ping_interval = 5  # 秒
        close_timeout = 60  # 当尝试关闭连接时，等待关闭帧的最长时间（秒）
        if self._ws_asr is None:
            self._ws_asr = await websockets.connect(
                full_url,
                extra_headers=headers,
                ping_timeout=ping_timeout,
                ping_interval=ping_interval,
                close_timeout=close_timeout,
            )
        if not self._ws_asr.open:
            self._ws_asr = await websockets.connect(
                full_url,
                extra_headers=headers,
                ping_timeout=ping_timeout,
                ping_interval=ping_interval,
                close_timeout=close_timeout,
            )
        #  把wav文件进行base64编码
        file_url = request.audio_url
        try:
            with open(file_url, 'rb') as f:
                audio_data = f.read()
                audio_base64 = base64.b64encode(audio_data)
                audio_base64 = audio_base64.decode('utf-8')
        except FileNotFoundError:
            raise ValueError('File not found. Please check the path and try again.')

        # 发送音频数据
        message = {
            "enableWords": True,
            "lang": request.language,
            "waitTime": 5,
            "chunkSize": 1024,
            "fileBase64": audio_base64,
            "finalResult": 'true' if request.final_result else 'false',
        }

        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')
        await self._ws_asr.send(json.dumps(message))

        # 4. 接收返回数据
        try:
            flag = False
            while self._ws_asr.open:
                if (
                    self._token in self.blacklist_token
                    or self._call_token in self.blacklist_call_token
                ):
                    raise ValueError('token or call_token is forbidden to send request')

                try:
                    if flag:
                        recv_data = await asyncio.wait_for(
                            self._ws_asr.recv(), timeout=50
                        )
                    else:
                        recv_data = await self._ws_asr.recv()
                except asyncio.TimeoutError:
                    await on_completed()
                    logging.info('service completed with timeout')
                    break

                if isinstance(recv_data, str):
                    recv_data = str(recv_data)
                    recv_data = json.loads(recv_data)

                    if recv_data.get('success', False):
                        await on_ready()
                        flag = True
                        continue

                    if recv_data.get('code', None) == 503:
                        self.blacklist_token.append(self._token)
                        self.blacklist_call_token.append(self._call_token)
                        raise ValueError('token or call_token is invalid')

                    if recv_data.get('end', False):
                        await on_completed()
                        break

                    await on_response(recv_data)

                else:
                    raise Exception("Received data is not str")
        except ConnectionClosedError as e:
            logging.error('ConnectionClosedError')
            # raise e
        except Exception as e:
            raise e
        logging.info('service completed')

    def translate_text(
        self,
        request: ai_cloud_sdk_4pd_models.BaseRequest = None,
    ) -> ai_cloud_sdk_4pd_models.BaseResponse:

        # 如果token或call_token在黑名单中，则抛出异常
        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f'{self._http_endpoint}{request.api}'
        headers = {
            'token': self._token,
            'call_token': self._call_token,
            'content-type': request.content_type,
        }

        payload = request.payload

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        # 如果返回码为503，则将token和call_token加入黑名单
        if response.json().get('code', None) == 503:
            self.blacklist_token.append(self._token)
            self.blacklist_call_token.append(self._call_token)
            raise ValueError('token or call_token is invalid')

        return ai_cloud_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )

    def tts(
        self,
        request: ai_cloud_sdk_4pd_models.BaseRequest = None,
    ):

        # 如果token或call_token在黑名单中，则抛出异常
        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f'{self._http_endpoint}{request.api}'
        headers = {
            'token': self._token,
            'call_token': self._call_token,
            'content-type': request.content_type,
        }

        payload = request.payload

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        return response
        #
        # # 如果返回码为503，则将token和call_token加入黑名单
        # if response.json().get('code', None) == 503:
        #     self.blacklist_token.append(self._token)
        #     self.blacklist_call_token.append(self._call_token)
        #     raise ValueError('token or call_token is invalid')
        #
        # return ai_cloud_sdk_4pd_models.BaseResponse(
        #     code=response.json().get('code', None),
        #     data=response.json().get('data', None),
        #     message=response.json().get('message', None),
        # )

    async def asr_batch(
        self,
        request: ai_cloud_sdk_4pd_models.ASRRequest = None,
        on_ready: callable = None,
        on_response: callable = None,
        on_completed: callable = None,
    ) -> None:

        if (
            self._token in self.blacklist_token
            or self._call_token in self.blacklist_call_token
        ):
            raise ValueError('token or call_token is forbidden to send request')

        full_url = f"{self._websocket_endpoint}{request.api}"
        headers = {
            'token': self._token,
            'call_token': self._call_token,
        }

        directory_path = request.batch_directory
        if not directory_path:
            raise ValueError('batch_directory is required')

        # 设置 ping 的超时时间和 ping 的间隔
        ping_timeout = 120  # 秒
        ping_interval = 5  # 秒
        close_timeout = 60  # 当尝试关闭连接时，等待关闭帧的最长时间（秒）
        if self._ws_asr is None:
            self._ws_asr = await websockets.connect(
                full_url,
                extra_headers=headers,
                ping_timeout=ping_timeout,
                ping_interval=ping_interval,
                close_timeout=close_timeout,
            )
        if not self._ws_asr.open:
            self._ws_asr = await websockets.connect(
                full_url,
                extra_headers=headers,
                ping_timeout=ping_timeout,
                ping_interval=ping_interval,
                close_timeout=close_timeout,
            )

        # 读取目录下的所有文件，筛选出wav文件
        files = os.listdir(directory_path)
        wav_files = []
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(file)

        # 把wav文件进行base64编码
        for file in wav_files:
            file_url = os.path.join(directory_path, file)

            try:
                with open(file_url, 'rb') as f:
                    audio_data = f.read()
                    audio_base64 = base64.b64encode(audio_data)
                    audio_base64 = audio_base64.decode('utf-8')
            except FileNotFoundError:
                raise ValueError('File not found. Please check the path and try again.')

            # 发送音频数据
            message = {
                "enableWords": True,
                "lang": request.language,
                "waitTime": 5,
                "chunkSize": 1024,
                "fileBase64": audio_base64,
            }

            if (
                self._token in self.blacklist_token
                or self._call_token in self.blacklist_call_token
            ):
                raise ValueError('token or call_token is forbidden to send request')
            await self._ws_asr.send(json.dumps(message))

            # 4. 接收返回数据
            try:
                flag = False
                while self._ws_asr.open:
                    if (
                        self._token in self.blacklist_token
                        or self._call_token in self.blacklist_call_token
                    ):
                        raise ValueError(
                            'token or call_token is forbidden to send request'
                        )
                    try:
                        if flag:
                            recv_data = await asyncio.wait_for(
                                self._ws_asr.recv(), timeout=4
                            )
                        else:
                            recv_data = await self._ws_asr.recv()
                    except asyncio.TimeoutError:
                        await on_completed(file_url)
                        logging.info('service completed with timeout')
                        break

                    if isinstance(recv_data, str):
                        recv_data = str(recv_data)
                        recv_data = json.loads(recv_data)

                        if recv_data.get('success', False):
                            await on_ready(file_url)
                            flag = True
                            continue

                        if recv_data.get('code', None) == 503:
                            self.blacklist_token.append(self._token)
                            self.blacklist_call_token.append(self._call_token)
                            raise ValueError('token or call_token is invalid')

                        if recv_data.get('end', False):
                            await on_completed(file_url)
                            break

                        await on_response(file_url, recv_data)

                    else:
                        raise Exception("Received data is not str")
            except ConnectionClosedError as e:
                logging.error('ConnectionClosedError')
                # raise e
            except Exception as e:
                raise e
            logging.info('service completed')
