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
	    window.location.href = _node.href;
	});
    });
});
