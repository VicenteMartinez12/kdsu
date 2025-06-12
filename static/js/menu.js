// ==========================================
//         FUNCIÓN GLOBAL DE ESPERA
// ==========================================
/**
 * Muestra la pantalla de espera (dimmer de Fomantic).
 * @param {string}  message    - Mensaje a mostrar (default: "Por favor espere...").
 * @param {boolean} fullscreen - true => pantalla completa, false => solo .main-content
 */
function pantallaEspera(message = "Por favor espere...", fullscreen = true) {
  let overlay = document.getElementById("globalWaitOverlay");
  let msg = document.getElementById("globalWaitMessage");

  if (!overlay || !msg) {
    console.warn(
      "No se encontró #globalWaitOverlay o #globalWaitMessage en el DOM."
    );
    return;
  }

  // Actualizar mensaje
  msg.textContent = message;

  // Limpiar posición previa
  overlay.classList.remove("page");

  // Mover overlay al lugar correcto dependiendo del modo
  if (fullscreen) {
    overlay.classList.add("page");
    if (overlay.parentElement !== document.body) {
      document.body.appendChild(overlay);
    }
  } else {
    const main = document.querySelector(".main-content");
    if (!main) {
      console.warn(
        "No se encontró '.main-content' para mostrar la espera parcial."
      );
      return;
    }
    if (overlay.parentElement !== main) {
      main.appendChild(overlay);
    }
  }

  // Mostrar el overlay
  $(overlay).dimmer({ closable: false }).dimmer("show");
}

/**
 * Oculta la pantalla de espera.
 */
function hideWaitScreen() {
  const overlay = document.getElementById("globalWaitOverlay");
  if (!overlay) return;
  $(overlay).dimmer("hide");
}

// ==========================================
//       Ejemplo: Botones de prueba
// ==========================================
$(document).ready(function () {
  $("#btnFullscreen").on("click", function () {
    // Modo FULLSCREEN, se cierra en 3s
    pantallaEspera("Procesando FULLSCREEN...", true, 3000);
  });

  $("#btnParcial").on("click", function () {
    // Modo parcial, se cierra en 5s
    pantallaEspera("Procesando PARCIAL...", false, 5000);
  });
});

$(document).ready(function () {
  const catalogoBtn = $("#plantillaConsultas");
  const contentDiv = $("#mainContent");

  if (catalogoBtn.length === 0) {
    console.error("No se encontró el botón #plantillaConsultas");
    return;
  }

  catalogoBtn.on("click", function (e) {
    e.preventDefault();

    $.ajax({
      url: "/orders/plantilla_consultas/",
      type: "GET",
      success: function (data) {
        const overlay = $("#globalWaitOverlay");
        if (overlay.length) {
          $("body").append(overlay.detach());
        }

        contentDiv.html(data);

        // cargarSucursales();

        pantallaEspera("Cargando plantilla nueva", false);

        initPlantilla();
      },

      error: function (xhr, status, error) {
        console.error("Error al cargar el catálogo:", status, error);
        contentDiv.html(`
            <div class="ui negative message">
              <div class="header">Error al cargar el contenido</div>
              <p>${xhr.status} - ${xhr.statusText}</p>
            </div>
          `);
      },
    });
  });
});

$(document).ready(function () {
  const catalogoBtn = $("#plantillaPdf");
  const contentDiv = $("#mainContent");

  if (catalogoBtn.length === 0) {
    console.error("No se encontró el botón #plantillaPdf");
    return;
  }

  catalogoBtn.on("click", function (e) {
    e.preventDefault();

    $.ajax({
      url: "/orders/plantilla_pdf/",
      type: "GET",
      success: function (data) {
        const overlay = $("#globalWaitOverlay");
        if (overlay.length) {
          $("body").append(overlay.detach());
        }

        // Limpia correctamente los dimmers y modals antes de cargar el nuevo contenido
        $(".ui.dimmer.modals").removeClass("active").removeAttr("style");
        $(".ui.modal").modal("hide").remove();

        contentDiv.html(data);

        // pantallaEspera("Cargando plantilla nueva", false);

        initPdf();
      },

      error: function (xhr, status, error) {
        console.error("Error al cargar el catálogo:", status, error);
        contentDiv.html(`
            <div class="ui negative message">
              <div class="header">Error al cargar el contenido</div>
              <p>${xhr.status} - ${xhr.statusText}</p>
            </div>
          `);
      },
    });
  });
});

$(document).ready(function () {
  const catalogoBtn = $("#descargaPedidos");
  const contentDiv = $("#mainContent");

  if (catalogoBtn.length === 0) {
    console.error("No se encontró el botón #descargaPedidos");
    return;
  }

  catalogoBtn.on("click", function (e) {
    e.preventDefault();

    $.ajax({
      url: "/orders/descarga_pedidos/",
      type: "GET",
      success: function (data) {
        const overlay = $("#globalWaitOverlay");
        if (overlay.length) {
          $("body").append(overlay.detach());
        }

        // Limpia correctamente los dimmers y modals antes de cargar el nuevo contenido
        $(".ui.dimmer.modals").removeClass("active").removeAttr("style");
        $(".ui.modal").modal("hide").remove();

        contentDiv.html(data);

        // pantallaEspera("Cargando plantilla nueva", false);

        initDescargaPedidos();
      },

      error: function (xhr, status, error) {
        console.error("Error al cargar el catálogo:", status, error);
        contentDiv.html(`
            <div class="ui negative message">
              <div class="header">Error al cargar el contenido</div>
              <p>${xhr.status} - ${xhr.statusText}</p>
            </div>
          `);
      },
    });
  });
});

$(document).ready(function () {
  const catalogoBtn = $("#calendarioCitas");
  const contentDiv = $("#mainContent");

  if (catalogoBtn.length === 0) {
    console.error("No se encontró el botón #calendarioCitas");
    return;
  }
  let DateTime = luxon.DateTime;

  catalogoBtn.on("click", function (e) {
    e.preventDefault();

    $.ajax({
      url: "/appointments/calendario/",
      type: "GET",
      success: function (data) {
        const overlay = $("#globalWaitOverlay");
        if (overlay.length) {
          $("body").append(overlay.detach());
        }

        // Limpia correctamente los dimmers y modals antes de cargar el nuevo contenido
        $(".ui.dimmer.modals").removeClass("active").removeAttr("style");
        $(".ui.modal").modal("hide").remove();

        contentDiv.html(data);

        /////valores desde backend////////////////
        const mappedEvents = appointments.map((e) => {
          let status = "";
          switch (e.status.toLowerCase()) {
            case "solicitada":
              status = "requested";
              break;
            case "confirmada":
              status = "confirmed";
              break;
            default:
              break;
          }
          return {
            title: "olaz",
            start: e.requested_date.split("T")[0],
            end: e.requested_date.split("T")[0],
            className: [status],
          };
        });
        console.log(mappedEvents, "<-------");

        // pantallaEspera("Cargando plantilla nueva", false);

        var calendarEl = document.getElementById("calendar");
        var calendar = new FullCalendar.Calendar(calendarEl, {
          dayCellContent: function (arg) {
            return {
              html: `<div data-date="${arg.date.getDate()}">${arg.date.getDate()}</div>`,
            };
          },
          dayCellDidMount: function (info) {
            //llama api
            //console.log("ola", info);
            // `info.el` is the DOM element for the cell
            // console.log(info.date.getTime(), info.date);
            if (info.date.getDay() === 0) {
              // Example: Sundays get red background
              info.el.classList.add("unavailable");
            } else if (
              info.date.getTime() < DateTime.now().toMillis() &&
              info.date.getDay() != 0 &&
              info.date.toDateString() != new Date().toDateString()
            ) {
              //validar si ya paso el dia
              console.log(
                "past",
                DateTime.now().startOf("day"),
                DateTime.fromJSDate(info.date).startOf("day")
              );
              info.el.classList.add("past");
            }
            /*
            const evts = mappedEvents.filter(me => me.start == info.el.dataset['date'])
            console.log("filter", evts);
            evts.forEach(e => {
              if(e.classname == 'confirmada'){
                info.el.classList.add('confirmed');
              } else if(e.classname == 'solicitada'){
                info.el.classList.add("requested");
              }
            }) */
          },
          firstDay: 0,
          height: 500,
          contentHeight: 400,
          locale: "es",
          headerToolbar: false,
          eventMouseEnter: function (eventInfo) {
            const el = eventInfo.el;
            el.classList.add("selected");
          },
          eventMouseLeave: function (eventInfo) {
            const el = eventInfo.el;
            el.classList.remove("selected");
          },
          events: mappedEvents,
          initialView: "dayGridFourWeek",
          views: {
            dayGridFourWeek: {
              type: "dayGrid",
              duration: { weeks: 4 },
            },
          },
          selectable: true,
          select: function (info) {
            console.log("select", info);
          },
          dateClick: function (info) {
            selected = info.dayEl;
          },
          eventClick: function (info) {
            alert("Event: " + info.event.title);
            alert(
              "Coordinates: " + info.jsEvent.pageX + "," + info.jsEvent.pageY
            );
            alert("View: " + info.view.type);

            // change the border color just for fun
            info.el.style.borderColor = "red";
          },
        });
        calendar.render();


      },

      error: function (xhr, status, error) {
        console.error("Error al cargar el catálogo:", status, error);
        contentDiv.html(`
            <div class="ui negative message">
              <div class="header">Error al cargar el contenido</div>
              <p>${xhr.status} - ${xhr.statusText}</p>
            </div>
          `);
      },
    });
  });
});
