from typing import Optional

from pydantic import BaseModel, validator

from akride import Constants
from akride.core.enums import DataType
from akride.core.exceptions import UserError


class SourceContainerData(BaseModel):
    id: str


class CreateDatasetIn(BaseModel):
    dataset_name: str
    dataset_namespace: str = "default"
    data_type: DataType = DataType.IMAGE
    glob_pattern: str = Constants.DEFAULT_IMAGE_BLOB_EXPR
    overwrite: bool = False
    sample_frame_rate: float = -1

    source_container_data: Optional[SourceContainerData] = None

    @validator("sample_frame_rate", always=True)
    def validate_frame_rate(cls, v: float, values) -> float:
        data_type = values.get("data_type")
        sample_frame_rate = v

        if data_type == DataType.IMAGE and sample_frame_rate != -1:
            raise UserError(
                message="Sample frame rate is not applicable for image datasets!",
            )

        return v

    @validator("glob_pattern", always=True)
    def set_glob_pattern(cls, v: str, values) -> str:
        data_type = values.get("data_type")
        glob_pattern = v

        if (
            data_type == DataType.VIDEO
            and glob_pattern == Constants.DEFAULT_IMAGE_BLOB_EXPR
        ):
            glob_pattern = Constants.DEFAULT_VIDEO_BLOB_EXPR

        return glob_pattern
