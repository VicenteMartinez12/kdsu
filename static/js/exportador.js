function descargarArchivo(contenido, nombreArchivo, tipoMime) {
    const blob = new Blob([contenido], { type: tipoMime });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = nombreArchivo;
    link.click();
  }


  function obtenerValorAnidado(objeto, ruta) {

    return ruta.split('.').reduce((acumulador, clave) => {

      return acumulador && acumulador[clave];
    }, objeto) || ''; 
  }
  
  
  function construirXML(data, config) {
    const {
      rootTag = 'items',
      itemTag = 'item',
      atributos = {}
    } = config;
  
    let xml = `<${rootTag}>\n`;
    data.forEach(obj => {
      let linea = `  <${itemTag}`;
      for (const [attr, path] of Object.entries(atributos)) {
        const valor = obtenerValorAnidado(obj, path);
        linea += ` ${attr}="${valor}"`;
      }
      linea += ` />\n`;
      xml += linea;
    });
    xml += `</${rootTag}>`;
    return xml;
  }
  
  function exportarCatalogo({ apiUrl, nombreArchivo, tipo, xmlConfig, generarCSV }) {
    const total = tabla.rows({ search: 'applied' }).count();
    const dataChecked = window.getCatalogoRegistros('checked');
    const dataFiltered = window.getCatalogoRegistros('filtered');
  
    const modo = (dataChecked.length === 0 || dataChecked.length === total)
      ? 'all'
      : 'checked';
  
    const datosAExportar = (modo === 'checked') ? dataChecked : dataFiltered;
  
    if (tipo === 'csv') {
      if (typeof generarCSV !== 'function') {
        console.error('No se definió una función generarCSV para este catálogo.');
        return;
      }
  
      const csvContent = generarCSV(datosAExportar);
      descargarArchivo(csvContent, `${nombreArchivo}.csv`, 'text/csv');
    }
  
    else if (tipo === 'json') {
      fetch(apiUrl)
        .then(resp => resp.json())
        .then(apiData => {
          const finalData = (modo === 'checked')
            ? apiData.filter(p => dataChecked.some(d => d.id == p.id))
            : apiData;
  
          const json = JSON.stringify(finalData, null, 2);
          descargarArchivo(json, `${nombreArchivo}.json`, 'application/json');
        });
    }
  
    else if (tipo === 'xml') {
      fetch(apiUrl)
        .then(resp => resp.json())
        .then(apiData => {
          const finalData = (modo === 'checked')
            ? apiData.filter(p => dataChecked.some(d => d.id == p.id))
            : apiData;
  
          const xml = construirXML(finalData, xmlConfig);
          descargarArchivo(xml, `${nombreArchivo}.xml`, 'application/xml');
        });
    }
  }
  

  function generarCSVGenerico(datos, encabezados = [], campos = []) {
    if (!Array.isArray(datos) || datos.length === 0) return '';
  
    // Si no se pasan encabezados o campos, tratamos de inferirlos del primer objeto
    if (encabezados.length === 0) {
      encabezados = campos.length > 0 ? campos : Object.keys(datos[0]);
    }
    if (campos.length === 0) {
      campos = encabezados;
    }
  
    const headerLine = encabezados.join(',');
  
    const filas = datos.map(row =>
      campos.map(campo => (row[campo] ?? '').toString().replace(/,/g, '')) // quita comas internas
    );
  
    return [headerLine, ...filas.map(f => f.join(','))].join('\n');
  }
  