from factory_sdk.datasets import Datasets
from factory_sdk.models import Models
from factory_sdk.adapters import Adapters
from factory_sdk.metrics import Metrics
from factory_sdk.preprocessors import Preprocessors
import requests
from pydantic import BaseModel
from factory_sdk.logging import logger
from typing import Optional, Type, Any
import os
from factory_sdk.exceptions.api import NotFoundException,GeneralAPIException,ConflictException,AuthenticationException
from factory_sdk.dto_old.state import FactoryState
import time
from rich import print

# Import tqdm for progress bar
from tqdm.auto import tqdm

# Optional: If you can install external libraries
try:
    from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
except ImportError:
    MultipartEncoder = None
    MultipartEncoderMonitor = None

class FactoryClient:
    def __init__(self,tenant:str, project: str, token:str, host: str="localhost", port: int = 8080, ssl: bool = False):
        """
        Initialize the FactoryClient with project, host, port, and SSL settings.
        """
        self._tenant=tenant
        self._project = project
        self._host = host
        self._port = port
        self._ssl = ssl
        self._token=token
        self.datasets = Datasets(client=self)
        self.models = Models(client=self)
        self.adapters = Adapters(client=self)
        self.metrics = Metrics(client=self)
        self.preprocessors = Preprocessors(client=self)
        self._session = requests.Session()  # Use a session for performance and connection pooling7

        #print sucessuffly connetced
        print(f"🛸FactoryClient is successfully connected and starts working on project [bold blue]{project}[/bold blue]\n")
    @property
    def _api_url(self) -> str:
        """
        Construct the base API URL based on the host, port, SSL, and project.
        """
        protocol = 'https' if self._ssl else 'http'
        return f"{protocol}://{self._host}:{self._port}/api/1/{self._tenant}/projects/{self._project}"

    def _request(self, method: str, path: str, **kwargs) -> Any:
        """
        Internal method to handle HTTP requests.

        Args:
            method (str): HTTP method ('GET', 'POST', 'PUT', etc.).
            path (str): API endpoint path.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Any: The response JSON or content.
        """
        url = f"{self._api_url}/{path}"
        res = self._session.request(method, url,headers={
            "Authorization":f"Bearer {self._token}"
        },**kwargs)

        if res.status_code == 404:
            raise NotFoundException(f"Resource not found: {method} {path}")
        elif res.status_code == 409:
            raise ConflictException(f"Conflict: {method} {path}")
        elif res.status_code == 401:
            raise AuthenticationException(f"Authentication failed: {method} {path}")
        if res.status_code != 200 and res.status_code != 201:
            try:
                error_msg = res.json()
                logger.error(error_msg)
                raise GeneralAPIException(error_msg)
            except ValueError:
               raise GeneralAPIException(f"Failed to {method} {path}. Status code: {res.status_code}")

        try:
            return res.json()
        except ValueError:
            return res.content  # Return raw content if response is not JSON
        
    def wait(self, path: str, timeout=360) -> None:
        start=time.time()
        while time.time()-start<timeout:
            url=f"{self._api_url}/{path}"
            res=self._session.get(url,headers={
                "Authorization":f"Bearer {self._token}"
            })
            if res.status_code==200:
                return
            elif res.status_code==408:
                time.sleep(1)
            else:
                raise GeneralAPIException(res.text)
                #raise GeneralAPIException(f"Failed to wait for {path}. Status code: {res.status_code}")
        raise Exception(f"Timeout waiting for {path}")

    def get(self, path: str, response_class: Optional[Type[BaseModel]] = None) -> Any:
        """
        Perform a GET request to the specified path.

        Args:
            path (str): The API endpoint path.
            response_class (Type[BaseModel], optional): Pydantic model class to parse the response.

        Returns:
            Any: The parsed response or raw JSON.
        """
        res_json = self._request('GET', path)
        if response_class and res_json:
            return response_class(**res_json)
        return res_json

    def post(self, path: str, data: BaseModel, response_class: Optional[Type[BaseModel]] = None) -> Any:
        """
        Perform a POST request to the specified path with the provided data.

        Args:
            path (str): The API endpoint path.
            data (BaseModel): The data to send in the POST request.
            response_class (Type[BaseModel], optional): Pydantic model class to parse the response.

        Returns:
            Any: The parsed response or raw JSON.
        """
        res_json = self._request('POST', path, json=data.model_dump() if data else None)
        if response_class and res_json:
            return response_class(**res_json)
        return res_json
    
    def put(self, path: str, data: BaseModel, response_class: Optional[Type[BaseModel]] = None) -> Any:
        """
        Perform a PUT request to the specified path with the provided data.

        Args:
            path (str): The API endpoint path.
            data (BaseModel): The data to send in the PUT request.
            response_class (Type[BaseModel], optional): Pydantic model class to parse the response.

        Returns:
            Any: The parsed response or raw JSON.
        """
        res_json = self._request('PUT', path, json=data.model_dump())
        if response_class and res_json:
            return response_class(**res_json)
        return res_json


    def put_file(self, path: str, file,buffer_size=16*1024*1024) -> Any:
        
        with open(file,"rb") as f:
            stream=requests.put(
                f"{self._api_url}/{path}",
                headers={
                    "Authorization":f"Bearer {self._token}"
                },
                data=f,
                stream=True
            )

            if stream.status_code!=200:
                try:
                    error_msg = stream.json()
                except ValueError:
                    error_msg = stream.text
                logger.error(error_msg)
                raise Exception(f"Failed to PUT {path}. Status code: {stream.status_code}")

