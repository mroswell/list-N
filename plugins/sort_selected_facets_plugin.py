from typing import Dict, List, Any

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


def get_sorted_selected_facets(
    selected_facets: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    sorted_selected_facets = sorted(selected_facets, key=_get_facet_sort_order)

    return sorted_selected_facets


@hookimpl
def prepare_jinja2_environment(env):

    env.filters["sort_selected_facets"] = get_sorted_selected_facets
