import re

from typing import Dict, Iterable, List

from datasette import hookimpl


RISK_LEVEL_QUERY_PATTERN = re.compile(r"Risk_level=[^&]*")


FACET_SORTING_ORDER_MAP = {
    "Risk_level": 1,
    "Active_ingredient": 2,
    "Use_site": 3,
    "Surface_type": 4,
    "Contact_time": 5,
    "Formulation_type": 6,
    "Date_on_List_N": 7,
    "Why_on_List_N": 8,
}


def _get_facet_sort_order(facet_data: Dict[str, str]) -> int:

    facet_name = facet_data.get("name")

    return FACET_SORTING_ORDER_MAP.get(facet_name, len(FACET_SORTING_ORDER_MAP) + 1)


def _get_cleaned_suggested_facets(
    suggested_facets: List[Dict[str, str]], query_string: str
) -> Iterable[Dict[str, str]]:
    """Cleaning operations:

    Remove duplicate facets. In case of duplicate, keep
    only the facet containing `_facet_array={facet_name}`
    query string in `toggle_url`, ignoring ones containing
    `_facet={facet_name}`.

    If the `query_string` only contains `Risk_level={value}`
    without `_facet=Risk_level`, add the data (`name` and
    `toggle_url`). And in all of the other facets data, remove
    the `Risk_level={value}` from the `toggle_url`.
    """

    cleaned_suggested_facets = {}

    # Handle duplicate facets
    for facet_data in suggested_facets:
        facet_name = facet_data.get("name")
        toggle_url = facet_data.get("toggle_url", "")

        _query_string = f"_facet_array={facet_name}"
        if _query_string in toggle_url:
            cleaned_suggested_facets[facet_name] = facet_data
            continue

        if facet_name not in cleaned_suggested_facets:
            cleaned_suggested_facets[facet_name] = facet_data

    # Handle Risk_level query string
    risk_level = "Risk_level"
    match = RISK_LEVEL_QUERY_PATTERN.search(query_string)

    if match:
        if f"_facet={risk_level}" not in query_string:
            if risk_level not in cleaned_suggested_facets:
                sample_toggle_url = ""

                # Remove `Risk_level={value}` references from all toggle_urls
                for _, facet_data in cleaned_suggested_facets.items():
                    if "toggle_url" in facet_data:
                        facet_data["toggle_url"] = (
                            RISK_LEVEL_QUERY_PATTERN.sub(
                                "", facet_data["toggle_url"]
                            )
                            .replace("?&", "?")
                            .replace("&&", "&")
                        )

                        if not sample_toggle_url:
                            sample_toggle_url = facet_data["toggle_url"]

                # Add `Risk_level` facet data
                url, *_ = sample_toggle_url.partition("?")

                risk_query_string = (
                    RISK_LEVEL_QUERY_PATTERN.sub("", query_string)
                    .replace("?&", "?")
                    .replace("&&", "&")
                )

                query_sep = "" if risk_query_string.endswith("?") else "&"

                risk_query_string = (
                    f"{risk_query_string}{query_sep}_facet={risk_level}"
                )
                risk_toggle_url = f"{url}?{risk_query_string}"

                cleaned_suggested_facets[risk_level] = dict(
                    name=risk_level, toggle_url=risk_toggle_url
                )

    if (
        risk_level not in cleaned_suggested_facets
        and f"_facet={risk_level}" not in query_string
    ):
        first_element = next(iter(cleaned_suggested_facets.values()), None)
        if first_element:

            _toggle_url = first_element.get("toggle_url")
            if _toggle_url:
                _toggle_url = re.sub(r"&[^&]*$", "", _toggle_url)
                risk_toggle_url = f"{_toggle_url}&_facet={risk_level}".replace(
                    "?&", "?"
                ).replace(
                    "&&", "&"
                )

                cleaned_suggested_facets[risk_level] = dict(
                    name=risk_level, toggle_url=risk_toggle_url
                )

    return cleaned_suggested_facets.values()


def get_sorted_suggested_facets(
    suggested_facets: List[Dict[str, str]], query_string: str
) -> List[Dict[str, str]]:

    cleaned_suggested_facets = _get_cleaned_suggested_facets(
        suggested_facets, query_string
    )

    sorted_suggested_facets = sorted(
        cleaned_suggested_facets, key=_get_facet_sort_order
    )

    return sorted_suggested_facets


@hookimpl
def prepare_jinja2_environment(env):

    env.filters["sort_facets"] = get_sorted_suggested_facets
