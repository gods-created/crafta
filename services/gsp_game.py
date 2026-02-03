from typing import Tuple, Optional
from configs import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION_NAME,
    S3_BUCKET_NAME,
    RESOURCE_GAME_URL,
)
from os.path import join
from openai import (
    OpenAI, 
    APIStatusError, 
    ConflictError, 
    APIConnectionError, 
    RateLimitError,
    PermissionDeniedError,
    APIError
)
from uuid import uuid4
from boto3 import resource
from botocore.exceptions import HTTPClientError, ConnectionError, BotoCoreError

class GSPGameService:
    def __init__(self, *args, **kwargs):
        self._openai_api_key = OPENAI_API_KEY
        self._openai_model = OPENAI_MODEL
        self._aws_access_key_id = AWS_ACCESS_KEY_ID
        self._aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        self._aws_region_name = AWS_REGION_NAME
        self._s3_bucket_name = S3_BUCKET_NAME
        self._resource_game_url = RESOURCE_GAME_URL
        self._client = None 
        self._s3_resource = None
        self.input = (
            'SYSTEM MESSAGE:' \
            'This is a production environment.' \
            'Any text outside valid HTML will cause a system failure.' \
            'You are a code generator.' \
            'Your task is to create a fully working game.' \
            'STRICT RULES:' \
            '- Output ONLY raw code.' \
            '- Do NOT write explanations, comments, markdown, or text outside the code.' \
            '- Do NOT wrap the code in ``` or any formatting.' \
            '- The output must be a single valid HTML file.' \
            '- All CSS and JavaScript must be included inside this HTML file.' \
            '- The game must run immediately when opened in a browser.' \
            '- If you violate any rule, regenerate the response correctly.' \
            'GAME REQUIREMENTS:' \
            '{0}'
        )

    def __enter__(self):
        self._client = OpenAI(api_key=self._openai_api_key)
        self._s3_resource = resource(
            's3', 
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            region_name=self._aws_region_name
        )

        return self
    
    def publish(self, file_name: str) -> str:
        return join(self._resource_game_url, file_name) 
    
    def save(self, output_text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        status, err_description, file_name = False, None, None

        try:
            file_name = str(uuid4()) + '.html'
            self._s3_resource.Object(self._s3_bucket_name, file_name).put(Body=output_text)
            status = not status

        except (
            HTTPClientError, 
            ConnectionError, 
            BotoCoreError
        ) as e:
            err_description = f'{e.__class__.__name__}: {str(e)}'

        except Exception as e:
            err_description = f'FATAL ERROR: {str(e)}'

        return status, err_description, file_name

    def generate(self, prompt: str) -> Tuple[bool, Optional[str], Optional[str]]:
        status, err_description, output_text = False, None, None 

        try:
            result = self._client.responses.create(
                model=self._openai_model,
                input=self.input.format(prompt),
                reasoning={ 'effort': 'high' },
            )

            output_text = result.output_text
            status = not status

        except (
            APIStatusError, 
            ConflictError, 
            APIConnectionError, 
            RateLimitError, 
            PermissionDeniedError,
            APIError,
        ) as e:
            err_description = f'{e.__class__.__name__}: {str(e)}'

        except Exception as e:
            err_description = f'FATAL ERROR: {str(e)}'

        return status, err_description, output_text
    
    def __exit__(self, *args, **kwargs):
        if self._client:
            self._client.close()