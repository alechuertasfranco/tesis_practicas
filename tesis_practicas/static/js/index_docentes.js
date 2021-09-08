window.onload = function() {
    $('#Tabs a').on('click', function(event) {
        event.preventDefault()
        $(this).tab('show')
    })

    $(document).on("click", ".modal_visar", function(e) {
        e.preventDefault();
        var $popup = $("#modalVisar");
        var url = $(this).data("popup-url");
        $(".modal-content", $popup).load(url, function() {
            $popup.modal("show");
            formatFormFileInput("div_id_proyecto_tesis", "proyecto_tesis", "Proyecto tesis")

            document.getElementById("id_proyecto_tesis").onchange = function(e) {
                var fileName = document.getElementById("id_proyecto_tesis").files[0].name;
                var nextSibling = e.target.nextElementSibling
                nextSibling.innerText = fileName
            }
        });
    });
};

function formatFormFileInput(id_div, name, label) {
    let div_id = document.getElementById(id_div);
    let link = div_id.childNodes[3].childNodes[1];

    if (link.tagName != 'A') {
        link = document.createElement('a');
        link.innerHTML = "No hay archivo"
        link.href = "#"
    }

    div_id.innerHTML = `
    <label for="id_${name}" class="">
      ${label}
    </label>
    <div id="id_${name}_input" class="">
      <div class="custom-file">
        <input type="file" name="proyecto_tesis" class="custom-file-input clearablefileinput form-control-file" id="id_proyecto_tesis" lang="es">
        <label class="custom-file-label" for="id_proyecto_tesis">Subir plan visado</label>
      </div>
    </div>
`;
}