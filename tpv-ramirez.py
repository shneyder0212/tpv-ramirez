import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tempfile
import os
from datetime import datetime, date
import random

# --- BASE DE DATOS DE PRODUCTOS Y CONFIGURACIÓN COMPLETA ---
INVENTARIO = [
    {"codigo": "0000000000001", "descripcion": "SAZON LIQUIDO RANCHERO 400ML", "costo": 1.50, "precio": 2.47, "iva": 21, "stock": 2.0, "caducidad": "15/08/2026"},
    {"codigo": "0000000000002", "descripcion": "GANDULES VERDES CON COCO GOYA", "costo": 1.60, "precio": 2.72, "iva": 10, "stock": 6.0, "caducidad": "20/09/2026"},
    {"codigo": "0000000000003", "descripcion": "OREGANO RANCHERO EN POLVO 90GR", "costo": 1.50, "precio": 2.47, "iva": 4, "stock": 12.0, "caducidad": "10/01/2027"},
    {"codigo": "0000000000020", "descripcion": "COCA COLA LATA 330 ML", "costo": 0.70, "precio": 1.23, "iva": 21, "stock": 61.0, "caducidad": "05/08/2026"},
    {"codigo": "8410199026482", "descripcion": "MAS MOVIL TODO INCLUIDO 15€", "costo": 5.00, "precio": 8.26, "iva": 21, "stock": 159.0, "caducidad": "31/12/2030"},
    {"codigo": "0000000000021", "descripcion": "CERVEZA PRESIDENTE LATA", "costo": 0.90, "precio": 1.50, "iva": 21, "stock": 50.0, "caducidad": "31/12/2026"},
    {"codigo": "0000000000022", "descripcion": "MABI SEIBO BOTELLA", "costo": 1.20, "precio": 2.00, "iva": 10, "stock": 30.0, "caducidad": "31/12/2026"},
    {"codigo": "0000000000023", "descripcion": "POLLO ENTERO FRESCO", "costo": 4.50, "precio": 7.50, "iva": 4, "stock": 10.0, "caducidad": "02/08/2026"},
]

# Historial de ventas global
HISTORIAL_VENTAS = []

DATOS_EMPRESA_DEFECTO = {
    "nombre_empresa": "MULTI SERVICIOS RAMIREZ",
    "nif_empresa": "02799425-A",
    "direccion_empresa": "AVDA. DR. FLEMING 9, 24009 LEON ESPANA"
}

USUARIOS = {
    "admin": {"nombre": "Shneyder Ramírez", "password": "1234", "rol": "admin"},
    "empleado": {"nombre": "Rafelin Mendez", "password": "1234", "rol": "empleado"}
}

CAJA_ABIERTA = False
TOTAL_CAJA_INICIAL = 0.0

class TPVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Servicios Ramírez - Terminal Punto de Venta Profesional")
        self.root.geometry("1280x800")
        self.root.state("zoomed")
        self.root.configure(bg="#f8fafc")

        # Configuración de estilos modernos y tipografías más grandes
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 12))
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

        self.usuario_actual = None
        self.rol_actual = None
        self.nombre_operador = ""
        self.cart = []
        self.total_var = tk.DoubleVar(value=0.0)

        self.main_container = tk.Frame(self.root, bg="#f8fafc")
        self.main_container.pack(fill="both", expand=True)

        self.mostrar_login()

    def mostrar_login(self):
        self.win_login = tk.Toplevel(self.root)
        self.win_login.title("Inicio de Sesión - Multi Servicios Ramírez")
        self.win_login.geometry("460x360")
        self.win_login.grab_set()
        self.win_login.lift()
        self.win_login.focus_force()
        self.win_login.protocol("WM_DELETE_WINDOW", self.root.destroy)

        tk.Label(self.win_login, text="🛒 MULTI SERVICIOS RAMÍREZ", font=("Segoe UI", 16, "bold"), fg="#1e293b").pack(pady=20)
        tk.Label(self.win_login, text="Av. Dr. Fleming 9, 24009 León España", font=("Segoe UI", 11), fg="#64748b").pack(pady=(0, 15))

        f = tk.Frame(self.win_login)
        f.pack(pady=10)

        tk.Label(f, text="Usuario:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        self.ent_user = tk.Entry(f, font=("Segoe UI", 12), width=18)
        self.ent_user.grid(row=0, column=1, pady=8, padx=8)
        self.ent_user.insert(0, "admin")
        self.ent_user.focus()

        tk.Label(f, text="Contraseña:", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        self.ent_pass = tk.Entry(f, font=("Segoe UI", 12), width=18, show="*")
        self.ent_pass.grid(row=1, column=1, pady=8, padx=8)
        self.ent_pass.insert(0, "1234")
        self.ent_pass.bind("<Return>", lambda e: self.validar_login())

        btn_ingresar = tk.Button(self.win_login, text="🔑 Ingresar al TPV", font=("Segoe UI", 12, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", cursor="hand2", command=self.validar_login, width=22, pady=8)
        btn_ingresar.pack(pady=20)

    def validar_login(self):
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get().strip()

        if user in USUARIOS and USUARIOS[user]["password"] == pwd:
            self.usuario_actual = user
            self.rol_actual = USUARIOS[user]["rol"]
            self.nombre_operador = USUARIOS[user]["nombre"]
            self.win_login.destroy()
            self.crear_interfaz()
            self.verificar_alertas_caducidad_automaticas()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def verificar_alertas_caducidad_automaticas(self):
        hoy = date.today()
        proximos_a_vencer = []
        for p in INVENTARIO:
            cad_str = p.get("caducidad", "")
            if cad_str:
                try:
                    f_cad = datetime.strptime(cad_str, "%d/%m/%Y").date()
                    dias_restantes = (f_cad - hoy).days
                    if dias_restantes <= 30:
                        proximos_a_vencer.append((p["descripcion"], cad_str, dias_restantes))
                except ValueError:
                    pass
        
        if proximos_a_vencer:
            mensaje = "⚠️ ¡ATENCIÓN: PRODUCTOS PRÓXIMOS A CADUCAR! ⚠️\n\nLos siguientes artículos están cerca de su fecha de vencimiento:\n\n"
            for desc, fecha, dias in proximos_a_vencer:
                if dias < 0:
                    mensaje += f"❌ [VENCIDO hace {abs(dias)} días]: {desc} (Fecha: {fecha})\n"
                elif dias == 0:
                    mensaje += f"⚠️ [VENCE HOY]: {desc} (Fecha: {fecha})\n"
                else:
                    mensaje += f"⏳ [Quedan {dias} días]: {desc} (Fecha: {fecha})\n"
            
            messagebox.showwarning("Alerta de Caducidad y Ofertas", mensaje)

    def crear_interfaz(self):
        header = tk.Frame(self.main_container, bg="#0f172a", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        lbl_titulo = tk.Label(
            header, text=f"⚡ MULTI SERVICIOS RAMÍREZ | Operador: {self.nombre_operador.upper()} ({self.rol_actual.upper()})",
            font=("Segoe UI", 13, "bold"), fg="white", bg="#0f172a", pady=15
        )
        lbl_titulo.pack(side="left", padx=20)

        btn_caja = tk.Button(header, text="💵 [F4] Caja", bg="#059669", fg="white", activebackground="#047857", activeforeground="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, command=self.gestion_caja)
        btn_caja.pack(side="right", padx=6, pady=15)

        btn_compras = tk.Button(header, text="📋 Compras", bg="#d97706", fg="white", activebackground="#b45309", activeforeground="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, command=self.ver_lista_compras)
        btn_compras.pack(side="right", padx=6, pady=15)

        btn_ranking = tk.Button(header, text="🔥 Top / Menos Vendidos", bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, command=self.ver_ranking_productos)
        btn_ranking.pack(side="right", padx=6, pady=15)

        btn_historico = tk.Button(header, text="📊 Ventas", bg="#7c3aed", fg="white", activebackground="#6d28d9", activeforeground="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, command=self.ver_historico_ventas)
        btn_historico.pack(side="right", padx=6, pady=15)

        if self.rol_actual == "admin":
            btn_config = tk.Button(header, text="⚙️ Config.", bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, command=self.abrir_configuracion)
            btn_config.pack(side="right", padx=6, pady=15)

        content = tk.Frame(self.main_container, bg="#f8fafc")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        left_panel = tk.Frame(content, bg="white", bd=0, highlightbackground="#cbd5e1", highlightthickness=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))

        frame_barcode = tk.Frame(left_panel, bg="#f1f5f9", pady=12, padx=12)
        frame_barcode.pack(fill="x", padx=15, pady=15)

        tk.Label(frame_barcode, text="🔍 [F1] Escanear Código o Buscar Producto:", font=("Segoe UI", 12, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w")
        
        self.txt_barcode = tk.Entry(frame_barcode, font=("Segoe UI", 14))
        self.txt_barcode.pack(fill="x", pady=8)
        self.txt_barcode.focus()
        self.txt_barcode.bind("<Return>", self.procesar_codigo_barras)

        self.txt_buscar = tk.Entry(left_panel, font=("Segoe UI", 12))
        self.txt_buscar.pack(fill="x", padx=15, pady=(0, 10))
        self.txt_buscar.bind("<KeyRelease>", self.filtrar_productos)

        columns = ("codigo", "descripcion", "precio", "iva", "stock")
        self.tabla_productos = ttk.Treeview(left_panel, columns=columns, show="headings", height=16)
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("descripcion", text="Descripción")
        self.tabla_productos.heading("precio", text="P. Venta (€)")
        self.tabla_productos.heading("iva", text="IVA")
        self.tabla_productos.heading("stock", text="Stock")

        self.tabla_productos.column("codigo", width=160, anchor="w")
        self.tabla_productos.column("descripcion", width=340, anchor="w")
        self.tabla_productos.column("precio", width=100, anchor="e")
        self.tabla_productos.column("iva", width=70, anchor="center")
        self.tabla_productos.column("stock", width=70, anchor="center")
        self.tabla_productos.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tabla_productos.bind("<Double-1>", lambda e: self.agregar_seleccionado_carrito())

        btn_agregar = tk.Button(
            left_panel, text="➕ Agregar Producto Seleccionado", font=("Segoe UI", 12, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", cursor="hand2", command=self.agregar_seleccionado_carrito, pady=12
        )
        btn_agregar.pack(fill="x", padx=15, pady=15)

        right_panel = tk.Frame(content, bg="white", bd=0, highlightbackground="#cbd5e1", highlightthickness=1, width=460)
        right_panel.pack(side="right", fill="both")
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="🧾 Ticket de Venta Actual", font=("Segoe UI", 14, "bold"), bg="white", fg="#0f172a").pack(anchor="w", padx=15, pady=15)

        cart_cols = ("producto", "cant", "precio", "subtotal")
        self.tabla_carrito = ttk.Treeview(right_panel, columns=cart_cols, show="headings", height=13)
        self.tabla_carrito.heading("producto", text="Producto")
        self.tabla_carrito.heading("cant", text="Cant.")
        self.tabla_carrito.heading("precio", text="Precio")
        self.tabla_carrito.heading("subtotal", text="Subtotal")
        self.tabla_carrito.column("producto", width=170)
        self.tabla_carrito.column("cant", width=55, anchor="center")
        self.tabla_carrito.column("precio", width=80, anchor="e")
        self.tabla_carrito.column("subtotal", width=95, anchor="e")
        self.tabla_carrito.pack(fill="both", expand=True, padx=15, pady=5)

        btn_quitar = tk.Button(right_panel, text="❌ [F6] Quitar ítem", font=("Segoe UI", 11, "bold"), bg="#ef4444", fg="white", activebackground="#dc2626", activeforeground="white", relief="flat", cursor="hand2", command=self.quitar_item_carrito, pady=6)
        btn_quitar.pack(fill="x", padx=15, pady=5)

        frame_totales = tk.Frame(right_panel, bg="#f1f5f9", padx=15, pady=12)
        frame_totales.pack(fill="x", padx=15, pady=8)

        self.lbl_base = tk.Label(frame_totales, text="Base Imponible: 0.00 €", font=("Segoe UI", 11), bg="#f1f5f9", fg="#334155")
        self.lbl_base.pack(anchor="w")
        self.lbl_iva_total = tk.Label(frame_totales, text="IVA Total: 0.00 €", font=("Segoe UI", 11), bg="#f1f5f9", fg="#334155")
        self.lbl_iva_total.pack(anchor="w")

        lbl_tot_txt = tk.Label(frame_totales, text="TOTAL A PAGAR:", font=("Segoe UI", 13, "bold"), bg="#f1f5f9", fg="#0f172a")
        lbl_tot_txt.pack(anchor="w", pady=(6,2))
        self.lbl_total_num = tk.Label(frame_totales, text="0.00 €", font=("Segoe UI", 22, "bold"), fg="#16a34a", bg="#f1f5f9")
        self.lbl_total_num.pack(anchor="w")

        frame_pago = tk.Frame(right_panel, bg="white", padx=15)
        frame_pago.pack(fill="x", pady=8)

        tk.Label(frame_pago, text="Paga con (€):", font=("Segoe UI", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_pago = tk.Entry(frame_pago, font=("Segoe UI", 12), width=12)
        self.ent_pago.grid(row=0, column=1, padx=8, pady=4)
        self.ent_pago.bind("<KeyRelease>", self.calcular_cambio)

        tk.Label(frame_pago, text="Cambio:", font=("Segoe UI", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=6)
        self.lbl_cambio = tk.Label(frame_pago, text="0.00 €", font=("Segoe UI", 13, "bold"), fg="#2563eb", bg="white")
        self.lbl_cambio.grid(row=1, column=1, sticky="w", padx=8)

        frame_acciones = tk.Frame(right_panel, bg="white")
        frame_acciones.pack(fill="x", padx=15, pady=15)

        btn_cobrar = tk.Button(
            frame_acciones, text="🟢 [F5] Cobrar Ticket", font=("Segoe UI", 12, "bold"),
            bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white", relief="flat", cursor="hand2", command=lambda: self.completar_venta(es_factura=False), pady=10
        )
        btn_cobrar.pack(fill="x", pady=4)

        btn_factura = tk.Button(
            frame_acciones, text="📄 [F3] Factura Nominativa", font=("Segoe UI", 12, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", cursor="hand2", command=lambda: self.completar_venta(es_factura=True), pady=10
        )
        btn_factura.pack(fill="x", pady=4)

        self.root.bind("<F1>", lambda e: self.txt_barcode.focus())
        self.root.bind("<F5>", lambda e: self.completar_venta(es_factura=False))
        self.root.bind("<F3>", lambda e: self.completar_venta(es_factura=True))
        self.root.bind("<F4>", lambda e: self.gestion_caja())
        self.root.bind("<F6>", lambda e: self.quitar_item_carrito())
        self.root.bind("<Escape>", lambda e: self.txt_barcode.focus())

        self.cargar_productos(INVENTARIO)

    def cargar_productos(self, lista):
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        for p in lista:
            self.tabla_productos.insert("", "end", values=(p["codigo"], p["descripcion"], f"{p['precio']:.2f}", f"{p['iva']}%", p["stock"]))

    def filtrar_productos(self, event=None):
        query = self.txt_buscar.get().lower()
        filtrados = [p for p in INVENTARIO if query in p["descripcion"].lower() or query in str(p["codigo"]).lower()]
        self.cargar_productos(filtrados)

    def procesar_codigo_barras(self, event=None):
        codigo = self.txt_barcode.get().strip()
        self.txt_barcode.delete(0, tk.END)
        if not codigo:
            return

        encontrado = next((p for p in INVENTARIO if str(p["codigo"]) == codigo or str(p["codigo"]).lstrip('0') == codigo.lstrip('0')), None)
        if encontrado:
            self.agregar_item_a_carrito(encontrado)
        else:
            messagebox.showwarning("No encontrado", f"No existe el producto con código: {codigo}")

    def agregar_seleccionado_carrito(self):
        selected = self.tabla_productos.selection()
        if not selected:
            return
        item_data = self.tabla_productos.item(selected[0], "values")
        codigo_sel = str(item_data[0]).strip()
        encontrado = next((p for p in INVENTARIO if str(p["codigo"]) == codigo_sel), None)
        if encontrado:
            self.agregar_item_a_carrito(encontrado)

    def agregar_item_a_carrito(self, p):
        for item in self.cart:
            if item["codigo"] == p["codigo"]:
                item["cant"] += 1
                item["subtotal"] = item["cant"] * p["precio"]
                self.actualizar_carrito()
                return

        self.cart.append({
            "codigo": p["codigo"],
            "desc": p["descripcion"],
            "precio": p["precio"],
            "costo": p["costo"],
            "iva": p["iva"],
            "cant": 1,
            "subtotal": p["precio"]
        })
        self.actualizar_carrito()

    def quitar_item_carrito(self):
        selected = self.tabla_carrito.selection()
        if not selected:
            return
        index = self.tabla_carrito.index(selected[0])
        del self.cart[index]
        self.actualizar_carrito()

    def actualizar_carrito(self):
        self.tabla_carrito.delete(*self.tabla_carrito.get_children())
        base_imponible = 0.0
        iva_total = 0.0

        for item in self.cart:
            self.tabla_carrito.insert("", "end", values=(item["desc"], item["cant"], f"{item['precio']:.2f}€", f"{item['subtotal']:.2f}€"))
            
            sub_base = item["subtotal"] / (1 + (item["iva"] / 100.0))
            sub_iva = item["subtotal"] - sub_base
            base_imponible += sub_base
            iva_total += sub_iva

        total_general = base_imponible + iva_total
        self.total_var.set(total_general)

        self.lbl_base.config(text=f"Base Imponible: {base_imponible:.2f} €")
        self.lbl_iva_total.config(text=f"IVA Total: {iva_total:.2f} €")
        self.lbl_total_num.config(text=f"{total_general:.2f} €")
        self.calcular_cambio()

    def calcular_cambio(self, event=None):
        try:
            paga = float(self.ent_pago.get())
            cambio = paga - self.total_var.get()
            if cambio >= 0:
                self.lbl_cambio.config(text=f"{cambio:.2f} €", fg="#2563eb")
            else:
                self.lbl_cambio.config(text="Falta dinero", fg="red")
        except ValueError:
            self.lbl_cambio.config(text="0.00 €", fg="#2563eb")

    def completar_venta(self, es_factura=False):
        global CAJA_ABIERTA
        if not CAJA_ABIERTA:
            messagebox.showwarning("Caja Cerrada", "Debe realizar la Apertura de Caja antes de realizar ventas.")
            self.gestion_caja()
            return

        total_venta = self.total_var.get()
        try:
            paga = float(self.ent_pago.get()) if self.ent_pago.get() else total_venta
        except ValueError:
            paga = total_venta

        cambio = max(0.0, paga - total_venta)

        datos_cliente = {}
        conceptos_libres = ""

        if es_factura:
            win_factura = tk.Toplevel(self.root)
            win_factura.title("Datos Factura Nominativa y Conceptos")
            win_factura.geometry("520x540")
            win_factura.grab_set()
            win_factura.lift()
            win_factura.focus_force()

            tk.Label(win_factura, text="📄 Datos Fiscales y Conceptos de Factura", font=("Segoe UI", 13, "bold"), fg="#1e293b").pack(pady=15)
            
            f_cont = tk.Frame(win_factura, padx=20)
            f_cont.pack(fill="both", expand=True)

            tk.Label(f_cont, text="Nombre del Cliente Completo:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=3)
            ent_nom_cli = tk.Entry(f_cont, width=45, font=("Segoe UI", 11))
            ent_nom_cli.pack(anchor="w", pady=3)

            tk.Label(f_cont, text="DNI / NIE / Pasaporte / NIF:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=3)
            ent_doc_cli = tk.Entry(f_cont, width=45, font=("Segoe UI", 11))
            ent_doc_cli.pack(anchor="w", pady=3)

            tk.Label(f_cont, text="Nombre de la Empresa Destino:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=3)
            ent_emp_cli = tk.Entry(f_cont, width=45, font=("Segoe UI", 11))
            ent_emp_cli.pack(anchor="w", pady=3)
            ent_emp_cli.insert(0, DATOS_EMPRESA_DEFECTO["nombre_empresa"])

            tk.Label(f_cont, text="Dirección Fiscal / NIF Empresa:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=3)
            ent_dir_cli = tk.Entry(f_cont, width=45, font=("Segoe UI", 11))
            ent_dir_cli.pack(anchor="w", pady=3)
            ent_dir_cli.insert(0, f"{DATOS_EMPRESA_DEFECTO['direccion_empresa']} - NIF: {DATOS_EMPRESA_DEFECTO['nif_empresa']}")

            tk.Label(f_cont, text="Conceptos Vendidos Personalizados (Ej: 4 menú a 10.00€):", font=("Segoe UI", 11, "bold"), fg="#2563eb").pack(anchor="w", pady=(10,3))
            ent_conceptos = tk.Entry(f_cont, width=45, font=("Segoe UI", 11))
            ent_conceptos.pack(anchor="w", pady=3)
            ent_conceptos.insert(0, "4 Menús a precio acordado")

            def confirmar_datos():
                nonlocal conceptos_libres
                datos_cliente["nombre_cliente"] = ent_nom_cli.get().strip()
                datos_cliente["doc_cliente"] = ent_doc_cli.get().strip()
                datos_cliente["empresa_cliente"] = ent_emp_cli.get().strip()
                datos_cliente["direccion_cliente"] = ent_dir_cli.get().strip()
                conceptos_libres = ent_conceptos.get().strip()
                win_factura.destroy()

            tk.Button(win_factura, text="✅ Generar Factura Oficial", bg="#16a34a", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2", command=confirmar_datos, width=28, pady=10).pack(pady=20)
            self.root.wait_window(win_factura)

        costo_total_venta = sum(item["costo"] * item["cant"] for item in self.cart)
        base_imp_total = sum((item["subtotal"] / (1 + item["iva"]/100.0)) for item in self.cart)
        ganancia_venta = base_imp_total - costo_total_venta

        num_ticket_aleatorio = f"01T126{random.randint(1000000000, 9999999999)}"

        fecha_ahora = datetime.now()
        registro_venta = {
            "fecha": fecha_ahora,
            "num_ticket": num_ticket_aleatorio,
            "total": total_venta,
            "ganancia": ganancia_venta,
            "items": list(self.cart),
            "tipo": "FACTURA" if es_factura else "TICKET",
            "cliente": datos_cliente if es_factura else None,
            "conceptos_libres": conceptos_libres if es_factura else ""
        }
        HISTORIAL_VENTAS.append(registro_venta)

        for item in self.cart:
            for p in INVENTARIO:
                if p["codigo"] == item["codigo"]:
                    p["stock"] = max(0.0, p["stock"] - item["cant"])

        self.imprimir_documento(registro_venta, paga, cambio)

        messagebox.showinfo("¡Operación Exitosa!", f"Documento procesado con éxito.\nTotal: {total_venta:.2f} €\nGanancia obtenida: {ganancia_venta:.2f} €")
        
        self.cart = []
        self.ent_pago.delete(0, tk.END)
        self.actualizar_carrito()
        self.cargar_productos(INVENTARIO)
        self.txt_barcode.focus()

    def imprimir_documento(self, venta, paga, cambio):
        doc_texto = "             MULTI SERVICIOS RAMIREZ            \n"
        doc_texto += "             AVDA. DR. FLEMING 9                \n"
        doc_texto += "             24009 LEON ESPANA                  \n\n"
        doc_texto += "Telf  655766134      NIF  02799425-A\n\n"
        
        if venta["tipo"] == "FACTURA" and venta.get("cliente"):
            cli = venta["cliente"]
            doc_texto += "========================================\n"
            doc_texto += "            FACTURA NOMINATIVA          \n"
            doc_texto += f"Cliente: {cli.get('nombre_cliente', '')}\n"
            doc_texto += f"Doc ID: {cli.get('doc_cliente', '')}\n"
            doc_texto += f"Empresa: {cli.get('empresa_cliente', '')}\n"
            doc_texto += f"Dirección: {cli.get('direccion_cliente', '')}\n"
            
            if venta.get("conceptos_libres"):
                doc_texto += f"Conceptos: {venta.get('conceptos_libres')}\n"
            
            doc_texto += "========================================\n\n"

        doc_texto += f"Ticket Nº {venta['num_ticket']}               {venta['fecha'].strftime('%d/%m/%Y')}\n"
        doc_texto += f"                                           {venta['fecha'].strftime('%H:%M')}\n\n"
        doc_texto += "UDS. ARTÍCULO                       PRECIO             IMPORTE\n"
        doc_texto += "--------------------------------------------------------------\n"
        
        if not venta["items"]:
            doc_texto += " (Factura emitida con conceptos personalizados)               \n"
        
        for item in venta["items"]:
            desc = item['desc'][:32].ljust(32)
            cant_str = f"{item['cant']:.2f}"[:6].rjust(6)
            precio_str = f"{item['precio']:.2f}€".rjust(8)
            import_str = f"{item['subtotal']:.2f}€".rjust(8)
            doc_texto += f"{cant_str} {desc}\n"
            doc_texto += f"{'':>35} {precio_str} {import_str}\n"

        doc_texto += "--------------------------------------------------------------\n"
        doc_texto += f"                         TOTAL               {venta['total']:.2f}€\n"
        doc_texto += "--------------------------------------------------------------\n"
        doc_texto += "      BASE IMPONIBLE              %IVA                     IVA\n"

        ivas_dict = {}
        for item in venta["items"]:
            iva_val = float(item["iva"])
            sub_b = item["subtotal"] / (1 + (iva_val / 100.0))
            sub_i = item["subtotal"] - sub_b
            if iva_val not in ivas_dict:
                ivas_dict[iva_val] = {"base": 0.0, "iva": 0.0}
            ivas_dict[iva_val]["base"] += sub_b
            ivas_dict[iva_val]["iva"] += sub_i

        for iva_pct, vals in ivas_dict.items():
            b_str = f"{vals['base']:.2f}€".rjust(15)
            p_str = f"{iva_pct:.1f}".rjust(15)
            i_str = f"{vals['iva']:.2f}€".rjust(15)
            doc_texto += f"{b_str} {p_str} {i_str}\n"

        doc_texto += "\n--------------------------------------------------------------\n"
        doc_texto += f"ENTREGADO                 {paga:.2f}€CAMBIO                   {cambio:.2f}€\n"
        doc_texto += "EFECTIVO\n"
        doc_texto += "--------------------------------------------------------------\n"
        doc_texto += f"LE ATENDIÓ {self.nombre_operador.upper()}\n"
        doc_texto += "DATOS DE LA EMPRESA EMISORA:\n"
        doc_texto += f"{DATOS_EMPRESA_DEFECTO['nombre_empresa']} - {DATOS_EMPRESA_DEFECTO['nif_empresa']}\n"
        doc_texto += f"{DATOS_EMPRESA_DEFECTO['direccion_empresa']}\n"
        doc_texto += "GRACIAS POR SU COMPRA. ES IMPRESCINDIBLE LA\n"
        doc_texto += "PRESENTACION DEL TICKET PARA CUALQUIER DEVOLUCION\n\n\n\n"

        filename = tempfile.mktemp(".txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc_texto)
        try:
            os.startfile(filename, "print")
        except Exception:
            pass

    def gestion_caja(self):
        global CAJA_ABIERTA, TOTAL_CAJA_INICIAL
        win_caja = tk.Toplevel(self.root)
        win_caja.title("Gestión de Apertura y Cierre de Caja")
        win_caja.geometry("440x380")
        win_caja.grab_set()
        win_caja.lift()
        win_caja.focus_force()

        tk.Label(win_caja, text="💵 Control de Caja Registradora", font=("Segoe UI", 14, "bold")).pack(pady=20)

        estado_txt = "ESTADO: ABIERTA 🟢" if CAJA_ABIERTA else "ESTADO: CERRADA 🔴"
        lbl_estado = tk.Label(win_caja, text=estado_txt, font=("Segoe UI", 12, "bold"), fg="green" if CAJA_ABIERTA else "red")
        lbl_estado.pack(pady=8)

        def abrir_caja_accion():
            global CAJA_ABIERTA, TOTAL_CAJA_INICIAL
            fondo = simpledialog.askfloat("Apertura", "Ingrese fondo inicial de caja (€):", parent=win_caja)
            if fondo is not None:
                CAJA_ABIERTA = True
                TOTAL_CAJA_INICIAL = fondo
                messagebox.showinfo("Caja", f"Caja abierta correctamente con fondo de {fondo:.2f} €")
                win_caja.destroy()

        def cerrar_caja_accion():
            global CAJA_ABIERTA
            if not CAJA_ABIERTA:
                messagebox.showwarning("Atención", "La caja ya se encuentra cerrada.")
                return

            hoy = datetime.now().date()
            ventas_hoy = [v for v in HISTORIAL_VENTAS if v["fecha"].date() == hoy]
            total_vendido = sum(v["total"] for v in ventas_hoy)
            ganancia_total = sum(v["ganancia"] for v in ventas_hoy)

            ticket_cierre = "========================================\n"
            ticket_cierre += "         CIERRE DE CAJA DIARIO          \n"
            ticket_cierre += "         Multi Servicios Ramírez        \n"
            ticket_cierre += f"         Fecha: {hoy.strftime('%d/%m/%Y')}          \n"
            ticket_cierre += "========================================\n"
            ticket_cierre += f"Operador: {self.nombre_operador}\n"
            ticket_cierre += f"Fondo Inicial: {TOTAL_CAJA_INICIAL:.2f} €\n"
            ticket_cierre += f"Total de Ventas: {total_vendido:.2f} €\n"
            ticket_cierre += f"Ganancia Neta Obtenida: {ganancia_total:.2f} €\n"
            ticket_cierre += "========================================\n"
            ticket_cierre += "       CIERRE REALIZADO CON ÉXITO       \n\n\n\n"

            filename = tempfile.mktemp(".txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(ticket_cierre)
            try:
                os.startfile(filename, "print")
            except Exception:
                pass

            CAJA_ABIERTA = False
            messagebox.showinfo("Cierre de Caja", f"Caja cerrada con éxito.\nVentas Totales: {total_vendido:.2f} €\nGanancia: {ganancia_total:.2f} €\nImprimiendo reporte...")
            win_caja.destroy()

        tk.Button(win_caja, text="🟢 Abrir Caja", font=("Segoe UI", 12, "bold"), bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white", relief="flat", cursor="hand2", width=24, command=abrir_caja_accion).pack(pady=10)
        tk.Button(win_caja, text="🔴 Cerrar Caja e Imprimir Reporte", font=("Segoe UI", 12, "bold"), bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white", relief="flat", cursor="hand2", width=28, command=cerrar_caja_accion).pack(pady=10)

    def ver_ranking_productos(self):
        win_rank = tk.Toplevel(self.root)
        win_rank.title("Top Ventas y Productos Menos Vendidos (Ofertas)")
        win_rank.geometry("860x560")
        win_rank.grab_set()
        win_rank.lift()
        win_rank.focus_force()

        notebook_rank = ttk.Notebook(win_rank)
        notebook_rank.pack(fill="both", expand=True, padx=12, pady=12)

        tab_top = tk.Frame(notebook_rank, bg="white")
        notebook_rank.add(tab_top, text="🔥 Productos Top Ventas")

        tk.Label(tab_top, text="Productos más demandados por tus clientes", font=("Segoe UI", 12, "bold"), bg="white", fg="#1e293b").pack(pady=12)

        cols_rank = ("codigo", "descripcion", "vendidos", "ingresos")
        t_top = ttk.Treeview(tab_top, columns=cols_rank, show="headings", height=14)
        t_top.heading("codigo", text="Código")
        t_top.heading("descripcion", text="Descripción")
        t_top.heading("vendidos", text="Unidades Vendidas")
        t_top.heading("ingresos", text="Ingresos Totales (€)")
        t_top.pack(fill="both", expand=True, padx=12, pady=8)

        tab_low = tk.Frame(notebook_rank, bg="white")
        notebook_rank.add(tab_low, text="📉 Productos Menos Vendidos (Para Ofertas)")

        tk.Label(tab_low, text="Artículos con menor salida (ideales para liquidación u ofertas)", font=("Segoe UI", 12, "bold"), bg="white", fg="#b91c1c").pack(pady=12)

        t_low = ttk.Treeview(tab_low, columns=cols_rank, show="headings", height=14)
        t_low.heading("codigo", text="Código")
        t_low.heading("descripcion", text="Descripción")
        t_low.heading("vendidos", text="Unidades Vendidas")
        t_low.heading("ingresos", text="Ingresos Totales (€)")
        t_low.pack(fill="both", expand=True, padx=12, pady=8)

        conteo_ventas = {}
        for p in INVENTARIO:
            conteo_ventas[p["codigo"]] = {"descripcion": p["descripcion"], "cant": 0.0, "ingresos": 0.0}

        for v in HISTORIAL_VENTAS:
            for item in v["items"]:
                cod = item["codigo"]
                if cod in conteo_ventas:
                    conteo_ventas[cod]["cant"] += item["cant"]
                    conteo_ventas[cod]["ingresos"] += item["subtotal"]

        lista_ordenada = sorted(conteo_ventas.items(), key=lambda x: x[1]["cant"], reverse=True)
        for cod, info in lista_ordenada:
            t_top.insert("", "end", values=(cod, info["descripcion"], f"{info['cant']:.2f}", f"{info['ingresos']:.2f} €"))

        lista_inversa = sorted(conteo_ventas.items(), key=lambda x: x[1]["cant"])
        for cod, info in lista_inversa:
            t_low.insert("", "end", values=(cod, info["descripcion"], f"{info['cant']:.2f}", f"{info['ingresos']:.2f} €"))

    def ver_historico_ventas(self):
        win_hist = tk.Toplevel(self.root)
        win_hist.title("Buscador de Ventas por Días, Meses y Años")
        win_hist.geometry("820x540")
        win_hist.grab_set()
        win_hist.lift()
        win_hist.focus_force()

        tk.Label(win_hist, text="📊 Historial de Ventas y Rendimiento", font=("Segoe UI", 14, "bold")).pack(pady=15)

        f_filtros = tk.Frame(win_hist)
        f_filtros.pack(pady=8)

        tk.Label(f_filtros, text="Filtrar por (DD/MM/AAAA o Mes MM o Año AAAA):", font=("Segoe UI", 11)).pack(side="left", padx=6)
        ent_filtro = tk.Entry(f_filtros, font=("Segoe UI", 11), width=16)
        ent_filtro.pack(side="left", padx=6)

        cols = ("fecha", "tipo", "total", "ganancia")
        tabla_hist = ttk.Treeview(win_hist, columns=cols, show="headings", height=16)
        tabla_hist.heading("fecha", text="Fecha y Hora")
        tabla_hist.heading("tipo", text="Tipo")
        tabla_hist.heading("total", text="Total Venta (€)")
        tabla_hist.heading("ganancia", text="Ganancia Neta (€)")
        tabla_hist.pack(fill="both", expand=True, padx=20, pady=12)

        def actualizar_tabla(lista):
            tabla_hist.delete(*tabla_hist.get_children())
            t_sum = 0.0
            g_sum = 0.0
            for v in lista:
                tabla_hist.insert("", "end", values=(v["fecha"].strftime('%d/%m/%Y %H:%M'), v["tipo"], f"{v['total']:.2f} €", f"{v['ganancia']:.2f} €"))
                t_sum += v["total"]
                g_sum += v["ganancia"]
            lbl_resumen.config(text=f"Total Ventas: {t_sum:.2f} €  |  Ganancia Total: {g_sum:.2f} €")

        def buscar():
            q = ent_filtro.get().strip()
            if not q:
                actualizar_tabla(HISTORIAL_VENTAS)
                return
            filtrados = [v for v in HISTORIAL_VENTAS if q in v["fecha"].strftime('%d/%m/%Y') or q in v["fecha"].strftime('%m') or q in v["fecha"].strftime('%Y')]
            actualizar_tabla(filtrados)

        tk.Button(f_filtros, text="Buscar", font=("Segoe UI", 11, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", cursor="hand2", padx=12, command=buscar).pack(side="left", padx=6)

        lbl_resumen = tk.Label(win_hist, text="Total Ventas: 0.00 €  |  Ganancia Total: 0.00 €", font=("Segoe UI", 12, "bold"), fg="#16a34a")
        lbl_resumen.pack(pady=12)

        actualizar_tabla(HISTORIAL_VENTAS)

    def ver_lista_compras(self):
        win_compras = tk.Toplevel(self.root)
        win_compras.title("Lista Privada de Productos a Comprar (Reposición)")
        win_compras.geometry("720x440")
        win_compras.grab_set()
        win_compras.lift()
        win_compras.focus_force()

        tk.Label(win_compras, text="🛒 Productos con Stock Bajo / Sugerencia de Compra", font=("Segoe UI", 14, "bold")).pack(pady=15)

        cols = ("codigo", "descripcion", "stock", "costo")
        tabla_c = ttk.Treeview(win_compras, columns=cols, show="headings", height=13)
        tabla_c.heading("codigo", text="Código")
        tabla_c.heading("descripcion", text="Descripción")
        tabla_c.heading("stock", text="Stock Actual")
        tabla_c.heading("costo", text="Costo Est. (€)")
        tabla_c.pack(fill="both", expand=True, padx=20, pady=8)

        faltantes = [p for p in INVENTARIO if p["stock"] <= 5.0]
        for p in faltantes:
            tabla_c.insert("", "end", values=(p["codigo"], p["descripcion"], p["stock"], f"{p.get('costo', 0.0):.2f} €"))

        tk.Label(win_compras, text="💡 Estos productos tienen stock bajo y necesitan reposición en almacén.", font=("Segoe UI", 10, "italic"), fg="#64748b").pack(pady=12)

    def abrir_configuracion(self):
        if self.rol_actual != "admin":
            messagebox.showerror("Acceso Denegado", "Solo el Administrador puede entrar a Configuración.")
            return

        win_conf = tk.Toplevel(self.root)
        win_conf.title("Configuración General, Inventario y Caducidades")
        win_conf.geometry("1020x720")
        win_conf.grab_set()
        win_conf.lift()
        win_conf.focus_force()

        notebook = ttk.Notebook(win_conf)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        tab_inv = tk.Frame(notebook, bg="white")
        notebook.add(tab_inv, text="📦 Inventario, Costos, IVA y Caducidad")

        f_form = tk.Frame(tab_inv, bg="white", padx=12, pady=12)
        f_form.pack(fill="x")

        tk.Label(f_form, text="Código:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, sticky="w", pady=4)
        e_cod = tk.Entry(f_form, font=("Segoe UI", 11), width=22)
        e_cod.grid(row=0, column=1, pady=4)

        tk.Label(f_form, text="Descripción:", font=("Segoe UI", 11), bg="white").grid(row=1, column=0, sticky="w", pady=4)
        e_desc = tk.Entry(f_form, font=("Segoe UI", 11), width=34)
        e_desc.grid(row=1, column=1, pady=4)

        tk.Label(f_form, text="Costo (€):", font=("Segoe UI", 11), bg="white").grid(row=2, column=0, sticky="w", pady=4)
        e_costo = tk.Entry(f_form, font=("Segoe UI", 11), width=16)
        e_costo.grid(row=2, column=1, pady=4)

        tk.Label(f_form, text="P. Venta (€):", font=("Segoe UI", 11), bg="white").grid(row=3, column=0, sticky="w", pady=4)
        e_precio = tk.Entry(f_form, font=("Segoe UI", 11), width=16)
        e_precio.grid(row=3, column=1, pady=4)

        tk.Label(f_form, text="IVA Selectivo:", font=("Segoe UI", 11), bg="white").grid(row=4, column=0, sticky="w", pady=4)
        combo_iva = ttk.Combobox(f_form, values=[21, 10, 4], width=14, state="readonly")
        combo_iva.grid(row=4, column=1, pady=4)
        combo_iva.set(21)

        tk.Label(f_form, text="Stock:", font=("Segoe UI", 11), bg="white").grid(row=5, column=0, sticky="w", pady=4)
        e_stock = tk.Entry(f_form, font=("Segoe UI", 11), width=16)
        e_stock.grid(row=5, column=1, pady=4)

        tk.Label(f_form, text="Caducidad (DD/MM/AAAA):", font=("Segoe UI", 11), bg="white").grid(row=6, column=0, sticky="w", pady=4)
        e_cad = tk.Entry(f_form, font=("Segoe UI", 11), width=16)
        e_cad.grid(row=6, column=1, pady=4)
        e_cad.insert(0, "31/12/2026")

        cols_conf = ("codigo", "desc", "costo", "precio", "iva", "stock", "cad")
        t_conf = ttk.Treeview(tab_inv, columns=cols_conf, show="headings", height=11)
        t_conf.heading("codigo", text="Código")
        t_conf.heading("desc", text="Descripción")
        t_conf.heading("costo", text="Costo")
        t_conf.heading("precio", text="P. Venta")
        t_conf.heading("iva", text="IVA")
        t_conf.heading("stock", text="Stock")
        t_conf.heading("cad", text="Caducidad (DD/MM/AAAA)")
        t_conf.pack(fill="both", expand=True, padx=12, pady=6)

        def actualizar_t_conf():
            t_conf.delete(*t_conf.get_children())
            for p in INVENTARIO:
                t_conf.insert("", "end", values=(p["codigo"], p["descripcion"], f"{p.get('costo', 0):.2f}", f"{p['precio']:.2f}", f"{p['iva']}%", p["stock"], p.get("caducidad", "N/D")))

        actualizar_t_conf()

        def seleccionar_item_tabla(event):
            selected = t_conf.selection()
            if not selected:
                return
            item_vals = t_conf.item(selected[0], "values")
            cod = item_vals[0]
            prod = next((p for p in INVENTARIO if p["codigo"] == cod), None)
            if prod:
                e_cod.delete(0, tk.END)
                e_cod.insert(0, prod["codigo"])
                e_desc.delete(0, tk.END)
                e_desc.insert(0, prod["descripcion"])
                e_costo.delete(0, tk.END)
                e_costo.insert(0, str(prod.get("costo", 0)))
                e_precio.delete(0, tk.END)
                e_precio.insert(0, str(prod["precio"]))
                combo_iva.set(str(prod["iva"]))
                e_stock.delete(0, tk.END)
                e_stock.insert(0, str(prod["stock"]))
                e_cad.delete(0, tk.END)
                e_cad.insert(0, str(prod.get("caducidad", "")))

        t_conf.bind("<ButtonRelease-1>", seleccionar_item_tabla)

        def guardar_producto_admin():
            cod = e_cod.get().strip()
            desc = e_desc.get().strip()
            cad = e_cad.get().strip()
            
            if cad:
                try:
                    datetime.strptime(cad, "%d/%m/%Y")
                except ValueError:
                    messagebox.showerror("Error de Formato", "La fecha de caducidad debe tener el formato DD/MM/AAAA (ej. 31/12/2026).")
                    return

            try:
                costo = float(e_costo.get().strip() or 0)
                precio = float(e_precio.get().strip() or 0)
                iva = int(combo_iva.get())
                stock = float(e_stock.get().strip() or 0)
            except ValueError:
                messagebox.showerror("Error", "Valores numéricos inválidos.")
                return

            if not cod or not desc or precio <= 0:
                messagebox.showerror("Error", "Rellene código, descripción y precio de venta.")
                return

            existente = next((p for p in INVENTARIO if p["codigo"] == cod), None)
            if existente:
                existente["descripcion"] = desc
                existente["costo"] = costo
                existente["precio"] = precio
                existente["iva"] = iva
                existente["stock"] = stock
                existente["caducidad"] = cad
                messagebox.showinfo("Actualizado", "Producto actualizado correctamente.")
            else:
                INVENTARIO.append({"codigo": cod, "descripcion": desc, "costo": costo, "precio": precio, "iva": iva, "stock": stock, "caducidad": cad})
                messagebox.showinfo("Guardado", "Nuevo producto agregado al inventario.")

            actualizar_t_conf()
            self.cargar_productos(INVENTARIO)

        tk.Button(f_form, text="💾 Guardar / Actualizar Producto", bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2", command=guardar_producto_admin).grid(row=7, column=0, columnspan=2, pady=12)

        tab_usr = tk.Frame(notebook, bg="white")
        notebook.add(tab_usr, text="🔑 Usuarios, Nombres y Claves")

        tk.Label(tab_usr, text="Gestión de Administradores y Empleados", font=("Segoe UI", 13, "bold"), bg="white").pack(pady=20)

        f_usr = tk.Frame(tab_usr, bg="white", padx=24)
        f_usr.pack(fill="x")

        tk.Label(f_usr, text="Seleccionar Usuario:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, sticky="w", pady=8)
        combo_usr = ttk.Combobox(f_usr, values=list(USUARIOS.keys()), state="readonly", width=18, font=("Segoe UI", 11))
        combo_usr.grid(row=0, column=1, pady=8)
        combo_usr.set("admin")

        tk.Label(f_usr, text="Nombre Completo:", font=("Segoe UI", 11), bg="white").grid(row=1, column=0, sticky="w", pady=8)
        e_nom_usr = tk.Entry(f_usr, font=("Segoe UI", 11), width=28)
        e_nom_usr.grid(row=1, column=1, pady=8)

        tk.Label(f_usr, text="Nueva Contraseña:", font=("Segoe UI", 11), bg="white").grid(row=2, column=0, sticky="w", pady=8)
        e_pass_usr = tk.Entry(f_usr, font=("Segoe UI", 11), width=28, show="*")
        e_pass_usr.grid(row=2, column=1, pady=8)

        def cargar_datos_usr(event=None):
            u = combo_usr.get()
            if u in USUARIOS:
                e_nom_usr.delete(0, tk.END)
                e_nom_usr.insert(0, USUARIOS[u]["nombre"])
                e_pass_usr.delete(0, tk.END)
                e_pass_usr.insert(0, USUARIOS[u]["password"])

        combo_usr.bind("<<ComboboxSelected>>", cargar_datos_usr)
        cargar_datos_usr()

        def guardar_cambios_usr():
            u = combo_usr.get()
            nuevo_nombre = e_nom_usr.get().strip()
            nueva_pass = e_pass_usr.get().strip()
            if not nuevo_nombre or not nueva_pass:
                messagebox.showerror("Error", "Rellene todos los campos.")
                return
            USUARIOS[u]["nombre"] = nuevo_nombre
            USUARIOS[u]["password"] = nueva_pass
            messagebox.showinfo("Éxito", f"Datos del usuario '{u}' actualizados correctamente.")

        tk.Button(tab_usr, text="💾 Actualizar Credenciales y Nombres", bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2", command=guardar_cambios_usr).pack(pady=25)

TPVMultiServicios = TPVApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TPVApp(root)
    root.mainloop()
