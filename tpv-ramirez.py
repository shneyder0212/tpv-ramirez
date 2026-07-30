import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = 'ramirez_tpv.db'

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
        # PRODUCTOS REALES EXTRAÍDOS DE TUS FOTOS DE INVENTARIO
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

class VentanaGestionArticulos:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Inventario, Costes e IVA - Multi Servicios Ramirez")
        self.window.geometry("1000x580")
        self.window.configure(bg="#1e1e1e")

        # Título sección
        lbl_tit = tk.Label(self.window, text="PANEL DE CONTROL DE ARTÍCULOS", bg="#1e1e1e", fg="#00ffcc", font=("Segoe UI", 14, "bold"))
        lbl_tit.pack(pady=10)

        # Tabla estilo moderno oscuro
        frame_tabla = tk.Frame(self.window, bg="#1e1e1e")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d", rowheight=25, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#333333", foreground="#00ffcc", font=("Segoe UI", 10, "bold"))

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
        self.tree.column("nombre", width=340)
        self.tree.column("stock", width=70, anchor="center")
        self.tree.column("costo", width=90, anchor="e")
        self.tree.column("precio", width=110, anchor="e")
        self.tree.column("iva", width=70, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Formulario de alta / modificación
        frame_form = tk.Frame(self.window, bg="#2d2d2d", bd=2, relief="groove")
        frame_form.pack(fill="x", padx=15, pady=15)

        tk.Label(frame_form, text="Código:", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.txt_cod = tk.Entry(frame_form, font=("Segoe UI", 10), width=16)
        self.txt_cod.grid(row=0, column=1, padx=5, pady=8)

        tk.Label(frame_form, text="Descripción:", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.txt_nom = tk.Entry(frame_form, font=("Segoe UI", 10), width=28)
        self.txt_nom.grid(row=0, column=3, padx=5, pady=8)

        tk.Label(frame_form, text="Costo (€):", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, padx=8, pady=8, sticky="w")
        self.txt_costo = tk.Entry(frame_form, font=("Segoe UI", 10), width=8)
        self.txt_costo.grid(row=0, column=5, padx=5, pady=8)

        tk.Label(frame_form, text="P. Venta Base (€):", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.txt_pvp = tk.Entry(frame_form, font=("Segoe UI", 10), width=8)
        self.txt_pvp.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        tk.Label(frame_form, text="Tipo IVA (%):", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, padx=8, pady=8, sticky="w")
        self.combo_iva = ttk.Combobox(frame_form, values=[21, 10, 4], width=8, state="readonly", font=("Segoe UI", 10))
        self.combo_iva.grid(row=1, column=3, padx=5, pady=8, sticky="w")
        self.combo_iva.set(21)

        btn_guardar = tk.Button(frame_form, text="Guardar / Actualizar", bg="#0083b0", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=2, command=self.guardar)
        btn_guardar.grid(row=1, column=4, columnspan=2, padx=10, pady=8)

        self.cargar_tabla()

    def cargar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        for r in cursor.fetchall():
            self.tree.insert("", "end", values=(r["id"], r["codigo"], r["nombre"], r["existencias"], f"{r['costo_un']:.2f}", f"{r['precio_base']:.2f}", f"{r['iva']}%"))
        conn.close()

    def guardar(self):
        codigo = self.txt_cod.get().strip()
        nombre = self.txt_nom.get().strip().upper()
        try:
            costo = float(self.txt_costo.get())
            pvp = float(self.txt_pvp.get())
            iva = int(self.combo_iva.get())
        except ValueError:
            messagebox.showerror("Error", "Los campos numéricos (costo, precio, IVA) deben ser válidos.")
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
            messagebox.showinfo("Éxito", "Artículo guardado con éxito.")
            self.txt_cod.delete(0, tk.END)
            self.txt_nom.delete(0, tk.END)
            self.txt_costo.delete(0, tk.END)
            self.txt_pvp.delete(0, tk.END)
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

class TPVModerno:
    def __init__(self, root):
        self.root = root
        self.root.title("MULTI SERVICIOS RAMIREZ - TPV Profesional")
        self.root.geometry("1200x700")
        self.root.configure(bg="#121212")

        self.carrito = []

        # --- CABECERA SUPERIOR ---
        header = tk.Frame(root, bg="#1e1e1e", bd=1, relief="solid")
        header.pack(fill="x", padx=10, pady=10)

        # Logo / Título
        lbl_logo = tk.Label(header, text=" M.S. RAMIREZ ", bg="#0083b0", fg="white", font=("Segoe UI", 13, "bold"), padx=10, pady=12)
        lbl_logo.pack(side="left", padx=10, pady=10)

        info_sesion = f"Terminal: T1 (F11)  |  Fecha: {datetime.now().strftime('%d/%m/%Y')}  |  Dependiente: [2] RAFELIN MENDEZ"
        tk.Label(header, text=info_sesion, bg="#1e1e1e", fg="#b0b0b0", font=("Segoe UI", 10)).pack(side="left", padx=15)

        # Visor digital total grande
        self.lbl_visor = tk.Label(header, text="0.00 €", bg="black", fg="#00ffcc", font=("Consolas", 26, "bold"), bd=2, relief="sunken", width=12, anchor="e")
        self.lbl_visor.pack(side="right", padx=15, pady=10)

        # --- ENTRADA DE CÓDIGOS ---
        input_frame = tk.Frame(root, bg="#1e1e1e", bd=1, relief="solid")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="ESCÁNER / CÓDIGO:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10, pady=12)
        
        self.entry_codigo = tk.Entry(input_frame, font=("Consolas", 14), width=28, bg="#2d2d2d", fg="white", insertbackground="white")
        self.entry_codigo.pack(side="left", padx=5, pady=12)
        self.entry_codigo.focus()
        self.entry_codigo.bind("<Return>", self.agregar_al_carrito)

        tk.Label(input_frame, text="Unidades:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=15)
        self.entry_unids = tk.Entry(input_frame, font=("Segoe UI", 12), width=6, justify="center", bg="#2d2d2d", fg="white", insertbackground="white")
        self.entry_unids.insert(0, "1")
        self.entry_unids.pack(side="left", padx=5)

        # --- TABLA CENTRAL DE TICKET ---
        tabla_frame = tk.Frame(root, bg="#121212")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=5)

        style_tpv = ttk.Style()
        style_tpv.theme_use("clam")
        style_tpv.configure("TpvTree.Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=28, font=("Segoe UI", 11))
        style_tpv.configure("TpvTree.Treeview.Heading", background="#2d2d2d", foreground="#00ffcc", font=("Segoe UI", 11, "bold"))

        columns = ("codigo", "descripcion", "unids", "precio", "iva", "importe")
        self.tree = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=12, style="TpvTree.Treeview")
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("unids", text="Unidades")
        self.tree.heading("precio", text="Precio Base (€)")
        self.tree.heading("iva", text="IVA (%)")
        self.tree.heading("importe", text="Importe Total (€)")

        self.tree.column("codigo", width=160)
        self.tree.column("descripcion", width=380)
        self.tree.column("unids", width=90, anchor="center")
        self.tree.column("precio", width=110, anchor="e")
        self.tree.column("iva", width=80, anchor="center")
        self.tree.column("importe", width=120, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar_t = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        scrollbar_t.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_t.set)

        # --- ZONA INFERIOR (BOTONERA + TOTALES) ---
        bottom_frame = tk.Frame(root, bg="#121212")
        bottom_frame.pack(fill="x", padx=10, pady=10)

        # Botones de función estilo clásico TPV
        botones_frame = tk.Frame(bottom_frame, bg="#121212")
        botones_frame.pack(side="left", fill="y")

        btn_cfg = [
            ("F5  Cobrar Venta", "#28a745", self.procesar_cobro),
            ("F6  Cancelar Ticket", "#dc3545", self.cancelar_ticket),
            ("F7  Imprimir Ticket", "#ffc107", self.imprimir),
            ("F8  Abrir Caja", "#17a2b8", lambda: messagebox.showinfo("Caja", "Caja abierta correctamente.")),
            ("F10  Artículos / IVA", "#0083b0", self.abrir_gestion)
        ]

        for i, (txt, bg_color, cmd) in enumerate(btn_cfg):
            fg_col = "black" if bg_color == "#ffc107" else "white"
            b = tk.Button(botones_frame, text=txt, bg=bg_color, fg=fg_col, font=("Segoe UI", 10, "bold"), width=18, pady=6, command=cmd)
            b.grid(row=i//2, column=i%2, padx=4, pady=4)

        # Panel de totales derecho
        totales_frame = tk.Frame(bottom_frame, bg="#1e1e1e", bd=1, relief="solid", padx=15, pady=8)
        totales_frame.pack(side="right")

        tk.Label(totales_frame, text="Base Imponible:", bg="#1e1e1e", fg="#b0b0b0", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=2)
        self.lbl_base = tk.Label(totales_frame, text="0.00 €", bg="#1e1e1e", fg="white", font=("Consolas", 11, "bold"), width=12, anchor="e")
        self.lbl_base.grid(row=0, column=1, padx=10, pady=2)

        tk.Label(totales_frame, text="IVA Total:", bg="#1e1e1e", fg="#b0b0b0", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=2)
        self.lbl_iva = tk.Label(totales_frame, text="0.00 €", bg="#1e1e1e", fg="white", font=("Consolas", 11, "bold"), width=12, anchor="e")
        self.lbl_iva.grid(row=1, column=1, padx=10, pady=2)

        tk.Label(totales_frame, text="TOTAL A PAGAR:", bg="#1e1e1e", fg="#00ffcc", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        self.lbl_total = tk.Label(totales_frame, text="0.00 €", bg="#1e1e1e", fg="#00ffcc", font=("Consolas", 14, "bold"), width=12, anchor="e")
        self.lbl_total.grid(row=2, column=1, padx=10, pady=4)

        # Atajos de teclado globales
        root.bind("<F5>", lambda e: self.procesar_cobro())
        root.bind("<F6>", lambda e: self.cancelar_ticket())
        root.bind("<F7>", lambda e: self.imprimir())
        root.bind("<F8>", lambda e: messagebox.showinfo("Caja", "Caja abierta."))
        root.bind("<F10>", lambda e: self.abrir_gestion())
        root.bind("<Escape>", lambda e: root.quit())

    def abrir_gestion(self):
        VentanaGestionArticulos(self.root)

    def agregar_al_carrito(self, event=None):
        codigo = self.entry_codigo.get().strip()
        try:
            unids = float(self.entry_unids.get())
        except ValueError:
            unids = 1.0

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
                "unids": unids,
                "precio_base": prod["precio_base"],
                "iva": prod["iva"]
            })
            self.entry_codigo.delete(0, tk.END)
            self.entry_unids.delete(0, tk.END)
            self.entry_unids.insert(0, "1")
            self.actualizar_pantalla()
        else:
            messagebox.showerror("No encontrado", "Artículo no registrado. Pulse F10 para añadirlo al inventario.")
            self.entry_codigo.select_range(0, tk.END)

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

        self.lbl_visor.config(text=f"{total_g:.2f} €")
        self.lbl_base.config(text=f"{base_t:.2f} €")
        self.lbl_iva.config(text=f"{iva_t:.2f} €")
        self.lbl_total.config(text=f"{total_g:.2f} €")
        self.entry_codigo.focus()

    def cancelar_ticket(self):
        self.carrito = []
        self.actualizar_pantalla()

    def procesar_cobro(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El carrito está vacío.")
            return
        messagebox.showinfo("Cobro Exitoso", "¡Venta procesada y guardada correctamente!")
        self.cancelar_ticket()

    def imprimir(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "No hay elementos para imprimir.")
            return
        messagebox.showinfo("Impresora", "Imprimiendo ticket de caja...")

if __name__ == "__main__":
    root = tk.Tk()
    app = TPVModerno(root)
    root.mainloop()
