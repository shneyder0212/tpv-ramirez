import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = 'tienda.db'

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
        productos_iniciales = [
            ('000000000006', 'AGUA VIVO 50ml', 10.00, 0.50, 1.00, 21),
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 0.00, 0.00, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.00, 2.11, 2.72, 4),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

class GestionInventarioWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Artículos, Costos e IVA - Multi Servicios Ramirez")
        self.window.geometry("900x500")
        self.window.configure(bg="#dcdcdc")
        
        # Tabla de productos
        frame_tabla = tk.Frame(self.window, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "codigo", "nombre", "stock", "costo", "precio_base", "iva")
        self.tree_inv = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        
        self.tree_inv.heading("id", text="ID")
        self.tree_inv.heading("codigo", text="Código")
        self.tree_inv.heading("nombre", text="Descripción")
        self.tree_inv.heading("stock", text="Stock")
        self.tree_inv.heading("costo", text="Costo (€)")
        self.tree_inv.heading("precio_base", text="P. Venta Base (€)")
        self.tree_inv.heading("iva", text="IVA (%)")

        self.tree_inv.column("id", width=40, anchor="center")
        self.tree_inv.column("codigo", width=120)
        self.tree_inv.column("nombre", width=300)
        self.tree_inv.column("stock", width=70, anchor="center")
        self.tree_inv.column("costo", width=90, anchor="e")
        self.tree_inv.column("precio_base", width=110, anchor="e")
        self.tree_inv.column("iva", width=60, anchor="center")

        self.tree_inv.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_inv.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_inv.configure(yscrollcommand=scrollbar.set)

        # Panel de formulario abajo para añadir/editar
        frame_form = tk.Frame(self.window, bg="#ececec", bd=2, relief="groove")
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="Código:", bg="#ececec", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.txt_cod = tk.Entry(frame_form, width=15)
        self.txt_cod.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Descripción:", bg="#ececec", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.txt_nom = tk.Entry(frame_form, width=25)
        self.txt_nom.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Costo (€):", bg="#ececec", font=("Arial", 9, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.txt_costo = tk.Entry(frame_form, width=8)
        self.txt_costo.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame_form, text="P. Venta (€):", bg="#ececec", font=("Arial", 9, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.txt_pvp = tk.Entry(frame_form, width=8)
        self.txt_pvp.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="IVA (%):", bg="#ececec", font=("Arial", 9, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_iva = ttk.Combobox(frame_form, values=[21, 10, 4], width=6, state="readonly")
        self.combo_iva.grid(row=1, column=3, padx=5, pady=5)
        self.combo_iva.set(21)

        tk.Button(frame_form, text="Guardar / Añadir Producto", bg="#b5651d", fg="white", font=("Arial", 9, "bold"), command=self.guardar_producto).grid(row=1, column=4, columnspan=2, padx=10, pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree_inv.get_children():
            self.tree_inv.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        for row in cursor.fetchall():
            self.tree_inv.insert("", "end", values=(row["id"], row["codigo"], row["nombre"], row["existencias"], f"{row['costo_un']:.2f}", f"{row['precio_base']:.2f}", f"{row['iva']}%"))
        conn.close()

    def guardar_producto(self):
        codigo = self.txt_cod.get().strip()
        nombre = self.txt_nom.get().strip().upper()
        try:
            costo = float(self.txt_costo.get())
            pvp = float(self.txt_pvp.get())
            iva = int(self.combo_iva.get())
        except ValueError:
            messagebox.showerror("Error", "Revise que los valores numéricos de costo, precio e IVA sean correctos.")
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
            self.txt_cod.delete(0, tk.END)
            self.txt_nom.delete(0, tk.END)
            self.txt_costo.delete(0, tk.END)
            self.txt_pvp.delete(0, tk.END)
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
        finally:
            conn.close()

class TPVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal Punto de Venta - Multi Servicios Ramirez")
        self.root.geometry("1100x650")
        self.root.configure(bg="#dcdcdc")

        self.carrito = []

        # --- CABECERA ---
        frame_top = tk.Frame(root, bg="#ececec", bd=2, relief="groove")
        frame_top.pack(fill="x", padx=10, pady=10)

        lbl_logo = tk.Label(frame_top, text="TPV", bg="#b5651d", fg="white", font=("Arial", 12, "bold"), padx=10, pady=10)
        lbl_logo.pack(side="left", padx=5, pady=5)
        
        info_text = "Terminal Punto de Venta\nTerminal punto de venta y control de almacén"
        tk.Label(frame_top, text=info_text, bg="#ececec", font=("Arial", 9), justify="left").pack(side="left", padx=5)

        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        sesion_text = f"Serie de Ticket: T1  (F11)\nFecha: {fecha_hoy}\nDependiente: 2  (F2)    RAFELIN MENDEZ"
        tk.Label(frame_top, text=sesion_text, bg="#ececec", font=("Arial", 9), justify="left").pack(side="left", padx=20)

        self.lbl_visor = tk.Label(frame_top, text="0.00€", bg="black", fg="#00ffcc", font=("Courier New", 28, "bold"), bd=3, relief="sunken", width=10, anchor="e")
        self.lbl_visor.pack(side="right", padx=10, pady=5)

        # --- ENTRADA DE ARTÍCULOS ---
        frame_input = tk.Frame(root, bg="#ececec", bd=2, relief="groove")
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Código:", bg="#ececec", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        self.entry_codigo = tk.Entry(frame_input, font=("Courier New", 11), width=20)
        self.entry_codigo.pack(side="left", padx=5, pady=5)
        self.entry_codigo.focus()
        self.entry_codigo.bind("<Return>", self.agregar_producto)

        tk.Label(frame_input, text="Unids:", bg="#ececec", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        self.entry_unids = tk.Entry(frame_input, font=("Arial", 11), width=6, justify="center")
        self.entry_unids.insert(0, "1.00")
        self.entry_unids.pack(side="left", padx=5)

        # --- TABLA CENTRAL ---
        frame_tabla = tk.Frame(root, bg="white", bd=2, relief="sunken")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("codigo", "descripcion", "unids", "precio", "iva", "importe")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("unids", text="Unids.")
        self.tree.heading("precio", text="Precio Base")
        self.tree.heading("iva", text="IVA")
        self.tree.heading("importe", text="Importe Total")

        self.tree.column("codigo", width=140)
        self.tree.column("descripcion", width=330)
        self.tree.column("unids", width=70, anchor="center")
        self.tree.column("precio", width=90, anchor="e")
        self.tree.column("iva", width=60, anchor="center")
        self.tree.column("importe", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True)

        # --- ZONA INFERIOR ---
        frame_bottom = tk.Frame(root, bg="#dcdcdc")
        frame_bottom.pack(fill="x", padx=10, pady=10)

        frame_botones = tk.Frame(frame_bottom, bg="#dcdcdc")
        frame_botones.pack(side="left", fill="y")

        tk.Button(frame_botones, text="F5  Venta", bg="#e1e1e1", fg="#990000", font=("Arial", 9, "bold"), width=12, command=self.procesar_venta).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="F7  Ticket", bg="#e1e1e1", fg="#990000", font=("Arial", 9, "bold"), width=12, command=self.imprimir_ticket).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="F6  Cancelar", bg="#e1e1e1", fg="#990000", font=("Arial", 9, "bold"), width=12, command=self.cancelar_venta).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="F8  Caja", bg="#e1e1e1", fg="#990000", font=("Arial", 9, "bold"), width=12, command=lambda: messagebox.showinfo("Caja", "Caja abierta")).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="F10 Artículos/IVA", bg="#b5651d", fg="white", font=("Arial", 9, "bold"), width=25, command=self.abrir_gestion).grid(row=2, column=0, columnspan=2, padx=2, pady=2)

        frame_totales = tk.Frame(frame_bottom, bg="#ececec", bd=2, relief="groove", padx=10, pady=5)
        frame_totales.pack(side="right")

        tk.Label(frame_totales, text="Base imponible:", bg="#ececec", font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5)
        self.lbl_base = tk.Label(frame_totales, text="0.00", bg="white", font=("Courier New", 10, "bold"), width=15, anchor="e", relief="sunken")
        self.lbl_base.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_totales, text="IVA Total:", bg="#ececec", font=("Arial", 9)).grid(row=1, column=0, sticky="w", padx=5)
        self.lbl_iva = tk.Label(frame_totales, text="0.00", bg="white", font=("Courier New", 10, "bold"), width=15, anchor="e", relief="sunken")
        self.lbl_iva.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_totales, text="Total:", bg="#ececec", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5)
        self.lbl_total = tk.Label(frame_totales, text="0.00", bg="white", font=("Courier New", 12, "bold"), fg="#990000", width=15, anchor="e", relief="sunken")
        self.lbl_total.grid(row=2, column=1, padx=5, pady=2)

        # Atajos
        root.bind("<F5>", lambda event: self.procesar_venta())
        root.bind("<F6>", lambda event: self.cancelar_venta())
        root.bind("<F7>", lambda event: self.imprimir_ticket())
        root.bind("<F8>", lambda event: messagebox.showinfo("Caja", "Caja abierta"))
        root.bind("<F10>", lambda event: self.abrir_gestion())
        root.bind("<Escape>", lambda event: root.quit())

    def abrir_gestion(self):
        GestionInventarioWindow(self.root)

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
            precio_base = prod["precio_base"]
            iva_pct = prod["iva"]
            
            self.carrito.append({
                "codigo": prod["codigo"],
                "nombre": prod["nombre"],
                "unidades": unidades,
                "precio_base": precio_base,
                "iva_pct": iva_pct
            })
            
            self.entry_codigo.delete(0, tk.END)
            self.entry_unids.delete(0, tk.END)
            self.entry_unids.insert(0, "1.00")
            self.actualizar_vista()
        else:
            messagebox.showerror("Error", "Artículo no encontrado. Pulse F10 para agregarlo al inventario.")

    def actualizar_vista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        base_total = 0.0
        iva_total = 0.0
        general_total = 0.0

        for item in self.carrito:
            imp_base = item["unidades"] * item["precio_base"]
            cuota_iva = imp_base * (item["iva_pct"] / 100)
            importe_con_iva = imp_base + cuota_iva

            base_total += imp_base
            iva_total += cuota_iva
            general_total += importe_con_iva

            self.tree.insert("", "end", values=(
                item["codigo"],
                item["nombre"],
                f"{item['unidades']:.2f}",
                f"{item['precio_base']:.2f}",
                f"{item['iva_pct']}%",
                f"{importe_con_iva:.2f}"
            ))

        self.lbl_visor.config(text=f"{general_total:.2f}€")
        self.lbl_base.config(text=f"{base_total:.2f}")
        self.lbl_iva.config(text=f"{iva_total:.2f}")
        self.lbl_total.config(text=f"{general_total:.2f}")

    def cancelar_venta(self):
        self.carrito = []
        self.actualizar_vista()
        self.entry_codigo.focus()

    def procesar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El ticket está vacío.")
            return
        messagebox.showinfo("Venta", "¡Venta cobrada y registrada con éxito!")
        self.cancelar_venta()

    def imprimir_ticket(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "No hay nada que imprimir.")
            return
        messagebox.showinfo("Ticket", "Imprimiendo ticket en impresora por defecto...")

if __name__ == "__main__":
    root = tk.Tk()
    app = TPVApp(root)
    root.mainloop()
