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

function verAlumno(boton){
    let id_boton=boton.id
    let id=id_boton.split('btnplan')[1]
    console.log(id)
    $.ajax({
        url:"/fetchAlumnoPractica/"+id+"/",
        type:"get",
        dataType:"json",
        success:function(response){
            $('#alumno_id').val(response['id_alumno']);
            $('#plan_id').val(response['id_plan']);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
      }
    });
}

let id_plan_practicas = document.getElementById("id_informe_final")

id_plan_practicas.onchange = function() {
    let input = document.getElementById("id_informe_final")
    let label = document.getElementById("id_informe_final_label")
    let fileName = input.value;
    label.innerHTML = fileName.split('fakepath\\')[1];
}
