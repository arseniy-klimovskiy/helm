from typing import Dict, List, Optional

from helm.benchmark.model_deployment_registry import (
    ModelDeployment,
    get_deployment_name_from_model_arg,
    get_model_deployment,
)
from helm.benchmark.model_metadata_registry import ModelMetadata
from helm.proxy.services.remote_service import RemoteService
from helm.proxy.services.service import GeneralInfo


_remote_deployment_registry: Dict[str, ModelDeployment] = {}


def get_remote_deployment(model_name: str) -> Optional[ModelDeployment]:
    """Returns a Model for the model_name."""
    return _remote_deployment_registry.get(model_name)


def check_and_register_remote_model(server_url: str, model_names: List[str]):
    try:
        service = RemoteService(server_url)
        info: GeneralInfo = service.get_general_info()
        models: Dict[str, ModelMetadata] = {}  # Associates a model name (not deployment) to a deployment.
        for model in info.all_models:
            models[model.name] = model
        for model_name in model_names:
            if model_name in models:
                metadata: ModelMetadata = models[model_name]
                model_deployment_name: str = get_deployment_name_from_model_arg(
                    metadata.name, can_return_empy=False, warn_arg_deprecated=False
                )
                deployment: ModelDeployment = get_model_deployment(model_deployment_name)
                _remote_deployment_registry[model_name] = deployment
            else:
                raise RuntimeError(f"remote service not contain {model_name}")
    except Exception as e:
        raise RuntimeError(f"check and register remote service error: {e}")
