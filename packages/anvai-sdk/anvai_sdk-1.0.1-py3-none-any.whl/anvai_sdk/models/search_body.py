from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_body_search_type import SearchBodySearchType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchBody")


@_attrs_define
class SearchBody:
    """
    Attributes:
        collection_id (Union[Unset, int]):  Example: 101.
        question (Union[Unset, str]):  Example: What are the key trends in Q1 2024 financial reports?.
        search_type (Union[Unset, SearchBodySearchType]):  Example: CS.
        file_name (Union[Unset, str]): (Optional) File name to limit the scope of the search. Example:
            Financial_Report_2024_Q1.pdf.
    """

    collection_id: Union[Unset, int] = UNSET
    question: Union[Unset, str] = UNSET
    search_type: Union[Unset, SearchBodySearchType] = UNSET
    file_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        collection_id = self.collection_id

        question = self.question

        search_type: Union[Unset, str] = UNSET
        if not isinstance(self.search_type, Unset):
            search_type = self.search_type.value

        file_name = self.file_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if collection_id is not UNSET:
            field_dict["collection_id"] = collection_id
        if question is not UNSET:
            field_dict["question"] = question
        if search_type is not UNSET:
            field_dict["search_type"] = search_type
        if file_name is not UNSET:
            field_dict["file_name"] = file_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_id = d.pop("collection_id", UNSET)

        question = d.pop("question", UNSET)

        _search_type = d.pop("search_type", UNSET)
        search_type: Union[Unset, SearchBodySearchType]
        if isinstance(_search_type, Unset):
            search_type = UNSET
        else:
            search_type = SearchBodySearchType(_search_type)

        file_name = d.pop("file_name", UNSET)

        search_body = cls(
            collection_id=collection_id,
            question=question,
            search_type=search_type,
            file_name=file_name,
        )

        search_body.additional_properties = d
        return search_body

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
