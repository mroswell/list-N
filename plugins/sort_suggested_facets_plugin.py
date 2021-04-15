from typing import Dict, Iterable, List

from datasette import hookimpl


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
    suggested_facets: List[Dict[str, str]]
) -> Iterable[Dict[str, str]]:
    """Remove duplicate facets. In case of duplicate, keep
    only the facet containing `_facet_array={facet_name}`
    query string in `toggle_url`, ignoring ones containing
    `_facet={facet_name}`.
    """

    cleaned_suggested_facets = {}

    for facet_data in suggested_facets:
        facet_name = facet_data.get("name")
        toggle_url = facet_data.get("toggle_url", "")

        query_string = f"_facet_array={facet_name}"
        if query_string in toggle_url:
            cleaned_suggested_facets[facet_name] = facet_data
            continue

        if facet_name not in cleaned_suggested_facets:
            cleaned_suggested_facets[facet_name] = facet_data

    return cleaned_suggested_facets.values()


def get_sorted_suggested_facets(
    suggested_facets: List[Dict[str, str]]
) -> List[Dict[str, str]]:

    cleaned_suggested_facets = _get_cleaned_suggested_facets(suggested_facets)

    sorted_suggested_facets = sorted(
        cleaned_suggested_facets, key=_get_facet_sort_order
    )

    return sorted_suggested_facets


@hookimpl
def prepare_jinja2_environment(env):

    env.filters["sort_facets"] = get_sorted_suggested_facets
