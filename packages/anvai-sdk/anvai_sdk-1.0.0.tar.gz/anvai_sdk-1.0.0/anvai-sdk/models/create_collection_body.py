from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="CreateCollectionBody")


@_attrs_define
class CreateCollectionBody:
    """
    Attributes:
        name (Union[Unset, str]): Name of the collection.
        files (Union[Unset, File]): File to upload.
    """

    name: Union[Unset, str] = UNSET
    files: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        files: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        files: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _files = d.pop("files", UNSET)
        files: Union[Unset, File]
        if isinstance(_files, Unset):
            files = UNSET
        else:
            files = File(payload=BytesIO(_files))

        create_collection_body = cls(
            name=name,
            files=files,
        )

        create_collection_body.additional_properties = d
        return create_collection_body

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
