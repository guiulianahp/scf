
function call_counter(url, pk) {
        window.open(url);
        $.get('YOUR_VIEW_HERE/'+pk+'/', function (data) {
        alert("counter updated!");
        });
    }



$(document).ready(function() {
   var default_table = $('#example').dataTable({
        "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": true,
        "bDestroy": true
    });

    var info_client_table = $('#info_client').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        'bSort': false,
        'aoColumns': [ 
              { sWidth: "50%", bSearchable: false, bSortable: false }, 
              { sWidth: "50%", bSearchable: false, bSortable: false },

        ],
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": false,
        "bDestroy": true
    });


    var product_table = $('#list_product').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": true,
        'iDisplayLength': 3,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
        "autoWidth": false,
        "bDestroy": true
    });

    var cotizacion_table = $('#list_cotizacion').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": false,
        "lengthChange": true,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": true,
        "bDestroy": true
    }); 
    
    var clients_modal_table = $('#list_clients_modal').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": true,
        'iDisplayLength': 5,
        "bDestroy": true
    });
    
    var cotizaciones_table = $('#list_cotizaciones').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": true,
        'iDisplayLength': 3,
        "bDestroy": true
    });

    var facturas_table = $('#factura_preview').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: true,
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": true,
        "bDestroy": true
    });

    var cliente_informacion = $('#informacion_cliente').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        responsive: false,
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": false,
        "bDestroy": true
    });
});