from inaSpeechSegmenter_api_models import (
    GetSegmentsResponse,
    GetSegmentsRequest,
)

import base64
import requests

class SegmenterClient:
    def __init__(
        self,
        api_url: str,
    ):
        self.api_url = api_url.strip("/")

    def get_segments(
        self,
        audio_file_name: str,
        audio_bytes: bytes,
    ) -> GetSegmentsResponse:
        audio_base64_bytes = base64.b64encode(audio_bytes)
        audio_base64_str = audio_base64_bytes.decode("utf-8")

        data = GetSegmentsRequest(
            filename=audio_file_name,
            audio_bytes_base64=audio_base64_str,
        )

        endpoint_url = f"{self.api_url}{GetSegmentsRequest.get_endpoint()}"

        response = requests.post(
            url=endpoint_url,
            json=data.model_dump(),
        )

        if response.status_code == 200:
            reponse_dict = response.json()
            return GetSegmentsResponse.model_validate(reponse_dict)
        else:
            raise Exception(f"Request to `{endpoint_url}` failed with status code {response.status_code}")
