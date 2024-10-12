var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    lineNumbers: true,
    mode:"htmlmixed",
    theme: "dracula",
});
editor.setSize("90vw", "80vh");
