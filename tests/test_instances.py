import pytest
from datacrunch_api.v1 import Instance, Instances


@pytest.fixture
def instances(mocker):
    mocker.patch("datacrunch_api.v1.instances.ApiSession")
    return Instances("dummy_client_id", "dummy_client_secret")


def test_get_instance(mocker, instances):
    instance_id = "test-instance-id"
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = {"id": "123", "name": "instance1"}

    result = instances.get_instance(instance_id)
    assert result == {"id": "123", "name": "instance1"}
    mock_session.get.assert_called_once_with(f"instances/{instance_id}")


def test_delete_instance(mocker, instances):
    instance_id = "test-instance-id"
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.put_raw.return_value.status_code = 202

    instances.delete_instance(instance_id)

    mock_session.put_raw.assert_called_once_with(
        f"instances",
        json={"action": "delete", "instance_id": instance_id},
    )


def test_deploy_instance(mocker, instances):
    instance = Instance(
        description="test-description",
        hostname="test-hostname",
        image="test-image",
        instance_type="test-instance-type",
        location_code="test-location-code",
    )
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.post.return_value = "123"

    result = instances.deploy(instance)
    assert result == "123"
    mock_session.post.assert_called_once_with("instances", json=instance.to_dict())


def test_get_instance_availabilities(mocker, instances):
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = [
        {
            "id": "123",
            "name": "startup-script1",
            "script": "#!/bin/bash\necho 'Hello, World!'",
        }
    ]
    result = instances.get_instance_type_availabilities()

    assert result == [
        {
            "id": "123",
            "name": "startup-script1",
            "script": "#!/bin/bash\necho 'Hello, World!'",
        }
    ]
    mock_session.get.assert_called_once_with("instance-availability?")


def test_get_instance_type_availability(mocker, instances):
    instance_type = "test-instance-type"
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = True
    result = instances.get_instance_type_availability(instance_type)

    assert result == True
    mock_session.get.assert_called_once_with(
        "instance-availability/test-instance-type?"
    )


def test_list_instance_types(mocker, instances):
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
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = expected_response

    result = instances.list_instance_types()

    assert result == expected_response
    mock_session.get.assert_called_once_with("instance-types?currency=EUR")


def test_list_instances(mocker, instances):
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "instance1"},
        {"id": "456", "name": "instance2"},
    ]

    result = instances.list_instances()
    assert result == [
        {"id": "123", "name": "instance1"},
        {"id": "456", "name": "instance2"},
    ]
    mock_session.get.assert_called_once_with("instances")


def test_list_locations(mocker, instances):
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "location1"},
        {"id": "456", "name": "location2"},
    ]

    result = instances.list_locations()
    assert result == [
        {"id": "123", "name": "location1"},
        {"id": "456", "name": "location2"},
    ]


def test_list_long_term_periods(mocker, instances):
    mock_session = mocker.patch.object(instances, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "period1"},
        {"id": "456", "name": "period2"},
    ]

    result = instances.list_long_term_periods()
    assert result == [
        {"id": "123", "name": "period1"},
        {"id": "456", "name": "period2"},
    ]
