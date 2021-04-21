const each = (qs, callback) => {
  var els = typeof qs === "string" ? document.querySelectorAll(qs) : qs;
  var i;
  for (i = 0; i < els.length; i++) {
    callback(els[i], i);
  }
};

const on = (event, qs, callback) => {
  each(qs, el => {
    el.addEventListener(event, callback);
  });
};


// Toggle extra columns
on("click", ".view-cols.js-click button", e => {
  e.target
    .closest(".table-wrapper")
    .querySelector("table")
    .classList.toggle("hide-columns");
});
function setSessionCookie(name, value, minutes) {
    document.cookie = name + "=" + value + ";path=/;SameSite=Lax;";
}

function deleteSessionCookie(name) {
    setSessionCookie(name, "");
}

document.addEventListener("DOMContentLoaded", function () {
    // Set `latest_selected_facet` cookie on Suggested facets click
    let suggestedFacets = document.querySelectorAll("a[class^='suggested-facet-']");

    Array.from(suggestedFacets).forEach(function (node) {
	node.addEventListener("click", function (event) {
	    event.preventDefault();
	    let _node = event.target;
	    let nodeClass = _node.className;
	    let facetName = nodeClass.replace("suggested-facet-", "");
	    setSessionCookie("latest_selected_facet", facetName);
	    window.location.href = _node.href;
	});
    });

    // Delete `latest_selected_facet` cookie on other link clicks
    let crossLinks = document.querySelectorAll("a:not([class^='suggested-facet-'])");

    Array.from(crossLinks).forEach(function (node) {
	node.addEventListener("click", function (event) {
	    event.preventDefault();
	    let _node = event.target;
	    deleteSessionCookie("latest_selected_facet");

	    let nodeHref = _node.href;

	    // If the selected facet is closed, remove all the references
	    // of the facet elements from query string
	    if (_node.className === "cross") {
		let hostPath = nodeHref.replace(/\?.*$/g, "");
		let queryString = nodeHref.replace(/^[^\?]+\?/, "");

		let removedFacet = _node.previousElementSibling.innerText.split(
		    /\s+/,
		    1,
		)[0];
		let removedFacetRegex = new RegExp(removedFacet);

		let queryStringParts = queryString.split("&");
		let outQueryStringParts = [];

		for (part of queryStringParts) {
		    if (!removedFacetRegex.test(part)) {
			outQueryStringParts.push(part);
		    }
		}

		if (outQueryStringParts.length === 0) {
		    nodeHref = hostPath;
		} else {
		    let outQueryString = outQueryStringParts.join("&");
		    nodeHref = hostPath + "?" + outQueryString;
		}
	    }

	    window.location.href = nodeHref;
	});
    });
});
