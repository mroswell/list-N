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