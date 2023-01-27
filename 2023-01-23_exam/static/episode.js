'use strict;'

/* Include the plugin to obtain the date for comments like "a few moment ago" or "3 days ago" etc. */
dayjs.extend(window.dayjs_plugin_relativeTime)


window.addEventListener("load", (event) => {

  /* COMMENT SECTION EP - Use of plugin 'RelativeTime' */
  document.querySelectorAll(".comment-date").forEach(function (elem) {
    elem.innerText = dayjs().to(dayjs(elem.innerText));
  });
  document.querySelector('#dateTextInput').value = dayjs().format('YYYY-MM-DD');

});