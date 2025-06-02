function initDescargaPedidos(){
    initPlantilla()



    $('#exportarPdf').on('click', function () {
      const registros = window.getCatalogoRegistros('checked');
      if (registros.length === 0) {
        alert('Selecciona al menos una orden.');
        return;
      }
    
      const companyIds = registros.map(r => r.company_id);
      const uniqueCompanyIds = [...new Set(companyIds)];
    
      if (uniqueCompanyIds.length > 1) {
        alert('Todas las órdenes seleccionadas deben pertenecer a la misma compañía.');
        return;
      }
    
      const companyId = uniqueCompanyIds[0];
      if (!companyId) {
        alert('No se encontró el company_id en una o más órdenes.');
        return;
      }
    
      const ids = registros.map(r => r.id);
      const url = `/orders/export_pdf/?` + ids.map(id => `order_ids[]=${id}`).join('&');
      window.open(url, '_blank');
    });
  
  
  
  
  
  
  
    $('#exportarXml').on('click', function () {
      const registros = window.getCatalogoRegistros('checked');
      if (registros.length === 0) {
        alert('Selecciona al menos una orden.');
        return;
      }
    
      const companyIds = registros.map(r => r.company_id);
      const uniqueCompanyIds = [...new Set(companyIds)];
    
      if (uniqueCompanyIds.length > 1) {
        alert('Todas las órdenes seleccionadas deben pertenecer a la misma compañía.');
        return;
      }
    
      const companyId = uniqueCompanyIds[0];
      if (!companyId) {
        alert('No se encontró el company_id en una o más órdenes.');
        return;
      }
    
      const ids = registros.map(r => r.id);
      const url = `/orders/export_xml/?` + ids.map(id => `order_ids[]=${id}`).join('&');
      window.open(url, '_blank');
    });
  
  
    $('#exportarExcel').on('click', function () {
      const registros = window.getCatalogoRegistros('checked');
      if (registros.length === 0) {
        alert('Selecciona al menos una orden.');
        return;
      }
    
      const companyIds = registros.map(r => r.company_id);
      const uniqueCompanyIds = [...new Set(companyIds)];
    
      if (uniqueCompanyIds.length > 1) {
        alert('Todas las órdenes deben ser de la misma compañía.');
        return;
      }
    
      const ids = registros.map(r => r.id);
      const url = `/orders/export_xml_excel/?` + ids.map(id => `order_ids[]=${id}`).join('&');
      window.open(url, '_blank');
    });


    $('#tablaPlantillaConsultas').off('click', '.plus.icon').on('click', '.plus.icon', function () {
        const orderId = $(this).closest('tr').data('id');
        cargarContenidoEnModal({
          modalId: 'detalleDescargaPedidos',
          tableMappings: [
            { tableId: 'tablaDescargaPedidos', dataKey: 'descargaPedidos' },
          ],
          fetchUrl: `/orders/detalle_descarga_pedidos/${orderId}/`
        });
      });

      $('#btnRefrescarDescargaPedidos').on('click', function () {
        const companyId = $('#filtroCompania').val();
        const status = $('#filtroEstatus').val();
      
        $.ajax({
          url: '/orders/descarga_pedidos/',
          type: 'GET',
          data: {
            company_id: companyId,
            status: status
          },
          success: function (data) {
            const overlay = $('#globalWaitOverlay');
            if (overlay.length) {
              $('body').append(overlay.detach());
            }
      
            $('.ui.dimmer.modals').removeClass('active').removeAttr('style');
            $('.ui.modal').modal('hide').remove();
      
            $('#mainContent').html(data);
            initDescargaPedidos();  // <-- esto vuelve a activar todo
          },
          error: function (xhr, status, error) {
            console.error("Error al refrescar:", status, error);
            $('#mainContent').html(`
              <div class="ui negative message">
                <div class="header">Error al cargar el contenido</div>
                <p>${xhr.status} - ${xhr.statusText}</p>
              </div>
            `);
          }
        });
      });
      


    function configurarVisibilidadFechasPorEstatus() {
      const $estatus = $('#filtroEstatus');
      const $fecha1 = $('#fecha1');
      const $fecha2 = $('#fecha2');
      
      function toggleFechas() {
        const valor = $estatus.val();
        if (valor === 'Pendiente') {
          $fecha1.show();
          $fecha2.show();
        } else {
          $fecha1.hide();
          $fecha2.hide();
        }
      }
    
      $estatus.on('change', toggleFechas);
      toggleFechas(); // Ejecuta al cargar
    }
      
      
    configurarVisibilidadFechasPorEstatus();


      // Función para mostrar/ocultar columna F.Descarga
      function actualizarColumnaFechaDescarga() {
        const estatus = $('#filtroEstatus').val();
    
        if (estatus === 'Pendiente') {
          $('.fecha-descarga').show();
        } else {
          $('.fecha-descarga').hide();
        }
      }
    
      // Ejecutar al cargar la página
      actualizarColumnaFechaDescarga();
    
      // Ejecutar cuando se cambia el estatus
      $('#filtroEstatus').on('change', function () {
        actualizarColumnaFechaDescarga();
      });
  












      
    
}