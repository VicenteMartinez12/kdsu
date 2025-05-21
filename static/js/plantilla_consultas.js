
let tablaConsultas;

function initPlantilla() {
  // Si ya existe una instancia previa del datatable, destrúyela
  if ($.fn.DataTable.isDataTable('#tablaPlantillaConsultas')) {
    $('#tablaPlantillaConsultas').DataTable().destroy();
  }
  const totalColumnas = $('#tablaPlantillaConsultas thead th').length;
  console.log(totalColumnas);
  // Ahora sí, creamos la nueva instancia
  tablaConsultas = $('#tablaPlantillaConsultas').DataTable({
    dom: 'lrtip',
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      zeroRecords: "No se encontraron resultados",
      info: "Mostrando _START_ de _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      }
    },
    columnDefs: [
      { orderable: false, targets: [0, totalColumnas - 1] }
    ],
    order: [],
    initComplete: function () {
      
      $('#tablaPlantillaConsultas').fadeIn();

      const wrapper = $('#tablaPlantillaConsultas_wrapper');
      const length = wrapper.find('.dataTables_length').detach();
      const info = wrapper.find('.dataTables_info').detach();
      const paginate = wrapper.find('.dataTables_paginate').detach();

      const footer = $('<div class="dataTables_footer"></div>');
      footer.append(length).append(info).append(paginate);
      wrapper.append(footer);

      $('#filtroTexto').on('keyup', function () {
        tablaConsultas.search(this.value).draw();
      });
       hideWaitScreen();
      
    }
  });

  $('.ui.dropdown').dropdown();
  configurarFiltradoFechas();

//  Checkbox global que selecciona todas las filas de todas las páginas
$('#tablaPlantillaConsultas thead').on('change', '#checkAll', function () {
  const isChecked = $(this).is(':checked');
  tablaConsultas.rows().every(function () {
    const row = this.node();
    $(row).find('input[type="checkbox"]').prop('checked', isChecked);
  });
});


//  Verifica si todos los checkbox están seleccionados en todas las páginas
$('#tablaPlantillaConsultas tbody').on('change', 'input[type="checkbox"]', function () {
  const total = tablaConsultas.rows().nodes().length;
  const checked = tablaConsultas.rows().nodes().to$().find('input[type="checkbox"]:checked').length;
  $('#checkAll').prop('checked', total === checked);
});


// Placeholder para futuras acciones
$('#tablaPlantillaConsultas').on('click', '.activar', function () {
  const id = $(this).closest('tr').data('id');
  alert('Activar/Desactivar ID: ' + id);
});

$('#tablaPlantillaConsultas').on('click', '.eliminar', function () {
  const id = $(this).closest('tr').data('id');
  alert('Eliminar ID: ' + id);
});

// Exponer función para obtener registros
window.getCatalogoRegistros = function (modo = 'all') {
  const campos = window.camposCatalogo || [];
  const tablaConsultas = $('#tablaPlantillaConsultas').DataTable();
  let data = [];
  let rows;

  if (modo === 'checked' || modo === 'filtered') {
    rows = tablaConsultas.rows({ search: 'applied' });
    console.log(`🔍 Modo '${modo}': obteniendo filas visibles en pantalla.`);
  } else {
    rows = tablaConsultas.rows();
    console.log(` Modo 'all': obteniendo todas las filas de la tabla.`);
  }

  rows.every(function () {
    const row = this.node();
    const checkbox = $(row).find('input[type="checkbox"]');

    if (modo === 'checked' && !checkbox.is(':checked')) return;

    const $row = $(row);

    const item = {
      id: $row.data('id'),
      company_id: $row.data('company-id') || null 
    };

    campos.forEach((campo, i) => {
      item[campo] = $row.find(`td:eq(${i + 1})`).text().trim(); 
    });

    console.log('✅ Registro agregado:', item);
    data.push(item);
  });

  console.log(`Total de registros devueltos (${modo}):`, data.length);
  return data;
};




$('#rangestart').calendar({
  type: 'date',
  endCalendar: $('#rangeend'),
  formatter: {
    date: function (date, settings) {
      if (!date) return '';
      const yyyy = date.getFullYear();
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const dd = String(date.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }
  }
});

$('#rangeend').calendar({
  type: 'date',
  startCalendar: $('#rangestart'),
  formatter: {
    date: function (date, settings) {
      if (!date) return '';
      const yyyy = date.getFullYear();
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const dd = String(date.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }
  }
});

// Forzar perder el foco inmediatamente al intentar escribir o enfocar
$('#fechaInicio, #fechaFin').on('focus', function(e) {
  $(this).blur();
});

$('#rangestart').calendar({
  type: 'date',
  endCalendar: $('#rangeend'),
  text: {
    days: ['D', 'L', 'M', 'M', 'J', 'V', 'S'],
    months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthsShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    today: 'Hoy',
    now: 'Ahora',
    am: 'AM',
    pm: 'PM'
  },
  formatter: {
    date: function (date, settings) {
      if (!date) return '';
      const dd = String(date.getDate()).padStart(2, '0');
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const yyyy = date.getFullYear();
      return `${dd}/${mm}/${yyyy}`;  // Día/Mes/Año en números
    }
  }
});

$('#rangeend').calendar({
  type: 'date',
  startCalendar: $('#rangestart'),
  text: {
    days: ['D', 'L', 'M', 'M', 'J', 'V', 'S'],
    months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthsShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    today: 'Hoy',
    now: 'Ahora',
    am: 'AM',
    pm: 'PM'
  },
  formatter: {
    date: function (date, settings) {
      if (!date) return '';
      const dd = String(date.getDate()).padStart(2, '0');
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const yyyy = date.getFullYear();
      return `${dd}/${mm}/${yyyy}`;  // Día/Mes/Año en números
    }
  }
});


function configurarFiltradoFechas() {
  $.fn.dataTable.ext.search = [];
  $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    if (!tablaConsultas) return true;
    const row = tablaConsultas.row(dataIndex).node();
    const fechaRow = row.getAttribute('data-fecha');
    const fechaInicio = $('#fechaInicio').val();
    const fechaFin = $('#fechaFin').val();
    if (!fechaInicio || !fechaFin) return true;
    const parseFecha = str => str.split('/').reverse().join('-');
    return fechaRow >= parseFecha(fechaInicio) && fechaRow <= parseFecha(fechaFin);
  });

  $('#btnRefrescar').off('click').on('click', function () {
    if (tablaConsultas) tablaConsultas.draw();
  });
}



function mostrarModalDetalles(modalId = 'detalleModal') {
  $(`#${modalId}`).modal('show');
}

function configurarTabs(modalId = 'detalleModal') {
  $(`#${modalId} .menu .item`).tab({
    onVisible: function (tabPath) {
      console.log(`Tab activo: ${tabPath}`);
      $(`#${modalId} .tab.segment`).hide();
      $(`#${modalId} .tab.segment[data-tab="${tabPath}"]`).show();
    }
  });
}

window.cargarContenidoEnModal = function ({ modalId, tableMappings, fetchUrl }) {
  console.log("Cargando contenido del modal desde:", fetchUrl);
  $.ajax({
    url: fetchUrl,
    method: 'GET',
    success: function (data) {
      tableMappings.forEach(mapping => {
        inicializarYMostrarDatos(`#${mapping.tableId}`, data[mapping.dataKey]);
      });
      configurarTabs(modalId);

      
      const firstTab = $(`#${modalId} .menu .item`).first();
      const firstTabPath = firstTab.data('tab');
      firstTab.addClass('active').siblings().removeClass('active');
      $(`#${modalId} .tab.segment`).hide();
      $(`#${modalId} .tab.segment[data-tab="${firstTabPath}"]`).show();
   
      mostrarModalDetalles(modalId);
    },
    error: function () {
      console.error("Error al cargar datos en el modal.");
    }
  });
};


function inicializarYMostrarDatos(selectorTabla, datos) {
  const $tabla = $(selectorTabla);

  if (!$tabla.length || !$tabla.find('thead th').length) {
    console.warn(`⚠️ La tabla ${selectorTabla} no está en el DOM o no tiene columnas definidas.`);
    return;
  }

  // Destruir y limpiar tabla previa
  if ($.fn.DataTable.isDataTable(selectorTabla)) {
    $tabla.DataTable().destroy();
    $tabla.closest('.dataTables_wrapper').remove();
  }

  // Limpiar tbody
  $tabla.find('tbody').empty();

  // Reconstruir tabla limpia
  const cleanTable = $(`<table id="${selectorTabla.replace('#', '')}" class="ui celled table">
    ${$tabla.html()}
  </table>`);
  $(selectorTabla).replaceWith(cleanTable);

  const totalColumnas = cleanTable.find('thead th').length;
  console.log(`Inicializando ${selectorTabla} con ${totalColumnas} columnas`);

  const dt = cleanTable.DataTable({
    dom: 'lrtip',
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      zeroRecords: "No se encontraron resultados",
      info: "Mostrando _START_ de _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      }
    },
    columnDefs: [
     
    ],
    order: [],
    initComplete: function () {
      cleanTable.fadeIn();
      const wrapper = $(`${selectorTabla}_wrapper`);
      wrapper.find('.dataTables_footer').remove();
      const length = wrapper.find('.dataTables_length').detach();
      const info = wrapper.find('.dataTables_info').detach();
      const paginate = wrapper.find('.dataTables_paginate').detach();
      const footer = $('<div class="dataTables_footer"></div>');
      footer.append(length).append(info).append(paginate);
      wrapper.append(footer);
    }
  });

  // Agregar datos
  if (Array.isArray(datos)) {
    datos.forEach(row => dt.row.add(Object.values(row)));
  }

  dt.draw();
}


// Limpieza de overlays duplicados o huérfanos
$('.ui.dimmer.modals').remove();

}