from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class LocalFacilitiesKeys:
    UNIT = "unit"
    DISTANCE_TO_NEAREST = "distance_to_nearest"


class LocalFacilitiesLegends:
    UNIT = "Unit used in the distance_to field"
    DISTANCE_TO_NEAREST = "Distance to the nearest loaction for a facility type"


L = LocalFacilitiesLegends


class LocalFacilities(DataGardenSubModel):
    unit: str = Field(default="km", description=L.UNIT)
    distance_to_nearest: dict[str, float] = Field(default=dict, description=L.DISTANCE_TO_NEAREST)

    class Meta:
        exclude_fields_in_has_values_check = [
            "unit",
        ]
