$(window).ready(function(){
    function notificaciones(data) {
        if (data.indicador == 0) {
            var type = "danger";
            var mensaje = data.mensaje;
        } else if (data.indicador == 1){
            var type = "info";
            var mensaje = data.mensaje;
        } else if (data.indicador == 2){
            var type = "success";
            var mensaje = data.mensaje;
            }

        $.notify({
            icon: 'fa fa-info-circle',
            message: "<strong>" + mensaje + "</strong>"
        }, {
            type: type,
            animate: {
                enter: 'animated bounceInDown',
                exit: 'animated bounceOutUp'
            },
            placement: {
                from: "top",
                align: "center"
            }
        });
    }

    function buscar_datos_remitente(numero, url, data) {
        if (numero != '') {
            $.ajax({
                url: url,
                type: 'get',
                data: data
            })
                .done(function (data) {
                    if (data.indicador == 0) {
                        $("#remitente_modal").modal('show');
                        $("#numero_id_remitente").val(numero);
                        $("#tipo_operacion").attr('value','nuevo');
                        $("#titulo_remitente").text('Nuevo Remitente');
                    } else if (data.indicador == 3) {
                        $("#editar_remitente").val(data.id);
                        $("#nombre_remitente").val(data.nombre);
                        $("#tipo_persona_remitente").val(data.tipo_persona).attr('selected', 'selected');
                        $("#tipo_id_remitente").val(data.tipo_id).attr('selected', 'selected');
                        $("#numero_id_remitente").val(data.numero_id);
                        $("#direccion_remitente").val(data.direccion);
                        $("#telefono_remitente").val(data.telefono);
                        $("#email_remitente").val(data.email);
                    } else {
                        $("#editar_remitente").val(data.id);
                        $("#text_nombre").text(data.nombre);
                        $("#text_tipo_persona").text(data.tipo_persona);
                        $("#text_tipo_id").text(data.tipo_id);
                        $("#text_numero_id").text(data.numero_id);
                        $("#text_direccion").text(data.direccion);
                        $("#text_telefono").text(data.telefono);
                        $("#text_email").text(data.email);
                        $("#img-user").attr('style','color:green;font-size: 120px');
                        $('#campos_form').find('input, textarea, select').removeAttr('disabled');
                        $('#editar_remitente').removeAttr('disabled');
                        $('#guardar_correspondencia_entrada').removeAttr('disabled');
                    }
                })
                .fail(function () {
                    var mensaje = "Ha ocurrido un error de comunicación con el servidor";
                    var type = "error";
                    notificaciones(mensaje, type);
                    $("#numero_id").focus();
                });
        } else {
            $("#numero_id").focus();
        }
    }

    $("#buscar_remitente").click(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var numero = $("#numero_id").val();
        var data = {numero_id: numero};
        var url = "/buscar_remitente";
        buscar_datos_remitente(numero, url, data);

    });

    $("#guardarRemitente").click(function(e)  {
        e.preventDefault();
        e.stopImmediatePropagation();
        var url = $("#form_guardar_remitente").attr('action');
        var f = $("#form_guardar_remitente");
        $.ajax({
            type: 'POST',
            url: url,
            data: f.serialize(),
            success: function (data) {
                var numero = $("#numero_id").val();
                var dato = {numero_id: numero};
                var url = "/buscar_remitente";
                $("#form_guardar_remitente")[0].reset();
                $('#remitente_modal').modal('hide');
                $("#titulo_remitente").text('Nuevo Remitente');
                $("#procedencia").focus();
                buscar_datos_remitente(numero, url, dato);
                notificaciones(data);
            },
            error: function (data) {
                var type = "error";
                var mensaje = ('Ha ocurrido un error de comunicacion con el servidor, los datos no han sido guardados');
                $("#form_guardar_remitente")[0].reset();
                $('#remitente_modal').modal('hide');
                notificaciones(mensaje, type);
            }
        });
        return false;
    });

    $("select[name=tipo_persona_remitente]").focusout(function () {
        if ($("select[name=tipo_persona_remitente]").val() == 1){
            $("select[name=tipo_id_remitente] option[value='3']").remove();
            if ($("select[name=tipo_id_remitente] option[value='1']").length == 0){
                $("select[name=tipo_id_remitente]").append('<option value="1">CC</option>');
                $("select[name=tipo_id_remitente]").append('<option value="2">CE</option>');
            }
        }else {
            $("select[name=tipo_id_remitente] option[value='1']").remove();
            $("select[name=tipo_id_remitente] option[value='2']").remove();
            if ($("select[name=tipo_id_remitente] option[value='3']").length == 0){
                $("select[name=tipo_id_remitente]").append('<option value="3">NIT</option>');
            }
        }
    });

    $("#dependencia").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var dependencia = $(this).val();
        if (dependencia != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {dependencia: dependencia}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data);
                }else{
                    $("select[name=serie_documental] option").remove();
                    $("select[name=serie_documental]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=serie_documental]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
            $('#copiaDestino').removeAttr('disabled');
        }else{
            $('#copiaDestino').attr('disabled', 'disabled');
        }
    });

    $("#serie_documental").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var serie_documental = $("#serie_documental").val();
        if (serie_documental != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {serie_documental: serie_documental}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data);
                }else{
                    $("select[name=subserie_documental] option").remove();
                    $("select[name=subserie_documental]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=subserie_documental]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
        }
    });

    $("#subserie_documental").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var subserie_documental = $("#subserie_documental").val();
        if (subserie_documental != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {subserie_documental: subserie_documental}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data)
                }else if (data.indicador == 2) {
                    $("#tipo_documental_retencion").attr('disabled', 'disabled');
                    $("#tipo_documental_retencion").removeAttr("required");
                }else{
                    $("#tipo_documental_retencion").attr('required', 'required');
                    $("#tipo_documental_retencion").removeAttr("disabled");
                    $("select[name=tipo_documental_retencion] option").remove();
                    $("select[name=tipo_documental_retencion]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=tipo_documental_retencion]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
        }
    });
    $("button[name=anular_correspondencia_entrada]").click(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
        var url = '/anular_correspondencia_entrada';
        swal({
            title: "Desea anular este registro?",
            text: "los archivos adjuntos no se podran recuperar",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#108225",
            confirmButtonText: "Si, borrar !",
            cancelButtonText: "Cancelar",
            closeOnConfirm: false
        }, function (isConfirm) {
            if (!isConfirm) return;
            $.ajax({
                type: 'get',
                url: url,
                data: {registro: valor},
                success: function (data) {
                    if (data.indicador == 2) {
                        swal("Exito!", data.mensaje, "success");
                        $('#'+valor).remove();
                    }else {
                        swal("Error", data.mensaje, "error");
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    swal("Error !", "Por favor actualice la pagina, o verifique su conexión a la red", "error");
                }

            });

        });
    });

    $("#procedencia").change(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var val = $("#procedencia option:selected").html();
        if (val == "Interna"){
           $("#depen_origen").removeAttr("hidden");
           $("#dependencia_origen").attr("required","required");
        } else {
           $("#depen_origen").attr("hidden","hidden");
           $("#dependencia_origen").removeAttr("required");
        }
    });

    $("button[name=editar_correspondencia_entrada]").click(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
        $.ajax({
            url: "/editar_correspondencia_entrada",
            type: 'get',
            data: {registro: valor}
        })
        .done(function (data) {
            $("#form-guardar_edicion_correspondencia").trigger("reset");
            $("#editar_correspondencia_entrada").attr('value',data.ids);
            $("#editar_procedencia").val(data.procedencia).attr("selected","selected");
            $("#editar_asunto").val(data.asunto);
            $("#editar_observacion").text(data.observacion);
            $("#editar_fecha_documento").val(data.fecha_documento);
            $("#editar_tipo_documento").val(data.tipo_documento).attr("selected","selected");
            $("#editar_numero_folios").val(data.folios);
            $("#editar_dependencia").val(data.dependencia).attr("selected","selected");
            $('#editar_serie_documental option').remove();
            $('#editar_serie_documental').append(new Option(data.nombreSerieDocumental, data.idSerieDocumental));
            $("#editar_serie_documental").val(data.idSerieDocumental).attr("selected","selected");
            $("#editar_serie_documental").attr("disabled","disabled");
            $('#editar_subserie_documental option').remove();
            $('#editar_subserie_documental').append(new Option(data.nombreSubserieDocuental, data.idSubserieDocumental));
            $("#editar_subserie_documental").val(data.idSubserieDocumental).attr("selected","selected");
            $("#editar_subserie_documental").attr("disabled","disabled");
            $('#editar_tipo_documental_retencion option').remove();
            $('#editar_tipo_documental_retencion').append(new Option(data.nombreTipoDocumental, data.idTipoDocumental));
            $("#editar_tipo_documental_retencion").val(data.idTipoDocumental).attr("selected","selected");
            $("#editar_tipo_documental_retencion").attr("disabled","disabled");
            $("#edicion_correspondencia_modal").modal('show');
        })
        .fail(function () {
            var data = {indicador:0,mensaje:'Ha ocurrido un error de comunicacion con el servidor, por favor actualice la pagina'};
            notificaciones(data);
        });
    });

    $("button[name=imprimir_etiqueta]").click( function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
        if(valor != 0) {
            window.open("/etiqueta_pdf?id_registro=" + valor, '_blank');
        }else{
            var mensaje = "No se ha ingresado un registro para generar la etiqueta";
            var type = 'danger';
            notificaciones(mensaje, type)
        }
    });

    $("#editar_dependencia").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var dependencia = $(this).val();
        if (dependencia != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {dependencia: dependencia}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data)
                }else{
                    $("select[name=editar_serie_documental] option").remove();
                    $("select[name=editar_serie_documental]").removeAttr('disabled');
                    $("select[name=editar_serie_documental]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=editar_serie_documental]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
        }
    });

    $("#editar_serie_documental").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var serie_documental = $(this).val();
        if (serie_documental != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {serie_documental: serie_documental}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data)
                }else{
                    $("select[name=editar_subserie_documental] option").remove();
                    $("select[name=editar_subserie_documental]").removeAttr('disabled');
                    $("select[name=editar_subserie_documental]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=editar_subserie_documental]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
        }
    });

    $("#editar_subserie_documental").change(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var subserie_documental = $(this).val();
        if (subserie_documental != '') {
            $.ajax({
                url: "/buscar_agr_documental",
                type: 'get',
                data: {subserie_documental: subserie_documental}
            })
            .done(function (data) {
                if (data.indicador == 0) {
                    notificaciones(data)
                }else{
                    $("#editar_tipo_documental_retencion").attr('required', 'required');
                    $("#editar_tipo_documental_retencion").removeAttr("disabled");
                    $("select[name=editar_tipo_documental_retencion] option").remove();
                    $("select[name=editar_tipo_documental_retencion]").append('<option value="">Seleccione</option>');
                    for(i=0; i<data.list.length; i++) {
                        var id = data.list[i].id;
                        var opciones = data.list[i].nombre;
                        $("select[name=editar_tipo_documental_retencion]").append('<option value='+ id +'>'+ opciones +'</option>');
                    }
                }
            })
            .fail(function () {
                var data = {indicador:0,mensaje:"Ha ocurrido un error de comunicación con el servidor, por favor actualice la página"};
                notificaciones(data);
            });
        }
    });

    $("#editar_remitente").click(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $("#tipo_operacion").attr('value','edicion');
        $("#titulo_remitente").text('Edición de Remitente');
        var numero = $(this).val();
        $('#editarId').attr('value',numero);
        var data = {identificador: numero};
        var url = "/buscar_remitente";
        $("#remitente_modal").modal('show');
        buscar_datos_remitente(numero, url, data);
    });

    $("#copiaDestino").click(function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var numero = $("#dependencia").val();
        $("#"+numero).attr("disabled", true);
        $("#copia_modal").modal('show');
    });

    $('#codigo_radicado').focusout(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        if($(this).val() != "" ){
            $('#numero_identificacion').attr('disabled','disabled')
        }
        else{
            $('#numero_identificacion').removeAttr('disabled')
        }
    });

    $('#numero_identificacion').focusout(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        if($(this).val() != "" ){
            $('#codigo_radicado').attr('disabled','disabled')
        }
        else{
            $('#codigo_radicado').removeAttr('disabled')
        }
    });

    $("#buscar_documento_radicado").click( function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        if($('#codigo_radicado').val()=='' && $('#numero_identificacion').val()!=''){
            $.ajax({
                type: 'GET',
                url: '/correspondencia_radicado',
                data: {numero_identificacion:$('#numero_identificacion').val()},
                success: function (data) {
                    if(data.indicador == 1) {
                        var registros = data.registros;
                        $.each(registros, function(i,item){
                            $('#nombre_radicado').text(registros[0].nombre);
                            $('#identificacion_radicado').text(registros[0].identificacion);
                            $('#campos').append(
                                '<div class="row"> \
                                    <div class="col-3"> \
                                        <p class="form-control form-control-sm">' + registros[i].fecha +'</p> \
                                    </div> \
                                    <div class="col-6">  \
                                        <p class="form-control form-control-sm">'+ registros[i].asunto +'</p> \
                                    </div> \
                                    <div class="col-3"> \
                                        <button class="btn btn-sm btn-block btn-primary codRadicado" name="codRadicado" value="'+ registros[i].codigoRadicado +'">\
                                        <i class="fa fa-search"></i>&emsp;Visualizar&emsp;</button> \
                                    </div> \
                                </div>'
                            );
                        });
                        $('#radicado_modal').modal('show');
                    }
                    else{
                        $('#numero_identificacion').val('');
                        $('#numero_identificacion').focus();
                        notificaciones(data);
                    }
                },
                error: function () {
                    var mensaje = ('Ha ocurrido un error de comunicacion con el servidor');
                    var data = {indicador:0, mensaje:mensaje};
                    notificaciones(data);
                }
            });
        }
        else if($('#codigo_radicado').val()!='' && $('#numero_identificacion').val()==''){
            var cod_radicado = $("#codigo_radicado").val();
            buscar_radicado(cod_radicado);
        }
        else{
            window.location.reload()
        }

    });

    function buscar_radicado(cod_radicado) {
        $.ajax({
            type: 'GET',
            url: '/correspondencia_radicado',
            data: {codigo_radicado: cod_radicado},
            success: function (data) {
                window.location.reload()
            },
            error: function () {
                var mensaje = ('Ha ocurrido un error de comunicacion con el servidor');
                var data = {indicador: 0, mensaje: mensaje};
                notificaciones(data);
            }
        });
        return false;
    }

    $("#campos").on('click','.codRadicado', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var cod_radicado = $(this).val();
        $('#radicado_modal').modal('hide');
        buscar_radicado(cod_radicado);
    });

    $("#forms-escaneo").on('click','.adjunto', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
        if($("#form-"+$(this).val()+" :input[name=adjunto]").val() != 0){
            var form = $("#form-" + $(this).val());
            var parametros = new FormData(form[0]);
            parametros.append("adjunto_id", $(this).val());
            $.ajax({
                type: form.attr('method'),
                url: form.attr('action'),
                data: parametros,
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data.indicador == 0) {
                        notificaciones(data);
                    }
                    else {
                        $('#escaneo-'+valor).remove();
                        notificaciones(data);
                    }
                },
                error: function () {
                    var mensaje = ('Ha ocurrido un error de comunicacion con el servidor');
                    var data = {indicador: 0, mensaje: mensaje};
                    notificaciones(data);
                }
            });
            return false;
        }
        else{
            $("#form-"+$(this).val()).find('input').focus();
        }
    });

    $(".selector_fecha").click(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $(".fecha").focus();
    });

    $("#reporte_corresp_ent").click(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        window.open("/corresp_entrada_pdf", '_blank');
    });
    $("button[name=inhabilitar_usuario]").click(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/inhabilitar_usuario',
            data: {id_usuario: $(this).val()},
            success: function (data) {
                if (data.indicador == 0) {
                    notificaciones(data);
                }
                else {
                    $('#user-'+valor).remove();
                    notificaciones(data);
                }
            },
            error: function () {
                var mensaje = ('Ha ocurrido un error de comunicacion con el servidor');
                var data = {indicador: 0, mensaje: mensaje};
                notificaciones(data);
            }
        });
        return false;
    });

    $("button[name=editar_usuario]").click(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var valor = $(this).val();
		$.ajax({
			url: "/editar_usuario",
			type: 'get',
            data: {id: valor}
        })
        .done(function(data){
            $("#form-guardar_edicion_usuario").trigger("reset");
            $("#editar_usuario").attr('value',data.ids);
            $("#editar_nombres").val(data.nombres);
            $("#editar_apellidos").val(data.apellidos);
            $("#editar_email").val(data.email);
            $("#editar_perfil").val(data.perfil).attr("selected","selected");
            $("#editar_oficina").val(data.oficina).attr("selected","selected");
            $("#edicion_usuario_modal").modal('show');
		})
        .fail(function () {
            var data = {indicador:0,mensaje:'Ha ocurrido un error de comunicacion con el servidor, por favor actualice la pagina'};
            notificaciones(data);
        });
    });


});
