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

  $('#exportarPdf').off('click').on('click', function () {
    console.log("Exportando a PDF...");
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
