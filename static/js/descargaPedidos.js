function initDescargaPedidos(){
    initPlantilla()


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
}