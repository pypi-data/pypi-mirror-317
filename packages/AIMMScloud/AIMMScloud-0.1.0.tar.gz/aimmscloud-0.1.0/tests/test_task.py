import pytest
from dotenv import load_dotenv
import os
from aimmscloud.aimms_task import Task
from datetime import datetime, timedelta
import time


@pytest.fixture
def setup_test():
    task_api = Task(
        host_url=os.getenv("HOST_URL"),
        api_key=os.getenv("API_KEY"),
    )
    return task_api


@pytest.fixture
def create_payload():
    payload = {
        "Jobs": [
            {
                "j": "Job-01",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 16},
                    {"m": "M-02", "ProcessTime": 18},
                    {"m": "M-03", "ProcessTime": 1},
                    {"m": "M-04", "ProcessTime": 14},
                    {"m": "M-05", "ProcessTime": 2},
                    {"m": "M-06", "ProcessTime": 11},
                    {"m": "M-07", "ProcessTime": 2},
                    {"m": "M-08", "ProcessTime": 10},
                    {"m": "M-09", "ProcessTime": 20},
                    {"m": "M-10", "ProcessTime": 12},
                    {"m": "M-11", "ProcessTime": 18},
                ],
            },
            {
                "j": "Job-02",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 9},
                    {"m": "M-02", "ProcessTime": 18},
                    {"m": "M-03", "ProcessTime": 4},
                    {"m": "M-04", "ProcessTime": 13},
                    {"m": "M-05", "ProcessTime": 5},
                    {"m": "M-06", "ProcessTime": 15},
                    {"m": "M-07", "ProcessTime": 18},
                    {"m": "M-08", "ProcessTime": 5},
                    {"m": "M-09", "ProcessTime": 10},
                    {"m": "M-10", "ProcessTime": 4},
                    {"m": "M-11", "ProcessTime": 11},
                ],
            },
            {
                "j": "Job-03",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 20},
                    {"m": "M-02", "ProcessTime": 16},
                    {"m": "M-03", "ProcessTime": 10},
                    {"m": "M-04", "ProcessTime": 11},
                    {"m": "M-05", "ProcessTime": 4},
                    {"m": "M-06", "ProcessTime": 4},
                    {"m": "M-07", "ProcessTime": 15},
                    {"m": "M-08", "ProcessTime": 11},
                    {"m": "M-09", "ProcessTime": 17},
                    {"m": "M-10", "ProcessTime": 19},
                    {"m": "M-11", "ProcessTime": 10},
                ],
            },
            {
                "j": "Job-04",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 18},
                    {"m": "M-02", "ProcessTime": 14},
                    {"m": "M-03", "ProcessTime": 2},
                    {"m": "M-04", "ProcessTime": 1},
                    {"m": "M-05", "ProcessTime": 11},
                    {"m": "M-06", "ProcessTime": 11},
                    {"m": "M-07", "ProcessTime": 11},
                    {"m": "M-08", "ProcessTime": 3},
                    {"m": "M-09", "ProcessTime": 14},
                    {"m": "M-10", "ProcessTime": 6},
                    {"m": "M-11", "ProcessTime": 2},
                ],
            },
            {
                "j": "Job-05",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 12},
                    {"m": "M-02", "ProcessTime": 8},
                    {"m": "M-03", "ProcessTime": 10},
                    {"m": "M-04", "ProcessTime": 9},
                    {"m": "M-05", "ProcessTime": 9},
                    {"m": "M-06", "ProcessTime": 4},
                    {"m": "M-07", "ProcessTime": 7},
                    {"m": "M-08", "ProcessTime": 2},
                    {"m": "M-09", "ProcessTime": 5},
                    {"m": "M-10", "ProcessTime": 19},
                    {"m": "M-11", "ProcessTime": 9},
                ],
            },
            {
                "j": "Job-06",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 15},
                    {"m": "M-02", "ProcessTime": 6},
                    {"m": "M-03", "ProcessTime": 10},
                    {"m": "M-04", "ProcessTime": 9},
                    {"m": "M-05", "ProcessTime": 7},
                    {"m": "M-06", "ProcessTime": 17},
                    {"m": "M-07", "ProcessTime": 4},
                    {"m": "M-08", "ProcessTime": 12},
                    {"m": "M-09", "ProcessTime": 3},
                    {"m": "M-10", "ProcessTime": 8},
                    {"m": "M-11", "ProcessTime": 10},
                ],
            },
            {
                "j": "Job-07",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 12},
                    {"m": "M-02", "ProcessTime": 9},
                    {"m": "M-03", "ProcessTime": 20},
                    {"m": "M-04", "ProcessTime": 12},
                    {"m": "M-05", "ProcessTime": 16},
                    {"m": "M-06", "ProcessTime": 4},
                    {"m": "M-07", "ProcessTime": 19},
                    {"m": "M-08", "ProcessTime": 10},
                    {"m": "M-09", "ProcessTime": 3},
                    {"m": "M-10", "ProcessTime": 19},
                    {"m": "M-11", "ProcessTime": 20},
                ],
            },
            {
                "j": "Job-08",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 12},
                    {"m": "M-02", "ProcessTime": 2},
                    {"m": "M-03", "ProcessTime": 13},
                    {"m": "M-04", "ProcessTime": 2},
                    {"m": "M-05", "ProcessTime": 9},
                    {"m": "M-06", "ProcessTime": 2},
                    {"m": "M-07", "ProcessTime": 14},
                    {"m": "M-08", "ProcessTime": 15},
                    {"m": "M-09", "ProcessTime": 2},
                    {"m": "M-10", "ProcessTime": 1},
                    {"m": "M-11", "ProcessTime": 5},
                ],
            },
            {
                "j": "Job-09",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 6},
                    {"m": "M-02", "ProcessTime": 9},
                    {"m": "M-03", "ProcessTime": 2},
                    {"m": "M-04", "ProcessTime": 17},
                    {"m": "M-05", "ProcessTime": 9},
                    {"m": "M-06", "ProcessTime": 2},
                    {"m": "M-07", "ProcessTime": 5},
                    {"m": "M-08", "ProcessTime": 9},
                    {"m": "M-09", "ProcessTime": 18},
                    {"m": "M-10", "ProcessTime": 12},
                    {"m": "M-11", "ProcessTime": 19},
                ],
            },
            {
                "j": "Job-10",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 14},
                    {"m": "M-02", "ProcessTime": 3},
                    {"m": "M-03", "ProcessTime": 5},
                    {"m": "M-04", "ProcessTime": 9},
                    {"m": "M-05", "ProcessTime": 3},
                    {"m": "M-06", "ProcessTime": 4},
                    {"m": "M-07", "ProcessTime": 1},
                    {"m": "M-08", "ProcessTime": 19},
                    {"m": "M-09", "ProcessTime": 12},
                    {"m": "M-10", "ProcessTime": 2},
                    {"m": "M-11", "ProcessTime": 14},
                ],
            },
            {
                "j": "Job-11",
                "Machines": [
                    {"m": "M-01", "ProcessTime": 16},
                    {"m": "M-02", "ProcessTime": 19},
                    {"m": "M-03", "ProcessTime": 9},
                    {"m": "M-04", "ProcessTime": 6},
                    {"m": "M-05", "ProcessTime": 10},
                    {"m": "M-06", "ProcessTime": 11},
                    {"m": "M-07", "ProcessTime": 18},
                    {"m": "M-08", "ProcessTime": 2},
                    {"m": "M-09", "ProcessTime": 6},
                    {"m": "M-10", "ProcessTime": 11},
                    {"m": "M-11", "ProcessTime": 8},
                ],
            },
        ]
    }
    return payload


def test_create_task(setup_test, create_payload):
    task_api = setup_test
    payload = create_payload
    out = task_api.create_task(
        app_name="test app task",
        app_version="0.1",
        service_name="JobSchedule",
        payload=payload,
    )
    assert out is not None


def test_get_tasks(setup_test):
    task_api = setup_test
    # yesterday = (datetime.now() - timedelta(days=1)).date().strftime("%Y-%m-%d")
    # tomorrow = (datetime.now() + timedelta(days=1)).date().strftime("%Y-%m-%d")
    out = task_api.get_tasks(app_name="test app task", app_version="0.1")
    assert out is not None


def test_get_task(setup_test, create_payload):
    # creat task
    task_api = setup_test
    payload = create_payload
    out = task_api.create_task(
        app_name="test app task",
        app_version="0.1",
        service_name="JobSchedule",
        payload=payload,
    )
    task_id = out["id"]
    out = task_api.get_task(task_id=task_id)
    assert out is not None


# ! does not work
# def test_interrupt_task(setup_test, create_payload):
#    # creat task
#    task_api = setup_test
#    payload = create_payload
#    out = task_api.create_task(
#        app_name="test app task",
#        app_version="0.1",
#        service_name="JobSchedule",
#        payload=payload,
#    )
#    task_id = out["id"]
#    out = task_api.interrupt_task(task_id=task_id)
#    assert out is not None


def test_delete_task(setup_test, create_payload):
    # creat task
    task_api = setup_test
    payload = create_payload
    out = task_api.create_task(
        app_name="test app task",
        app_version="0.1",
        service_name="JobSchedule",
        payload=payload,
    )
    task_id = out["id"]
    out = task_api.delete_task(task_id=task_id)
    assert out is not None


def test_get_task_response(setup_test, create_payload):
    # creat task
    task_api = setup_test
    payload = create_payload
    out = task_api.create_task(
        app_name="test app task",
        app_version="0.1",
        service_name="JobSchedule",
        payload=payload,
    )
    task_id = out["id"]
    # wait for 10 seconds
    time.sleep(10)
    running = True
    while running:
        out = task_api.get_task(task_id=task_id)
        if out["state"] == "completed":
            running = False
        time.sleep(5)
    out = task_api.get_task_response(task_id=task_id)
    assert out is not None
