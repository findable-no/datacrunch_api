import pytest
from datacrunch_api.v1 import (
    AutoUpdate,
    Compute,
    Container,
    ContainerRegistrySettings,
    Deployments,
    Deployment,
    Environment,
    HealthCheck,
    QueueLoad,
    Scaling,
    ScalingPolicy,
    ScalingTriggers,
    VolumeMounts,
)


@pytest.fixture
def deployments(mocker):
    mocker.patch("datacrunch_api.v1.deployments.ApiSession")
    return Deployments("dummy_client_id", "dummy_client_secret")


@pytest.fixture
def deployment() -> Deployment:
    return Deployment(
        name="test-deployment",
        compute=Compute(
            name=Compute.Names.GENERAL,
        ),
        container_registry_settings=ContainerRegistrySettings(
            is_private=False,
        ),
        containers=[
            Container(
                autoupdate=AutoUpdate(enabled=True, mode="latest"),
                environment=Environment(),
                healthcheck=HealthCheck(
                    enabled=True,
                    path="/health",
                    port=8000,
                ),
                name="test-container",
                image="test-image:latest",
                exposed_port=8000,
                volume_mounts=VolumeMounts([]),
            )
        ],
        scaling=Scaling(
            min_replica_count=1,
            max_replica_count=10,
            queue_message_ttl_seconds=100,
            concurrent_requests_per_replica=10,
            scale_down_policy=ScalingPolicy(delay_seconds=10),
            scale_up_policy=ScalingPolicy(delay_seconds=10),
            scaling_triggers=ScalingTriggers(queue_load=QueueLoad(threshold=100)),
        ),
    )


@pytest.fixture
def scaling() -> Scaling:
    return Scaling(
        min_replica_count=1,
        max_replica_count=10,
        queue_message_ttl_seconds=100,
        concurrent_requests_per_replica=10,
        scale_down_policy=ScalingPolicy(delay_seconds=10),
        scale_up_policy=ScalingPolicy(delay_seconds=10),
        scaling_triggers=ScalingTriggers(queue_load=QueueLoad(threshold=100)),
    )


def test_list_container_deployments(mocker, deployments):
    expected_response = [
        {
            "id": "deploy-1",
            "name": "test-deployment-1",
            "status": "running",
            "created_at": "2024-01-01T00:00:00Z",
        },
        {
            "id": "deploy-2",
            "name": "test-deployment-2",
            "status": "stopped",
            "created_at": "2024-01-01T00:00:00Z",
        },
    ]
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_response

    result = deployments.list_container_deployments()

    assert result == expected_response
    mock_session.get.assert_called_once_with("container-deployments")


def test_get_container_deployment(mocker, deployments):
    deployment_id = "test-deploy-id"
    expected_response = {
        "id": deployment_id,
        "name": "test-deployment",
        "status": "running",
        "created_at": "2024-01-01T00:00:00Z",
    }
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_response

    result = deployments.get_container_deployment(deployment_id)

    assert result == expected_response
    mock_session.get.assert_called_once_with(f"container-deployments/{deployment_id}")


def test_create_container_deployment(mocker, deployments, deployment):
    expected_response = {
        "id": "new-deploy-id",
        "name": deployment.name,
        "status": "creating",
    }
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post.return_value = expected_response

    result = deployments.create_container_deployment(deployment)

    assert result == expected_response
    mock_session.post.assert_called_once_with(
        "container-deployments", json=deployment.to_dict()
    )


def test_update_deployment(mocker, deployments, deployment):
    deployment_id = "test-deploy-id"
    expected_response = {
        "id": deployment_id,
        "name": deployment.name,
        "status": "updating",
    }
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.patch.return_value = expected_response

    result = deployments.update_container_deployment(deployment_id, deployment)

    assert result == expected_response
    mock_session.patch.assert_called_once_with(
        f"container-deployments/{deployment_id}", json=deployment.to_dict()
    )


def test_delete_deployment(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.delete.return_value.status_code = 204

    deployments.delete_container_deployment(deployment_id)

    mock_session.delete.assert_called_once_with(
        f"container-deployments/{deployment_id}"
    )


def test_restart_deployment(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post_raw.return_value.status_code = 201

    deployments.restart_deployment(deployment_id)

    mock_session.post_raw.assert_called_once_with(
        f"container-deployments/{deployment_id}/restart",
        json={},
    )


def test_get_deployment_status(mocker, deployments):
    deployment_id = "test-deploy-id"
    expected_status = {"status": "running"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_status

    result = deployments.get_deployment_status(deployment_id)

    assert result == expected_status
    mock_session.get.assert_called_once_with(
        f"container-deployments/{deployment_id}/status"
    )


def test_get_deployment_scaling(mocker, deployments):
    deployment_id = "test-deploy-id"
    expected_scaling = {"status": "running"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_scaling

    result = deployments.get_deployment_scaling(deployment_id)

    assert result == expected_scaling
    mock_session.get.assert_called_once_with(
        f"container-deployments/{deployment_id}/scaling"
    )


def test_get_deployment_replicas(mocker, deployments):
    deployment_id = "test-deploy-id"
    expected_replicas = {"status": "running"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_replicas

    result = deployments.get_deployment_replicas(deployment_id)

    assert result == expected_replicas
    mock_session.get.assert_called_once_with(
        f"container-deployments/{deployment_id}/replicas"
    )


def test_get_environment_variables(mocker, deployments):
    deployment_id = "test-deploy-id"
    expected_environment_variables = {"status": "running"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.get.return_value = expected_environment_variables

    result = deployments.get_environment_variables(deployment_id)

    assert result == expected_environment_variables
    mock_session.get.assert_called_once_with(
        f"container-deployments/{deployment_id}/environment-variables"
    )


def test_update_deployment_scaling(mocker, deployments, scaling):
    deployment_id = "test-deploy-id"
    scaling_config = scaling.to_dict()
    expected_response = {"status": "updating"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.patch.return_value = expected_response

    result = deployments.update_deployment_scaling(deployment_id, scaling_config)

    assert result == expected_response
    mock_session.patch.assert_called_once_with(
        f"container-deployments/{deployment_id}/scaling",
        json=scaling_config,
    )


def test_purge_deployment_queue(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post.return_value = {"status": "updating"}

    result = deployments.purge_deployment_queue(deployment_id)

    assert result == {"status": "updating"}
    mock_session.post.assert_called_once_with(
        f"container-deployments/{deployment_id}/purge-queue",
        json={},
    )


def test_pause_deployment(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post.return_value = {"status": "updating"}

    result = deployments.pause_deployment(deployment_id)

    assert result == {"status": "updating"}
    mock_session.post.assert_called_once_with(
        f"container-deployments/{deployment_id}/pause",
        json={},
    )


def test_resume_deployment(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post.return_value = {"status": "updating"}

    result = deployments.resume_deployment(deployment_id)

    assert result == {"status": "updating"}
    mock_session.post.assert_called_once_with(
        f"container-deployments/{deployment_id}/resume",
        json={},
    )


def test_create_environment_variables(mocker, deployments):
    deployment_id = "test-deploy-id"
    environment_variables = {"status": "updating"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.post.return_value = environment_variables

    result = deployments.create_environment_variables(
        deployment_id, environment_variables
    )

    assert result == environment_variables
    mock_session.post.assert_called_once_with(
        f"container-deployments/{deployment_id}/environment-variables",
        json=environment_variables,
    )


def test_update_environment_variables(mocker, deployments):
    deployment_id = "test-deploy-id"
    environment_variables = {"status": "updating"}
    mock_session = mocker.patch.object(deployments, "api_session")
    mock_session.patch.return_value = environment_variables

    result = deployments.update_environment_variables(
        deployment_id, environment_variables
    )

    assert result == environment_variables
    mock_session.patch.assert_called_once_with(
        f"container-deployments/{deployment_id}/environment-variables",
        json=environment_variables,
    )


def test_delete_environment_variables(mocker, deployments):
    deployment_id = "test-deploy-id"
    mock_session = mocker.patch.object(deployments, "api_session")

    deployments.delete_environment_variables(deployment_id)

    mock_session.delete.assert_called_once_with(
        f"container-deployments/{deployment_id}/environment-variables"
    )


def test_validate_response(deployments):
    response = {"status": "updating"}
    assert deployments.validate_response(response) == response

    error_response = {"code": "invalid_request", "message": "Invalid request"}
    with pytest.raises(Deployments.InvalidRequest):
        deployments.validate_response(error_response)

    success_response = {"code": "success", "status": "updating"}
    assert deployments.validate_response(success_response) == success_response
