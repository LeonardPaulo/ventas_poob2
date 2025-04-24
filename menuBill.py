from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))

class CrudClients(ICrud):
    def create(self): 
        validar = Valida() 
        borrarPantalla() 
        print('\033c', end='') 
        gotoxy(2,1);print(green_color+"*"*90+reset_color) 
        gotoxy(30,2);print(blue_color+"Registro de Cliente") 
    
    # Leer clientes existentes primero para validar cédula
        json_file = JsonFile(path+'/archivos/clients.json') 
        clientes = json_file.read()
    
        gotoxy(15,4);print("Cédula:") 
        dni = validar.cedula("Error: Cédula inválida o ya registrada", 23, 4, clientes)
    
        gotoxy(15,5);print("Nombre:") 
        nombre = validar.solo_letras("Error: Solo letras", 23, 5)
    
        gotoxy(15,6);print("Apellido:") 
        apellido = validar.solo_letras("Error: Solo letras", 25, 6)
    
        gotoxy(15,7);print("¿Cliente con tarjeta? (s/n):") 
        gotoxy(44,7);card = input().lower() == 's' 
    
        cliente = RegularClient(nombre, apellido, dni, card) 
        clientes.append(cliente.getJson()) 
        json_file.save(clientes) 
        gotoxy(15,9);print("😊 Cliente guardado exitosamente 😊") 
        time.sleep(2)

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Actualización de Cliente")
        gotoxy(15,4);print("Ingrese Cédula:")
        gotoxy(31,4);dni = validar.solo_numeros("Error: Solo números",31,4)
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clientes = json_file.read()
        for i, cliente in enumerate(clientes):
            if cliente["dni"] == dni:
                gotoxy(15,5);print("Nombre actual: " + cliente["nombre"])
                gotoxy(15,6);print("Nuevo nombre (Enter para mantener):")
                gotoxy(51,6);nuevo_nombre = input() or cliente["nombre"]
                gotoxy(15,7);print("Apellido actual: " + cliente["apellido"])
                gotoxy(15,8);print("Nuevo apellido (Enter para mantener):")
                gotoxy(53,8);nuevo_apellido = input() or cliente["apellido"]
                
                clientes[i] = RegularClient(nuevo_nombre, nuevo_apellido, dni, cliente["valor"] > 0).getJson()
                json_file.save(clientes)
                gotoxy(15,10);print("😊 Cliente actualizado exitosamente 😊")
                break
        else:
            gotoxy(15,6);print("❌ Cliente no encontrado ❌")
        time.sleep(2)

    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminación de Cliente")
        gotoxy(15,4);print("Ingrese Cédula:")
        gotoxy(31,4);dni = validar.solo_numeros("Error: Solo números",31,4)
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clientes = json_file.read()
        for i, cliente in enumerate(clientes):
            if cliente["dni"] == dni:
                gotoxy(15,6);print(f"¿Está seguro de eliminar a {cliente['nombre']} {cliente['apellido']}? (s/n):")
                if input().lower() == 's':
                    clientes.pop(i)
                    json_file.save(clientes)
                    gotoxy(15,8);print("😊 Cliente eliminado exitosamente 😊")
                else:
                    gotoxy(15,8);print("❌ Operación cancelada ❌")
                break
        else:
            gotoxy(15,6);print("❌ Cliente no encontrado ❌")
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Consulta de Clientes")
        gotoxy(15,4);print("1. Consultar por cédula")
        gotoxy(15,5);print("2. Consultar todos")
        gotoxy(15,6);print("Seleccione una opción (1-2):")
        validar = Valida()
        gotoxy(44,6);opcion = validar.solo_numeros("Error: Solo números",44,6)
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clientes = json_file.read()
        
        if opcion == "1":
            gotoxy(15,8);print("Ingrese la cédula:")
            gotoxy(34,8);dni = validar.solo_numeros("Error: Solo números",34,8)
            cliente_encontrado = False
            fila = 12  # Inicializamos fila aquí
            
            for cliente in clientes:
                if cliente['dni'] == dni:
                    gotoxy(5,10);print("DNI          Nombre      Apellido    Descuento")
                    gotoxy(5,11);print("-"*50)
                    gotoxy(5,12);print(f"{cliente['dni']:<12} {cliente['nombre']:<11} {cliente['apellido']:<11} {cliente['valor']*100}%")
                    cliente_encontrado = True
                    break
            
            if not cliente_encontrado:
                gotoxy(15,10);print("❌ Cliente no encontrado ❌")
                fila = 10  # Ajustamos fila si no se encuentra el cliente
        else:
            gotoxy(5,8);print("DNI          Nombre      Apellido    Descuento")
            gotoxy(5,9);print("-"*50)
            fila = 10
            for cliente in clientes:
                gotoxy(5,fila);print(f"{cliente['dni']:<12} {cliente['nombre']:<11} {cliente['apellido']:<11} {cliente['valor']*100}%")
                fila += 1
        
        gotoxy(5,fila+2);input("Presione Enter para continuar...")

class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Producto")
        gotoxy(15,4);print("ID:")
        id = int(validar.solo_numeros("Error: Solo números",19,4))
        gotoxy(15,5);print("Descripción:")
        gotoxy(28,5);descripcion = validar.solo_letras("Error: Solo letras", 28, 5)
        gotoxy(15,6);print("Precio:")
        precio = float(validar.solo_numeros("Error: Solo números",23,6))
        gotoxy(15,7);print("Stock:")
        stock = int(validar.solo_numeros("Error: Solo números",22,7))
        
        producto = Product(id, descripcion, precio, stock)
        json_file = JsonFile(path+'/archivos/products.json')
        productos = json_file.read()
        productos.append(producto.getJson())
        json_file.save(productos)
        gotoxy(15,9);print("😊 Producto guardado exitosamente 😊")
        time.sleep(2)

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Actualización de Producto")
        gotoxy(15,4);print("ID del producto:")
        id = int(validar.solo_numeros("Error: Solo números",32,4))
        
        json_file = JsonFile(path+'/archivos/products.json')
        productos = json_file.read()
        for i, producto in enumerate(productos):
            if producto["id"] == id:
                gotoxy(15,5);print("Descripción actual: " + producto["descripcion"])
                gotoxy(15,6);print("Nueva descripción (Enter para mantener):")
                gotoxy(56,6);nueva_desc = validar.solo_letras("Error: Solo letras", 56, 6) or producto["descripcion"]
                gotoxy(15,7);print(f"Precio actual: {producto['precio']}")
                gotoxy(15,8);print("Nuevo precio (Enter para mantener):")
                gotoxy(51,8);nuevo_precio = float(validar.solo_numeros("Error: Solo números",51,8) or producto["precio"])
                gotoxy(15,9);print(f"Stock actual: {producto['stock']}")
                gotoxy(15,10);print("Nuevo stock (Enter para mantener):")
                gotoxy(50,9);nuevo_stock = int(validar.solo_numeros("Error: Solo números",50,9) or producto["stock"])
                
                productos[i] = Product(id, nueva_desc, nuevo_precio, nuevo_stock).getJson()
                json_file.save(productos)
                gotoxy(15,12);print("😊 Producto actualizado exitosamente 😊")
                break
        else:
            gotoxy(15,6);print("❌ Producto no encontrado ❌")
        time.sleep(2)

    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminación de Producto")
        gotoxy(15,4);print("ID del producto:")
        id = int(validar.solo_numeros("Error: Solo números",32,4))
        
        json_file = JsonFile(path+'/archivos/products.json')
        productos = json_file.read()
        for i, producto in enumerate(productos):
            if producto["id"] == id:
                gotoxy(15,6);print(f"¿Está seguro de eliminar {producto['descripcion']}? (s/n):")
                if input().lower() == 's':
                    productos.pop(i)
                    json_file.save(productos)
                    gotoxy(15,8);print("😊 Producto eliminado exitosamente 😊")
                else:
                    gotoxy(15,8);print("❌ Operación cancelada ❌")
                break
        else:
            gotoxy(15,6);print("❌ Producto no encontrado ❌")
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Consulta de Productos")
        
        json_file = JsonFile(path+'/archivos/products.json')
        productos = json_file.read()
        
        gotoxy(5,4);print("ID    Descripción    Precio    Stock")
        gotoxy(5,5);print("-"*50)
        fila = 6
        for producto in productos:
            gotoxy(5,fila);print(f"{producto['id']:<6} {producto['descripcion']:<14} {producto['precio']:<9} {producto['stock']}")
            fila += 1
        
        gotoxy(5,fila+2);input("Presione Enter para continuar...")

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Modificación de Venta")
        gotoxy(15,4);print("Ingrese número de factura:")
        try:
            factura = validar.solo_numeros("Error: Solo números",40,4)
        
            json_file = JsonFile(path+'/archivos/invoices.json')
            ventas = json_file.read()
            encontrado = False
        
            for i, venta in enumerate(ventas):
                if venta["factura"] == int(factura):
                    encontrado = True
                    gotoxy(15,6);print(f"Fecha: {venta['Fecha']}")
                    gotoxy(15,7);print(f"Cliente: {venta['cliente']}")
                    gotoxy(15,8);print(f"Total: ${venta['total']}")
                
                    gotoxy(15,10);print("Detalles de la venta:")
                    fila = 11
                    for detalle in venta["detalle"]:
                        gotoxy(15,fila);print(f"Producto: {detalle['poducto']}, Cantidad: {detalle['cantidad']}, Precio: ${detalle['precio']}")
                        fila += 1
                
                    gotoxy(15,fila+1);print("Por razones de auditoría, no se permite modificar ventas realizadas.")
                    gotoxy(15,fila+2);print("Se sugiere crear una nota de crédito y realizar una nueva venta.")
                    gotoxy(15,fila+4);print("¿Desea crear una nueva venta? (s/n):")
                    if input().lower() == 's':
                        self.create()
                    else:
                        gotoxy(15,fila+5);print("❌ Operación cancelada ❌")
                    break
        
            if not encontrado:
                gotoxy(15,6);print("❌ Factura no encontrada ❌")
            
        except ValueError as e:
            gotoxy(15,6);print("❌ Error: Número de factura inválido ❌")
        except Exception as e:
            gotoxy(15,6);print(f"❌ Error inesperado: {str(e)} ❌")
    
        time.sleep(2)
        
    def delete(self):  # Añadido self como parámetro
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminación de Venta")
        gotoxy(15,4);print("Ingrese número de factura:")
        factura = validar.solo_numeros("Error: Solo números",40,4)
        
        json_file = JsonFile(path+'/archivos/invoices.json')
        ventas = json_file.read()
        encontrado = False
        
        for i, venta in enumerate(ventas):
            if venta["factura"] == int(factura):
                encontrado = True
                gotoxy(15,6);print(f"Fecha: {venta['Fecha']}")
                gotoxy(15,7);print(f"Cliente: {venta['cliente']}")
                gotoxy(15,8);print(f"Total: ${venta['total']}")
                
                gotoxy(15,10);print("¿Está seguro de eliminar esta venta? (s/n):")
                if input().lower() == 's':
                    gotoxy(15,12);print("Creando nota de crédito...")
                    nota_credito = {
                        "tipo": "nota_credito",
                        "factura_original": venta["factura"],
                        "fecha": str(datetime.datetime.now()),
                        "cliente": venta["cliente"],
                        "total": venta["total"]
                    }
                    
                    try:
                        json_file_nc = JsonFile(path+'/archivos/notas_credito.json')
                        notas = json_file_nc.read()
                        notas.append(nota_credito)
                        json_file_nc.save(notas)
                        
                        ventas.pop(i)
                        json_file.save(ventas)
                        gotoxy(15,14);print("😊 Venta eliminada y nota de crédito generada exitosamente 😊")
                    except Exception as e:
                        gotoxy(15,14);print(f"❌ Error al procesar la operación: {str(e)} ❌")
                else:
                    gotoxy(15,12);print("❌ Eliminación cancelada ❌")
                break
        
        if not encontrado:
            gotoxy(15,6);print("❌ Factura no encontrada ❌")
        
        time.sleep(2)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        crud_clients = CrudClients()
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients.create()
            elif opc1 == "2":
                crud_clients.update()
            elif opc1 == "3":
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients.consult()
            print("Regresando al menu Clientes...")
            time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        crud_products = CrudProducts()
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_products.create()
            elif opc2 == "2":
                crud_products.update()
            elif opc2 == "3":
                crud_products.delete()
            elif opc2 == "4":
                crud_products.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
    
    print("Regresando al menu Principal...")
    time.sleep(2)            

borrarPantalla()

input("Presione una tecla para salir...")
borrarPantalla()

