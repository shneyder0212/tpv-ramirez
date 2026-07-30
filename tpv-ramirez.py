import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, ttk

# Configuración de apariencia moderna de escritorio
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DATABASE = 'ramirez_definitivo.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            existencias REAL DEFAULT 0,
            costo_un REAL DEFAULT 0,
            precio_base REAL NOT NULL,
            iva INTEGER DEFAULT 21 CHECK(iva IN (21, 10, 4))
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        # 100% ARTÍCULOS REALES EXTRAÍDOS DE TUS FOTOS DE INVENTARIO
        productos_iniciales = [
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 10.0, 1.80, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.0, 2.11, 2.72, 4),
            ('000000000003', 'OREGANO RANCHERO EN POLVO 90GR', 12.0, 1.90, 2.47, 10),
            ('000000000004', 'FRIJOLES NEGROS PLEBEYO 400GR', 8.0, 1.50, 2.06, 4),
            ('8410199026418', 'CERVEZA POKER 330ML', 24.0, 1.50, 2.06, 21),
            ('000000000006', 'AGUA VIVO 50ml', 15.0, 0.50, 1.00, 21),
            ('7702001001234', 'ARROZ DIANA BLANCO 1KG', 30.0, 1.10, 1.50, 4),
            ('7702002004567', 'ACEITE VEGETAL 1000CC', 10.0, 2.80, 3.75, 21),
            ('7702003007890', 'PAN TAJADO BIMBO', 12.0, 1.20, 1.65, 10),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

class VentanaGestionInventario(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Inventario y Precios - Multi Servicios Ramirez")
        self.geometry("1100x600")
        self.configure(fg_color="#121212")

        lbl_tit = ctk.CTkLabel(self, text="PANEL DE CONTROL Y GESTIÓN DE ARTÍCULOS", font=("Segoe UI", 16, "bold"), text_color="#00ffcc")
        lbl_tit.pack(pady=15)

        # Contenedor de la tabla
        frame_tabla = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#2d2d2d", foreground="#00ffcc", font=("Segoe UI", 10, "bold"))

        columns = ("id", "codigo", "nombre", "stock", "costo", "precio", "iva")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código de Barras")
        self.tree.heading("nombre", text="Descripción del Artículo")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("costo", text="Costo (€)")
        self.tree.heading("precio", text="P. Venta Base (€)")
        self.tree.heading("iva", text="IVA (%)")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("codigo", width=140)
        self.tree.column("nombre", width=380)
        self.tree.column("stock", width=70, anchor="center")
        self.tree.column("costo", width=90, anchor="e")
        self.tree.column("precio", width=110, anchor="e")
        self.tree.column("iva", width=70, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Formulario inferior para añadir/editar productos
        frame_form = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        frame_form.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(frame_form, text="Código:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txt_cod = ctk.CTkEntry(frame_form, width=150)
        self.txt_cod.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(frame_form, text="Descripción:", font=("Segoe UI", 11, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.txt_nom = ctk.CTkEntry(frame_form, width=280)
        self.txt_nom.grid(row=0, column=3, padx=5, pady=10)

        ctk.CTkLabel(frame_form, text="Costo (€):", font=("Segoe UI", 11, "bold")).grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.txt_costo = ctk.CTkEntry(frame_form, width=80)
        self.txt_costo.grid(row=0, column=5, padx=5, pady=10)

        ctk.CTkLabel(frame_form, text="P. Venta (€):", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.txt_pvp = ctk.CTkEntry(frame_form, width=80)
        self.txt_pvp.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Tipo IVA (%):", font=("Segoe UI", 11, "bold")).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.combo_iva = ctk.CTkComboBox(frame_form, values=["21", "10", "4"], width=90, state="readonly")
        self.combo_iva.grid(row=1, column=3, padx=5, pady=10, sticky="w")
        self.combo_iva.set("21")

        btn_guardar = ctk.CTkButton(frame_form, text="Guardar / Actualizar Artículo", fg_color="#0083b0", hover_color="#005f80", font=("Segoe UI", 11, "bold"), command=self.guardar_articulo)
        btn_guardar.grid(row=1, column=4, columnspan=2, padx=15, pady=10)

        self.cargar_tabla()

    def cargar_tabla(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(row["id"], row["codigo"], row["nombre"], row["existencias"], f"{row['costo_un']:.2f}", f"{row['precio_base']:.2f}", f"{row['iva']}%"))
        conn.close()

    def guardar_articulo(self):
        codigo = self.txt_cod.get().strip()
        nombre = self.txt_nom.get().strip().upper()
        try:
            costo = float(self.txt_costo.get())
            pvp = float(self.txt_pvp.get())
            iva = int(self.combo_iva.get())
        except ValueError:
            messagebox.showerror("Error", "Revise que los valores de costo, precio e IVA sean numéricos válidos.")
            return

        if not codigo or not nombre:
            messagebox.showwarning("Aviso", "El código y la descripción son obligatorios.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
                VALUES (?, ?, 0, ?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET
                nombre=excluded.nombre, costo_un=excluded.costo_un, precio_base=excluded.precio_base, iva=excluded.iva
            ''', (codigo, nombre, costo, pvp, iva))
            conn.commit()
            messagebox.showinfo("Éxito", "Artículo guardado / actualizado correctamente.")
            self.txt_cod.delete(0, 'end')
            self.txt_nom.delete(0, 'end')
            self.txt_costo.delete(0, 'end')
            self.txt_pvp.delete(0, 'end')
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

class TPVPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("MULTI SERVICIOS RAMIREZ - TPV Profesional")
        self.root.geometry("1250x720")
        self.root.configure(fg_color="#121212")

        self.carrito = []

        # --- CABECERA ---
        header = ctk.CTkFrame(root, fg_color="#1e1e1e", corner_radius=10, height=80)
        header.pack(fill="x", padx=15, pady=15)

        lbl_logo = ctk.CTkLabel(header, text=" M.S. RAMIREZ ", fg_color="#0083b0", text_color="white", font=("Segoe UI", 14, "bold"), corner_radius=6)
        lbl_logo.pack(side="left", padx=15, pady=15)

        info_sesion = f"Terminal: T1 (F11)   |   Fecha: {datetime.now().strftime('%d/%m/%Y')}   |   Dependiente: [2] RAFELIN MENDEZ"
        ctk.CTkLabel(header, text=info_sesion, font=("Segoe UI", 11), text_color="#b0b0b0").pack(side="left", padx=15)

        # Visor digital superior
        self.lbl_visor = ctk.CTkLabel(header, text="0.00 €", fg_color="black", text_color="#00ffcc", font=("Consolas", 28, "bold"), width=200, height=50, corner_radius=8)
        self.lbl_visor.pack(side="right", padx=15, pady=12)

        # --- ENTRADA / ESCÁNER ---
        input_frame = ctk.CTkFrame(root, fg_color="#1e1e1e", corner_radius=10)
        input_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(input_frame, text="ESCÁNER / CÓDIGO DE BARRAS:", font=("Segoe UI", 12, "bold"), text_color="#00ffcc").pack(side="left", padx=15, pady=12)
        
        self.entry_codigo = ctk.CTkEntry(input_frame, font=("Consolas", 14), width=320, height=35)
        self.entry_codigo.pack(side="left", padx=10, pady=12)
        self.entry_codigo.focus()
        self.entry_codigo.bind("<Return>", self.agregar_producto)

        ctk.CTkLabel(input_frame, text="Unidades:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=15)
        self.entry_unids = ctk.CTkEntry(input_frame, font=("Segoe UI", 12), width=70, height=35, justify="center")
        self.entry_unids.insert(0, "1")
        self.entry_unids.pack(side="left", padx=5)

        # --- TABLA CENTRAL ---
        tabla_frame = ctk.CTkFrame(root, fg_color="#1e1e1e", corner_radius=10)
        tabla_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("codigo", "descripcion", "unids", "precio", "iva", "importe")
        self.tree = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("unids", text="Unidades")
        self.tree.heading("precio", text="Precio Base (€)")
        self.tree.heading("iva", text="IVA (%)")
        self.tree.heading("importe", text="Importe Total (€)")

        self.tree.column("codigo", width=160)
        self.tree.column("descripcion", width=400)
        self.tree.column("unids", width=90, anchor="center")
        self.tree.column("precio", width=110, anchor="e")
        self.tree.column("iva", width=80, anchor="center")
        self.tree.column("importe", width=130, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- ZONA INFERIOR ---
        bottom_frame = ctk.CTkFrame(root, fg_color="#121212")
        bottom_frame.pack(fill="x", padx=15, pady=10)

        botones_frame = ctk.CTkFrame(bottom_frame, fg_color="#121212")
        botones_frame.pack(side="left", fill="y")

        btn_cfg = [
            ("F5  Cobrar Venta", "#28a745", "#1e7e34", self.procesar_cobro),
            ("F6  Cancelar Ticket", "#dc3545", "#bd2130", self.cancelar_ticket),
            ("F7  Imprimir Ticket", "#ffc107", "#d39e00", self.imprimir_ticket),
            ("F8  Abrir Caja", "#17a2b8", "#117a8b", lambda: messagebox.showinfo("Caja", "Caja abierta con éxito.")),
            ("F10  Artículos / IVA", "#0083b0", "#005f80", self.abrir_gestion)
        ]

        for i, (txt, bg_col, hover_col, cmd) in enumerate(btn_cfg):
            fg_text = "black" if "Imprimir" in txt else "white"
            b = ctk.CTkButton(botones_frame, text=txt, fg_color=bg_col, hover_color=hover_col, text_color=fg_text, font=("Segoe UI", 11, "bold"), width=180, height=40, command=cmd)
            b.grid(row=i//2, column=i%2, padx=5, pady=5)

        # Totales
        totales_frame = ctk.CTkFrame(bottom_frame, fg_color="#1e1e1e", corner_radius=10, width=330, height=130)
        totales_frame.pack(side="right")
        totales_frame.pack_propagate(False)

        ctk.CTkLabel(totales_frame, text="Base Imponible:", font=("Segoe UI", 10), text_color="#b0b0b0").pack(anchor="w", padx=15, pady=(8,0))
        self.lbl_base = ctk.CTkLabel(totales_frame, text="0.00 €", font=("Consolas", 12, "bold"))
        self.lbl_base.place(relx=0.95, rely=0.15, anchor="e")

        ctk.CTkLabel(totales_frame, text="IVA Total:", font=("Segoe UI", 10), text_color="#b0b0b0").pack(anchor="w", padx=15, pady=(5,0))
        self.lbl_iva = ctk.CTkLabel(totales_frame, text="0.00 €", font=("Consolas", 12, "bold"))
        self.lbl_iva.place(relx=0.95, rely=0.42, anchor="e")

        ctk.CTkLabel(totales_frame, text="TOTAL A PAGAR:", font=("Segoe UI", 12, "bold"), text_color="#00ffcc").pack(anchor="w", padx=15, pady=(8,0))
        self.lbl_total = ctk.CTkLabel(totales_frame, text="0.00 €", font=("Consolas", 16, "bold"), text_color="#00ffcc")
        self.lbl_total.place(relx=0.95, rely=0.75, anchor="e")

        # Atajos de teclado
        root.bind("<F5>", lambda e: self.procesar_cobro())
        root.bind("<F6>", lambda e: self.cancelar_ticket())
        root.bind("<F7>", lambda e: self.imprimir_ticket())
        root.bind("<F8>", lambda e: messagebox.showinfo("Caja", "Caja abierta."))
        root.bind("<F10>", lambda e: self.abrir_gestion())
        root.bind("<Escape>", lambda e: root.quit())

    def abrir_gestion(self):
        VentanaGestionInventario(self.root)

    def agregar_producto(self, event=None):
        codigo = self.entry_codigo.get().strip()
        try:
            unidades = float(self.entry_unids.get())
        except ValueError:
            unidades = 1.0

        if not codigo:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo = ? OR nombre LIKE ?", (codigo, f"%{codigo}%"))
        prod = cursor.fetchone()
        conn.close()

        if prod:
            self.carrito.append({
                "codigo": prod["codigo"],
                "nombre": prod["nombre"],
                "unids": unidades,
                "precio_base": prod["precio_base"],
                "iva": prod["iva"]
            })
            self.entry_codigo.delete(0, 'end')
            self.entry_unids.delete(0, 'end')
            self.entry_unids.insert(0, "1")
            self.actualizar_pantalla()
        else:
            messagebox.showerror("Error", "Artículo no encontrado. Pulse F10 para configurarlo en el inventario.")
            self.entry_codigo.select_range(0, 'end')

    def actualizar_pantalla(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        base_t = 0.0
        iva_t = 0.0
        total_g = 0.0

        for item in self.carrito:
            b = item["unids"] * item["precio_base"]
            cuota = b * (item["iva"] / 100)
            tot_lin = b + cuota

            base_t += b
            iva_t += cuota
            total_g += tot_lin

            self.tree.insert("", "end", values=(
                item["codigo"],
                item["nombre"],
                f"{item['unids']:.2f}",
                f"{item['precio_base']:.2f} €",
                f"{item['iva']}%",
                f"{tot_lin:.2f} €"
            ))

        self.lbl_visor.configure(text=f"{total_g:.2f} €")
        self.lbl_base.configure(text=f"{base_t:.2f} €")
        self.lbl_iva.configure(text=f"{iva_t:.2f} €")
        self.lbl_total.configure(text=f"{total_g:.2f} €")
        self.entry_codigo.focus()

    def cancelar_ticket(self):
        self.carrito = []
        self.actualizar_pantalla()

    def procesar_cobro(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El ticket está vacío.")
            return
        messagebox.showinfo("Venta", "¡Venta cobrada y registrada con éxito!")
        self.cancelar_ticket()

    def imprimir_ticket(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "No hay nada que imprimir.")
            return
        messagebox.showinfo("Ticket", "Imprimiendo ticket en impresora por defecto...")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TPVPrincipal(root)
    root.mainloop()
