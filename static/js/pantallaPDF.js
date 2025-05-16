function configurarTabsPdf() {
  console.log("Configurando tabs para PDF");
  $('#detalleModal .menu .item').tab({
    onVisible: function (tabPath) {
      console.log(`Tab activo: ${tabPath}`);
      $('#detalleModal .tab.segment').hide();
      $(`#detalleModal .tab.segment[data-tab="${tabPath}"]`).show();
    }
  });
}

function initPdf() {
  console.log("Inicializando plantilla PDF...");

  initPlantilla();
  configurarTabsPdf();

  $('#exportarPdf').on('click', function () {
    const registros = window.getCatalogoRegistros('checked');
    if (registros.length === 0) {
      alert('Selecciona al menos una orden.');
      return;
    }
    const ids = registros.map(r => r.id);
    const companyId = 1; // O toma el id de la compañía activa en tu contexto
  
    const url = `/orders/pdf/?company_id=${companyId}&` + ids.map(id => `order_ids[]=${id}`).join('&');
    window.open(url, '_blank');
  });

  $('#tablaPlantillaConsultas').off('click', '.plus.icon').on('click', '.plus.icon', function () {
    const orderId = $(this).closest('tr').data('id');  // Se llama orderId
    console.log("Abriendo detalle para la orden:", orderId);

    cargarContenidoEnModal({
      modalId: 'detalleModal',
      tableMappings: [
        { tableId: 'tablaDetalle', dataKey: 'detalles' },
        { tableId: 'tablaCostos', dataKey: 'costos' }
      ],
      fetchUrl: `/orders/detalle_orden/${orderId}/`
    });
  });
}



