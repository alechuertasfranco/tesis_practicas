//----------------------------------- JavaScript para plan_practica---------------------------------
//----------------------------------------------------------------------------------------------------

let id_plan_practicas = document.getElementById("id_plan_practicas")
let id_derecho_tramite = document.getElementById("id_derecho_tramite")

id_plan_practicas.onchange = function() {
    let input = document.getElementById("id_plan_practicas")
    let label = document.getElementById("id_plan_practicas_label")
    let fileName = input.value;
    label.innerHTML = fileName.split('fakepath\\')[1];
}

id_derecho_tramite.onchange = function() {
    let input = document.getElementById("id_derecho_tramite")
    let label = document.getElementById("id_derecho_tramite_label")
    let fileName = input.value;
    label.innerHTML = fileName.split('fakepath\\')[1];
}

