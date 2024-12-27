from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSummaryResponse200")


@_attrs_define
class GetSummaryResponse200:
    """
    Attributes:
        summary (Union[Unset, list[str]]):  Example: ["The financial report highlights the organization's revenue growth
            of 15% in Q1 2024.", 'Key expenses include marketing and technology investments, with a focus on customer
            acquisition.'].
        summary_length (Union[Unset, int]):  Example: 2.
        summary_ratio (Union[Unset, float]):  Example: 0.05.
        no_of_words_in_file (Union[Unset, int]):  Example: 2000.
        no_of_summary_tokens (Union[Unset, int]):  Example: 100.
    """

    summary: Union[Unset, list[str]] = UNSET
    summary_length: Union[Unset, int] = UNSET
    summary_ratio: Union[Unset, float] = UNSET
    no_of_words_in_file: Union[Unset, int] = UNSET
    no_of_summary_tokens: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary: Union[Unset, list[str]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary

        summary_length = self.summary_length

        summary_ratio = self.summary_ratio

        no_of_words_in_file = self.no_of_words_in_file

        no_of_summary_tokens = self.no_of_summary_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if summary_length is not UNSET:
            field_dict["summary_length"] = summary_length
        if summary_ratio is not UNSET:
            field_dict["summary_ratio"] = summary_ratio
        if no_of_words_in_file is not UNSET:
            field_dict["no_of_words_in_file"] = no_of_words_in_file
        if no_of_summary_tokens is not UNSET:
            field_dict["no_of_summary_tokens"] = no_of_summary_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        summary = cast(list[str], d.pop("summary", UNSET))

        summary_length = d.pop("summary_length", UNSET)

        summary_ratio = d.pop("summary_ratio", UNSET)

        no_of_words_in_file = d.pop("no_of_words_in_file", UNSET)

        no_of_summary_tokens = d.pop("no_of_summary_tokens", UNSET)

        get_summary_response_200 = cls(
            summary=summary,
            summary_length=summary_length,
            summary_ratio=summary_ratio,
            no_of_words_in_file=no_of_words_in_file,
            no_of_summary_tokens=no_of_summary_tokens,
        )

        get_summary_response_200.additional_properties = d
        return get_summary_response_200

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
