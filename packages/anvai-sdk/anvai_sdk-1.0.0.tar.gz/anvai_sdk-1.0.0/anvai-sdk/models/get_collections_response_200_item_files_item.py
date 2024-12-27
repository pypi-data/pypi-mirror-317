import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCollectionsResponse200ItemFilesItem")


@_attrs_define
class GetCollectionsResponse200ItemFilesItem:
    """
    Attributes:
        id (Union[Unset, int]):  Example: 1001.
        collection (Union[Unset, int]):  Example: 101.
        file_type (Union[Unset, str]):  Example: raw.
        file_name (Union[Unset, str]):  Example: Financial_Report_2024_Q1.pdf.
        file_size (Union[Unset, int]):  Example: 2048576.
        file_kind (Union[Unset, str]):  Example: pdf.
        uploaded_date (Union[Unset, datetime.datetime]):  Example: 2024-01-15T10:30:00.000Z.
    """

    id: Union[Unset, int] = UNSET
    collection: Union[Unset, int] = UNSET
    file_type: Union[Unset, str] = UNSET
    file_name: Union[Unset, str] = UNSET
    file_size: Union[Unset, int] = UNSET
    file_kind: Union[Unset, str] = UNSET
    uploaded_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        collection = self.collection

        file_type = self.file_type

        file_name = self.file_name

        file_size = self.file_size

        file_kind = self.file_kind

        uploaded_date: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded_date, Unset):
            uploaded_date = self.uploaded_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if collection is not UNSET:
            field_dict["collection"] = collection
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if file_size is not UNSET:
            field_dict["file_size"] = file_size
        if file_kind is not UNSET:
            field_dict["file_kind"] = file_kind
        if uploaded_date is not UNSET:
            field_dict["uploaded_date"] = uploaded_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        collection = d.pop("collection", UNSET)

        file_type = d.pop("file_type", UNSET)

        file_name = d.pop("file_name", UNSET)

        file_size = d.pop("file_size", UNSET)

        file_kind = d.pop("file_kind", UNSET)

        _uploaded_date = d.pop("uploaded_date", UNSET)
        uploaded_date: Union[Unset, datetime.datetime]
        if isinstance(_uploaded_date, Unset):
            uploaded_date = UNSET
        else:
            uploaded_date = isoparse(_uploaded_date)

        get_collections_response_200_item_files_item = cls(
            id=id,
            collection=collection,
            file_type=file_type,
            file_name=file_name,
            file_size=file_size,
            file_kind=file_kind,
            uploaded_date=uploaded_date,
        )

        get_collections_response_200_item_files_item.additional_properties = d
        return get_collections_response_200_item_files_item

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
