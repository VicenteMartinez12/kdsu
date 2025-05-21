function configurarTabsPdf() {
  $('#detalleModal .menu .item').tab({
    onVisible: function (tabPath) {
      $('#detalleModal .tab.segment').hide();
      $(`#detalleModal .tab.segment[data-tab="${tabPath}"]`).show();
    }
  });
}

function initPdf() {
  initPlantilla();
  configurarTabsPdf();

  $('#exportarPdf').on('click', function () {
    const registros = window.getCatalogoRegistros('checked');
    if (registros.length === 0) {
      alert('Selecciona al menos una orden.');
      return;
    }

    const ids = registros.map(r => r.id);
  const firstOrderId = registros[0].id;
const firstRow = $(`#tablaPlantillaConsultas tr[data-id="${firstOrderId}"]`);
const companyId = firstRow.data('company-id');

    const url = `/orders/export_pdf/?company_id=${companyId}&` + ids.map(id => `order_ids[]=${id}`).join('&');
    window.open(url, '_blank');
  });

  $('#tablaPlantillaConsultas').off('click', '.plus.icon').on('click', '.plus.icon', function () {
    const orderId = $(this).closest('tr').data('id');
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
