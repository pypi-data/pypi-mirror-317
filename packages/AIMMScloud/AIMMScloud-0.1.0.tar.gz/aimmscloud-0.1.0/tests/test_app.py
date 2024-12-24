import pytest
from dotenv import load_dotenv
import os
from aimmscloud.aimms_application import Application


@pytest.fixture
def setup_test():
    load_dotenv()
    app_api = Application(
        host_url=os.getenv("HOST_URL"),
        api_key=os.getenv("API_KEY"),
    )
    return app_api


def test_get_all_apps_info(setup_test):
    app_api = setup_test
    out = app_api.get_all_apps_info()
    assert out is not None


def test_create_app_category(setup_test):
    app_api = setup_test
    out = app_api.create_app_category("test123")
    assert out["value"] == "test123"


def test_update_application_category(setup_test):
    app_api = setup_test
    out = app_api.create_app_category("test456")
    out = app_api.update_application_category(
        new_category_name="test23456",
        category_id=out["id"],
    )
    assert out is not None


def test_delete_app_category(setup_test):
    app_api = setup_test
    out = app_api.create_app_category("test789")
    out = app_api.delete_app_category(out["id"])
    assert out == "Category deleted"


# ! will always fail because of API response
# def test_get_all_app_categories(setup_test):
#    app_api = setup_test
#    out = app_api.get_all_app_categories()
#    assert out is not None


def test_get_aimms_versions(setup_test):
    app_api = setup_test
    out = app_api.get_aimms_versions()
    assert out is not None


def test_publish_app(setup_test):
    app_api = setup_test
    out = app_api.publish_app(
        file_name="FlowShop.aimmspack",
        iconfile_name="test_icon.png",
        aimms_version="24.6.2.9-linux64-x86-vc143",
        application_description="Test application 789",
        application_name="test app 789",
        application_version="1.0",
        attributes={
            "isWebUI": "true",
            "ServerLicense": "Default",
        },
        projectCategory="publish_test",
        publish_behavior=0,
    )
    assert out is not None
    # publish an app with additional metadata
    app_api = setup_test
    out = app_api.publish_app(
        file_name="FlowShop.aimmspack",
        iconfile_name="test_icon.png",
        aimms_version="24.6.2.9-linux64-x86-vc143",
        application_description="Test application task 123",
        application_name="test app task 123",
        application_version="0.1",
        attributes={
            "isWebUI": "true",
            "ServerLicense": "Default",
        },
        projectCategory="publish_test",
        publish_behavior=0,
        metadata={"projectVersion": "0.2"},
    )
    assert out is not None


def test_update_app(setup_test):
    app_api = setup_test
    out = app_api.update_app(
        project_name="test app task 123",
        project_version="0.2",
        attributes={"isWebUI": "false"},
    )
    assert out is not None


def test_get_app_info(setup_test):
    app_api = setup_test
    out = app_api.get_app_info("test app task", "0.1")
    assert out is not None


def test_delete_apps(setup_test):
    app_api = setup_test
    out1 = app_api.delete_app("test app task 123", "0.2")
    out2 = app_api.delete_app("test app 789", "1.0")
    assert out1 == "Application deleted" and out2 == "Application deleted"
