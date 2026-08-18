// Give Markdown tables the Bootstrap look, and track the active theme.
$(document).ready(function () {
  $("table").each(function () {
    if (determineComputedTheme() == "dark") {
      $(this).addClass("table-dark");
    } else {
      $(this).removeClass("table-dark");
    }

    // The news table on the about page manages its own styling.
    if ($(this).parents('[class*="news"]').length == 0 && $(this).parents("code").length == 0) {
      $(this).addClass("table-hover");
    }
  });
});
