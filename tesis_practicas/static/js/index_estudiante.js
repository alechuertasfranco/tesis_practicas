let div_id_proyecto_tesis
let link_proyecto_tesis
let html_proyecto_tesis

window.onload = function() {
    div_id_proyecto_tesis = document.getElementById("div_id_proyecto_tesis")
    link_proyecto_tesis = div_id_proyecto_tesis.childNodes[3].childNodes[1]
    html_proyecto_tesis = div_id_proyecto_tesis.innerHTML
    console.log(html_proyecto_tesis)
    div_id_proyecto_tesis.innerHTML = `
      <label for="id_proyecto_tesis" class=" requiredField">
        Proyecto tesis<span class="asteriskField">*</span>
      </label>
      <div id="id_proyecto_tesis_input" class="">
        <div class="input-group mb-3">
          <input type="text" class="form-control" value="${link_proyecto_tesis.innerHTML}" readonly>
          <div class="input-group-append">
            <a class="btn btn-outline-secondary" href="${link_proyecto_tesis.href}">
              <i class="fa fa-download mr-2" aria-hidden="true"></i>Descargar archivo
            </a>
          </div>
        </div>
      </div>
    `
}

function edit() {
    document.getElementById("id_proyecto_tesis_input").innerHTML = `
      <div class="custom-file">
        <input type="file" name="proyecto_tesis" class="custom-file-input clearablefileinput form-control-file" id="id_proyecto_tesis">
        <label class="custom-file-label" for="id_proyecto_tesis">${link_proyecto_tesis.innerHTML}</label>
      </div>
      <input type="file" name="proyecto_tesis" class="clearablefileinput form-control-file" id="id_proyecto_tesis">
    `
    console.log(document.getElementById("id_proyecto_tesis_input"))
}

function modalPracticas() {
    Swal.fire({
            "title": "Acceso denegado",
            "text": "Debe completar el total de horas de practicas para tener acceso al plan de proyecto de tesis.",
            "icon": "error",
        })
        .then(function() {
            window.location.href = "/"
        })
}