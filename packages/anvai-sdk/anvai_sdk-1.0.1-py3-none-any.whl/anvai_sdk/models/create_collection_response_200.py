from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_collection_response_200_files_item import CreateCollectionResponse200FilesItem


T = TypeVar("T", bound="CreateCollectionResponse200")


@_attrs_define
class CreateCollectionResponse200:
    """
    Attributes:
        id (Union[Unset, int]):  Example: 101.
        name (Union[Unset, str]):  Example: Banking Insights.
        user (Union[Unset, int]):  Example: 501.
        files (Union[Unset, list['CreateCollectionResponse200FilesItem']]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    user: Union[Unset, int] = UNSET
    files: Union[Unset, list["CreateCollectionResponse200FilesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        user = self.user

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if user is not UNSET:
            field_dict["user"] = user
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_collection_response_200_files_item import CreateCollectionResponse200FilesItem

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        user = d.pop("user", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = CreateCollectionResponse200FilesItem.from_dict(files_item_data)

            files.append(files_item)

        create_collection_response_200 = cls(
            id=id,
            name=name,
            user=user,
            files=files,
        )

        create_collection_response_200.additional_properties = d
        return create_collection_response_200

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
