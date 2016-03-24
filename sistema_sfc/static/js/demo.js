/* JS del proyecto */

function cerrar_modal(){
    $('.info_cliente').modal({ show: false })
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

// Funcion obtener Cookie para el envio ajax Django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function llenar_tabla_observaciones(){
    
    var longitud = $('#list_observaciones > tbody > tr').length + 1;
    var observacion = document.getElementById('inputObservacion').value;

    if (observacion != "") {
        var row = '<tr><td class="numeroObservacion">'+longitud+'</td><td class="textoObservacion">'+observacion+'</td><td><a type="button" id="eliminarFilaObservacion" class="btn btn-block btn-danger eliminarFilaObservacion" ><i class="fa fa-close"></i></a></td></tr>';
        $('#list_observaciones').append(row);

        longitud = $('#list_observaciones > tbody > tr').length + 1;
        document.getElementById('inputObservacion').value = "";
        document.getElementById('labelObservacion').innerHTML = "Observación Nro "+ longitud;

        $('#list_observaciones').show();
    }
    else{
        alert("Debe introducir una Observación");
    } 
};

// Obtener el cliente seleccionado y colocarlo en la tabla de informacion
// del cliente
function getClientModal(id_client, rif_client, nombre_client, telefono_client, correo_client){
    
    $("#nombre_client").text(nombre_client);
    
    var table = $('#info_client').DataTable();
    table.clear().draw();
    var row = '<tr id="rif_cliente"><th>Rif</th><td>'+rif_client+'</td></tr><tr><th>Email:</th><td>'+correo_client+'</td></tr><tr><th>Teléfono:</th><td>'+telefono_client+'</td></tr>'
    $('#info_client').append(row);

    $("#Modal_client").modal('hide');
    $("#add_client").hide();
    $("#edit_client").show();
    $('#id_cliente').val(rif_client);
    $("#contendor_info_cliente").show();
    $('#contenedor_productos').show();    

    console.log(document.getElementById('id_cliente').value);
};

/* Annadir elementos en la tabla cotizacion de acuerdo a los productos seleccionados de la tabla produtos*/
function llenar_tabla(id_producto,descripcion,precio_tp,precio_tg){

    console.log(precio_tp);
    console.log(precio_tg);

    var seleccion_cliente = document.getElementById('seleccion_cliente');

    var producto = {
        id_producto : id_producto,
        descripcion : descripcion,
        precio_tp   : precio_tp,
        precio_tg   : precio_tg
    } 

    var csrftoken = getCookie('csrftoken');
    
    $.ajax({
        type: 'POST',
        url: '/add/cotizacion/',                            
        data: {producto: producto,csrfmiddlewaretoken:csrftoken},    
        success: function (newProducto) {
            $('#contenedor_cotizacion').show();     
            var total_cotizacion = $('#total_cotizacion').val();
            var row = '<tr><td class="inputValue">'+id_producto+'</td><td>'+descripcion+'</td><td><select class="inputCotizacion" name="precio_unitario"><option value=S:'+precio_tp+'>S</option><option value=M:'+precio_tp+'>M</option><option value=L:'+precio_tp+'>L</option><option value=XL:'+precio_tg+'>XL</option></select></td><td class="inputValue"><input class="inputCotizacion" name="cantidad" type="text" value="0" style ="width:70px"></td><td><input class="inputCotizacion" name = "porcentaje" type="text" value="0" style="width:70px"></td><td id="precio_unitario" class="inputValue" >'+precio_tp+'</td><td id="precio_total">0</td><td><a type="button" id="deleteRow" class="btn btn-block btn-danger" data-toggle="tooltip" title="Eliminar Producto" ><i class="fa fa-close"></i></a></td></tr>';

            $('#list_cotizacion').append(row);
            
            $('#total_cotizacion').val(0 + parseFloat(total_cotizacion).toFixed(2));
            $('#total_cotizacion').show();
            $('#total_label').show();
            document.getElementById("btnSavePrice").disabled = false; 
            
        },
        error: function(error){
            console.log(error);
        }
       });
};

// Funcion que guarda una cotizacion creada
function guardar_cotizacion(){
    var csrftoken = getCookie('csrftoken');
    var rif_client;

    var data_final_cotizacion = [];
    var json_cotizacion = {"id":"","cantidad":"","talla":"", "precio":"", "ganancia":""};
    var tabla_cotizacion = document.getElementById('list_cotizacion');

    var data_final_observacion = [];
    var json_observacion = {"observacion":""};
    var tabla_observacion = document.getElementById('list_observaciones');

    //for x que revisa cada fila de la tabla de cotizaciones
    for (var x = 2; x < tabla_cotizacion.rows.length; x++) {
        //for y que revisa cada columna de la tabla
        for (var y = 0; y < tabla_cotizacion.rows[x].cells.length-1; y++) {
            
            // si la celda es un input
            if(tabla_cotizacion.rows[x].cells[y].firstChild.data == undefined){
                //si la columna es precio
                if(y == 2){
                    json_cotizacion['talla']  = tabla_cotizacion.rows[x].cells[y].firstChild.value.split(':')[0];
                }
                //si la columna es cantidad
                if(y == 3){
                    json_cotizacion['cantidad'] = tabla_cotizacion.rows[x].cells[y].firstChild.value;
                }
                //si la columna es cantidad
                if(y == 4){
                    json_cotizacion['ganancia'] = parseFloat(tabla_cotizacion.rows[x].cells[y].firstChild.value.replace(',','.'));
                }
            }

            else{
                // si columna es el id del producto
                if(y == 0){
                    json_cotizacion['id'] = tabla_cotizacion.rows[x].cells[y].firstChild.data;
                }
                if(y == 5){
                json_cotizacion['precio'] = parseFloat(tabla_cotizacion.rows[x].cells[y].firstChild.data.replace(',','.'));
            }     
            }
        }
        data_final_cotizacion.push(json_cotizacion);
        json_cotizacion = {"id":"","cantidad":"","talla":"", "precio":"", "ganancia":""};
    }

    //for x que revisa cada fila de la tabla de observaciones
    for (var x = 1; x < tabla_observacion.rows.length; x++) {
        //for y que revisa cada columna de la tabla
        for (var y = 0; y < tabla_observacion.rows[x].cells.length-1; y++) {
            json_observacion['observacion'] = tabla_observacion.rows[x].cells[1].firstChild.data
            
        }
        data_final_observacion.push(json_observacion);
        json_observacion = {"observacion":""};
    }

    if ($('#info_client > tbody > tr').length == 1 ){
            alert('Debe seleccionar el Cliente');
        }
    else{

        var table_client = document.getElementById('info_client');
        rif_client       = document.getElementById('id_cliente').value;
        console.log(JSON.stringify(data_final_observacion));
        console.log(rif_client);
        $.ajax({
            type: 'POST',
            url: '/save/cotizacion/',                            
            data: {'value':JSON.stringify(data_final_cotizacion),'observaciones':JSON.stringify(data_final_observacion), 'rifClient':rif_client, csrfmiddlewaretoken:csrftoken},
            success:function(data){
                alert('Cotización Creada Exitosamente');
                window.location.replace("/cotizacion/");
            },
            error: function(error){
                alert('Error en la creación de la Cotización');
                console.log(error);          
            }
        })
    }
};

// Funcion para editar cotizacion
function editar_cotizacion(id_cotizacion){
    
    var csrftoken = getCookie('csrftoken');
    var data_final = [];
    var json = {"id":"","cantidad":"","talla":"", "precio":"", "ganancia":""};
    var row_table_client = document.getElementById('rif_cliente')
    
    rif_client = document.getElementById('id_cliente').value;    
    var oTBL = document.getElementById('list_cotizacion');

    var data_final_observacion = [];
    var json_observacion = {"observacion":""};
    var tabla_observacion = document.getElementById('list_observaciones');
    
    //for x que revisa cada fila de la tabla
    for (var x = 1; x < oTBL.rows.length; x++) {
        //for y que revisa cada columna de la tabla
        for (var y = 0; y < oTBL.rows[x].cells.length-1; y++) {
            
            // si la celda es un input
            if(oTBL.rows[x].cells[y].firstChild.data == undefined){
                //si la columna es precio
                if(y == 2){
                    json['talla']  = oTBL.rows[x].cells[y].firstChild.value.split(':')[0];
                }
                //si la columna es cantidad
                if(y == 3){
                    json['cantidad'] = oTBL.rows[x].cells[y].firstChild.value;
                }
                //si la columna es cantidad
                if(y == 4){
                    json['ganancia'] = parseFloat(oTBL.rows[x].cells[y].firstChild.value.replace(',','.'));
                }
            }

            else{
                // si columna es el id del producto
                if(y == 0){
                    json['id'] = oTBL.rows[x].cells[y].firstChild.data;
                }
                if(y == 5){
                    json['precio'] = parseFloat(oTBL.rows[x].cells[y].firstChild.data.replace(',','.'));
                }      
            }
        }
        data_final.push(json);
        json = {"id":"","cantidad":"","talla":"", "precio":"", "ganancia":""};
    }

    //for x que revisa cada fila de la tabla de observaciones
    for (var x = 1; x < tabla_observacion.rows.length; x++) {
        //for y que revisa cada columna de la tabla
        for (var y = 0; y < tabla_observacion.rows[x].cells.length-1; y++) {
            json_observacion['observacion'] = tabla_observacion.rows[x].cells[1].firstChild.data
            
        }
        data_final_observacion.push(json_observacion);
        json_observacion = {"observacion":""};
    }
    
    
    $.ajax({
    type: 'POST',
    url: '/edit/cotizacion/'+id_cotizacion+'/',                            
    data: {'value':JSON.stringify(data_final),'observaciones':JSON.stringify(data_final_observacion),'id_cotizacion':id_cotizacion, 'rifClient':rif_client, csrfmiddlewaretoken:csrftoken},
    success:function(data){
        alert('Cotización actualizada Exitosamente');
        window.location.replace("/cotizacion/");
    },
    error: function(error){
        alert('Error en la actualización de la Cotización');
        console.log(error);          
    }
   });
};

// Funcion que muestra una vista previa de la cotizacion para convertirse
// en factura
function ver_cotizacion(id_cotizacion){

    var csrftoken = getCookie('csrftoken');
    var iva = 12;
    $('#informacion_cliente tbody').empty();
    $('#factura_preview tbody').empty();
    $("#contenedor_factura_preview").show();    
    $("#cotizacion_collapse").collapse('hide');

    $.ajax({
    type: 'GET',
    data: {csrfmiddlewaretoken:csrftoken},
    url: '/cotizacion/'+id_cotizacion+'/',
    success:function(response){
        subtotal = response.total;
        iva_total = (subtotal*iva)/100;
        total = iva_total+subtotal;
        $('#text_id_cotizacion').text('Cotización #'+id_cotizacion);
        for (var i=0; i<response.tabla.length; i++){
            var objeto = response.tabla[i];
            var row = '<tr><td class="inputValue">'+objeto['id']+'</td><td>'+objeto['descripcion']+'</td><td>'+objeto['talla']+'</td><td class="inputValue">'+objeto['cantidad']+'</td><td>'+objeto['ganancia']+'</td><td class="inputValue" >'+objeto['precio_unitario']+'</td><td>'+objeto['precio_total']+'</td></tr>';
            $('#factura_preview').append(row);
        }
        var row_subtotal_cotizacion = '<tr><td></td><td></td><td></td><td></td><td></td><th>Sub Total</th><td style="float:right">'+subtotal+'</td></tr>'
        var iva_cotizacion = '<tr><td></td><td></td><td></td><td></td><td></td><th>IVA 12 %</th><td style="float:right">'+iva_total+'</td></tr>'
        var row_total_cotizacion = '<tr><td></td><td></td><td></td><td></td><td></td><th>Sub Total</th><td style="float:right">'+total+'</td></tr>'
        var row_cliente = '<tr><th>Nombre</th><td>'+response.cliente['nombre']+'</td></tr><tr><th>Rif</th><td>'+response.cliente['rif']+'</td></tr><tr><th>Email:</th><td>'+response.cliente['correo']+'</td></tr><tr><th>Teléfono:</th><td>'+response.cliente['telefono']+'</td></tr><tr><th>Direccion</th><td>'+response.cliente['direccion']+'</td></tr>';
        
        $('#factura_preview').append(row_subtotal_cotizacion);
        $('#factura_preview').append(iva_cotizacion);
        $('#factura_preview').append(row_total_cotizacion);
        $('#informacion_cliente').append(row_cliente);
    
    },
    error: function(error){
        console.log(error);          
    }
   });
}

// Funcion que crea una factura
function crear_factura(){
    var booleann = true;
    var id_cotizacion;
    var id_factura;
    var csrftoken = getCookie('csrftoken');
    /*
    
    if ($('table#list_cotizaciones tr:last').index() +1 == 0 ){
        alert('No existen cotizaciones activas');
        booleann = false;
    }*/

    if ($('#factura_preview > tbody > tr').length == 1 && booleann){
        alert('Debe seleccionar una cotización');
        booleann = false;
    }
    else{
        id_cotizacion = $('#text_id_cotizacion').text().split('#')[1];
    }

    if(document.getElementById('input_id_factura').value === '' && booleann){
        alert('Debe introducir el Nro de la factura');
        booleann = false;
    }
    else{
        id_factura = document.getElementById('input_id_factura').value;
    }

    if(isNaN(document.getElementById('input_id_factura').value) && booleann){
        alert('Debe introducir un formato de factura correcto. Ejem: 058');
        booleann = false;
    }
    else{
        id_factura = document.getElementById('input_id_factura').value;
    }


    if (booleann){

        $.ajax({
            type: 'POST',
            data: {id_cotizacion:id_cotizacion, id_factura: id_factura, csrfmiddlewaretoken:csrftoken},
            url: '/add/factura/',
            success:function(response){
                alert('Factura Creada Exitosamente')
                window.location.replace("/facturacion/");
            
            },
            error: function(error){
                alert(error.responseText);}
           });
    }
}

function guardar_observacion(){
    alert("Observaciones Guardadas Exitosamente");
    $('#Modal_observaciones').modal('hide');
}

/* Carga del documento */
$(document).ready(function(){

    /* evento para eliminar filas de la tabla de observaciones*/
    $(document).on('click', '#eliminarFilaObservacion', function(e){

        var count = 1;
        var numero_filas = $('#list_observaciones > tbody > tr').length;
        var tabla_observacion = document.getElementById('list_observaciones');

        if (numero_filas == 1 ){
            $('#list_observaciones').hide();
            document.getElementById('list_observaciones').deleteRow(1); 
            document.getElementById('inputObservacion').value = "";
            document.getElementById('labelObservacion').innerHTML = "Observación Nro "+ (numero_filas);

        }
        else{
            var i = this.parentNode.parentNode.rowIndex; //Obtener el id de la fila a borrar
            document.getElementById('list_observaciones').deleteRow(i); //Eliminar la fila con id obtenido anteriormente 
            document.getElementById('inputObservacion').value = "";
            document.getElementById('labelObservacion').innerHTML = "Observación Nro "+ (numero_filas);
            
        }

        // Setear la tabla de observaciones con sus id correspondientes
        for (var x = 1; x < tabla_observacion.rows.length; x++) {
            //for y que revisa cada columna de la tabla
            for (var y = 0; y < tabla_observacion.rows[x].cells.length-1; y++) {
                tabla_observacion.rows[x].cells[0].firstChild.data = count
                
            }
            count += 1
        }


    });

    /* evento para eliminar filas y actualizar el total de la cotizacion */
    $(document).on('click', '#deleteRow', function(e){
        var i; //contador de fila
        var row; //fila
        var total;
        var numero_filas;
        var precio_total; //precio total de la fila seleccionada
        var total_cotizacion; //Total de la tabla cotizacion


        numero_filas = $('#list_cotizacion > tbody > tr').length;
        row = $(this).closest("tr");
        
        if (numero_filas == 1 ){
            $('#contenedor_cotizacion').hide();
        };

        i = this.parentNode.parentNode.rowIndex; //Obtener el id de la fila a borrar
        document.getElementById('list_cotizacion').deleteRow(i); //Eliminar la fila con id obtenido anteriormente 

        total_cotizacion = parseFloat($('#total_cotizacion').val()); //Obtener el total de la cotizacion
        precio_total = parseFloat(row.find("td[id^='precio_total']").text()); //Obtener el precio total de esa fila

        total = (total_cotizacion - precio_total).toFixed(2); //Calcular el nuevo total

        $('#total_cotizacion').val(total); //Actualizar el precio total

        //Si precio es igual a 0 escondemos el input que muestra el precio total
        if( parseInt(total) == 0 && numero_filas == 1) {
            $('#total_cotizacion').hide();
            $('#total_label').hide();
            $('#contenedor_cotizacion').hide();
            document.getElementById("btnSavePrice").disabled = true; 
        }
        
    });

    /* evento para cuando el select de las tallas del producto es cambiado, entonces actualizar precio unitatio
    y el total de la cotizacion */
    $(document).on('change', 'select[class="inputCotizacion"]', function(){
        alert('aq')
        var val = 0;
        var total = 0;

        var row;
        var total;        
        var talla;
        var precio;
        var cantidad;
        var porcentaje;
        var precio_total;
        var total_cotizacion;

        row = $(this).closest("tr");
        console.log($(this).val());
        precio = parseFloat($(this).val().split(':')[1].replace(',','.')); // Obtener el precio del producto
        talla  = $(this).val().split(':')[0];

        total_cotizacion = parseFloat($('#total_cotizacion').val().replace(',','.')); //Obtener el total de la cotizacion
        cantidad = parseInt(row.find("input[name^='cantidad']").val()); // Obtener la cantidad de productos
        porcentaje = parseFloat(row.find("input[name^='porcentaje']").val().replace(',','.')); // Obtener el porcentaje dado
        precio_total = parseFloat(row.find("td[id^='precio_total']").text().replace(',','.')); //Obtener el precio total de esa fila antes de modificarlo
        
        total = (precio * cantidad) * (1 + (porcentaje/100)); //Calcular el precio total dado el porcentaje, cantidad y precio unitario
        
        $(this).parent().siblings('td[id^=precio_unitario]').html(precio.toFixed(2)); //Actualizar precio unitario
        $(this).parent().siblings('td[id^=precio_total]').html(total.toFixed(2));//Actualizar el precio total de esa fila

        total_cotizacion = (total_cotizacion - precio_total) + total; //calcular el total de la cotizacion
        $('#total_cotizacion').val(total_cotizacion.toFixed(2));  //actualizar el total de la cotizacion  */  

        console.log(precio);
    });

    /* evento para cuando los input de cantidad y porcentaje son cambiados, entonces actualizar precio*/
    $(document).on('keyup', 'input[class="inputCotizacion"]', function(){

        var $this       = $(this);
        var booleann    = true;
        var $row        = $(this).closest("tr");
        var $cantidad   = parseInt($row.find("input[name^='cantidad']").val()); //obtener la cantidad 
        var $porcentaje = parseFloat($row.find("input[name^='porcentaje']").val()); //obtener el porcentaje

        if( !isNumber($cantidad)){alert('Cantidad inválida'); booleann = false};
        if( !isNumber($porcentaje)){alert('Ganancia inválida'); booleann = false};

        if (booleann){
            var $precio_unitario = $row.find("select[name^='precio_unitario']").val(); //obtener el precio unitario de la fila
            var $precio = parseFloat($precio_unitario.split(':')[1]); //convertir a flotante

            var $total_cotizacion = parseFloat($('#total_cotizacion').val()); //Obtener el total de la cotizacion
            
            var $precio_total = parseFloat($row.find("td[id^='precio_total']").text()); //Obtener el precio total de esa fila antes de modificarlo
            
            var $total = ($precio * $cantidad) * (1 + ($porcentaje/100)); //calcular el total

            $(this).parent().siblings("td[id^='precio_total']").html($total.toFixed(2)); // actualizar el precio total de esa fila

            $total_cotizacion = ($total_cotizacion- $precio_total) + $total; //calcular el total de la cotizacion
            $('#total_cotizacion').val($total_cotizacion.toFixed(2));  //actualizar el total de la cotizacion     
        }
        
    });

    /*  */
    $(document).on('change', 'select[name="observaciones"]', function(){
        var longitud = $('#list_observaciones > tbody > tr').length + 1;
        var select        = document.getElementById("select-observaciones");
        var selectedValue = select.options[select.selectedIndex].value;
        
        var row = '<tr><td class="numeroObservacion">'+longitud+'</td><td class="textoObservacion">'+selectedValue+'</td><td><a type="button" id="eliminarFilaObservacion" class="btn btn-block btn-danger eliminarFilaObservacion" ><i class="fa fa-close"></i></a></td></tr>';
        $('#list_observaciones').append(row);

        longitud = $('#list_observaciones > tbody > tr').length + 1;
        document.getElementById('inputObservacion').value = "";
        document.getElementById('labelObservacion').innerHTML = "Observación Nro "+ longitud;

        $('#list_observaciones').show();

    });

    /* Eliminar un renglon del datatable de la vista de totales de
       Cliente, Producto, Facturas, Cotizacion, Prospecto*/
    $(".delete").on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            console.log(Pid);
            var name = $(this).data('name');
            $('#modal_id').val(Pid);
            $('#modal_name').text(name);       
    });

    /* Convertir un cliente en PRospecto*/
    $(".convertir").on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#modal_id_prospecto').val(Pid);
            $('#modal_name_prospecto').text(name);
           
    });
  
    var options = {
        success:function(response)
            {   console.log(response);
                if(response.status=="True"){
                    console.log(response);
                    var idProd = response.input_id;
                    var elementos= $("#example"+' >tbody >tr').length;
                    if(elementos==1){
                            location.reload();
                    }else{
                        $("#Modal").modal('hide');
                        $('#'+idProd).remove();
                    }
                    alert('Eliminado Exitosamente');
                }else{
                    console.log(response);
                    alert('Hubo un error al eliminar: ' + response.mensaje);
                    $("#Modal").modal('hide');
                };
            }
    };

    var options_prospecto = {
        success:function(response)
            {   
                if(response.status){
                    var csrftoken = getCookie('csrftoken');
                    var id = response.data.id
                    $.ajax({
                        type: 'POST',
                        data: {nombre:response.data, prospecto:true, csrfmiddlewaretoken:csrftoken},
                        url: '/add/cliente/'+id+'/',
                        success:function(response){
                            window.location.replace("/add/cliente/"+id+"/");
                        
                        },
                        error: function(error){
                            alert('Error en convertir prospesto');
                            console.log(error);          
                        }
                    });

                    
                }else{
                    alert("Hubo un error al convertir cliente!");
                    $("#ModaltoClient").modal('hide');
                };
            }
    };

    $("#frmEliminar").ajaxForm(options);
    $("#frmConvertir").ajaxForm(options_prospecto);

    
    if($('#list_cotizacion > tbody > tr').length == 0){
        $('#contenedor_cotizacion').hide();
    }
    else{
        $('#contenedor_cotizacion').show();
         document.getElementById("btnSavePrice").disabled = false;

    }

    if ($('#info_client > tbody > tr').length == 0 ){
        $('contenedor_productos').hide();
    }
    else{
        $('#contenedor_productos').show();
    }


    /*************** Codigo para crear un popover bajo una clase *********/
    var originalLeave = $.fn.popover.Constructor.prototype.leave;
    $.fn.popover.Constructor.prototype.leave = function(obj){
      var self = obj instanceof this.constructor ?
        obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)
      var container, timeout;

      originalLeave.call(this, obj);

      if(obj.currentTarget) {
        container = $(obj.currentTarget).siblings('.popover')
        timeout = self.timeout;
        container.one('mouseenter', function(){
          //We entered the actual popover – call off the dogs
          clearTimeout(timeout);
          //Let's monitor popover content instead
          container.one('mouseleave', function(){
            $.fn.popover.Constructor.prototype.leave.call(self, self);
          });
        })
      }
    };
    $('body').popover({ selector: '[data-popover]', trigger: 'click hover', placement: 'auto', delay: {show: 50, hide: 400}});
    /*********************************************************************/
    });