
function verAlumno(boton){
    let id_boton=boton.id
    let id=id_boton.split('btnplan')[1]
    $.ajax({
        url:"/fetchAlumnoPractica/"+id+"/",
        type:"get",
        dataType:"json",
        success:function(response){
            $('.alumno_id').val(response['id_alumno']);
            $('.plan_id').val(response['id_plan']);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
      }
    });
}

function info_plan(boton){
    let id_boton=boton.id
    let id=id_boton.split('btninfo_plan')[1]
    $.ajax({
        url:"/info_plan/"+id+"/",
        type:"get",
        dataType:"json",
        success:function(response){
            $('#infoPlan_nro_matricula').val(response['nro_matricula']);
            $('#infoPlan_nombres').val(response['nombres']);
            $('#infoPlan_apellidos').val(response['apellidos']);
            $('#infoPlan_escuela').val(response['escuela'].split('Escuela de ')[1]);
            $('#infoPlan_semestre').val(response['ciclo_academico']);
            $('#infoPlan_empresa').val(response['razon_social']);
            $('#infoPlan_contacto').val(response['nombres_C']);
            $('#infoPlan_telefono').val(response['telefono']);
            $('#infoPlan_asesor').val(response['nombres_Asesor'] + " " +response['apellidos_Asesor']);
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