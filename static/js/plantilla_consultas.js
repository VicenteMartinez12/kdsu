
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

      $('#filtroSeleccion input').on('keyup', function () {
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



}
