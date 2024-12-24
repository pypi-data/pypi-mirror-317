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
import json
import httpx
import time

from vipas.exceptions import ClientException
from vipas.logger import LoggerClient

class RESTClientObject:
    def __init__(self, configuration) -> None:
        timeout = httpx.Timeout(300.0) # All requests will timeout after 300 seconds in all operations
        self.client = httpx.Client(timeout=timeout)
        self.logger_client = LoggerClient(__name__)

    def request(self, model_id, url, headers=None, body=None, async_mode=True):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        """
        # Prepare headers and body for the request
        headers = headers or {}

        if body is not None:
            body = json.dumps(body)

        try:
            if async_mode:
                # Make the HTTP request using httpx
                predict_data = self._handle_async_request(model_id, url, headers=headers, body=body)
            else:
                # Make the HTTP request using httpx
                predict_data = self._handle_sync_request(model_id, url, headers=headers, body=body)
            
            return self._process_predict_response(predict_data)
        
        except ClientException as e:
            raise e

    def _handle_sync_request(self, model_id, url, headers=None, body=None):
        """Handles synchronous requests."""
        try:
            predict_response = self.client.request("POST", f"{url}?model_id={model_id}", headers=headers, content=body)
            predict_response.raise_for_status()
            predict_data = predict_response.json()

            return predict_data
        except httpx.HTTPStatusError as e:
            # Handle any HTTP errors that occur while making the request
            error_detail = predict_response.json().get('detail', predict_response.text)
            raise ClientException.from_response(http_resp=predict_response, body=error_detail, data=None)
        except httpx.RequestError as e:
            # Handle any Request errors that occur while making the request
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except Exception as e:
            # Handle any other exceptions that may occur
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

    def _handle_async_request(self, model_id, url, headers=None, body=None):
        """Handles asynchronous requests."""
        try:
            task_response = self.client.request("POST", f"{url}/add_task?model_id={model_id}", headers=headers, content=body)
            task_response.raise_for_status()
            task_data = task_response.json()
                
            transaction_id = task_data.get("transaction-id", None)
        except httpx.HTTPStatusError as e:
            # Handle any HTTP errors that occur while making the request
            error_detail = task_response.json().get('detail', task_response.text)
            raise ClientException.from_response(http_resp=task_response, body=error_detail, data=None)
        except httpx.RequestError as e:
            # Handle any Request errors that occur while making the request
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except Exception as e:
            # Handle any other exceptions that may occur
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
        #Retrying to get the status for the current transaction id 
        return self._poll_status_and_get_result(url, headers, transaction_id)
        
    def _poll_status_and_get_result(self, url, headers, transaction_id):
        """Polls the status endpoint and retrieves the result."""
        poll_intervals = [1, 3, 3, 3, 5, 5]  # Initial intervals
        max_poll_time = 300  # Max poll time in seconds
        total_time = 0

        while total_time < max_poll_time:
            try:
                status_response = self.client.request("GET", f"{url}/status?transaction-id={transaction_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                if status.startswith("completed") or status.startswith("failed"):
                    return self._get_result(url, headers, transaction_id)

            except httpx.RequestError as e:
                raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
            except httpx.HTTPStatusError as e:
                error_detail = status_response.json().get('detail', status_response.text)
                raise ClientException.from_response(http_resp=status_response, body=error_detail, data=None)
            except ClientException as e:
                raise e
            except Exception as e:
                raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

            # Wait before retrying
            interval = poll_intervals.pop(0) if poll_intervals else 5  # Use 5 seconds interval if no more intervals
            total_time += interval
            time.sleep(interval)

        raise ClientException(status=504, body="Gateway Timeout: Polling timed out, please try again.", data=None)
    
    def _get_result(self, url, headers, transaction_id):
        """Retrieves the result from the result endpoint."""
        try:
            result_response = self.client.request("GET", f"{url}/result?transaction-id={transaction_id}", headers=headers)
            result_response.raise_for_status()
            result_data = result_response.json()
            return result_data
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = result_response.json().get('detail', result_response.text)
            raise ClientException.from_response(http_resp=result_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

    def _process_predict_response(self, predict_data):
        """Processes the predict response."""
        payload_type = predict_data.get("payload_type", None)
        if payload_type == "url":
            try:
                return self._get_output_data_from_url(predict_data)
            except ClientException as e:
                raise e
        elif payload_type == "content":
            return predict_data.get("output_data", None)
        else:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _get_output_data_from_url(self, predict_data):
        """Retrieves output data from the provided URL."""
        try:
            output_data_response = self.client.request("GET", predict_data.get("payload_url"))
            output_data_response.raise_for_status()
            output_data = output_data_response.json()

            extractor = predict_data.get("extractor", None)
            if extractor is not None:
                # Define the function and execute the logic from the schema string
                local_vars = {'output_data': output_data}
                exec(extractor, globals(), local_vars)
                output_data = local_vars['extracted_output_data']
            
            return output_data
        except httpx.HTTPStatusError as e:
            error_detail = output_data_response.json().get('detail', output_data_response.text)
            raise ClientException.from_response(http_resp=output_data_response, body=error_detail, data=None)
        except httpx.RequestError as e:
            # Handle any errors that occur while making the request
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except Exception as e:
            # Handle any other exceptions that may occur
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _override_model(self, model_id, override_model, url, headers):
        """Retrieves the build deployment status for the model."""
        try:
            override_model_response = self.client.request("POST", f"{url}/override/model?model_id={model_id}&override_model={override_model}", headers=headers)
            override_model_response.raise_for_status()

            override_model_response_data = override_model_response.json()
            if override_model_response_data.get("status") == "completed":
                self.logger_client.info(f"Override model for model: {model_id} completed successfully with project status: {override_model_response_data.get('project_status')}.")
                return
    
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = override_model_response.json().get('detail', override_model_response.text)
            raise ClientException.from_response(http_resp=override_model_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
        self._poll_override_model_status(model_id, url, headers)
        
    def _poll_override_model_status(self, model_id, url, headers):
        """Polls the override model status endpoint and retrieves the result."""
        poll_intervals = [1, 3, 3, 3, 5, 5]  # Initial intervals
        max_poll_time = 300  # Max poll time in seconds
        total_time = 0

        while total_time < max_poll_time:
            try:
                status_response = self.client.request("GET", f"{url}/override/model/status?model_id={model_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                if status == "completed":
                    self.logger_client.info(f"Override model for model: {model_id} completed successfully with project status: {status_data.get('project_status')}.")
                    return 
                
                elif status == "failed":
                    raise ClientException(status=500, body="Internal Server Error: Model override failed, please try again.", data=None)
                
                self.logger_client.info(f"Overriding is inprogress for model: {model_id} with project status: {status_data.get('project_status')}.")
            except httpx.RequestError as e:
                raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
            except httpx.HTTPStatusError as e:
                error_detail = status_response.json().get('detail', status_response.text)
                raise ClientException.from_response(http_resp=status_response, body=error_detail, data=None)
            except ClientException as e:
                raise e
            except Exception as e:
                raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)   

            # Wait before retrying
            interval = poll_intervals.pop(0) if poll_intervals else 5  # Use 5 seconds interval if no more intervals
            total_time += interval
            time.sleep(interval)

        raise ClientException(status=504, body="Gateway Timeout: Polling timed out, please try again.", data=None)
    
    def _list_model_transformer_base_image(self, model_id, url):
        """Retrieves the model transformer base image for the model."""
        try:
            model_transformer_base_image_response = self.client.request("GET", f"{url}/list/model/transformer/base/image?model_id={model_id}")
            model_transformer_base_image_response.raise_for_status()
            model_transformer_base_image_data = model_transformer_base_image_response.json()
            
            return model_transformer_base_image_data
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = model_transformer_base_image_response.json().get('detail', model_transformer_base_image_response.text)
            raise ClientException.from_response(http_resp=model_transformer_base_image_response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _generate_presigned_model_upload_url(self, model_id, files_metadata, model_framework_type, model_configuration_content, url, headers):
        """Retrieves the presigned model upload URL for the model."""
        try:
            body = {
                "model_id": model_id,
                "files": files_metadata,
                "framework_type": model_framework_type,
                "model_details": model_configuration_content
            }

            presigned_model_upload_response = self.client.request("POST", f"{url}/generate/presigned/model/upload/url", headers=headers, json=body)
            presigned_model_upload_response.raise_for_status()
            presigned_model_upload_data = presigned_model_upload_response.json()
            
            presigned_urls = presigned_model_upload_data.get("presigned_upload_urls")
            
            return presigned_urls
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = presigned_model_upload_response.json().get('detail', presigned_model_upload_response.text)
            raise ClientException.from_response(http_resp=presigned_model_upload_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _generate_presigned_transformer_upload_url(self, model_id, files_metadata, url, headers):
        """Retrieves the presigned transformer upload URL for the model."""
        try:
            body = {
                "model_id": model_id,
                "files": files_metadata
            }

            presigned_transformer_upload_response = self.client.request("POST", f"{url}/generate/presigned/transformer/upload/url", headers=headers, json=body)
            presigned_transformer_upload_response.raise_for_status()
            presigned_transformer_upload_data = presigned_transformer_upload_response.json()
            
            presigned_urls = presigned_transformer_upload_data.get("presigned_upload_urls")
            
            return presigned_urls
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = presigned_transformer_upload_response.json().get('detail', presigned_transformer_upload_response.text)
            raise ClientException.from_response(http_resp=presigned_transformer_upload_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
    
    def _upload_file_with_presigned_url(self, presigned_url, form_data):
        """Uploads the file to S3 using the presigned URL."""
        try:
            with httpx.Client() as client: # Another client is needed since we are using the presigned URL
                presigned_upload_response = client.request("POST", presigned_url, files=form_data)
                presigned_upload_response.raise_for_status()

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None) 
        except httpx.HTTPStatusError as e:
            error_detail = presigned_upload_response.json().get('detail', presigned_upload_response.text)
            raise ClientException.from_response(http_resp=presigned_upload_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

    def _stage_transformer(self, model_id, transformer_total_folder_size, url, headers):
        """Stages the transformer for the model."""
        try:
            body = {
                "model_id": model_id,
                "folder_size": transformer_total_folder_size
            }

            stage_transformer_response = self.client.request("POST", f"{url}/stage/transformer", headers=headers, json=body)
            stage_transformer_response.raise_for_status()
            stage_transformer_data = stage_transformer_response.json()
            
            return stage_transformer_data
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = stage_transformer_response.json().get('detail', stage_transformer_response.text)
            raise ClientException.from_response(http_resp=stage_transformer_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

    def _stage_model_and_build_transformer(self, model_id, model_total_folder_size, model_framework_type, processor_image, url, HF_model_configuration_content, headers):
        """Stages the model and builds the transformer for the model."""
        try:
            body = {
                "model_id": model_id,
                "folder_size": model_total_folder_size if model_total_folder_size else 1,
                "framework_type": model_framework_type,
                "hugging_face_config": HF_model_configuration_content,
                "base_image": processor_image
            }

            stage_model_response = self.client.request("POST", f"{url}/stage/model/build/transformer", headers=headers, json=body)
            stage_model_response.raise_for_status()

            stage_model_data = stage_model_response.json()
            if stage_model_data.get("status") == "completed":
                self.logger_client.info(f"Stage model and build transformer for model: {model_id} completed successfully with project status: {stage_model_data.get('project_status')}.")
                return
        
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = stage_model_response.json().get('detail', stage_model_response.text)
            raise ClientException.from_response(http_resp=stage_model_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
        self._poll_stage_model_and_build_transformer_status(model_id, url, headers)

    def _poll_stage_model_and_build_transformer_status(self, model_id, url, headers):
        """Polls the stage model and build transformer status endpoint and retrieves the result."""
        poll_intervals = [1, 3, 3, 3, 5, 5]  # Initial intervals
        max_poll_time = 300  # Max poll time in seconds
        total_time = 0

        while total_time < max_poll_time:
            try:
                status_response = self.client.request("GET", f"{url}/stage/model/build/transformer/status?model_id={model_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                if status == "completed":
                    self.logger_client.info(f"Stage model and build transformer for model: {model_id} completed successfully with project status: {status_data.get('project_status')}.")
                    return

                elif status == "failed":
                    raise ClientException(status=500, body="Internal Server Error: Stage model and build transformer failed, please try again.", data=None)
                
                self.logger_client.info(f"Stage model and build transformer for model: {model_id} is inprogress with project status: {status_data.get('project_status')}")

            except httpx.RequestError as e:
                raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
            except httpx.HTTPStatusError as e:
                error_detail = status_response.json().get('detail', status_response.text)
                raise ClientException.from_response(http_resp=status_response, body=error_detail, data=None)
            except ClientException as e:
                raise e
            except Exception as e:
                raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)   

            # Wait before retrying
            interval = poll_intervals.pop(0) if poll_intervals else 5  # Use 5 seconds interval if no more intervals
            total_time += interval
            time.sleep(interval)    

        raise ClientException(status=504, body="Gateway Timeout: Polling timed out, please try again.", data=None)
    
    def _launch_model_transformer(self, model_id, url, headers):
        """Launches the model transformer for the model."""
        try:
            body = {
                "model_id": model_id
            }

            launch_model_transformer_response = self.client.request("POST", f"{url}/launch/model/transformer", headers=headers, json=body)
            launch_model_transformer_response.raise_for_status()

            launch_model_transformer_data = launch_model_transformer_response.json()
            if launch_model_transformer_data.get("status") == "completed":
                self.logger_client.info(f"Launch model transformer for model: {model_id} completed successfully with project status: {launch_model_transformer_data.get('project_status')}.")
                return

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = launch_model_transformer_response.json().get('detail', launch_model_transformer_response.text)
            raise ClientException.from_response(http_resp=launch_model_transformer_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
        self._poll_launch_model_transformer_status(model_id, url, headers)

    def _poll_launch_model_transformer_status(self, model_id, url, headers):
        """Polls the launch model transformer status endpoint and retrieves the result."""
        poll_intervals = [1, 3, 3, 3, 5, 5]  # Initial intervals
        max_poll_time = 300  # Max poll time in seconds
        total_time = 0

        while total_time < max_poll_time:
            try:
                status_response = self.client.request("GET", f"{url}/launch/model/transformer/status?model_id={model_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                if status == "completed":
                    self.logger_client.info(f"Launch model transformer for model: {model_id} completed successfully with project status: {status_data.get('project_status')}.")
                    return
                
                elif status == "failed":
                    raise ClientException(status=500, body="Internal Server Error: Launch model transformer failed, please try again.", data=None)
                
                self.logger_client.info(f"Launch model transformer for model: {model_id} is inprogress with project status: {status_data.get('project_status')}")

            except httpx.RequestError as e:
                raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
            except httpx.HTTPStatusError as e:
                error_detail = status_response.json().get('detail', status_response.text)
                raise ClientException.from_response(http_resp=status_response, body=error_detail, data=None)
            except ClientException as e:
                raise e
            except Exception as e:
                raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
            
            # Wait before retrying
            interval = poll_intervals.pop(0) if poll_intervals else 5  # Use 5 seconds interval if no more intervals
            total_time += interval
            time.sleep(interval)

        raise ClientException(status=504, body="Gateway Timeout: Polling timed out, please try again.", data=None)
    
    def _evaluate_model(self, model_id, challenge_id, url, headers):
        """Evaluates the model against the challenge."""
        try:

            evaluate_model_response = self.client.request("POST", f"{url}/evaluate/model/add/task?model_id={model_id}&challenge_id={challenge_id}", headers=headers)
            evaluate_model_response.raise_for_status()

            transaction_id = evaluate_model_response.json().get("transaction-id")
        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = evaluate_model_response.json().get('detail', evaluate_model_response.text)
            raise ClientException.from_response(http_resp=evaluate_model_response, body=error_detail, data=None)
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
        return self._poll_evaluate_model_status_and_get_result(transaction_id, model_id, challenge_id, url, headers)
    
    def _poll_evaluate_model_status_and_get_result(self, transaction_id, model_id, challenge_id, url, headers):
        """Polls the evaluate model status endpoint and retrieves the result."""
        poll_intervals = [1, 3, 3, 3, 5, 5]  # Initial intervals
        max_poll_time = 1500  # Max poll time in seconds
        total_time = 0

        while total_time < max_poll_time:
            try:
                status_response = self.client.request("GET", f"{url}/evaluate/model/status?transaction_id={transaction_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                if status.startswith("completed") or status.startswith("failed"):
                    self.logger_client.info(f"Evaluate model for model: {model_id} against the challenge: {challenge_id} completed successfully.")
                    return self._get_evaluate_model_result(transaction_id, url, headers)
                
                self.logger_client.info(f"Evaluate model for model: {model_id} against the challenge: {challenge_id} is inprogress.")

            except httpx.RequestError as e:
                raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
            except httpx.HTTPStatusError as e:
                error_detail = status_response.json().get('detail', status_response.text)
                raise ClientException.from_response(http_resp=status_response, body=error_detail, data=None)
            except ClientException as e:
                raise e
            except Exception as e:
                raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
            
            # Wait before retrying
            interval = poll_intervals.pop(0) if poll_intervals else 5  # Use 5 seconds interval if no more intervals
            total_time += interval
            time.sleep(interval)    

        raise ClientException(status=504, body="Gateway Timeout: Polling timed out, please try again.", data=None)
    
    def _get_evaluate_model_result(self, transaction_id, url, headers):
        """Gets the evaluate model result."""
        try:
            evaluate_model_result_response = self.client.request("GET", f"{url}/evaluate/model/result?transaction_id={transaction_id}", headers=headers)
            evaluate_model_result_response.raise_for_status()
            evaluate_model_result_data = evaluate_model_result_response.json()
            
            return evaluate_model_result_data

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = evaluate_model_result_response.json().get('detail', evaluate_model_result_response.text)
            raise ClientException.from_response(http_resp=evaluate_model_result_response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _get_challenge_submission(self, method, url, params, body, headers):
        try:
            challenge_submission_response = self.client.request(method, url=url, params=params, json=body, headers=headers)
            challenge_submission_response.raise_for_status()
            challenge_submission_data = challenge_submission_response.json()
            
            return challenge_submission_data

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = challenge_submission_response.json().get('detail', challenge_submission_response.text)
            raise ClientException.from_response(http_resp=challenge_submission_response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
    
    def _create_model(self, url, project_data, headers):     
        try:
            create_model_result_response = self.client.request(method="POST", url=f"{url}/create/model", headers=headers, json=project_data)
            create_model_result_response.raise_for_status()
            create_model_result_response = create_model_result_response.json()
            
            return create_model_result_response

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = create_model_result_response.json().get('detail', create_model_result_response.text)
            raise ClientException.from_response(http_resp=create_model_result_response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
    
    def _get_token(self, method, url, params, body, headers):
        
        try:
            self.logger_client.info(f"Generating Temporary Access Token for user {body.get('username','')}.")
            token_response = self.client.request(method, url=url, params=params, json=body, headers=headers)
            token_response.raise_for_status()
            token_data = token_response.json()
            self.logger_client.info(f"Temporary Access Token generated for user {body.get('username','')}.")
            return token_data

        except httpx.RequestError as e:
            raise ClientException(status=400, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = token_response.json().get('detail', token_response.text)
            raise ClientException.from_response(http_resp=token_response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)

                
    def _get_logs(self, url: str, params: dict, headers: dict) -> dict:
        try:
            response = self.client.request(method="GET", url=url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            raise ClientException(status=502, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = response.json().get('detail', response.text)
            raise ClientException.from_response(http_resp=response, body=error_detail, data=None)
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)
        
    def _get_logs(self, url: str, params: dict, headers: dict) -> dict:

        self.logger_client.info(f"Starting _get_logs method. Beginning log retrieval process for model ID: {params['model_id']}.")

        try:
            self.logger_client.info(f"Initiating GET request with model id: {params['model_id']}.")
            
            response = self.client.request(method="GET", url=url, params=params, headers=headers)
            response.raise_for_status()
            
            self.logger_client.info(f"Request to fetch logs for model ID {params['model_id']} was successful. Status Code: {response.status_code}")
            self.logger_client.info(
                f"Exiting _get_logs method. Successfully retrieved logs for model ID: {params['model_id']}. "
            )
            return response.json()

        except httpx.RequestError as e:
            self.logger_client.error(f"RequestError occurred while fetching logs for model ID {params['model_id']}: {str(e)}")
            raise ClientException(status=502, body="Bad Gateway: Request Error occurred, please try again.", data=None)
        except httpx.HTTPStatusError as e:
            error_detail = response.json().get('detail', response.text)
            self.logger_client.error(
                f"HTTPStatusError occurred while fetching logs for model ID {params['model_id']}. Status Code: {response.status_code}, Error Detail: {error_detail}"
            )
            raise ClientException.from_response(http_resp=response, body=error_detail, data=None)
        except ClientException as e:
            self.logger_client.error(f"ClientException occurred while fetching logs for model ID {params['model_id']}: {str(e)}")
            raise e
        except Exception as e:
            self.logger_client.error(f"Unexpected error occurred while fetching logs for model ID {params['model_id']}: {str(e)}")
            raise ClientException(status=500, body="Internal Server Error: Unexpected error occurred, please try again.", data=None)