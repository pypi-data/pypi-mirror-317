# coding: utf-8

"""
    AIMMS Cloud rest API client for the application API
"""
from aimmscloud.aimms_cloud_api import AIMMScloudapi
from aimms_openapi_client.api.application_api import ApplicationApi
from aimms_openapi_client.api.publishing_api import PublishingApi
from aimms_openapi_client.models.pro_app_category import PROAppCategory
from aimms_openapi_client.models.pro_app_patch import PROAppPatch
from aimms_openapi_client.models.pro_app_metadata import PROAppMetadata

import json
import random


class Application(AIMMScloudapi):
    """Class to work with the AIMMS Cloud Application API

    :param host_url: Base url of your AIMMS account.
        Something like `https://myaccount.aimms.cloud/pro-api/v2`
    :param api_key: API key to authenticate with the AIMMS Cloud API.
        You need to create an API key in the AIMMS Cloud web interface.
        For more information please look at: https://documentation.aimms.com/cloud/rest-api.html#api-keys-and-scopes
    """

    def __init__(self, host_url: str, api_key: str):
        super().__init__(host_url, api_key)
        self.application_api = ApplicationApi(self.api_client)
        self.publishing_api = PublishingApi(self.api_client)

    # ! API needs to be changed here the PRO APP Category needs to change
    def create_app_category(self, category_name: str) -> dict:
        """Creates a new application category


        :param category_name: Name of the new category
        :return: JSON object with the new category
        """
        json_var = {"value": category_name}
        pro_app_category = PROAppCategory().from_dict(json_var)
        object_type = self.application_api.create_application_category(
            pro_app_category=pro_app_category
        )
        return json.loads(object_type.to_json())

    def delete_app(self, project_name: str, project_version: str) -> dict:
        """Deletes an application


        :param project_name: Name of the application to delete
        :param project_version: Version of the application to delete
        :return: String indicating the application was deleted
        """
        self.application_api.delete_app(project_name, project_version)
        return "Application deleted"

    def delete_app_category(self, category_id: str) -> dict:
        """Deletes an application category


        :param category_id: Id of the category to delete
        :return: String indicating the category was deleted
        """
        self.application_api.delete_application_category(category_id)
        return "Category deleted"

    def get_aimms_versions(self) -> list:
        """Gets all available AIMMS versions


        :return: JSON object with the available AIMMS versions
        """
        object_type = self.publishing_api.get_aimms_versions()
        version_var = object_type.to_dict()
        versions = list(set([x["id"] for x in version_var["versions"]]))
        return versions

    # ! API needs to be changed here
    # ActuallyIs = [{'id': '481eda5e-d0e4-42...37c', 'value': 'test3'}]
    # ShouldBe = {"application_categories":[{'id': '481eda5e-d0e4-42...37c', 'value': 'test3'}]}
    def get_all_app_categories(self) -> dict:
        """Gets all application categories


        :return: JSON object with the available categories
        """
        object_type = self.application_api.get_all_application_categories()
        return json.loads(object_type.to_json())

    def get_all_apps_info(self) -> dict:
        """Gets all applications and their meta data


        :return: JSON object with the available applications
        """
        object_type = self.application_api.get_all_apps_info()
        return json.loads(object_type.to_json())

    def get_app_info(self, project_name: str, project_version: str) -> dict:
        """Gets information about an application


        :param project_name: Name of the application
        :param project_version: Version of the application
        :return: JSON object with the application information
        """
        object_type = self.application_api.get_app_info(project_name, project_version)
        return json.loads(object_type.to_json())

    def get_apps_info(self, project_name: str) -> dict:
        """Gets information about all applications in a category


        :param project_name: Name of the application
        :return: JSON object with the application information
        """
        object_type = self.application_api.get_apps_info(project_name)
        return json.loads(object_type.to_json())

    # use only the file name --> the generated code will take care of the rest
    def publish_app(
        self,
        file_name: str,
        iconfile_name: str,
        aimms_version: str,
        application_description: str,
        application_name: str,
        application_version: str,
        attributes: dict,
        projectCategory: str = "",
        publish_behavior: int = 1,
        metadata: dict = None,
    ) -> dict:
        """Publishes an application


        :param file_name: the path to the AIMMSpack file
        :param iconfile_name: the path to the icon file
        :param aimms_version: the version of AIMMS to use
        :param application_description: the description of the application
        :param application_name: the name of the application
        :param application_version: the version of the application
        :param attributes: dictionary with the specific metadata for publishing such as isWebUI, ServerLicense, etc.
        :param projectCategory: the category of the application
        :param publish_behavior: 0 to publish new application, 1 to update existing application
        :param metadata: additional metadata for the application
        :return: JSON object with the published application information
        """
        if not aimms_version in self.get_aimms_versions():
            raise ValueError("Invalid AIMMS version")
        metadata_dict = {
            "aimmsVersionId": aimms_version,
            "attributes": attributes,
            "description": application_description,
            "name": application_name,
            "projectCategory": projectCategory,
            "projectVersion": application_version,
            "publishBehavior": publish_behavior,
        }
        # add and overwrite metadata if it is not None
        if metadata is not None and isinstance(metadata, dict):
            metadata_dict.update(metadata)

        metadata = PROAppMetadata().from_dict(metadata_dict)
        object_type = self.application_api.publish_app(
            file=file_name,
            icon=iconfile_name,
            metadata=metadata,
            _content_type="multipart/form-data",
        )
        return json.loads(object_type.to_json())

    def update_app(
        self, project_name: str, project_version: str, attributes: dict
    ) -> dict:
        """Updates an application


        :param project_name: Name of the application
        :param project_version: Version of the application
        :param attributes: Dictionary with the attributes to update
        :return: JSON object with the updated application information
        """
        # check if the attributes not null
        if attributes is None:
            raise ValueError("Attributes cannot be None")
        pro_app_patch = PROAppPatch().from_dict({"attributes": {}.update(attributes)})
        object_type = self.application_api.update_app(
            project_name, project_version, pro_app_patch=pro_app_patch
        )
        return json.loads(object_type.to_json())

    # ! API needs to be changed here the PRO APP Category needs to change
    def update_application_category(
        self, new_category_name: str, category_id: str
    ) -> dict:
        """Updates an application category


        :param category_id: Id of the category to update
        :param new_category_name: New name of the category
        :return: JSON object with the updated category
        """
        random_integer = self._generate_random_integer()
        json_var = {"id": random_integer, "value": new_category_name}
        pro_app_category = PROAppCategory().from_dict(json_var)
        object_type = self.application_api.update_application_category(
            category_id, pro_app_category=pro_app_category
        )
        return json.loads(object_type.to_json())
