from typing import Dict, Optional

from akridata_akrimanager_v2 import DockerImageReq


def get_featurizer_docker_image_request(
    name: str,
    namespace: str,
    description: str,
    repository_id: str,
    image_name: str,
    image_tag: str,
    filter_type: str,
    command: str,
    properties: Dict[str, int],
    gpu_filter: Optional[bool] = None,
    gpu_mem_fraction: Optional[float] = None,
    allow_no_gpu: bool = True,
) -> DockerImageReq:
    return DockerImageReq(
        name=name,
        namespace=namespace,
        repository_id=repository_id,
        image_name=image_name,
        image_tag=image_tag,
        filter_type=filter_type,
        gpu_filter=gpu_filter,
        gpu_mem_fraction=gpu_mem_fraction,
        allow_no_gpu=allow_no_gpu,
        properties=properties,
        command=command,
        description=description,
    )
