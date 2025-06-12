//const api = "http://10.105.17.29:8092/kdsu/";
//const api = "http://192.168.100.241:8092/kdsu/";
///100.126
const api = "http://localhost:8000/";
const portal = api + "appointments/";
const SUPPLIER_TYPES = {
  NORMAL: "0",
  MENSAJERIA: "1",
  INTERNO: "2",
};
const SHIPMENT_TYPES = {
  CENTRA: 1,
  SUCURSAL: 2,
};

const LOAD_TYPES = {
  PALLET: 1,
  BOXES: 2,
  BULK: 3,
  MIXED: 4,
};

let pgCalendarioCitasTipoProveedor = null;
let kdsuParams = new URLSearchParams(window.location.search);
let bIsCentra = true;
let transportData = {};
let layoutOpt = {
  topStart: null,
  topEnd: null,
  //bottomStart: "info",
  bottomEnd: "paging",
  bottomStart: null,
  //bottomEnd: null,
};
const getDataTableLanguage = async () => {
  return {
    aria: {
      sortAscending: "Activar para ordenar la columna de manera ascendente",
      sortDescending: "Activar para ordenar la columna de manera descendente",
    },
    autoFill: {
      cancel: "Cancelar",
      fill: "Rellene todas las celdas con <i>%d</i>",
      fillHorizontal: "Rellenar celdas horizontalmente",
      fillVertical: "Rellenar celdas verticalmente",
    },
    buttons: {
      collection: "Colección",
      colvis: "Visibilidad",
      colvisRestore: "Restaurar visibilidad",
      copy: "Copiar",
      copyKeys:
        "Presione ctrl o u2318 + C para copiar los datos de la tabla al portapapeles del sistema. <br /> <br /> Para cancelar, haga clic en este mensaje o presione escape.",
      copySuccess: {
        1: "Copiada 1 fila al portapapeles",
        _: "Copiadas %d fila al portapapeles",
      },
      copyTitle: "Copiar al portapapeles",
      csv: "CSV",
      excel: "Excel",
      pageLength: {
        "-1": "Mostrar todas las filas",
        _: "Mostrar %d filas",
      },
      pdf: "PDF",
      print: "Imprimir",
      createState: "Crear Estado",
      removeAllStates: "Borrar Todos los Estados",
      removeState: "Borrar Estado",
      renameState: "Renombrar Estado",
      savedStates: "Guardar Estado",
      stateRestore: "Restaurar Estado",
      updateState: "Actualizar Estado",
    },
    infoThousands: ",",
    loadingRecords: "Cargando...",
    paginate: {
      first: "Primero",
      last: "Último",
      next: "Siguiente",
      previous: "Anterior",
    },
    processing: "Procesando...",
    search: "Buscar:",
    searchBuilder: {
      add: "Añadir condición",
      button: {
        0: "Constructor de búsqueda",
        _: "Constructor de búsqueda (%d)",
      },
      clearAll: "Borrar todo",
      condition: "Condición",
      deleteTitle: "Eliminar regla de filtrado",
      leftTitle: "Criterios anulados",
      logicAnd: "Y",
      logicOr: "O",
      rightTitle: "Criterios de sangría",
      title: {
        0: "Constructor de búsqueda",
        _: "Constructor de búsqueda (%d)",
      },
      value: "Valor",
      conditions: {
        date: {
          after: "Después",
          before: "Antes",
          between: "Entre",
          empty: "Vacío",
          equals: "Igual a",
          not: "Diferente de",
          notBetween: "No entre",
          notEmpty: "No vacío",
        },
        number: {
          between: "Entre",
          empty: "Vacío",
          equals: "Igual a",
          gt: "Mayor a",
          gte: "Mayor o igual a",
          lt: "Menor que",
          lte: "Menor o igual a",
          not: "Diferente de",
          notBetween: "No entre",
          notEmpty: "No vacío",
        },
        string: {
          contains: "Contiene",
          empty: "Vacío",
          endsWith: "Termina con",
          equals: "Igual a",
          not: "Diferente de",
          startsWith: "Inicia con",
          notEmpty: "No vacío",
          notContains: "No Contiene",
          notEndsWith: "No Termina",
          notStartsWith: "No Comienza",
        },
        array: {
          equals: "Igual a",
          empty: "Vacío",
          contains: "Contiene",
          not: "Diferente",
          notEmpty: "No vacío",
          without: "Sin",
        },
      },
      data: "Datos",
    },
    searchPanes: {
      clearMessage: "Borrar todo",
      collapse: {
        0: "Paneles de búsqueda",
        _: "Paneles de búsqueda (%d)",
      },
      count: "{total}",
      emptyPanes: "Sin paneles de búsqueda",
      loadMessage: "Cargando paneles de búsqueda",
      title: "Filtros Activos - %d",
      countFiltered: "{shown} ({total})",
      collapseMessage: "Colapsar",
      showMessage: "Mostrar Todo",
    },
    select: {
      cells: {
        1: "1 celda seleccionada",
        _: "%d celdas seleccionadas",
      },
      columns: {
        1: "1 columna seleccionada",
        _: "%d columnas seleccionadas",
      },
      rows: {
        1: "1 fila seleccionada",
        _: "%d filas seleccionadas",
      },
    },
    thousands: ",",
    datetime: {
      previous: "Anterior",
      hours: "Horas",
      minutes: "Minutos",
      seconds: "Segundos",
      unknown: "-",
      amPm: ["am", "pm"],
      next: "Siguiente",
      months: {
        0: "Enero",
        1: "Febrero",
        10: "Noviembre",
        11: "Diciembre",
        2: "Marzo",
        3: "Abril",
        4: "Mayo",
        5: "Junio",
        6: "Julio",
        7: "Agosto",
        8: "Septiembre",
        9: "Octubre",
      },
      weekdays: [
        "Domingo",
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
      ],
    },
    editor: {
      close: "Cerrar",
      create: {
        button: "Nuevo",
        title: "Crear Nuevo Registro",
        submit: "Crear",
      },
      edit: {
        button: "Editar",
        title: "Editar Registro",
        submit: "Actualizar",
      },
      remove: {
        button: "Eliminar",
        title: "Eliminar Registro",
        submit: "Eliminar",
        confirm: {
          _: "¿Está seguro que desea eliminar %d filas?",
          1: "¿Está seguro que desea eliminar 1 fila?",
        },
      },
      multi: {
        title: "Múltiples Valores",
        restore: "Deshacer Cambios",
        noMulti:
          "Este registro puede ser editado individualmente, pero no como parte de un grupo.",
        info: "Los elementos seleccionados contienen diferentes valores para este registro. Para editar y establecer todos los elementos de este registro con el mismo valor, haga click o toque aquí, de lo contrario conservarán sus valores individuales.",
      },
      error: {
        system:
          'Ha ocurrido un error en el sistema (<a target="\\" rel="\\ nofollow" href="\\"> Más información</a>).',
      },
    },
    decimal: ".",
    emptyTable: "No hay datos disponibles en la tabla",
    zeroRecords: "No se encontraron coincidencias",
    info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
    infoFiltered: "(Filtrado de _MAX_ total de entradas)",
    lengthMenu: "Mostrar _MENU_ entradas",
    stateRestore: {
      removeTitle: "Eliminar",
      creationModal: {
        search: "Buscar",
        button: "Crear",
        columns: {
          search: "Columna de búsqueda",
          visible: "Columna de visibilidad",
        },
        name: "Nombre:",
        order: "Ordenar",
        paging: "Paginar",
        scroller: "Posición de desplazamiento",
        searchBuilder: "Creador de búsquedas",
        select: "Selector",
        title: "Crear nuevo",
        toggleLabel: "Incluye:",
      },
      duplicateError: "Ya existe un valor con el mismo nombre",
      emptyError: "No puede ser vacío",
      emptyStates: "No se han guardado",
      removeConfirm: "Esta seguro de eliminar %s?",
      removeError: "Fallo al eliminar",
      removeJoiner: "y",
      removeSubmit: "Eliminar",
      renameButton: "Renombrar",
      renameLabel: "Nuevo nombre para %s:",
      renameTitle: "Renombrar",
    },
    infoEmpty: "No hay datos para mostrar",
  };
};

const esMX = {
  aria: {
    sortAscending: "Activar para ordenar la columna de manera ascendente",
    sortDescending: "Activar para ordenar la columna de manera descendente",
  },
  autoFill: {
    cancel: "Cancelar",
    fill: "Rellene todas las celdas con <i>%d</i>",
    fillHorizontal: "Rellenar celdas horizontalmente",
    fillVertical: "Rellenar celdas verticalmente",
  },
  buttons: {
    collection: "Colección",
    colvis: "Visibilidad",
    colvisRestore: "Restaurar visibilidad",
    copy: "Copiar",
    copyKeys:
      "Presione ctrl o u2318 + C para copiar los datos de la tabla al portapapeles del sistema. <br /> <br /> Para cancelar, haga clic en este mensaje o presione escape.",
    copySuccess: {
      1: "Copiada 1 fila al portapapeles",
      _: "Copiadas %d fila al portapapeles",
    },
    copyTitle: "Copiar al portapapeles",
    csv: "CSV",
    excel: "Excel",
    pageLength: {
      "-1": "Mostrar todas las filas",
      _: "Mostrar %d filas",
    },
    pdf: "PDF",
    print: "Imprimir",
    createState: "Crear Estado",
    removeAllStates: "Borrar Todos los Estados",
    removeState: "Borrar Estado",
    renameState: "Renombrar Estado",
    savedStates: "Guardar Estado",
    stateRestore: "Restaurar Estado",
    updateState: "Actualizar Estado",
  },
  infoThousands: ",",
  loadingRecords: "Cargando...",
  paginate: {
    first: "Primero",
    last: "Último",
    next: "Siguiente",
    previous: "Anterior",
  },
  processing: "Procesando...",
  search: "Buscar:",
  searchBuilder: {
    add: "Añadir condición",
    button: {
      0: "Constructor de búsqueda",
      _: "Constructor de búsqueda (%d)",
    },
    clearAll: "Borrar todo",
    condition: "Condición",
    deleteTitle: "Eliminar regla de filtrado",
    leftTitle: "Criterios anulados",
    logicAnd: "Y",
    logicOr: "O",
    rightTitle: "Criterios de sangría",
    title: {
      0: "Constructor de búsqueda",
      _: "Constructor de búsqueda (%d)",
    },
    value: "Valor",
    conditions: {
      date: {
        after: "Después",
        before: "Antes",
        between: "Entre",
        empty: "Vacío",
        equals: "Igual a",
        not: "Diferente de",
        notBetween: "No entre",
        notEmpty: "No vacío",
      },
      number: {
        between: "Entre",
        empty: "Vacío",
        equals: "Igual a",
        gt: "Mayor a",
        gte: "Mayor o igual a",
        lt: "Menor que",
        lte: "Menor o igual a",
        not: "Diferente de",
        notBetween: "No entre",
        notEmpty: "No vacío",
      },
      string: {
        contains: "Contiene",
        empty: "Vacío",
        endsWith: "Termina con",
        equals: "Igual a",
        not: "Diferente de",
        startsWith: "Inicia con",
        notEmpty: "No vacío",
        notContains: "No Contiene",
        notEndsWith: "No Termina",
        notStartsWith: "No Comienza",
      },
      array: {
        equals: "Igual a",
        empty: "Vacío",
        contains: "Contiene",
        not: "Diferente",
        notEmpty: "No vacío",
        without: "Sin",
      },
    },
    data: "Datos",
  },
  searchPanes: {
    clearMessage: "Borrar todo",
    collapse: {
      0: "Paneles de búsqueda",
      _: "Paneles de búsqueda (%d)",
    },
    count: "{total}",
    emptyPanes: "Sin paneles de búsqueda",
    loadMessage: "Cargando paneles de búsqueda",
    title: "Filtros Activos - %d",
    countFiltered: "{shown} ({total})",
    collapseMessage: "Colapsar",
    showMessage: "Mostrar Todo",
  },
  select: {
    cells: {
      1: "1 celda seleccionada",
      _: "%d celdas seleccionadas",
    },
    columns: {
      1: "1 columna seleccionada",
      _: "%d columnas seleccionadas",
    },
    rows: {
      1: "1 fila seleccionada",
      _: "%d filas seleccionadas",
    },
  },
  thousands: ",",
  datetime: {
    previous: "Anterior",
    hours: "Horas",
    minutes: "Minutos",
    seconds: "Segundos",
    unknown: "-",
    amPm: ["am", "pm"],
    next: "Siguiente",
    months: {
      0: "Enero",
      1: "Febrero",
      10: "Noviembre",
      11: "Diciembre",
      2: "Marzo",
      3: "Abril",
      4: "Mayo",
      5: "Junio",
      6: "Julio",
      7: "Agosto",
      8: "Septiembre",
      9: "Octubre",
    },
    weekdays: [
      "Domingo",
      "Lunes",
      "Martes",
      "Miércoles",
      "Jueves",
      "Viernes",
      "Sábado",
    ],
  },
  editor: {
    close: "Cerrar",
    create: {
      button: "Nuevo",
      title: "Crear Nuevo Registro",
      submit: "Crear",
    },
    edit: {
      button: "Editar",
      title: "Editar Registro",
      submit: "Actualizar",
    },
    remove: {
      button: "Eliminar",
      title: "Eliminar Registro",
      submit: "Eliminar",
      confirm: {
        _: "¿Está seguro que desea eliminar %d filas?",
        1: "¿Está seguro que desea eliminar 1 fila?",
      },
    },
    multi: {
      title: "Múltiples Valores",
      restore: "Deshacer Cambios",
      noMulti:
        "Este registro puede ser editado individualmente, pero no como parte de un grupo.",
      info: "Los elementos seleccionados contienen diferentes valores para este registro. Para editar y establecer todos los elementos de este registro con el mismo valor, haga click o toque aquí, de lo contrario conservarán sus valores individuales.",
    },
    error: {
      system:
        'Ha ocurrido un error en el sistema (<a target="\\" rel="\\ nofollow" href="\\"> Más información</a>).',
    },
  },
  decimal: ".",
  emptyTable: "No hay datos disponibles en la tabla",
  zeroRecords: "No se encontraron coincidencias",
  info: "Registros: _START_ de _TOTAL_",
  infoFiltered: "(Filtrado de _MAX_ total de entradas)",
  lengthMenu: "_MENU_",
  stateRestore: {
    removeTitle: "Eliminar",
    creationModal: {
      search: "Buscar",
      button: "Crear",
      columns: {
        search: "Columna de búsqueda",
        visible: "Columna de visibilidad",
      },
      name: "Nombre:",
      order: "Ordenar",
      paging: "Paginar",
      scroller: "Posición de desplazamiento",
      searchBuilder: "Creador de búsquedas",
      select: "Selector",
      title: "Crear nuevo",
      toggleLabel: "Incluye:",
    },
    duplicateError: "Ya existe un valor con el mismo nombre",
    emptyError: "No puede ser vacío",
    emptyStates: "No se han guardado",
    removeConfirm: "Esta seguro de eliminar %s?",
    removeError: "Fallo al eliminar",
    removeJoiner: "y",
    removeSubmit: "Eliminar",
    renameButton: "Renombrar",
    renameLabel: "Nuevo nombre para %s:",
    renameTitle: "Renombrar",
  },
  infoEmpty: "No hay datos para mostrar",
};

const selectionRel = {
  create: "multi",
  view: "single",
  modify: "single",
  delete: "single",
};

const defaultDTConfig = (rel) => {
  return {
    aaData: [],
    layout: layoutOpt,
    select: {
      //toggleable: false,
      style: selectionRel[rel],
      //info: false,
    },
    language: esMX,
    columnDefs: [
      {
        targets: 0,
        className: "dt-control",
        searchable: false,
        orderable: false,
        /*render: function (data, type, row, meta) {
        return `<input data-appointment="${row[1]}"  data-appointmentType="${row[9]}" class="chk-new" type="checkbox" name="" onchange="handleRowSelect(this)" />`;
      },*/
      },
      {
        targets: [1, 2, 3, 4, 5, 6, 7],
        searchable: true,
        orderable: false,
      },
      {
        targets: 8,
        visible: true,
      },
    ],
    initComplete: function () {
      const api = this.api();
      api.columns().every(function () {
        let column = this;
        let title = column.header().textContent;
        if (column.index() == 0 && rel == "create") {
          let checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.className = "form-control";
          checkbox.style.height = "15px";
          column.header().replaceChildren(checkbox);
          const dtInstance = this;
          checkbox.addEventListener("click", function () {
            dtInstance.context[0].api.rows().select();
          });
        }
        if (column.index() != 0 && column.index() != 9) {
          // Create input element
          let input = document.createElement("input");
          input.placeholder = title;
          input.className = "ui input form-control";
          input.placeholder = "";
          column.header().replaceChildren(input);

          // Event listener for user input
          input.addEventListener("keyup", () => {
            if (column.search() !== this.value) {
              column.search(input.value).draw();
            }
          });
        }
      });
    },
  };
};

function warningMsg(msg) {
  document.getElementById("warningBody").textContent = msg;
  $("#modal-warning").modal({
    allowMultiple: true,
  });
  $("#modal-warning").modal("show");
}

function successMsg(msg, footerMessages = "") {
  document
    .querySelectorAll("#modal-success .content  p")
    .forEach((p) => p.remove());
  if (footerMessages.length > 0) {
    let textNodes = [];
    const p = document.createElement("p");
    p.textContent = footerMessages;
    p.className = "text-muted text-left";
    footerMessages.forEach((t) => {
      const p = document.createElement("p");
      p.textContent = t;
      p.className = "text-muted text-left";
      p.style.lineHeight = ".9rem";
      textNodes.push(p);
    });

    textNodes.forEach((n) => {
      document.getElementById("successBody").prepend(n);
    });
  }
  document
    .getElementById("successBody")
    .insertAdjacentHTML("afterbegin", "<p>" + msg + "</p>");

  $("#modal-success").modal("show");
}

function showLoading(show = true) {
  show
    ? (document.querySelector(".loader").style.display = "flex")
    : (document.querySelector(".loader").style.display = "none");
}

async function loadUIVariables() {
  const urlParams = new URLSearchParams(window.location.search);
  kdsuParams = {
    token: urlParams.get("token"),
    module: urlParams.get("module"),
  };
  //loadPermissions();

  const renewalDate = new Date().toLocaleString("es-ES");
  document.querySelector("#last-update").textContent =
    "Actualizado el: " + renewalDate;
  if (bIsCentra) {
    //document.querySelector("#liConfirm").style.display = "inline";
  }
  document.querySelector("#ipt-pallets").value = 0;
  document.querySelector("#ipt-volume").value = 1;
  //CambiaPaginaProvCI
  //012
  /*
  //Page_Init
  const metrics = await CentraMetrics({
    token: kdsuParams.token,
    modulo: kdsuParams.module,
  });

  if (metrics.hasOwnProperty("success")) {
    if (!metrics.success) {
      console.log(metrics.success, "|||||");
      warningMsg("Error al consultar información de usuario");
      //window.location.reload();
    }
  } else {
    console.error();
    metrics.data.TipoProveedor;
  }

  if (metrics.data.TipoProveedor.toString() == SUPPLIER_TYPES.MENSAJERIA) {
    //PROV MENSAJERÍA
    pgCalendarioCitasTipoProveedor == SUPPLIER_TYPES.MENSAJERIA;
  } else if (
    metrics.data.TipoProveedor.toString() == SUPPLIER_TYPES.MENSAJERIA
  ) {
    //PROV CONSUMO INTERNO
    pgCalendarioCitasTipoProveedor = SUPPLIER_TYPES.MENSAJERIA;
  } else {
    //PROV NORMAL
    pgCalendarioCitasTipoProveedor = SUPPLIER_TYPES.NORMAL;
  }
 */
  /*  if (pgCalendarioCitasTipoProveedor == SUPPLIER_TYPES.NORMAL) {
    document.querySelector("#btnModify").style.display = "block";
    document.querySelector("#btnCancel").style.display = "block";
    document.querySelector("#btnNew").textContent = "Solicitar cita";
    document.querySelector("#refCalendario").textContent =
      "Calendario de citas";
    document.querySelector("#btnAppointmentFormat").onclick = receptionPDF;
  } else {
    document.querySelector("#title-appointment").textContent = "Información";
    document.querySelector("#btnModify").style.display = "none";
    document.querySelector("#btnCancel").style.display = "none";
    document.querySelector("#btnNew").textContent = "Generar Relación de Envío";
    document.querySelector("#refCalendario").textContent = "Relación de Envío";
    document.querySelector("#btnAppointmentFormat").onclick = pdf;
  } */

  var inactivityTime = function () {
    var time;
    window.onload = resetTimer;
    // DOM Events
    document.onmousemove = resetTimer;
    document.onkeydown = resetTimer;

    function updateCalendar() {
      document.querySelectorAll(".input-number").forEach((e) => {
        //e.addEventListener("input", handleNumbers);
        e.addEventListener("input", function () {
          numericInputOnInput(this);
        });
        e.addEventListener("blur", function () {
          numericInputOnBlur(this);
        });
        e.addEventListener("paste", function (event) {
          numericInputOnPaste(event, this);
        });
      });
      setInterval(() => {
        const tds = [...document.querySelectorAll(".refreshable")];
        const renewalDate = new Date().toLocaleString("es-ES");
        for (let index = 0; index < tds.length; index++) {
          const element = tds[index];
          element.onrefresh();
          element.dataset.dateModified = renewalDate;
        }
        document.querySelector("#last-update").textContent =
          "Actualizado el: " + renewalDate;
      }, 20000);
    }

    function resetTimer() {
      clearTimeout(time);
      time = setTimeout(updateCalendar, 30000);
    }
  };
  //inactivityTime();
  loadEvents();
}

async function loadPermissions() {
  const permissionList =
    portal +
    "buscaboton?token=" +
    kdsuParams.token +
    "&modulo=" +
    kdsuParams.module +
    "";
  try {
    const permissions = await fetch(permissionList);
    const permissionsJSON = await permissions.json();
    sessionUser = permissionsJSON[0].UserName;
    validateResult(permissionsJSON);
    const objectsList = {
      248: {
        html: "lirefresh",
        display: "block",
      },
      249: {
        html: "linew",
        display: "block",
      },
      287: {
        html: "liview",
        display: "block",
      },
      250: {
        html: "liupdate",
        display: "block",
      },
      251: {
        html: "licancel",
        display: "block",
      },
      289: {
        html: "liDownload",
        display: "block",
      },
    };

    for (const permission of permissionsJSON) {
      //console.log(document.getElementById(objectsList[permission.ID].html));
      document
        .getElementById(objectsList[permission.ID].html)
        .setAttribute(
          "style",
          "display: " + objectsList[permission.ID].display
        );
    }
  } catch (error) {
    console.error(error);
    warningMsg("Hubo un problema al consultar los permisos del usuario.");
  }
}

//main ****

//new

//new appoint
async function createAppointment(data) {
  const endpoint = portal + "store/";
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const respJSON = await resp.json();
  return respJSON;
}

//view
async function getAppointmentsToBeAdded(type) {
  const appointmentsList = portal + "orders_to_be_appointed/";
  const appointments = await fetch(appointmentsList);
  const appointmentsJSON = await appointments.json();
  return appointmentsJSON;
}

async function getAppointments(data) {
  const endpoint = portal + "orders_by_date/";
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),

    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const respJSON = await resp.json();
  return respJSON;
}

async function getAppointmentsDetail(appointmentId) {
  const appointmentsList = portal + "orders_detail_by_appointment/";
  const appointments = await fetch(appointmentsList);
  const appointmentsJSON = await appointments.json();
  return appointmentsJSON;
}

//modificar
async function getAppointmentsToBeModified(appointmentId) {
  const appointmentsList =
    portal +
    "pgcalendariocitas/consultapedidosxmodificar?tipocita=1" +
    "&cita=" +
    appointmentId +
    "&token=" +
    kdsuParams.token +
    "&modulo=" +
    kdsuParams.module +
    "";
  const appointments = await fetch(appointmentsList);
  //console.log(appointmentsList);
  const appointmentsJSON = await appointments.json();
  //validateResult(appointmentsJSON);
  return appointmentsJSON;
}


async function getAvailabilityData(date) {
  const availabilityCheck =
    portal +
    "pgcalendariocitas/validadiaconfirmadosolicitado?fecha=" +
    date +
    " 00:00:00&token=" +
    kdsuParams.token +
    "&modulo=" +
    kdsuParams.module +
    "";
  const availability = await fetch(availabilityCheck);
  const availabilityJSON = await availability.json();

  return {
    date: availabilityJSON[0].Fecha,
    isAvailable: !Boolean(availabilityJSON[0].Tiempo),
    isRequested: Boolean(availabilityJSON[0].Solicitada),
    isConfirmed: Boolean(availabilityJSON[0].Confirmada),
  };
}
async function isDayNotAvailable(date) {
  const availabilityCheck =
    portal +
    "pgcalendariocitas/validadianodisponible?fecha=" +
    date +
    " 00:00:00&token=" +
    kdsuParams.token +
    "&modulo=" +
    kdsuParams.module +
    "";
  const availability = await fetch(availabilityCheck);
  const availabilityJSON = await availability.json();
  if (availabilityJSON.length < 1) {
    return false;
  }
  return availabilityJSON[0].Tiempo > 0;
}

async function checkStatus(date, statusToCheck) {
  let statusEndpoint =
    statusToCheck == "requested"
      ? "validadiasolicitado"
      : "validadiaconfirmado";
  const statusCheck =
    portal +
    "pgcalendariocitas/" +
    statusEndpoint +
    "?fecha=" +
    date +
    " 00:00:00" +
    "&token=" +
    kdsuParams.token +
    "&modulo=" +
    kdsuParams.module +
    "";
  const status = await fetch(statusCheck);
  const statusJSON = await status.json();
  if (statusJSON.length < 1) {
    return false;
  }
  return Boolean(statusJSON[0][STATUSES[statusToCheck]]);
}

//update
async function updateAppointment(data) {
  const endpoint = portal + "pgcalendariocitas/agendacita_modificar";
  data.token = kdsuParams.token;
  data.modulo = kdsuParams.module;
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const respJSON = await resp.json();
  validateResult(respJSON);
  return respJSON;
}

//cancel
async function cancelAppointment(data) {
  const endpoint = portal + "pgcalendariocitas/agendacita_cancelar";
  data.token = kdsuParams.token;
  data.modulo = kdsuParams.module;
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const respJSON = await resp.json();
  validateResult(respJSON);
  return respJSON;
}

//lbl
async function getSerialPrintInstruction(appointmentId, user) {
  const endpoint =
    "http://192.168.100.241:8092/kdsu/portal/pgcalendariocitas/etiquetaSerialesPorCita";
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      idCita: appointmentId,
      token: kdsuParams.token,
      modulo: kdsuParams.module,
    }),
  });

  const respJSON = await resp.json();
  console.log(resp);
  validateResult(respJSON);
  let lblCmd = { etiqueta: "" };
  if (respJSON.success) {
    lblCmd = respJSON.data.map((r) => r.etiqueta).reduce((a, b) => a + b);
  }

  const a = document.querySelector("#lbl");
  const file = new Blob([lblCmd]);
  a.href = URL.createObjectURL(file);
  a.download = `${user}_${appointmentId}.lbl`;
  a.click();
}

//bultos
async function getBulks(user) {
  const datef = selected.dataset.date.split("/");
  const dateff = datef[2] + "-" + datef[1] + "-" + datef[0];
  //2024-10-02T23:59"
  //"2024-07-01T09:44:00"
  const endpoint =
    "http://192.168.100.241:8092/kdsu/portal/pgcalendariocitas/reporteEtiquetasPorBultos";
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      username: user,
      fechaInicial: dateff + "T00:00:00",
      fechaFinal: dateff + "T23:59:00",
      token: kdsuParams.token,
      modulo: kdsuParams.module,
    }),
  });

  const respJSON = await resp.json();
  console.log(respJSON);
  validateResult(respJSON);
  return respJSON;
}

const generateQRLine = (data) => {
  return [
    data.Proveedor,
    data.Sucursal,
    data.Sucursal,
    data.Pedido,
    data.Fecha,
    data.Factura,
    data.BultosXFactura,
    data.Bulto,
    data.Codigo,
  ].join(" ");
};

//pdf
async function pdf() {
  //collapseSidebar();
  showLoading(true);
  window.jsPDF = window.jspdf.jsPDF;
  window.html2canvas = html2canvas;
  window.DOMPurify = DOMPurify;
  const logo = await getTonyLogo();
  const doc = new jsPDF("p", "pt", "letter");
  try {
    const pdfData = await getPDFData({
      tipo: document.querySelector("#cmb-method").value,
      username: sessionUser,
      idCita: rowSelected[1],
      /*fechaInicial: "2024-07-01T09:44:00",
    fechaFinal: "2024-07-10T23:59:59",*/
    });

    const mappedData = [];
    pdfData.data.CabeceraCita.forEach((e) => {
      mappedData.push({
        head: e.$,
        detail: e.DetalleCita.map((f) => f.$),
      });
    });

    const selected = mappedData.filter(
      (a) => a.head.Id_Cita == rowSelected[1]
    )[0];

    const first = selected.head;
    const qrLine = formatPDFQRLine(first);
    const qrTemp = await getQRCode(qrLine);
    let title = "RELACIÓN DE ENVÍO";
    //35
    ///////////////////////////////////////////////////////////////////////////////////
    doc.addImage(qrTemp, "PNG", 405, 72, 72, 72);
    doc.addImage(logo, "PNG", 45, 38, 191 / 2, 81 / 2);
    doc.setFontSize(10);
    doc.setFont("helvetica", "bold");
    doc.text(first.NombreCompania, 240, 45);

    doc.text(title, 258, 50 + doc.getFontSize());
    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    doc.text("ENTREGA:", 100, 95, { align: "right" });
    doc.text("PROVEEDOR:", 100, 110, { align: "right" });
    doc.text("CONTACTO:", 100, 125, { align: "right" });
    doc.text("TRANSPORTISTA:", 100, 140, { align: "right" });
    doc.setFont("helvetica", "bold");
    doc.text(first.TipoCita, 105, 95);
    const manufacturer = `${first.Proveedor} ${first.NombreProveedor}`;
    doc.text(manufacturer, 105, 110);
    const underline = doc.getTextWidth(manufacturer);
    doc.line(105, 112, 105 + underline, 112);
    doc.text(first.Contacto, 105, 125);
    doc.text(first.Transportista, 105, 140);

    if (document.querySelector("#pdf-tbl")) {
      document.querySelector("#pdf-tbl").remove();
    }

    const rows = selected.detail
      .map((r) => {
        return {
          branch: r.Sucursal,
          branchName: r.NombreSucursal,
          order: r.Pedido,
          orderDate: r.Fecha,
          bill: r.Factura,
          nBulksByBill: r.BultosxFactura,
          billDate: r.FechaFactura,
          nBulks: r.NoBultos,
        };
      })
      .concat(
        selected.detail.map((r) => {
          return {
            branch: r.Sucursal,
            branchName: r.NombreSucursal,
            order: r.Pedido,
            orderDate: r.Fecha,
            bill: r.Factura,
            nBulksByBill: r.BultosxFactura,
            billDate: r.FechaFactura,
            nBulks: r.NoBultos,
          };
        })
      );

    const totalBulks = rows
      .map((r) => r.nBulks)
      .reduce((acc, a) => Number(acc) + Number(a));
    const header = {
      appointmentId: selected.head.Id_Cita,
      nBills: selected.detail.length,
      weight: selected.head.Peso,
      volume: selected.head.Volumen,
      bulks: selected.head.Bultos,
      date: selected.head.FechaCita,
      total: totalBulks,
    };

    const tables = createPDFTable(header, rows);
    setTimeout(() => {
      doc.html(tables, {
        callback: function (doc) {
          doc.save(`CitaParaRecepcionMcia_${first.Id_Cita}`);
        },
        x: 8,
        y: 160,
        html2canvas: {
          width: 8,
        },
      });
      showLoading(false);
      ///doc.output("pdfobjectnewwindow");
      //document.querySelector("#pdf-tbl").remove();
    }, 2000);
  } catch (err) {
    warningMsg("Error al generar el reporte");
  }
  ///////////////////////////////////////////////////////////////////////////////////
  //doc.save("CitaParaRecepcionMcia_.pdf");
}

async function receptionPDF() {
  //collapseSidebar();
  showLoading(true);
  window.jsPDF = window.jspdf.jsPDF;
  window.html2canvas = html2canvas;
  window.DOMPurify = DOMPurify;
  const logo = await getTonyLogo();
  const doc = new jsPDF("p", "pt", "letter");
  try {
    const pdfData = await getPDFData({
      tipo: document.querySelector("#cmb-method").value,
      username: sessionUser,
      idCita: rowSelected[1],
      /*fechaInicial: "2024-07-01T09:44:00",
    fechaFinal: "2024-07-10T23:59:59",*/
    });

    const mappedData = [];
    pdfData.data.CabeceraCita.forEach((e) => {
      mappedData.push({
        head: e.$,
        detail: e.DetalleCita.map((f) => f.$),
      });
    });

    const selected = mappedData.filter(
      (a) => a.head.Id_Cita == rowSelected[1]
    )[0];

    const first = selected.head;
    const qrLine = formatPDFQRLine(first);
    const qrTemp = await getQRCode(qrLine);
    let title = "CITA PARA RECEPCIÓN DE BULTOS";
    //35
    ///////////////////////////////////////////////////////////////////////////////////
    doc.addImage(qrTemp, "PNG", 370, 72, 72, 72);
    doc.addImage(logo, "PNG", 45, 38, 191 / 2, 81 / 2);
    doc.setFontSize(10);
    doc.setFont("helvetica", "bold");
    doc.text(first.NombreCompania, 240, 45);

    doc.text(title, 200, 50 + doc.getFontSize());
    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    doc.text("ENTREGA:", 100, 95, { align: "right" });
    doc.text("PROVEEDOR:", 100, 110, { align: "right" });
    doc.text("CONTACTO:", 100, 125, { align: "right" });
    doc.text("TRANSPORTISTA:", 100, 140, { align: "right" });
    doc.setFont("helvetica", "bold");
    doc.text(first.TipoCita, 105, 95);
    const manufacturer = `${first.Proveedor} ${first.NombreProveedor}`;
    doc.text(manufacturer, 105, 110);
    const underline = doc.getTextWidth(manufacturer);
    doc.line(105, 112, 105 + underline, 112);
    doc.text(first.Contacto, 105, 125);
    doc.text(first.Transportista, 105, 140);

    doc.setFont("helvetica", "normal");
    doc.text("TIPO TRANSPORTE:", 100, 155, { align: "right" });
    doc.text("TIPO CARGA:", 250, 155, { align: "right" });
    doc.text("PLACAS:", 350, 155, { align: "right" });
    doc.text("CHOFER:", 100, 170, { align: "right" });
    doc.text("NO.PERSONAS", 347, 170, { align: "right" });
    doc.setFont("helvetica", "bold");
    doc.text(first.TipoTransporte, 100 + 8, 155);
    doc.text(first.TipoCarga, 250 + 8, 155);
    doc.text(first.Placas, 350 + 8, 155);
    doc.text(first.Chofer, 100 + 8, 170);
    doc.text(":______", 352 + doc.getTextWidth(":______"), 170, {
      align: "right",
    });

    if (document.querySelector("#pdf-tbl")) {
      document.querySelector("#pdf-tbl").remove();
    }

    const rows = selected.detail.map((r) => {
      return {
        branch: r.Sucursal,
        branchName: r.NombreSucursal,
        order: r.Pedido,
        orderDate: r.Fecha,
        bill: r.Factura,
        nBulksByBill: r.BultosxFactura,
        billDate: r.FechaFactura,
        nBulks: r.NoBultos,
      };
    });

    const totalBulks = rows
      .map((r) => r.nBulks)
      .reduce((acc, a) => Number(acc) + Number(a));
    const header = {
      appointmentId: selected.head.Id_Cita,
      nBills: selected.detail.length,
      weight: selected.head.Peso,
      volume: selected.head.Volumen,
      bulks: selected.head.Bultos,
      date: selected.head.FechaCita,
      total: totalBulks,
      time: selected.head.HoraCita,
      allocatedTime: selected.head.TiempoAsignado,
      anden: selected.head.Id_Anden,
    };

    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    doc.text("NO. DE CITA:", 486 - 27, 128);
    doc.text("FECHA DE CITA:", 486 - 27, 143);
    doc.text("HORA DE CITA:", 486 - 27, 158);
    doc.text("T.ASIGNADO:", 486 - 27, 173);
    doc.text("No.ANDEN:", 486 - 27, 188);
    doc.setFont("helvetica", "bold");
    doc.text(header.appointmentId, 551 - 27, 128);
    doc.text(header.date, 551 - 27, 143);
    doc.text(header.time, 551 - 27, 158);
    doc.text(header.allocatedTime, 551 - 27, 173);
    doc.text(header.anden, 551 - 27, 188);
    doc.setLineWidth(1);
    doc.line(477 - 27, 117, 596 - 27, 117);
    doc.line(477 - 27, 117, 477 - 27, 195);
    doc.line(596 - 27, 117, 596 - 27, 195);
    doc.line(477 - 27, 195, 596 - 27, 195);
    doc.setLineWidth(0.200025);
    //612 792
    const tables = createReceptionPDFTable(header, rows, doc, first);
    setTimeout(() => {
      doc.html(tables, {
        callback: function (doc) {
          doc.output("pdfobjectnewwindow");
          //doc.save(`CitaParaRecepcionMcia_${first.Id_Cita}`);
        },
        x: 8,
        y: 175,
        html2canvas: {
          width: 8,
        },
      });
      showLoading(false);
      ///doc.output("pdfobjectnewwindow");
      //document.querySelector("#pdf-tbl").remove();
    }, 2000);
  } catch (err) {
    warningMsg("Error al generar el reporte");
  }
  ///////////////////////////////////////////////////////////////////////////////////
  //doc.save("CitaParaRecepcionMcia_.pdf");
}

const STATUSES = {
  requested: "Solicitada",
  confirmed: "Confirmada",
};

function returnTable(headers, id) {
  const table = document.createElement("table");
  table.id = id;
  table.className = "table";
  table.createTHead();
  table.tHead;
  table.tHead.appendChild(document.createElement("tr"));
  table.tHead.appendChild(document.createElement("tr"));
  const tr = table.querySelectorAll("tr")[0];
  for (let index = 0; index < headers.length; index++) {
    const th = document.createElement("th");
    th.textContent = headers[index];
    tr.appendChild(th);
  }
  const tr2 = table.querySelectorAll("tr")[1];
  for (let index = 0; index < headers.length; index++) {
    const th = document.createElement("th");
    th.classList.add("filterable");
    tr2.appendChild(th);
  }
  table.createTBody();
  return table;
}

async function fillCombos() {
  //fill combos
  [...document.querySelectorAll(".cmb")].forEach((i) => {
    $(i).select2({
      allowClear: true,
      placeholder: "Selecciona una opción",
      minimumResultsForSearch: -1,
    });
  });
  loadEvents();
}

///pdf
async function getTonyLogo() {
  return new Promise((resolve, reject) => {
    let img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = "assets/img/tonylogo.png";
  });
}

async function getQRCode(qrLine) {
  return new Promise((resolve, reject) => {
    window.jsPDF = window.jspdf.jsPDF;
    window.html2canvas = html2canvas;
    window.DOMPurify = DOMPurify;
    const qrElement = document.createElement("div");
    const qrDom = new QRCode(qrElement, qrLine);
    let img = qrDom._oDrawing._elImage;
    img.onload = () => resolve(img);
    img.onerror = reject;
  });
}

function createPDFTable(header, rows) {
  let rowHTML = "";
  rows.forEach((r, idx) => {
    if (idx % 29 == 0 && idx > 0) {
      rowHTML += `<tr style="font-size: 9px"><td colspan="11" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">  </td></tr>`;
    }
    rowHTML += ` <tr style="font-size: 9px;word-spacing:9px" >
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.branch}</td>
        <td colspan="4" style="padding: 0px 2px 0px 2px;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold; text-align: left;" align="left">${r.branchName}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.order}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.orderDate}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.bill}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.nBulksByBill}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.billDate}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.nBulks}</td>
      </tr>`;
  });
  document.querySelector(".test").insertAdjacentHTML(
    "afterbegin",
    `

  <table id="pdf-tbl" style="width: 67%; border-collapse: collapse;" >
    <thead>
      <tr style="font-size:7px">
        <td colspan="8" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center; border-top: none; border-left: none;" align="center"></td>
        <td colspan="4" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center; border-bottom: none; border-top: 2px solid black;" align="center">
          <table class="nb" style="width:100%; border-collapse: collapse;" >
            <tr style="border: 0px solid red;">
              <td colspan="11" style="padding: 0px 0px 0px 1px; text-align: left; border: 0px solid red;width:90px" align="left">ENVÍO:</td>
              <td colspan="1" style="padding: 0px 0px 0px 0px;border: 0px solid red;" align="left;"><strong style="border: 0px solid red;">${header.appointmentId}</strong></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr style="font-size:7px">
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">FACTURAS X ENVÍO:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.nBills}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">BULTOS X ENVÍO:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.bulks}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">VOL MP X ENVÍO:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.volume}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">PESO KG.X ENVÍO:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: left;" align="left"><strong>${header.weight}</strong></td>
        <td colspan="4" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center; border-top: none;" align="center">
          <table class="nb" style=" border-collapse: collapse;" >
            <tr style="border: 0px solid red;">
              <td style="padding: 0px 2px 0px 2px; text-align: center; border: 0px solid red;" align="left" ><span style="border: 0px solid red;">FECHA ENTREGA:</span></td>
              <td style="padding: 0px 2px 0px 2px; text-align: center; border: 0px solid red;" align="center"><strong style="border: 0px solid red;">                                ${header.date}</strong></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr style="font-size:7px">
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">SUC.</td>
        <td colspan="4" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">NOMBRE SUCURSAL</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">PEDIDO</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">F.PEDIDO</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 3px 0px 3px; text-align: center;" align="center">FACTURA</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">BTOS. FACT</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">FECHA</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">BULTOS</td>
      </tr>
    </thead>
    <tbody>
      ${rowHTML}
      <tr style="font-size: 9px">
        <td colspan="9" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" align="center"></td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" align="center">BTOS. X ENVÍO :</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" ; align="center">${header.total}</td>
      </tr>
    </tbody>
  </table>
    `
  );
  return document.querySelector("#pdf-tbl");
}

function createReceptionPDFTable(header, rows, doc, main) {
  const mainDiv = document.createElement("div");
  /*mainDiv.style.width = "82%";
  mainDiv.style.height = "80vh";*/
  mainDiv.style.width = "82%";
  mainDiv.style.height = "75vh";
  mainDiv.id = "pdf-tbl";
  let rowHTML = "";

  let rowCounter = 0;
  let rowLimit = 20;
  let accBulksBranch = 0;
  let j = 0;

  let rows2 = rows;

  const arraysDivididos = dividirArray(rows2, 20);
  console.log(
    Array.from(
      new Set(
        rows.map((b) => b.branch),
        "<<<<<<<"
      )
    )
  );

  let wholeHTML = [];
  let tmp = [];
  let isNewPage = false;
  let extra = "";
  let height = "";
  arraysDivididos.forEach((ds, idx) => {
    console.log(ds);
    if (idx > 0) {
      doc.addPage();
      height = "";
      rowHTML = "";
      rowCounter = 1;
      const first = main;
      isNewPage = true;
      const qrLine = formatPDFQRLine(first);
      const qrTemp = getQRCode(qrLine);
      qrTemp.then((d) => doc.addImage(d, "PNG", 370, 72, 72, 72));
      let title = "CITA PARA RECEPCIÓN DE BULTOS";
      ///////////////////////////////////////////////////////////////////////////////////
      const logo = getTonyLogo();
      logo.then((l) => doc.addImage(l, "PNG", 45, 38, 191 / 2, 81 / 2));
      doc.setFontSize(10);
      doc.setFont("helvetica", "bold");
      doc.text(first.NombreCompania, 240, 45);

      doc.text(title, 200, 50 + doc.getFontSize());
      doc.setFontSize(8);
      doc.setFont("helvetica", "normal");
      doc.text("ENTREGA:", 100, 95, { align: "right" });
      doc.text("PROVEEDOR:", 100, 110, { align: "right" });
      doc.text("CONTACTO:", 100, 125, { align: "right" });
      doc.text("TRANSPORTISTA:", 100, 140, { align: "right" });
      doc.setFont("helvetica", "bold");
      doc.text(first.TipoCita, 105, 95);
      const manufacturer = `${first.Proveedor} ${first.NombreProveedor}`;
      doc.text(manufacturer, 105, 110);
      const underline = doc.getTextWidth(manufacturer);
      doc.line(105, 112, 105 + underline, 112);
      doc.text(first.Contacto, 105, 125);
      doc.text(first.Transportista, 105, 140);

      doc.setFont("helvetica", "normal");
      doc.text("TIPO TRANSPORTE:", 100, 155, { align: "right" });
      doc.text("TIPO CARGA:", 250, 155, { align: "right" });
      doc.text("PLACAS:", 350, 155, { align: "right" });
      doc.text("CHOFER:", 100, 170, { align: "right" });
      doc.text("NO.PERSONAS", 347, 170, { align: "right" });
      doc.setFont("helvetica", "bold");
      doc.text(first.TipoTransporte, 100 + 8, 155);
      doc.text(first.TipoCarga, 250 + 8, 155);
      doc.text(first.Placas, 350 + 8, 155);
      doc.text(first.Chofer, 100 + 8, 170);
      doc.text(":______", 352 + doc.getTextWidth(":______"), 170, {
        align: "right",
      });
      doc.setFontSize(8);
      doc.setFont("helvetica", "normal");
      doc.text("NO. DE CITA:", 480 - 27, 130);
      doc.text("FECHA DE CITA:", 480 - 27, 144);
      doc.text("HORA DE CITA:", 480 - 27, 158);
      doc.text("T.ASIGNADO:", 480 - 27, 172);
      doc.text("No.ANDEN:", 480 - 27, 188);
      doc.setFont("helvetica", "bold");
      doc.text(header.appointmentId, 545 - 27, 130);
      doc.text(header.date, 545 - 27, 144);
      doc.text(header.time, 545 - 27, 158);
      doc.text(header.allocatedTime, 545 - 27, 172);
      doc.text(header.anden, 545 - 27, 188);
      doc.setLineWidth(1);
      doc.line(471 - 27, 116, 591 - 27, 116);
      doc.line(471 - 27, 116, 471 - 27, 194);
      doc.line(591 - 27, 116, 591 - 27, 194);
      doc.line(471 - 27, 194, 591 - 27, 194);
      doc.setLineWidth(0.200025);
    } else {
      isNewPage = false;
    }
    let previous = ds[idx].branch;
    ds.forEach((r, idz, arr) => {
      //if (previous == r.branch) {
      rowHTML += ` <tr style="font-size: 9px;border:0px solid red; word-spacing:15px">
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.branch}</td>
        <td colspan="4" style="padding: 0px 2px 0px 2px;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold; text-align: left;">${r.branchName}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.order}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.orderDate}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.bill}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.nBulksByBill}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.billDate}</td>
        <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center;  border-left: 0px solid black; border-right: 0px solid black;  font-weight: bold;" align="center">${r.nBulks}</td>
      </tr>`;
      accBulksBranch += Number(r["nBulks"]);
      //} else {
      let next = [];
      if (ds[idx + 1] != undefined) {
        next = ds[idx + 1];
      } else {
        next = { branch: r.branch };
      }

      if (next.branch != r.branch || idz == ds.length - 1) {
        rowHTML += ` <tr style="font-size: 8px">
          <td colspan="9" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" align="center"></td>
          <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" align="center"><strong>BTOS. X SUC:</strong></td>
          <td colspan="1" style="padding: 0px 2px 0px 2px; text-align: center; border: none;" ; align="center"><b>${accBulksBranch}</b></td>
        </tr>`;
        accBulksBranch = 0;
      }
      //}
      rowCounter += 1;
      previous = r.branch;
    });

    if (rowCounter >= rowLimit) {
      const nbreaks = ds.length * 0.5 + 1;
      //for (let i = 0; i < nbreaks; i++) {
      //extra += `<p style="height:${nbreaks}px"></p>`;
      //}
      rowCounter = 1;
    }

    const footerHTML = `
   <div class="ft" style="font-size:8px;width:870px;height:180px;">
        <div role="region" tabindex="0" style="display: flex; gap: 9px">
          <table style="border: 1px solid black; width:33%;">
            <thead>
              <tr>
                <th style="border: 1px solid black;height:10px" width="150">
                  <strong>CUMPLIÓ CON LOS REQUISITOS</strong>
                </th>
                <th
                  style="border: 1px solid black;height:10px; text-align: center"
                  width="25"
                >
                  SI
                </th>
                <th
                  style="border: 1px solid black;height:10px; text-align: center"
                  width="25"
                >
                  NO
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="border: 1px solid black;height:10px">Cita</td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black;height:10px">A tiempo</td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black;height:10px">
                  Bultos con etiqueta centra
                </td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black;height:10px">
                  Etiquetas de lado frontal superior derecho
                </td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black;height:10px">
                  Tarimas de madera tipo estándar o tacón en buen estado
                </td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black;height:10px">
                  Entrega ordenada por sucursal-factura
                </td>
                <td style="border: 1px solid black;height:10px"></td>
                <td style="border: 1px solid black;height:10px"></td>
              </tr>
            </tbody>
          </table>
          <table style="border: 1px solid black; width:33%">
            <thead>
              <tr>
                <th style="border: 1px solid black" width="150">
                  <strong>CUMPLIÓ CON LOS REQUISITOS</strong>
                </th>
                <th
                  style="border: 1px solid black; text-align: center"
                  width="25"
                >
                  SI
                </th>
                <th
                  style="border: 1px solid black; text-align: center"
                  width="25"
                >
                  NO
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="border: 1px solid black">Copia de factura</td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black">
                  Personal suficiente para entrega
                </td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black">
                  Bultos rechazados     <strong>¿Cuantos?</strong>
                </td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black">
                  Facturas rechazadas     <strong>¿Cuantos?</strong>
                </td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black">
                  Bultos no agendados     <strong>¿Cuantos?</strong>
                </td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
              <tr>
                <td style="border: 1px solid black">
                  Facturas no agendadas     <strong>¿Cuantos?</strong>
                </td>
                <td style="border: 1px solid black"></td>
                <td style="border: 1px solid black"></td>
              </tr>
            </tbody>
          </table>
        </div>
        <table style="border: 1px solid black;width:67%">
          <tr>
            <td><strong style="font: size 1rem">OBSERVACIONES:</strong></td>
          </tr>
          <tr>
            <td style="height:18px"></td>
          </tr>
        </table>
    </div></div>
     <div style="margin: 0 33%;display:table"> <span >${
       doc.getCurrentPageInfo().pageNumber
     }</span></div>
    <br/> <br/> <br/> <br/> <br/> <br/> <br/>
    </div>

  `;

    wholeHTML.push(`
    <div style="display:flex;flex-direction:column;justify-content:space-between;height:600px">
    <table  style="width: 67%;border-collapse: collapse;${height ? "" : ""}" >
    <thead>
      <tr style="font-size:7px">
        <td colspan="8" style="padding: 0px 2px 0px 2px; text-align: center; border-top: none; border-left: none;" align="center"></td>
        <td colspan="1" style=" padding: 0px 2px 0px 2px; text-align: center; border-top: none; border-left: none;" align="center"></td>
        <td colspan="3" style=" padding: 0px 2px 0px 2px; text-align: center; border-bottom: none; border-top: 0px solid red;" align="center">
          <table class="nb" style="width:100%; border-collapse: collapse;" >
            <tr style="border: 0px solid black;">
              <td colspan="12" style="padding: 0px 0px 0px 1px; text-align: left; border: 0px solid black;width:90px" align="left"></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr style="font-size:7px">
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">FACTURAS:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.nBills}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">BULTOS:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.bulks}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 1px 0px 2px; text-align: center;" align="center">PALLETS:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: right;" align="right">
          <strong>              ${header.volume}</strong>
        </td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;" align="center">VOL. M³:</td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: left;" align="left"><strong>${
          header.volume
        }</strong></td>
        <td style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: left;" align="left">
        <table>
          <tr>
          <td style="border-right:1px solid black;padding:0px 2px 0px 2px;text-align:left">PESO KG:</td>
          <td style="padding:0px 2px 0px 2px;text-align:left"><strong>${
            header.weight
          }</strong></td>
          </tr>
        </table>
        </td>


      </tr>
      <tr style="font-size:7px">
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:25px" align="center">SUC.</td>
        <td colspan="4" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:75px" align="center">NOMBRE SUCURSAL</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:40px" align="center">PEDIDO</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:40px" align="center">F.PEDIDO</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 3px 0px 3px; text-align: center;width:50px" align="center">FACTURA</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:60px" align="center">BTOS. FACT</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:60px" align="center">FECHA</td>
        <td colspan="1" style="border: 1px solid black; padding: 0px 2px 0px 2px; text-align: center;width:60px" align="center">BULTOS</td>
      </tr>
    </thead>
    <tbody>
      ${rowHTML}
    </tbody>
  </table>
    ${footerHTML}
           ${extra}
    `);
  });
  mainDiv.insertAdjacentHTML("afterbegin", wholeHTML);

  document.querySelector(".test").appendChild(mainDiv);
  return document.querySelector("#pdf-tbl");
}
async function getPDFData(data) {
  const endpoint =
    "http://192.168.100.241:8092/kdsu/portal/pgcalendariocitas/reportesCitasRecepcionMercancia";
  data.token = kdsuParams.token;
  data.modulo = kdsuParams.module;
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(data),
  });
  const respJSON = await resp.json();
  validateResult(respJSON);
  return respJSON;
}

function formatPDFQRLine(head) {
  return [
    head.Id_Cita,
    head.TipoCita,
    head.Compania,
    head.FechaCita,
    head.HoraCita,
    head.TiempoAsignado,
    head.Anden,
    head.Bultos,
    head.Pallets,
  ].join("|");
}
async function getTransport(appointmentId) {
  const data = {};
  const endpoint = portal + "pgcalendariocitas/agendaCitasOp7";
  data.token = kdsuParams.token;
  data.modulo = kdsuParams.module;
  data.idCita = appointmentId;

  try {
    const resp = await fetch(endpoint, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(data),
    });
    const respJSON = await resp.json();
    //validateResult(respJSON);
    return respJSON;
  } catch (error) {
    console.log(error);
  }
}
async function completeData() {
  //warningMsg("Debe capturar los datos del transportista.");
  ///api
  const transportData = await getTransport(
    document.querySelector('input[name="ipt-appointment"').value
  );

  if (transportData.hasOwnProperty("success")) {
    document.querySelector("input[name='transport'").value =
      transportData.data.Transportista;
    document.querySelector("input[name='plates'").value =
      transportData.data.Placas;
    document.querySelector("input[name='driver'").value =
      transportData.data.Chofer;
    [...document.querySelectorAll("#frmTransport .disableable")].forEach((b) =>
      b.classList.remove("disabled")
    );
  } else {
    document.querySelector("input[name='transport'").value = "";
    document.querySelector("input[name='plates'").value = "";
    document.querySelector("input[name='driver'").value = "";
  }

  console.log(transportData, "transport");
  if (pgCalendarioCitasTipoProveedor == SUPPLIER_TYPES.MENSAJERIA) {
    document.querySelector("input[name='transport'").value = "POR MENSAJERÍA";
    document.querySelector("input[name='plates'").value = "NO APLICA";
    document.querySelector("input[name='driver'").value = "NO APLICA";
  } else if (pgCalendarioCitasTipoProveedor == SUPPLIER_TYPES.INTERNO) {
    document.querySelector("input[name='transport'").value = "ENTREGA LOCAL";
    document.querySelector("input[name='plates'").value = "NO APLICA";
    document.querySelector("input[name='driver'").value = "NO APLICA";
  }
  $("#complete").modal({ backdrop: "static" });
  $("#complete").modal("show");
}

function handleNumbers(ev) {
  ev.currentTarget.value = pruneNothingButNumbers(ev.currentTarget.value);
}

function pruneNothingButNumbers(string) {
  return string.replace(/[^\d]/, "");
}

//transp
async function saveCarrier(carrierData) {
  const transportData = {
    chofer: carrierData.driver,
    username: sessionUser,
    idCita: rowSelected[1],
    placas: carrierData.plates,
    transportista: carrierData.transport,
  };
  transportData.token = kdsuParams.token;
  transportData.modulo = kdsuParams.module;
  const endpoint =
    "http://192.168.100.241:8092/kdsu/portal/pgcalendariocitas/guardarChoferTransportistaPlacas";
  const resp = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(transportData),
  });
  const respJSON = await resp.json();
  validateResult(respJSON);
  return respJSON;
}

async function setTransportData() {
  const transportInputs = [
    ...document.querySelector("#frmTransport").querySelectorAll("input"),
  ];
  const inputs = transportInputs.map((i) => i.value);
  if (inputs.some((v) => v == "")) {
    warningMsg("Ingresa todos los campos");
    return;
  }
  const [appointmentId, transport, plates, driver] = inputs;
  transportData = {
    appointmentId: appointmentId,
    transport: transport,
    plates: plates,
    driver: driver,
  };
  const isSuccessful = await saveCarrier(transportData);
  if (isSuccessful) {
    successMsg("Datos del transportista guardados con éxito.");
    [...document.querySelectorAll("#frmTransport .disableable")].forEach((b) =>
      b.classList.remove("disabled")
    );
  } else {
    transportData = {};
    warningMsg(
      "No fue posible guardar los datos del Transportista en este momento. Por favor intente más tarde."
    );
  }
}

async function downloadReception() {
  setTransportData();
  receptionPDF();
}

function dividirArray(array, tamano) {
  const resultado = [];
  for (let i = 0; i < array.length; i += tamano) {
    resultado.push(array.slice(i, i + tamano));
  }
  return resultado;
}

async function CentraMetrics(data) {
  const endpoint = portal + "pgcalendariocitas/centraIndicadoresDatos";
  data.token = kdsuParams.token;
  data.modulo = kdsuParams.module;

  try {
    const resp = await fetch(endpoint, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(data),
    });
    const respJSON = await resp.json();
    //validateResult(respJSON);
    return respJSON;
  } catch (error) {
    console.log(error);
  }
}

/* VALIDAR TOKEN */
function reloadParent() {
  window.parent.postMessage("Reload", "*");
}

/* collapse */
function collapseSidebar() {
  window.parent.postMessage("Collapse", "*");
}

function validateResult(result) {
  if (typeof result === "object") {
    if (Array.isArray(result[0])) {
      if (result[0].hasOwnProperty("RESULTADO")) {
        if (result[0].RESULTADO === false) {
          warningMsg(
            "El token actual expiró. Se renovará al recargar la página."
          );
          setTimeout(() => {
            reloadParent();
          }, 2000);
          throw new Error("Error de Credenciales");
        }
      }
    }
  } else if (typeof result === "string") {
    warningMsg(
      "Ha ocurrido un error al realizar la consulta, favor de volver a intentarlo. Si el problema persiste contacte a Mesa de Servicios"
    );
    throw new Error("Error de Consulta");
  }
}

async function loadEvents() {
  console.log("event");
  $("#cmb-load").on("change", function (ev) {
    console.log("hi", ev.currentTarget);
    if (
      ev.currentTarget.value == LOAD_TYPES.PALLET ||
      ev.currentTarget.value == LOAD_TYPES.MIXED
    ) {
      document.querySelector("#ipt-pallets").removeAttribute("readonly");
      //set ""? why
    } else {
      document.querySelector("#ipt-pallets").setAttribute("readonly", true);
    }
  });
  /*document.querySelector("#cmb-load").addEventListener("change", function (ev) {
    console.log("hi", ev.currentTarget.value);
    if (
      ev.currentTarget.value == LOAD_TYPES.PALLET ||
      ev.currentTarget.value == LOAD_TYPES.MIXED
    ) {

      ev.currentTarget.removeAttribute("readonly");
      //set ""? why
    } else {
      ev.currentTarget.setAttribute("readonly", true);
    }
  });*/
}

function displayZeroWarning(dt) {
  let billsWarning = [];
  let zeroBulksWarning = `Estas facturas ${billsWarning.join(
    ","
  )} no se agregarán porque no se les especificó una cantidad de bultos. Por favor verifique esta información.`;
  dt.rows({ selected: true, page: "all" }).forEach((r) => {
    const data = r.data();
    if (data[5] < 1) {
      billsWarning.push(data[4]);
    }
  });

  let hasZeroBulksWarning = billsWarning.length > 0;
  if (hasZeroBulksWarning) {
    warningMsg(zeroBulksWarning);
  }
  return hasZeroBulksWarning;
}

function clearFields() {
  console.log("limpio");
  const ipts = [...document.querySelectorAll(".app-input")];
  ipts.forEach((i) => (i.value = ""));
  $("#cmb-method").val("-1");
  $("#cmb-transport").val("-1");
  $("#cmb-load").val("-1");
  $("#cmb-method").trigger("change");
  $("#cmb-transport").trigger("change");
  $("#cmb-load").trigger("change");
}

function getCSRFToken() {
  let name = "csrftoken";
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
