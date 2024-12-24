# coding: utf-8
"""
  Copyright (c) 2024 Vipas.AI
 
  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license which prohibits
  redistribution and use in any form, without the express prior written consent
  of Vipas.AI.
  
  This code is proprietary to Vipas.AI and is protected by copyright and
  other intellectual property laws. You may not modify, reproduce, perform,
  display, create derivative works from, repurpose, or distribute this code or any portion of it
  without the express prior written permission of Vipas.AI.
  
  For more information, contact Vipas.AI at legal@vipas.ai
"""  # noqa: E501

import os
import re
import pybreaker
import json
import asyncio
from typing import Tuple, Optional, List, Dict, Any
from pydantic import Field, StrictStr
from typing_extensions import Annotated
from ratelimit import limits, sleep_and_retry

from vipas.config import Config
from vipas import _rest
from vipas.logger import LoggerClient
from vipas.exceptions import ClientException,UnauthorizedException
from vipas.constant import ALLOWED_MODEL_FRAMEWORK_TYPES

RequestSerialized = Tuple[str, str, Dict[str, str], Optional[Any]]

class ModelClient:
    """
        Model client for Vipas API proxy service.
        :param config: Configuration object for this client
    """
    def __init__(self, configuration=None) -> None:
        # Every time a new client is created, we need to configure it
        if configuration is None:
            configuration = Config()
        self.configuration = configuration

        self.rest_client = _rest.RESTClientObject(configuration)
        self.logger_client = LoggerClient(__name__)
        self._configure_decorators()

    def _configure_decorators(self):
        vps_env_type = os.getenv('VPS_ENV_TYPE')
        if vps_env_type == 'vipas-streamlit':
            self.rate_limit = lambda func: func  # No-op decorator
            self.breaker = pybreaker.CircuitBreaker(fail_max=20, reset_timeout=60)  # 20 failures per minute
        else:
            self.breaker = pybreaker.CircuitBreaker(fail_max=10, reset_timeout=60)  # 10 failures per minute
            self.rate_limit = limits(calls=20, period=60)  # 20 calls per minute
        
        # Apply decorators dynamically for the predict method
        self.predict = self.breaker(self.predict)
        self.predict = self.rate_limit(self.predict)
        self.predict = sleep_and_retry(self.predict)

    def predict(
        self,
        model_id: Annotated[StrictStr, Field(description="Unique identifier for the model from which the prediction is requested")],
        input_data: Annotated[Any, Field(description="Input for the prediction")],
        async_mode: Annotated[bool, Field(description="Indicates whether the SDK operates in asynchronous mode or not.")] = True
    ) -> dict:
        """
            Get Model Prediction

            Retrieves predictions from a specified model based on the provided input data. This endpoint is useful for generating real-time predictions from machine learning models.

            :param model_id: Unique identifier for the model from which the prediction is requested (required)
            :type model_id: str

            :param input_data: Input for the prediction (required)
            :type input_data: Any

            :param async_mode: Indicates whether the SDK operates in asynchronous mode or not.
            :type async_mode: bool

            :return: Returns the result object.
        """
        if async_mode:
            return self.async_predict(model_id=model_id, input_data=input_data)
        
        return self.sync_predict(model_id=model_id, input_data=input_data)
    
    def sync_predict(
        self,
        model_id: Annotated[StrictStr, Field(description="Unique identifier for the model from which the prediction is requested")],
        input_data: Annotated[Any, Field(description="Input for the prediction")],  
    ) -> dict:
        """
            Handle Sync Model Prediction
        """
        # Validate input data size
        self._validate_input_data_size(input_data)

        _param = self._predict_serialize(
            model_id=model_id,
            input_data=input_data
        )

        response_data = self._call_api(
            *_param,
            async_mode=False
        )
        return response_data
    
    def async_predict(
        self,
        model_id: Annotated[StrictStr, Field(description="Unique identifier for the model from which the prediction is requested")],
        input_data: Annotated[Any, Field(description="Input for the prediction")],
    ) -> dict:
        """
            Handle Async Model Prediction
        """
        # Validate input data size
        self._validate_input_data_size(input_data)

        _param = self._async_predict_serialize(
            model_id=model_id,
            input_data=input_data
        )

        response_data = self._call_api(
            *_param
        )
        return response_data

    def _predict_serialize(
        self,
        model_id,
        input_data
    ) -> RequestSerialized:

        _header_params: Dict[str, Optional[str]] =  {}
        _body: Any = None
        
        if input_data is not None:
            _body = input_data

        # set the HTTP header `Accept`
        _header_params['Accept'] = '*/*'
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        _header_params['vps-env-type'] = self.configuration.get_vps_env_type()
        if self.configuration.get_vps_app_id():
            _header_params['vps-app-id'] = self.configuration.get_vps_app_id()

        #Request url
        url = self.configuration.host + '/predict'
        return model_id, url, _header_params, _body
    
    def _async_predict_serialize(
        self,
        model_id,
        input_data
    ) -> RequestSerialized:

        _header_params: Dict[str, Optional[str]] =  {}
        _body: Any = None
        
        if input_data is not None:
            _body = input_data

        # set the HTTP header `Accept`
        _header_params['Accept'] = '*/*'
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        _header_params['vps-env-type'] = self.configuration.get_vps_env_type()
        if self.configuration.get_vps_app_id():
            _header_params['vps-app-id'] = self.configuration.get_vps_app_id()

        #Request url
        url = self.configuration.host + '/async_predict'
        return model_id, url, _header_params, _body

    def _call_api(
        self,
        model_id,
        url,
        header_params=None,
        body=None,
        async_mode=True
    ) -> dict:
        """Makes the HTTP request (synchronous)
        :param method: Method to call.
        :param url: Path to method endpoint.
        :param header_params: Header parameters to be placed in the request header.
        :param body: Request body.
        :return: dict of response data.
        """

        try:
            # perform request and return response
            response_data = self.rest_client.request(
                model_id, url,
                headers=header_params,
                body=body,
                async_mode=async_mode
            )

        except ClientException as e:
            raise e

        return response_data
    
    def _validate_input_data_size(self, input_data):
        """
        Validates that the size of input_data is less than 10 MB.

        :param input_data: The data to validate.
        :raises ClientException: If the input_data size is greater than 10 MB.
        """
        max_size_mb = 10
        max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

        if isinstance(input_data, str):
            input_size = len(input_data)
        elif isinstance(input_data, bytes):
            input_size = len(input_data)
        elif isinstance(input_data, (list, dict)):
            input_size = len(json.dumps(input_data))
        else:
            # Convert other types to string and check their length
            input_size = len(str(input_data))

        if input_size > max_size_bytes:
            raise ClientException(413, f"Payload size more than {max_size_mb} MB is not allowed.")

    def publish(
        self,
        model_id: Annotated[StrictStr, Field(description="Unique identifier for the model to be published")],
        model_folder_path: Annotated[Optional[StrictStr], Field(description="Path to the folder containing model files")] = None,
        model_framework_type: Annotated[StrictStr, Field(description="Framework type of the model (e.g., TensorFlow, PyTorch, ONNX)")] = None,
        onnx_config_path: Annotated[Optional[StrictStr], Field(description="Optional path to the ONNX config file if the model is ONNX based")] = None,
        hf_config_path: Annotated[Optional[StrictStr], Field(description="Optional path to the HUGGING_FACE config file if the model is HUGGING_FACE based")] = None,
        processor_folder_path: Annotated[Optional[StrictStr], Field(description="Path to the folder containing processor files if applicable")] = None,
        processor_image: Annotated[Optional[StrictStr], Field(description="Docker base image for the processor")] = None,
        auto_launch: Annotated[bool, Field(description="Indicates whether to automatically launch the model after upload")] = True,
        override_model: Annotated[bool, Field(description="Indicates whether to override any existing model deployment")] = True
    ) -> dict:
        """
        Publishes a new model and optionally launches it. Rolls back any previously launched model if applicable.

        :param model_id: Unique identifier for the model to be published.
        :param model_folder_path: Path to the folder containing model files.
        :param model_framework_type: Framework type of the model (e.g., TensorFlow, PyTorch, ONNX, Xgboost, Sklearn).
        :param onnx_config_path: Optional path to the ONNX config file if the model is ONNX based.
        :param processor_folder_path: Path to the folder containing processor files if applicable.
        :param processor_image: Docker base image for the processor.
        :param auto_launch: Indicates whether to automatically launch the model after upload.
        :param override_model: Indicates whether to override any existing model deployment.
        :return: Returns a dictionary containing the result of the publish operation.
        """
        self.logger_client.info(f"Publishing model {model_id} with framework type {model_framework_type}.")

        _header_params: Dict[str, Optional[str]] =  {}
        # set the HTTP header `Accept`
        _header_params['Accept'] = '*/*'
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        _header_params['vps-env-type'] = self.configuration.get_vps_env_type()

        # Host header
        host = self.configuration.host

        if model_framework_type not in ALLOWED_MODEL_FRAMEWORK_TYPES:
            raise ClientException(400, f"Model framework type {model_framework_type} is not supported.")

        self.logger_client.info(f"Overriding model {model_id} with framework type {model_framework_type}, according to {override_model} flag.")
        self.rest_client._override_model(
            model_id, override_model, host,
            headers=_header_params
        )

        model_configuration_content = None

        # Getting the files metadata from the model folder to generate the presigned upload url
        model_total_folder_size = 1
        if model_folder_path:
            model_files_metadata, model_total_folder_size = self._get_files_metadata(model_folder_path)

        if model_framework_type == 'onnx':
            if onnx_config_path is None:
                raise ClientException(400, f"ONNX config path is required for {model_framework_type} model.")
            
            # Read the ONNX config file content
            with open(onnx_config_path, 'r') as file:
                model_configuration_content = file.read()

        
        HF_model_configuration_content = {}
        
        if model_framework_type and model_framework_type.startswith('hugging_face'):
            if hf_config_path is None:
                raise ClientException(400, f"HUGGING_FACE config path is required for {model_framework_type} model.")
            
            # Read the HUGGING_FACE config file content
            with open(hf_config_path, 'r') as file:
                HF_model_configuration_content = file.read()
                HF_model_configuration_content = json.loads(HF_model_configuration_content)

        else:
            
            self.logger_client.info(f"Starting upload for model {model_id} with framework type {model_framework_type} and total folder size {model_total_folder_size} bytes.")
            # Generating the presigned upload url
            presigned_urls = self.rest_client._generate_presigned_model_upload_url(
                model_id, model_files_metadata, model_framework_type, model_configuration_content, host,
                headers=_header_params
            )

            self.logger_client.info(f"Uploading model {model_id} with framework type {model_framework_type} and total folder size {model_total_folder_size} bytes.")
            # Upload each model file using the presigned URLs
            self._upload_files_with_presigned_urls(presigned_urls, model_files_metadata, model_id)

            if processor_folder_path:
                self.logger_client.info(f"Fetching the list of processor images supported for {model_framework_type} model {model_id}.")
                allowed_processor_images = self.rest_client._list_model_transformer_base_image(model_id, host)
                self.logger_client.info(f"List of processor images supported for {model_framework_type} model {model_id}: {', '.join(allowed_processor_images)}")

                if processor_image is None:
                    self.logger_client.error(f"Processor image is not provided for {model_framework_type} model {model_id}, use any of the following: {', '.join(allowed_processor_images)}")
                    raise ClientException(400, f"Processor image is required for model {model_id}, use any of the following: {', '.join(allowed_processor_images)}.")
                
                if processor_image not in allowed_processor_images:
                    self.logger_client.error(f"Processor image {processor_image} is not supported for {model_framework_type} model {model_id}, use any of the following: {', '.join(allowed_processor_images)}")
                    raise ClientException(400, f"Processor image {processor_image} is not supported, use any of the following: {', '.join(allowed_processor_images)}.")
                
                processor_files_metadata, processor_total_folder_size = self._get_files_metadata(processor_folder_path)

                self.logger_client.info(f"Starting upload for the processor of model {model_id}  with total folder size {processor_total_folder_size} bytes.")
                # Generating the presigned upload url
                presigned_urls = self.rest_client._generate_presigned_transformer_upload_url(
                    model_id, processor_files_metadata, host,
                    headers=_header_params
                )

                self.logger_client.info(f"Uploading processor of {model_id} with total folder size {processor_total_folder_size} bytes.")
                # Upload each processor file using the presigned URLs
                self._upload_files_with_presigned_urls(presigned_urls, processor_files_metadata, model_id)

                self.logger_client.info(f"Staging processor of {model_id} with total folder size {processor_total_folder_size} bytes.")
                #Staging the processor
                self.rest_client._stage_transformer(
                    model_id, processor_total_folder_size, host,
                    headers=_header_params
                )

        self.logger_client.info(f"Staging model and building processor of {model_id} with total folder size {model_total_folder_size} bytes.")

        # Stage the model and build the transformer if applicable
        self.rest_client._stage_model_and_build_transformer(
            model_id, model_total_folder_size, model_framework_type, processor_image, host, HF_model_configuration_content,
            headers=_header_params
        )

        if auto_launch:
            self.logger_client.info(f"Launching model {model_id} and related processor.")
            self.rest_client._launch_model_transformer(model_id, host, headers=_header_params)

        self.logger_client.info(f"Model {model_id} and related processor launched successfully, optionally, open this url to run your model in UI: https://vipas.ai/models/{model_id}.")

        return {"status": "success"}
        
    
    def _upload_files_with_presigned_urls(self, presigned_urls: List[dict], files_metadata: List[dict], model_id: str):
        """
        Uploads the files to S3 using the presigned URLs.

        :param presigned_urls: List of presigned URLs returned by the backend for each file.
        :param files_metadata: List of files' metadata to be uploaded.
        """
        for presigned_url, file_metadata in zip(presigned_urls, files_metadata):
            file_path = file_metadata['file_path']
            with open(file_path, 'rb') as file:
                form_data = {
                    key: (None, value) for key, value in presigned_url["fields"].items()
                }
                form_data["file"] = (file_metadata['file_name'], file, "application/octet-stream")

                # Upload file using rest client
                self.rest_client._upload_file_with_presigned_url(
                    presigned_url['url'], form_data
                )
                # Log the successful upload
                self.logger_client.info(f"File {file_metadata['file_name']} uploaded successfully for model: {model_id}.")

    def _get_files_metadata(self, folder_path: str):
        """
            Traverses the specified folder and returns a list of file metadata.

            :param folder_path: The path to the folder to traverse.
            :return: A list of file metadata.
        """

        file_metadata_list = []
        total_folder_size = 0  # To store the total size of the folder

        parent_folder_name = os.path.basename(folder_path.rstrip(os.sep))

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filePath = os.path.join(root, file)
                fileSize = os.path.getsize(filePath)
                total_folder_size += fileSize
                # Get the relative path of the file from the folder_path
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                # Prepend the parent folder name to the relative path
                relative_path_with_parent = os.path.join(parent_folder_name, relative_path)
                file_metadata_list.append({
                    "file_name": file,
                    "file_size": fileSize,
                    "file_type": os.path.splitext(file)[1],
                    'file_relative_path': relative_path_with_parent,
                    "file_path": filePath
                })

        return file_metadata_list, total_folder_size

    def evaluate(
        self, 
        model_id : Annotated[StrictStr, Field(description="Unique identifier for the model from which the prediction is requested")],
        challenge_id : Annotated[StrictStr, Field(description="Unique identifier for the challenge from which the prediction is requested")],) -> dict:
        """
            Evaluates the performance of a model based on a specific challenge.

            This method is used to request and retrieve predictions from a specified 
            model for a given challenge.

            :param model_id: Unique identifier for the model from which the prediction is requested (required)
            :param challenge_id: Unique identifier for the challenge from which the prediction is requested (required)

            :return: Returns the result object.
        """
        self.logger_client.info(f"Evaluating model {model_id} against the challenge {challenge_id}.")

        _header_params: Dict[str, Optional[str]] =  {}
        # set the HTTP header `Accept`
        _header_params['Accept'] = '*/*'
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        _header_params['vps-env-type'] = self.configuration.get_vps_env_type()

        # Host header
        host = self.configuration.host

        return self.rest_client._evaluate_model(
            model_id, challenge_id, host,
            headers=_header_params
        )

    def create_model(
        self, project_name: str, project_description: str = None, price: Optional[float] = 0.0, currency: Optional[str] = "INR",
        permissions: dict = {"search_visibility": "private", "api_access": "private", "share_model": "private"}) -> str:

        self.logger_client.info(f"Initiating model creation. Name: '{project_name}', Price: {price}, Currency: '{currency}'")

        try:
            url = f"{self.configuration.host}"
            project_data={
                "project_name": project_name, 
                "project_description": project_description, 
                "price": price, 
                "currency": currency, 
                "permissions": permissions
            }

            headers={"vps-auth-token": self.configuration.get_vps_auth_token()}
        
            response_data = self.rest_client._create_model(url, project_data, headers)

            if not response_data.get("model_id"):
                self.logger_client.error("Model ID missing in response")
                raise ClientException(
                    status_code=500,
                    detail="Model creation failed - no model ID returned"
                )
            self.logger_client.info(f"Model successfully created with ID: {response_data['model_id']}. You can view your model at: https://vipas.ai/models/{response_data['model_id']}.")
            return response_data["model_id"]
    
        except ClientException as e:
            raise e
        
    def get_logs(self, model_id: str) -> dict:

        self.logger_client.info(f"Entering get_logs method. Initiating log retrieval for model_id: {model_id}")
        try:
            url = f"{self.configuration.host}/get/logs"
            headers = {"vps-auth-token": self.configuration.get_vps_auth_token()}
            params = {"model_id": model_id}

            self.logger_client.info(
                f"Preparing API request for retrieving logs for model_id: {model_id}."
            )
            # Make the API request
            logs_response = self.rest_client._get_logs(url, params, headers)

            self.logger_client.info(
                f"Exiting get_logs method. Logs retrieved successfully for model_id: {model_id}. "
            )
            return logs_response

        except ClientException as e:
            self.logger_client.error(
                f"An error occurred while retrieving logs for model_id: {model_id}. "
                f"Error details: {str(e)}"
            )
            raise e