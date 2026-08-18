$(document).ready(function () {
  // Toggle the abstract, award and bibtex panels of a publication entry.
  // Opening one closes the other two.
  const panels = ["abstract", "award", "bibtex"];
  panels.forEach(function (panel) {
    $("a." + panel).click(function () {
      const entry = $(this).parent().parent();
      panels.forEach(function (other) {
        if (other === panel) {
          entry.find("." + panel + ".hidden").toggleClass("open");
        } else {
          entry.find("." + other + ".hidden.open").toggleClass("open");
        }
      });
    });
  });

  // Show the author list of a publication entry on hover.
  $('[data-toggle="popover"]').popover({ trigger: "hover" });
});
