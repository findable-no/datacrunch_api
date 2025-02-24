import pytest
from datacrunch_api.v1 import StartupScript, StartupScripts


@pytest.fixture
def startup_scripts(mocker):
    mocker.patch("datacrunch_api.v1.startup_scripts.ApiSession")
    return StartupScripts("dummy_client_id", "dummy_client_secret")


def test_add_startup_script(mocker, startup_scripts):
    startup_script = StartupScript(
        name="new-startup-script", script="#!/bin/bash\necho 'Hello, World!'"
    )
    mock_session = mocker.patch.object(startup_scripts, "api_session")
    mock_session.post_raw.return_value.status_code = 201

    startup_scripts.add_startup_script(startup_script)

    mock_session.post_raw.assert_called_once_with(
        "scripts", json=startup_script.to_dict()  # type: ignore
    )


def test_delete_startup_script(mocker, startup_scripts):
    startup_script_id = "test-startup-script-id"
    mock_session = mocker.patch.object(startup_scripts, "api_session")
    mock_session.delete.return_value.status_code = 200

    startup_scripts.delete_startup_script(startup_script_id)

    mock_session.delete.assert_called_once_with(f"scripts/{startup_script_id}")


def test_delete_startup_scripts(mocker, startup_scripts):
    startup_script_ids = ["test-startup-script-id-1", "test-startup-script-id-2"]
    mock_session = mocker.patch.object(startup_scripts, "api_session")
    mock_session.delete.return_value.status_code = 200

    startup_scripts.delete_startup_scripts(startup_script_ids)

    mock_session.delete.assert_called_once_with(
        "scripts", json={"scripts": startup_script_ids}  # type: ignore
    )


def test_get_startup_script(mocker, startup_scripts):
    startup_script_id = "test-startup-script-id"
    mock_session = mocker.patch.object(startup_scripts, "api_session")
    mock_session.get.return_value = {
        "id": "123",
        "name": "startup-script1",
        "script": "#!/bin/bash\necho 'Hello, World!'",
    }
    result = startup_scripts.get_startup_script(startup_script_id)

    assert result == {
        "id": "123",
        "name": "startup-script1",
        "script": "#!/bin/bash\necho 'Hello, World!'",
    }


def test_list_startup_scripts(mocker, startup_scripts):
    expected_response = [
        {
            "id": "123",
            "name": "startup-script1",
            "script": "#!/bin/bash\necho 'Hello, World!'",
        },
        {
            "id": "456",
            "name": "startup-script2",
            "script": "#!/bin/bash\necho 'Hello, World!'",
        },
    ]
    mock_session = mocker.patch.object(startup_scripts, "api_session")
    mock_session.get.return_value = expected_response

    result = startup_scripts.list_startup_scripts()

    assert result == expected_response
    mock_session.get.assert_called_once_with("scripts")
