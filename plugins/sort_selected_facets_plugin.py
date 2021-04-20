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


def _get_actual_facet_name(facet_query: str) -> str:

    for facet_name in FACET_SORTING_ORDER_MAP.keys():
        if facet_query.startswith(facet_name):
            return facet_name

    return ""


def _get_latest_selected_facet(query_string: str) -> str:

    pre, _, query = query_string.rpartition("&")

    if query:
        *_, facet_query = query.partition("=")
        return _get_actual_facet_name(facet_query)

    if "&" not in pre:
        return ""

    return _get_latest_selected_facet(pre)


def _add_highlight_css_class_to_selected_facet(
    selected_facets: List[Dict[str, Any]],
    latest_selected_facet: str,
    css_class_name: str = "fade-bg",
):

    out_selected_facets = []

    for selected_facet in selected_facets:

        highlight_class = (
            css_class_name if selected_facet["name"] == latest_selected_facet else ""
        )
        selected_facet["highlight_class"] = highlight_class

        out_selected_facets.append(selected_facet)

    return out_selected_facets


def get_sorted_selected_facets(
    selected_facets: List[Dict[str, Any]], query_string: str
) -> List[Dict[str, Any]]:

    latest_selected_facet = _get_latest_selected_facet(query_string)

    out_selected_facets = _add_highlight_css_class_to_selected_facet(
        selected_facets, latest_selected_facet
    )

    sorted_selected_facets = sorted(out_selected_facets, key=_get_facet_sort_order)

    return sorted_selected_facets


@hookimpl
def prepare_jinja2_environment(env):

    env.filters["sort_selected_facets"] = get_sorted_selected_facets
