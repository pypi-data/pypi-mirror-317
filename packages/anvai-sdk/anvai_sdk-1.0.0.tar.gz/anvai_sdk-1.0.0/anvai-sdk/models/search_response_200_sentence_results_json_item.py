from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_response_200_sentence_results_json_item_metadata import (
        SearchResponse200SentenceResultsJsonItemMetadata,
    )


T = TypeVar("T", bound="SearchResponse200SentenceResultsJsonItem")


@_attrs_define
class SearchResponse200SentenceResultsJsonItem:
    """
    Attributes:
        page_content (Union[Unset, str]):  Example: Revenue increased by 15% in Q1 2024 due to improved sales and
            customer retention efforts..
        metadata (Union[Unset, SearchResponse200SentenceResultsJsonItemMetadata]):
    """

    page_content: Union[Unset, str] = UNSET
    metadata: Union[Unset, "SearchResponse200SentenceResultsJsonItemMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page_content = self.page_content

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_content is not UNSET:
            field_dict["page_content"] = page_content
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_response_200_sentence_results_json_item_metadata import (
            SearchResponse200SentenceResultsJsonItemMetadata,
        )

        d = src_dict.copy()
        page_content = d.pop("page_content", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SearchResponse200SentenceResultsJsonItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SearchResponse200SentenceResultsJsonItemMetadata.from_dict(_metadata)

        search_response_200_sentence_results_json_item = cls(
            page_content=page_content,
            metadata=metadata,
        )

        search_response_200_sentence_results_json_item.additional_properties = d
        return search_response_200_sentence_results_json_item

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
