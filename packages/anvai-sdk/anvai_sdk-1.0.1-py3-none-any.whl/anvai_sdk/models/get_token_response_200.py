from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetTokenResponse200")


@_attrs_define
class GetTokenResponse200:
    """
    Attributes:
        refresh (Union[Unset, str]):  Example: eyJhbGciOiJIfgiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo
            xNzAp0aSI6Ijc5YzZmNTU3MzJjMDQyNzdiNTI1OTUyMzc3NWY1ZTA3IiwidXNlcl9pZCI6MX0.8pM59gbeWnbS4wpRT7suKESKWi8CnkVLGOsHBK
            K-IAasad.
        access (Union[Unset, str]):  Example: eyJhbGciOiJIUzI1NiIgfXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAp0aS
            I6Ijc5YzZmNTU3MzJjMDQyNzdiNTI1OTUyMzc3NWY1ZTA3IiwidXNlcl9pZCI6MX0.8pM59gbeWnbS4wpRT7suKESKWi8CnkVLGOsHBKK-
            IAasad.
    """

    refresh: Union[Unset, str] = UNSET
    access: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        refresh = self.refresh

        access = self.access

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if refresh is not UNSET:
            field_dict["refresh"] = refresh
        if access is not UNSET:
            field_dict["access"] = access

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        refresh = d.pop("refresh", UNSET)

        access = d.pop("access", UNSET)

        get_token_response_200 = cls(
            refresh=refresh,
            access=access,
        )

        get_token_response_200.additional_properties = d
        return get_token_response_200

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
