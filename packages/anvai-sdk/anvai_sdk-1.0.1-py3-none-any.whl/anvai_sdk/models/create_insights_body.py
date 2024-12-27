from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInsightsBody")


@_attrs_define
class CreateInsightsBody:
    """
    Attributes:
        task_to_run (Union[Unset, str]): Comma-separated list of tasks to execute. task list `enable_search`,
            `generate_summary` Example: enable_search,generate_summary.
    """

    task_to_run: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        task_to_run = self.task_to_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if task_to_run is not UNSET:
            field_dict["task_to_run"] = task_to_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        task_to_run = d.pop("task_to_run", UNSET)

        create_insights_body = cls(
            task_to_run=task_to_run,
        )

        create_insights_body.additional_properties = d
        return create_insights_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
