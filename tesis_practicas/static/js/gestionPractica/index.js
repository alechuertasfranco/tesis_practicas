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