from django.db import models

from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import Value
from django.db.models.functions import Concat
from decimal import Decimal
# Create your models here.

# Importing models from the catalogs app
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product
from kdsu.companies.orders.models import Order, OrderDetail
import xmlschema


class Documento(models.Model):
    compania = models.ForeignKey(Company, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ordenes = models.ManyToManyField(Order)
    folio = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    totalPeso = models.IntegerField()
    totalBultos = models.IntegerField()

    def __str__(self):
        return f'{self.folio}'


class Factura(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    serie = models.CharField(max_length=100)
    folio = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    impuestos = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    total = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    uuid = models.UUIDField()

    @staticmethod
    def validar_cfdi(xml_route):
        resp = {"cfdi": {
            "valido": True,
            "validaciones": [],
            "resultado": {}
        }}
        schema = xmlschema.XMLSchema([
            'kdsu/companies/documents/schemas/cfdv40.xsd',
            'kdsu/companies/documents/schemas/TimbreFiscalDigitalv11.xsd',
            'kdsu/companies/documents/schemas/AddendaK.xsd',
            'kdsu/companies/documents/schemas/AddendaKdsu20.xsd',
        ],
            defuse='always',
            allow='local')
        xmlRoute = xml_route
        #sd = schema.to_dict(xmlRoute)
        try:
            if schema.is_valid(xmlRoute):
                sd = schema.to_dict(xmlRoute)
                emisor = sd['cfdi:Emisor']['@Rfc']
                receptor = sd['cfdi:Receptor']['@Rfc']
                uuid = sd['cfdi:Complemento']['tfd:TimbreFiscalDigital'][0]['@UUID']
                # busca emisor
                isValidEmisor = Supplier.objects.filter(
                    rfc__exact=emisor).exists()
                if not isValidEmisor:
                    resp['cfdi']['validaciones'].append(
                        {'emisor': "El RFC emisor no es válido o no se encuentra registrado en el sistema"})
                    resp['cfdi']['valido'] = False
                # busca receptor
                isValidReceptor = Company.objects.filter(
                    rfc__exact=receptor).exists()
                if not isValidReceptor:
                    resp['cfdi']['validaciones'].append(
                        {'receptor': "El RFC receptor no es válido o no se encuentra registrado en el sistema"})
                    resp['cfdi']['valido'] = False
                    # Verificar que no exista otra “factura” ya registrada con el mismo “uuid”
                billExists = Factura.objects.filter(
                    uuid=uuid).exists()
                # if billExists:
                #     resp['cfdi']['validaciones'].append(
                #         {'documento': "Ya existe un documento registrado con esa serie y folio"})
                #     resp['cfdi']['valido'] = False
                # Verificar que no exista un “documento” de la misma compañía (obtenida por el RFC receptor),
                docName = sd['@TipoDeComprobante'] + sd['@Serie']
                cia = Company.objects.filter(rfc__exact=receptor)
                prov = Supplier.objects.filter(rfc__exact=emisor)
                resp['cfdi']['cia'] = cia
                resp['cfdi']['prov'] = prov
                docs = Documento.objects.filter(compania__in=cia).filter(proveedor__in=prov)
                docExists = Factura.objects.filter(documento__in=docs).annotate(doc_name=Concat(
                    'serie', Value(''), 'folio')).filter(folio__exact=docName).exists()
                # proveedor (obtenido por el RFC emisor), y folio (concatenando serie + folio del elemento Comprobante del cfdi)
                # if docExists:
                #     resp['cfdi']['validaciones'].append(
                #         {'uuid': "Ya existe una factura registrada con el mismo UUID"})
                #     resp['cfdi']['valido'] = False
                
                # Si pasa las validaciones, lo agrega al resultado
                resp['cfdi']['resultado'] = sd
                
            else:
                print("El archivo no contiene una estructura CFDI válida")
                resp['cfdi']['validaciones']['cfdi'] = "El archivo no contiene una estructura CFDI válida"
        except xmlschema.XMLSchemaValidationError as e:
            print(f"XML validation error: {e}")
        except FileNotFoundError:
            print("Error: Schema or XML file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return resp
    
    @staticmethod
    def cargar_cfdi(xml_route):
        resp = {"cfdi": {
            "valido": True,
            "validaciones": [],
            "resultado": {}
        }}
        # Ejecutar la validación primero
        resultado_validacion = Factura.validar_cfdi(xml_route)
        xml_dic = resultado_validacion['cfdi']['resultado']
        
        # Si no es válido, devolver el mensaje de error tal cual lo trae validar_cfdi
        if not resultado_validacion.get('cfdi', {}).get('valido', False):
            resp['cfdi']['valido'] = False
            resp['cfdi']['validaciones'].append({'cfdi': "El CFDI no es válido"})
            resp['cfdi']['validaciones'].append(resultado_validacion['cfdi']['validaciones'])
            return resp

        # Si no trae nodo Addenda, error
        if not 'cfdi:Addenda' in xml_dic and not xml_dic['cfdi:Addenda']:
            resp['cfdi']['valido'] = False
            resp['cfdi']['validaciones'].append({'cfdi': "El CFDI no contiene Addenda"})
            return resp
        # Si no trae ni nodo KDSU ni nodo BOVEDA FISCAL, error.
        if not 'kdsu:KDSU' in xml_dic['cfdi:Addenda'] and not xml_dic['cfdi:Addenda']['kdsu:KDSU']:
            if not 'bovadd:BOVEDAFISCAL' in xml_dic['cfdi:Addenda'] and not xml_dic['cfdi:Addenda']['bovadd:BOVEDAFISCAL']:
                resp['cfdi']['valido'] = False
                resp['cfdi']['validaciones'].append({'cfdi': "El CFDI no contiene kdsu ni boveda fiscal"})
                return resp
        # Si trae nodo BOVEDA FISCAL pero no trae nodo KDSU, queda pendiente el caso
        if 'bovadd:BOVEDAFISCAL' in xml_dic['cfdi:Addenda'] and xml_dic['cfdi:Addenda']['bovadd:BOVEDAFISCAL'] and not 'kdsu:KDSU' in xml_dic['cfdi:Addenda'] and not xml_dic['cfdi:Addenda']['kdsu:KDSU']:
            resp['cfdi']['valido'] = False
            resp['cfdi']['validaciones'].append({'cfdi': "El CFDI contiene Boveda Fiscal pero no contiene KDSU. Caso pendiente revisión"})
            return resp
        
        # listado con un diccionario de desglose por cada conceptokdsu
        desglose_conceptos = []
        info_entrega = []
        trae_addenda = False
        if 'cfdi:Addenda' in xml_dic and xml_dic['cfdi:Addenda']:
            addenda = xml_dic['cfdi:Addenda']
            if 'kdsu:KDSU' in addenda:
                kdsu_data = addenda['kdsu:KDSU'][0]
                if 'kdsu:ConceptosKDSU' in kdsu_data:
                    trae_addenda = True
                    conceptos_kdsu = kdsu_data['kdsu:ConceptosKDSU']
                    info_entrega = kdsu_data.get('kdsu:Entrega', [])
                    conceptos = conceptos_kdsu.get('kdsu:ConceptoKDSU', [])
                    folio = None
                    info_entrega['serie'] = xml_dic.get('@Serie') or ''
                    info_entrega['folio'] = xml_dic.get('@Folio') or ''
                    
                    # Ambos Serie y Folio existen y tienen valor
                    if '@Serie' in xml_dic and xml_dic['@Serie'] and '@Folio' in xml_dic and xml_dic['@Folio']:
                        folio = xml_dic['@Serie'] + xml_dic['@Folio']
                    # Solo Serie existe y tiene valor, Folio no existe o está vacío
                    elif '@Serie' in xml_dic and xml_dic['@Serie'] and (('@Folio' not in xml_dic) or not xml_dic.get('@Folio')):
                        folio = xml_dic['@Serie']
                    # Solo Folio existe y tiene valor, Serie no existe o está vacío
                    elif (('@Serie' not in xml_dic) or not xml_dic.get('@Serie')) and '@Folio' in xml_dic and xml_dic['@Folio']:
                        folio = xml_dic['@Folio']
                    elif 'cfdi:Complemento' in xml_dic and xml_dic['cfdi:Complemento']:
                        complemento = xml_dic['cfdi:Complemento']
                        # Validar que exista 'tfd:TimbreFiscalDigital' como lista no vacía
                        if 'tfd:TimbreFiscalDigital' in complemento and isinstance(complemento['tfd:TimbreFiscalDigital'], list) and len(complemento['tfd:TimbreFiscalDigital']) > 0:
                            timbre = complemento['tfd:TimbreFiscalDigital'][0]
                            # Validar que contenga '@UUID' y que no sea vacío o None
                            if '@UUID' in timbre and timbre['@UUID']:
                                folio = xml_dic['cfdi:Complemento']['tfd:TimbreFiscalDigital'][0]['@UUID']
                    
                    info_entrega['folio_armado'] = folio
                    if folio is None:
                        resp['cfdi']['valido'] = False
                        resp['cfdi']['validaciones'].append({'folio': "El CFDI no contiene un valor para folio válido (Serie, Folio o UUID)"})
                        return resp
                    
                    for concepto in conceptos:
                        # Fabricas un nuevo diccionario manualmente
                        nuevo_concepto = {}                        
                        # Extraes solo las propiedades que quieres
                        if '@Orden' in concepto:
                            nuevo_concepto['orden'] = concepto['@Orden']
                        if '@Bulto' in concepto:
                            nuevo_concepto['bulto'] = concepto['@Bulto']
                        if '@CantidadOrden' in concepto:
                            nuevo_concepto['cantidad'] = concepto['@CantidadOrden']
                        if '@CodigoOrden' in concepto:
                            nuevo_concepto['codigoOrden'] = concepto['@CodigoOrden']
                        if '@CodigoFactura' in concepto: # EL CÓDIGO FACTURA ES LO MISMO EL QUE EL SKU
                            nuevo_concepto['sku'] = concepto['@CodigoFactura']
                        if '@PesoUnidadFacturaGr' in concepto:
                            nuevo_concepto['peso'] = concepto['@PesoUnidadFacturaGr']
                        nuevo_concepto['folio'] = folio
                        
                        # Agregas el nuevo objeto al arreglo final
                        desglose_conceptos.append(nuevo_concepto)

        if 'cfdi:Impuestos' in xml_dic:
            impuestos = 0
            if '@TotalImpuestosTrasladados' in xml_dic['cfdi:Impuestos']:
                impuestos += float(xml_dic['cfdi:Impuestos']['@TotalImpuestosTrasladados'])
            if '@TotalImpuestosRetenidos' in xml_dic['cfdi:Impuestos']:
                impuestos += float(xml_dic['cfdi:Impuestos']['@TotalImpuestosRetenidos'])
            info_entrega['impuestos'] = impuestos;
        
        validacion_desglose = Desglose.validar_desglose(desglose_conceptos, True) # CAMBIAR FALSE BRO
        return validacion_desglose
        for val_desg in validacion_desglose:
            if not val_desg['desglose']['valido']:
                resp['cfdi']['valido'] = False

        if not resp['cfdi']['valido']:
            return validacion_desglose
        from decimal import Decimal
        from django.db import transaction
        try:
            with transaction.atomic():
                documento = Documento.objects.create(
                    compania=resultado_validacion['cfdi']['cia'].first(),
                    proveedor=resultado_validacion['cfdi']['prov'].first(),
                    folio=info_entrega['folio_armado'],
                    totalPeso=Decimal(info_entrega['@TotalPesoKg']),
                    totalBultos=int(info_entrega['@TotalBultos'])
                )
                factura = Factura.objects.create(
                    documento=documento,
                    serie=info_entrega['serie'],
                    folio=info_entrega['folio'],
                    fecha=xml_dic['cfdi:Complemento']['tfd:TimbreFiscalDigital'][0]['@FechaTimbrado'],
                    subtotal=Decimal(xml_dic['@SubTotal']),
                    impuestos=info_entrega['impuestos'],
                    total=Decimal(xml_dic['@Total']),
                    uuid=xml_dic['cfdi:Complemento']['tfd:TimbreFiscalDigital'][0]['@UUID']
                )
                
                resp['cfdi']['resultado']['documento'] = documento;
                resp['cfdi']['resultado']['factura'] = factura;
                factura_detalles = []
                for x in xml_dic['cfdi:Conceptos']['cfdi:Concepto']:
                    factura_detalle = Factura_detalle.objects.create(
                        factura=factura,
                        sku=x['@NoIdentificacion'],
                        claveProductoSat=x['@ClaveProdServ'],
                        claveUnidadSat=x['@ClaveUnidad'],
                        descripcion=x['@Descripcion'],
                        valorUnitario=x['@ValorUnitario'],
                        descuento=x.get('@Descuento') or 0,
                        importe=x['@Importe']
                    )
                    factura_detalles.append(factura_detalle)
                from pathlib import Path
                ruta = Path(xml_route)
                # Directorio (sin el nombre del archivo)
                directorio = str(ruta.parent)

                # Nombre del archivo sin extensión
                nombre_sin_extension = ruta.stem  # equivalente a os.path.splitext(nombre)[0]
                
                archivo = Factura_archivo.objects.create(
                    factura=factura,
                    nombre=nombre_sin_extension,
                    tipo='XML',
                    ruta=directorio
                )
                desgloses = []
                if trae_addenda:
                    for desglose in desglose_conceptos:
                        order_detail = OrderDetail.objects.get(order__order_id=desglose['orden'], product__sku=desglose['codigoOrden'])
                        
                        desglose = Desglose.objects.create(
                            documento=documento,
                            factura=factura,
                            bulto=desglose['bulto'],
                            order_detail=order_detail,
                            cantidad_orden=order_detail.quantity,
                            factura_detalle=next((detalle for detalle in factura_detalles if detalle.sku == desglose['sku']), None),
                            cantidad_factura=desglose['cantidad'],
                            peso_unitario_factura=desglose['peso'],
                        )
                        desgloses.append(desglose)
        except Exception as e:
            print(e)
            resp['cfdi']['valido'] = False
            resp['cfdi']['validaciones'].append({'registro': "Hubo un error al guardar los registros"})
            # resp['cfdi']['error'].append(e)
            return resp
        
        return resp

    def __str__(self):
        return self.documento


class Factura_detalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    claveProductoSat = models.CharField(max_length=10)
    claveUnidadSat = models.CharField(max_length=5)
    unidadSat = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=200)
    valorUnitario = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    descuento = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    importe = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal('0.0000'))


class Factura_archivo(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=250)
    tipo = models.CharField(max_length=5)
    ruta = models.CharField(max_length=200)


class Desglose(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    bulto = models.IntegerField()
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    cantidad_orden = models.IntegerField()
    factura_detalle = models.ForeignKey(
        Factura_detalle, on_delete=models.CASCADE)
    cantidad_factura = models.IntegerField(default=0)
    peso_unitario_factura = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal('0.0000'))
    
    
    #VALIDAR FACTURA SE USA CUANDO:
    #Se sube el desglose por separado
    #NO SE USA CUANDO
    #Se carga el CFDI con Addenda
    @staticmethod
    def validar_desglose(lista_desgloses, validar_factura):
        resultados = []
        from django.db.models import Sum
        #extraer folios únicos de la lista de desgloses
        folios = list(set(desg["folio"] for desg in lista_desgloses))
        
        if validar_factura:
            for folio in folios:
                validaciones = {}
                resultado = {
                    "desglose": {
                        "folio": folio,
                        "valido": True,
                        "validaciones": {}
                    }
                }
                # BUSCA QUE EL FOLIO EXISTA EN LA TABLA DE FACTURA
                try:
                    factura = Factura.objects.annotate(serie_folio=Concat('serie', Value(''), 'folio')).get(serie_folio=folio)
                except Factura.DoesNotExist:
                    valido = False
                    validaciones["sin_factura"] = "La factura no se ha cargado en el sistema"
                    resultado["desglose"]["valido"] = valido
                    resultado["desglose"]["validaciones"] = validaciones
                    resultados.append(resultado)
                    continue  # Saltar al siguiente elemento

                # SI LA FACTURA EXISTE, SE TOMA SU DOCUMENTO Y SE VALIDA QUE TODAVÍA NO TENGA INFORMACIÓN DE DESGLOSE CARGADA, SE BUSCA POR DOCUMENTO Y FACTURA
                try:
                    documento = Documento.objects.get(folio=folio)
                except Documento.DoesNotExist:
                    documento = None
                if documento:
                    desgloses = Desglose.objects.filter(documento=documento, factura=factura)
                    if desgloses.exists():
                        valido = False
                        validaciones["desglose_cargado"] = "Ya se cargó un desglose para este folio y serie"
                        resultado["desglose"]["valido"] = valido
                        resultado["desglose"]["validaciones"] = validaciones
                        resultados.append(resultado)
                        continue  # Saltar al siguiente elemento
                    
                    bultos = [int(desg['bulto']) for desg in lista_desgloses if desg['folio'] == folio]
                    bultos_documento = documento.totalBultos
                    faltantes = [i for i in range(1, bultos_documento + 1) if i not in bultos]
                    if faltantes:
                        valido = False
                        validaciones["bulto_faltante"] = "Los bultos " + ", ".join(str(f) for f in faltantes) + " no se encuentran en el desglose."
                        resultado["desglose"]["valido"] = valido
                        resultado["desglose"]["validaciones"] = validaciones
                        resultados.append(resultado)
                        continue  # Saltar al siguiente elemento
                    
                    sobrantes = [b for b in bultos if b not in set(range(1, bultos_documento + 1))]
                    if sobrantes:
                        valido = False
                        validaciones["bulto_extra"] = "La factura solo debe contener "+ str(bultos_documento) +" bultos. Bultos sobrantes: " + ", ".join(str(s) for s in sobrantes) + "."
                        resultado["desglose"]["valido"] = valido
                        resultado["desglose"]["validaciones"] = validaciones
                        resultados.append(resultado)
                        continue  # Saltar al siguiente elemento

        for elemento in lista_desgloses:
            resultado = {
                "desglose": elemento.copy()
            }
            valido = True
            validaciones = {}

            orden = elemento.get("orden")
            codigoOrden = elemento.get("codigoOrden")
            cantidad = elemento.get("cantidad")
            folio = elemento.get("folio")
            
            # Buscar el detalle de la orden
            try:
                order_detail = OrderDetail.objects.get(order__order_id=orden, product__sku=codigoOrden)
            except OrderDetail.DoesNotExist:
                valido = False
                validaciones["no_existe"] = "El documento contiene productos que no existen en la orden"
                resultado["desglose"]["valido"] = valido
                resultado["desglose"]["validaciones"] = validaciones
                resultados.append(resultado)
                continue  # Saltar al siguiente elemento

            # Validar cantidad no mayor a la solicitada
            if int(cantidad) > order_detail.quantity:
                valido = False
                validaciones["surtido"] = "El documento no puede surtir más de lo solicitado en la orden"

            # Sumar lo ya surtido en desgloses anteriores
            suma_existente = Desglose.objects.filter(order_detail=order_detail).aggregate(total=Sum('cantidad_orden'))['total'] or 0
            total_surtido = suma_existente + int(cantidad)

            if total_surtido > order_detail.quantity:
                valido = False
                validaciones["surtido"] = "El documento no puede surtir más de lo solicitado en la orden"

            resultado["desglose"]["valido"] = valido
            resultado["desglose"]["validaciones"] = validaciones if not valido else []
            resultados.append(resultado)

        return resultados
