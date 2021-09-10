
function verAlumno(boton){
    let id_boton=boton.id
    let id=id_boton.split('btnplan')[1]
    $.ajax({
        url:"/fetchAlumnoPractica/"+id+"/",
        type:"get",
        dataType:"json",
        success:function(response){
            let label = document.getElementById("modalVisar_h5")
            label.innerHTML=response['nombres'] + response['apellidos']
            $('#alumno_id').val(response['id_alumno']);
            $('#plan_id').val(response['id_plan']);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
      }
    });
}

let id_plan_practicas = document.getElementById("id_plan_practicas")

id_plan_practicas.onchange = function() {
    let input = document.getElementById("id_plan_practicas")
    let label = document.getElementById("id_plan_practicas_label")
    let fileName = input.value;
    label.innerHTML = fileName.split('fakepath\\')[1];
}


function downloadURI(boton) 
{
    ruta=boton.getAttribute("ruta")
    url=boton.getAttribute("url")
    nombre=ruta.split('plan_practica/')[1];
    var link = document.createElement("a");
    link.download = nombre;
    link.href = url;
    link.click();
}