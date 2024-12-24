# aimmscloud

The aimmscloud Python library is a lightweight library to make calls to the AIMMS Cloud rest API. You can use this library to publish AIMMS applications and execute tasks.

- [Getting Started](#getting-started)
- [Publish an app](#publish-an-app)
- [Create and run a task](#create-and-run-a-task)
- [Further development](#further-development)

## Getting Started

Run the following command to install the aimmscloud library:

```shell
pip install aimmscloud
```

After installation you first need to provide a HOST_URL and an API_KEY before you can make any calls. 


```python
from aimmscloud.aimms_application import Application

app_api = Application(
    host_url="https://<accountname>.aimms.cloud/pro-api/v2",
    api_key="<API_KEY>",
)
```

## Publish an app

You can publish an app by building an AIMMSpack using the AIMMS IDE. When publishing an app you need to provide metadata such as the applicationname and version.

```python
app_api.publish_app(
    file_name="example.aimmspack",
    iconfile_name="icon.png",
    aimms_version="<aimms version to use>",
    application_description="<app description>",
    application_name="<app name>",
    application_version="<app version>",
    attributes={
        "isWebUI": "true",
        "ServerLicense": "Default",
    },
    projectCategory="<app category>",
    publish_behavior=0,
)
```

## Create and run a task

When you app is published you can run tasks with the create_task call. Note tasks are only available if you registered a task as an service in DEX. The payload variable is optional and only needs to be used when your task expects an input. Inputs are passed as an Python dictionary.

```python
task_api = Task(
    host_url="https://<accountname>.aimms.cloud/pro-api/v2",
    api_key="<API_KEY>",
)

out = task_api.create_task(
    app_name="<app name>",
    app_version="<app version>",
    service_name="<DEX service name>",
    payload=payload,
)
```

If your task has a response, for example the result data of the optimization such as a schedule, you can retrieve this with the following call once the task is complete.

```python
out = task_api.get_task_response(task_id=task_id)
```

## Further development

This project is under active development by AIMMS bv.