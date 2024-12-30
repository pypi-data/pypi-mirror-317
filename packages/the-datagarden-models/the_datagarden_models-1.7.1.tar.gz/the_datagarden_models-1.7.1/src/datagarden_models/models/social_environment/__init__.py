from pydantic import Field

from ..base import DataGardenModel, DataGardenModelLegends
from .local_facilities import LocalFacilities, LocalFacilitiesKeys


class SocialEnvironmentV1Keys(
    LocalFacilitiesKeys,
):
    LOCAL_FACILITIES = "local_facilities"
    DATAGARDEN_MODEL_NAME = "SocialEnvironment"


class SocialEnvironmentV1Legends(DataGardenModelLegends):
    MODEL_LEGEND = "Social environment data for a region. "
    LOCAL_FACILITIES = "Information about available of local facilities"


L = SocialEnvironmentV1Legends


class SocialEnvironmentV1(DataGardenModel):
    datagarden_model_version: str = Field("v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION)
    local_facilities: LocalFacilities = Field(default_factory=LocalFacilities, description=L.LOCAL_FACILITIES)
