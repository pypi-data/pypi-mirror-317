# coding: utf-8

"""
    AIMMS Cloud rest API client for the task API
"""
from aimmscloud.aimms_cloud_api import AIMMScloudapi
from aimms_openapi_client.api.task_api import TaskApi

import json
from datetime import datetime


class Task(AIMMScloudapi):
    """Class to work with the AIMMS Cloud Task API

    :param host_url: Base url of your AIMMS account.
        Something like `https://myaccount.aimms.cloud/pro-api/v2`
    :param api_key: API key to authenticate with the AIMMS Cloud API.
        You need to create an API key in the AIMMS Cloud web interface.
        For more information please look at: https://documentation.aimms.com/cloud/rest-api.html#api-keys-and-scopes
    """

    def __init__(self, host_url: str, api_key: str):
        super().__init__(host_url, api_key)
        self.task_api = TaskApi(self.api_client)

    # ? openapi generated does not support bytes body yet
    # https://github.com/openapi-generators/openapi-python-client/discussions/821
    def create_task(
        self, app_name: str, app_version: str, service_name: str, payload: dict
    ) -> dict:
        """Creates a new task

        :param app_name: Name of the application
        :param app_version: Version of the application
        :param service_name: Name of the service/task to be created
        :param payload: data as input for the task needs to be a dictionary
        :return: JSON object with the new task and its metadata
        """
        if payload and isinstance(payload, dict):
            object_type = self.task_api.create_task(
                app_name=app_name,
                app_version=app_version,
                service_name=service_name,
                body=payload,
            )
        else:
            object_type = self.task_api.create_task(
                app_name=app_name, app_version=app_version, service_name=service_name
            )
        return json.loads(object_type.to_json())

    def get_task(self, task_id: str) -> dict:
        """Get a task by its id

        :param task_id: ID of the task
        :return: JSON object with the task and its metadata
        """
        object_type = self.task_api.get_task(id=task_id)
        return json.loads(object_type.to_json())

    # ! Not sure if this works
    def get_tasks(
        self,
        app_name: str,
        app_version: str,
        before_date: datetime.date = None,
        after_date: datetime.date = None,
    ) -> dict:
        """Get the tasks of an application

        :param task_id: ID of the task
        :return: JSON object with the status of the task
        """
        object_type = self.task_api.get_tasks(
            app_name=app_name,
            app_version=app_version,
            before=before_date,
            after=after_date,
        )
        return json.loads(object_type.to_json())

    # ! Not sure if this works
    def interrupt_task(self, task_id: str) -> dict:
        """Interrupt a task

        :param task_id: ID of the task
        :return: JSON object with the status of the task
        """
        self.task_api.interrupt_task(id=task_id)
        return f"Task with {task_id} interrupted"

    # ? seems to work
    def delete_task(self, task_id: str) -> dict:
        """Delete a task

        :param task_id: ID of the task
        :return: JSON object with the status of the task
        """
        self.task_api.delete_task(id=task_id)
        return f"Task with {task_id} deleted"

    # ? API needs to be changed here but works for now
    def get_task_response(self, task_id: str) -> dict:
        """Get the response of a task by its id

        :param task_id: ID of the task
        :return: JSON object with the response of the task
        """
        object_type = self.task_api.get_task_response(id=task_id)
        return object_type.decode("utf-8")
