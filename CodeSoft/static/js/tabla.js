$(document).ready(function() {
$("#transaccionesTable").DataTable({

    "language": {
        url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
        "search": "Buscar:",
        "lengthMenu": "Mostrar _MENU_ registros por página",
        "zeroRecords": "No se encontraron resultados",
        "info": "Mostrando página _PAGE_ de _PAGES_",
        "infoEmpty": "No hay registros disponibles",
        "infoFiltered": "(filtrado de _MAX_ registros totales)",
        "paginate": {
            "first": "Primero",
            "last": "Último",
            "next": "Siguiente",
            "previous": "Anterior"
        },
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "searchPlaceholder": "Buscar...",
        "emptyTable": "No hay datos disponibles en la tabla",
        "thousands": ",",

    },
   

});
});
   