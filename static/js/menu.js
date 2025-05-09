  // ==========================================
  //         FUNCIÓN GLOBAL DE ESPERA
  // ==========================================
  /**
   * Muestra la pantalla de espera (dimmer de Fomantic).
   * @param {string}  message    - Mensaje a mostrar (default: "Por favor espere...").
   * @param {boolean} fullscreen - true => pantalla completa, false => solo .main-content
   */
  function pantallaEspera(message = "Por favor espere...", fullscreen = true) {
    let overlay = document.getElementById('globalWaitOverlay');
    let msg     = document.getElementById('globalWaitMessage');
  
    if (!overlay || !msg) {
      console.warn("No se encontró #globalWaitOverlay o #globalWaitMessage en el DOM.");
      return;
    }
  
    // Actualizar mensaje
    msg.textContent = message;
  
    // Limpiar posición previa
    overlay.classList.remove('page');
  
    // Mover overlay al lugar correcto dependiendo del modo
    if (fullscreen) {
      overlay.classList.add('page');
      if (overlay.parentElement !== document.body) {
        document.body.appendChild(overlay);
      }
    } else {
      const main = document.querySelector('.main-content');
      if (!main) {
        console.warn("No se encontró '.main-content' para mostrar la espera parcial.");
        return;
      }
      if (overlay.parentElement !== main) {
        main.appendChild(overlay);
      }
    }
  
    // Mostrar el overlay
    $(overlay).dimmer({ closable: false }).dimmer('show');
  


  }
  
  


  /**
   * Oculta la pantalla de espera.
   */
  function hideWaitScreen() {
    const overlay = document.getElementById('globalWaitOverlay');
    if (!overlay) return;
    $(overlay).dimmer('hide');
  }
  

  // ==========================================
  //       Ejemplo: Botones de prueba
  // ==========================================
  $(document).ready(function(){
    $('#btnFullscreen').on('click', function(){
      // Modo FULLSCREEN, se cierra en 3s
      pantallaEspera("Procesando FULLSCREEN...", true, 3000);
    });

    $('#btnParcial').on('click', function(){
      // Modo parcial, se cierra en 5s
      pantallaEspera("Procesando PARCIAL...", false, 5000);
    });
  });





  $(document).ready(function () {
    const catalogoBtn = $('#plantillaConsultas');
    const contentDiv = $('#mainContent');
  
    if (catalogoBtn.length === 0) {
      console.error("No se encontró el botón #plantillaConsultas");
      return;
    }
  
    catalogoBtn.on('click', function (e) {
      e.preventDefault();
  
      $.ajax({
        url: '/orders/plantilla_consultas/',
        type: 'GET',
        success: function (data) {
          const overlay = $('#globalWaitOverlay');
          if (overlay.length) {
            $('body').append(overlay.detach()); 
          }
          
          contentDiv.html(data); 
          
          // cargarSucursales();
          
          //  pantallaEspera("Cargando Plantilla...", false);
    
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
       
        }
      });
    });
  });
  
  
  
  



