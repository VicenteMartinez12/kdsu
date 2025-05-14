let tabsConfigurados = false;

function configurarTabs() {
  if (tabsConfigurados) return;

  $('#detalleModal .menu .item').tab({
    onVisible: function(tabPath) {
      console.log('Tab activo:', tabPath);
      $('#detalleModal .tab.segment').hide();
      $(`#detalleModal .tab.segment[data-tab="${tabPath}"]`).show();
    }
  });

  tabsConfigurados = true;
}


function initPdf() {
  console.log("Inicializando plantilla PDF...");

  // Aquí podrías cargar datos dinámicamente si lo necesitas
  // Por ahora solo inicializa el comportamiento base de plantilla
  initPlantilla();

  // Aquí puedes agregar lógica específica para PDF si lo deseas
  $('#exportarCsv').off('click').on('click', function () {
    console.log("Exportar CSV desde PDF");
  });

  $('#exportarJson').off('click').on('click', function () {
    console.log("Exportar JSON desde PDF");
  });

  $('#exportarXml').off('click').on('click', function () {
    console.log("Exportar XML desde PDF");
  });
}
