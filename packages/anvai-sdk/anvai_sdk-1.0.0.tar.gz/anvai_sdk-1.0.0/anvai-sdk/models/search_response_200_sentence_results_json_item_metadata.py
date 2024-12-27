from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResponse200SentenceResultsJsonItemMetadata")


@_attrs_define
class SearchResponse200SentenceResultsJsonItemMetadata:
    """
    Attributes:
        source (Union[Unset, str]):  Example: Financial_Report_2024_Q1.pdf.
        page (Union[Unset, int]):  Example: 3.
        total_pages (Union[Unset, int]):  Example: 25.
    """

    source: Union[Unset, str] = UNSET
    page: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        page = self.page

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if page is not UNSET:
            field_dict["page"] = page
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        source = d.pop("source", UNSET)

        page = d.pop("page", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        search_response_200_sentence_results_json_item_metadata = cls(
            source=source,
            page=page,
            total_pages=total_pages,
        )

        search_response_200_sentence_results_json_item_metadata.additional_properties = d
        return search_response_200_sentence_results_json_item_metadata

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
