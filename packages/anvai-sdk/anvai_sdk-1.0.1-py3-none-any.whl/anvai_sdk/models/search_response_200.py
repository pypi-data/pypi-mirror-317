from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_response_200_sentence_results_json_item import SearchResponse200SentenceResultsJsonItem


T = TypeVar("T", bound="SearchResponse200")


@_attrs_define
class SearchResponse200:
    """
    Attributes:
        sentence_results_json (Union[Unset, list['SearchResponse200SentenceResultsJsonItem']]):
    """

    sentence_results_json: Union[Unset, list["SearchResponse200SentenceResultsJsonItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sentence_results_json: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sentence_results_json, Unset):
            sentence_results_json = []
            for sentence_results_json_item_data in self.sentence_results_json:
                sentence_results_json_item = sentence_results_json_item_data.to_dict()
                sentence_results_json.append(sentence_results_json_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sentence_results_json is not UNSET:
            field_dict["sentence_results_json"] = sentence_results_json

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_response_200_sentence_results_json_item import SearchResponse200SentenceResultsJsonItem

        d = src_dict.copy()
        sentence_results_json = []
        _sentence_results_json = d.pop("sentence_results_json", UNSET)
        for sentence_results_json_item_data in _sentence_results_json or []:
            sentence_results_json_item = SearchResponse200SentenceResultsJsonItem.from_dict(
                sentence_results_json_item_data
            )

            sentence_results_json.append(sentence_results_json_item)

        search_response_200 = cls(
            sentence_results_json=sentence_results_json,
        )

        search_response_200.additional_properties = d
        return search_response_200

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
