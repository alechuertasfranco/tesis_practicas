let name_doc_proyecto_tesis;
let name_doc_informe_final;

window.onload = function() {
    formatFormFileInput("div_id_proyecto_tesis", "proyecto_tesis", "Proyecto tesis")
    formatFormFileInput("div_id_informe_final", "informe_final", "Informe final")
};

function edit() {
    let proyecto_tesis_input = document.getElementById("id_proyecto_tesis_input")
    let informe_final_input = document.getElementById("id_informe_final_input")

    proyecto_tesis_input.innerHTML = `
      <div class="custom-file">
        <input type="file" name="proyecto_tesis" class="custom-file-input clearablefileinput form-control-file" id="id_proyecto_tesis" lang="es">
        <label class="custom-file-label" for="id_proyecto_tesis">${name_doc_proyecto_tesis}</label>
      </div>
    `;
    informe_final_input.innerHTML = `
      <div class="custom-file">
        <input type="file" name="informe_final" class="custom-file-input clearablefileinput form-control-file" id="id_informe_final" lang="es">
        <label class="custom-file-label" for="id_informe_final">${name_doc_informe_final}</label>
      </div>
    `;

    proyecto_tesis_input.onchange = function() {
        let input = proyecto_tesis_input.childNodes[1];
        let fileName = input.childNodes[1].value;
        input.childNodes[3].innerHTML = fileName.split('fakepath\\')[1];
    }

    informe_final_input.onchange = function() {
        let input = informe_final_input.childNodes[1];
        let fileName = input.childNodes[1].value;
        input.childNodes[3].innerHTML = fileName.split('fakepath\\')[1];
    }

    document.getElementById("btn_levantar_observaciones").removeAttribute("disabled");
}

function formatFormFileInput(id_div, name, label) {
    let div_id = document.getElementById(id_div);
    let link = div_id.childNodes[3].childNodes[1];

    if (link.tagName != 'A') {
        link = document.createElement('a');
        link.innerHTML = "No hay archivo"
        link.href = "#"
    }
    if (name == 'proyecto_tesis') name_doc_proyecto_tesis = link.innerHTML
    if (name == 'informe_final') name_doc_informe_final = link.innerHTML

    div_id.innerHTML = `
      <label for="id_${name}" class="">
        ${label}
      </label>
      <div id="id_${name}_input" class="">
        <div class="input-group mb-3">
          <input type="text" class="form-control" value="${link.innerHTML}" readonly>
          <div class="input-group-append">
            <a class="btn btn-outline-secondary" href="${link.href}">
              <i class="fa fa-download mr-2" aria-hidden="true"></i>Descargar archivo
            </a>
          </div>
        </div>
      </div>
  `;
}

function modalPracticas() {
    Swal.fire({
        title: "Acceso denegado",
        text: "Debe completar el total de horas de practicas para tener acceso al plan de proyecto de tesis.",
        icon: "error",
    }).then(function() {
        window.location.href = "/";
    });
}