pywebview_bridge_text = """
window.pywebview.api
  .process_form(
    file.name,
    base64String,
    selectType.value,
    randomInput.checked
  )
  .then((response) => {
    if (response.had_error) {
      renderErrors(response.errors);
    }

    prog.style.display = "none";
    prog.setAttribute("aria-hidden", "true");
    clearAll();
  })
  .catch((err) => {
    console.error("Erro:", err);
  });
};
"""

starting_delimiter = "// BEGIN (não remover essa linha)"
ending_delimiter = "// END (não remover essa linha)"