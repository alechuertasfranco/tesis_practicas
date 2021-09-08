//----------------------------------- JavaScript para asesor_practica---------------------------------
//----------------------------------------------------------------------------------------------------

function verAsesor(id){
    console.log(id);
    $.ajax({
        url:"/verAsesor/"+id+"/",
        type:"get",
        dataType:"json",
        success:function(response){
            $('#nombre').val(response['nombres']);
            $('#apellido').val(response['apellidos']);
            $('#titulo').val(response['titulo']);
            $('#telefono').val(response['telefono']);
            $('#correo').val(response['email']);
            $('#asesor_id').val(response['id']);
        }
    });
}

function aparecer() {
    var x = document.getElementById("info-asesor");
    if (x.style.display === "none") {
        x.style.display = "block";
    }

    id = document.getElementById("id_asesor").value;
    verAsesor(id);
}
