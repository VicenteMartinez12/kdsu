
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
      
    }
  });

  $('.ui.dropdown').dropdown();


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
    console.log(`📦 Modo 'all': obteniendo todas las filas de la tabla.`);
  }

  rows.every(function () {
    const row = this.node();
    const checkbox = $(row).find('input[type="checkbox"]');

    if (modo === 'checked' && !checkbox.is(':checked')) return;

    const item = { id: $(row).data('id') };
    campos.forEach((campo, i) => {
      item[campo] = $(row).find(`td:eq(${i + 1})`).text().trim(); // +1 porque el td[0] es el checkbox
    });
    console.log('✅ Registro agregado:', item);
    data.push(item);
  });
  console.log(`📊 Total de registros devueltos (${modo}):`, data.length);
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



//Filtrado de fechas
// Limpiar filtros anteriores
$.fn.dataTable.ext.search = [];

// Definir nuevo filtro personalizado
$.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
  if (!tablaConsultas) return true;

  const row = tablaConsultas.row(dataIndex).node();
  const fechaRow = row.getAttribute('data-fecha'); // Formato: YYYY-MM-DD

  const fechaInicioStr = $('#fechaInicio').val(); // Formato: DD/MM/YYYY
  const fechaFinStr = $('#fechaFin').val();

  if (!fechaInicioStr || !fechaFinStr) return true; // Si no hay rango, mostrar todo

  // Convertir de DD/MM/YYYY a YYYY-MM-DD
  const parseFecha = (str) => {
    const [dd, mm, yyyy] = str.split('/');
    return `${yyyy}-${mm}-${dd}`;
  };

  const fechaInicio = parseFecha(fechaInicioStr);
  const fechaFin = parseFecha(fechaFinStr);

  console.log(`🔍 Filtro de fechas desde ${fechaInicio} hasta ${fechaFin} (fila: ${fechaRow})`);

  // Comparar fechas
  return fechaRow >= fechaInicio && fechaRow <= fechaFin;
});

// Ejecutar filtro al dar clic en Refrescar
$('#btnRefrescar').off('click').on('click', function () {
  console.log('🔄 Aplicando filtros por fechas...');
  if (tablaConsultas) {
    tablaConsultas.draw();
  }
});




function initDetalleModalTable() {
  if ($.fn.DataTable.isDataTable('#tablaDetalle')) {
    $('#tablaDetalle').DataTable().destroy();
  }

  const totalColumnas = $('#tablaDetalle thead th').length;
  console.log('Total columnas en tablaDetalle:', totalColumnas);

  $('#tablaDetalle').DataTable({
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
      const wrapper = $('#tablaDetalle_wrapper');
      const length = wrapper.find('.dataTables_length').detach();
      const info = wrapper.find('.dataTables_info').detach();
      const paginate = wrapper.find('.dataTables_paginate').detach();

      const footer = $('<div class="dataTables_footer"></div>');
      footer.append(length).append(info).append(paginate);
      wrapper.append(footer);
    }
  });
}



$('#tablaPlantillaConsultas').on('click', '.plus.icon', function () {
  const row = $(this).closest('tr');
  const orderId = row.find('td:eq(1)').text();
  const category = row.find('td:eq(2)').text();
  const status = row.find('td:eq(4)').text();

  const tableBody = $('#tablaDetalle tbody');
  tableBody.empty();
  tableBody.append(`
    <tr><td>${orderId}</td><td>${category}</td><td>${status}</td></tr>
  `);

  // Inicializa el DataTable del modal con la misma configuración
  initDetalleModalTable();

  // Muestra el modal
  $('#detalleModal').modal('show');
});


}
