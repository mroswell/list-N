import re

from typing import Dict, Iterable, List

from datasette import hookimpl


SAFER_OR_TOXIC_QUERY_PATTERN = re.compile(r"Safer_or_Toxic=[^&]*")


FACET_SORTING_ORDER_MAP = {
    "Safer_or_Toxic": 1,
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

    If the `query_string` only contains `Safer_or_Toxic={value}`
    without `_facet=Safer_or_Toxic`, add the data (`name` and
    `toggle_url`). And in all of the other facets data, remove
    the `Safer_or_Toxic={value}` from the `toggle_url`.
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

    # Handle Safer_or_Toxic query string
    safer_or_toxic = "Safer_or_Toxic"
    match = SAFER_OR_TOXIC_QUERY_PATTERN.search(query_string)

    if match:
        if f"_facet={safer_or_toxic}" not in query_string:
            if safer_or_toxic not in cleaned_suggested_facets:
                sample_toggle_url = ""

                # Remove `Safer_or_Toxic={value}` references from all toggle_urls
                for _, facet_data in cleaned_suggested_facets.items():
                    if "toggle_url" in facet_data:
                        facet_data["toggle_url"] = (
                            SAFER_OR_TOXIC_QUERY_PATTERN.sub(
                                "", facet_data["toggle_url"]
                            )
                            .replace("?&", "?")
                            .replace("&&", "&")
                        )

                        if not sample_toggle_url:
                            sample_toggle_url = facet_data["toggle_url"]

                # Add `Safer_or_Toxic` facet data
                url, *_ = sample_toggle_url.partition("?")

                safer_or_toxic_query_string = (
                    SAFER_OR_TOXIC_QUERY_PATTERN.sub("", query_string)
                    .replace("?&", "?")
                    .replace("&&", "&")
                )

                query_sep = "" if safer_or_toxic_query_string.endswith("?") else "&"

                safer_or_toxic_query_string = (
                    f"{safer_or_toxic_query_string}{query_sep}_facet={safer_or_toxic}"
                )
                safer_or_toxic_toggle_url = f"{url}?{safer_or_toxic_query_string}"

                cleaned_suggested_facets[safer_or_toxic] = dict(
                    name=safer_or_toxic, toggle_url=safer_or_toxic_toggle_url
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
