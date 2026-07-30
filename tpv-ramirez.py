from datetime import datetime, date
import pandas as pd
import streamlit as st

# Configuración de página con diseño moderno y colores llamativos
st.set_page_config(
    page_title="TPV - Multi Servicios Ramirez", page_icon="⚡", layout="centered"
)

# Estilos CSS personalizados para darle un toque moderno, colorido y delicado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar credenciales y datos en session_state
if "admin_nombre" not in st.session_state:
  st.session_state.admin_nombre = "Administrador"
if "empleado_nombre" not in st.session_state:
  st.session_state.empleado_nombre = "Empleado de Turno"
if "rol_activo" not in st.session_state:
  st.session_state.rol_activo = None

# Base de datos completa con todos los artículos de tus listados
if "inventario" not in st.session_state:
  st.session_state.inventario = pd.DataFrame([
      # --- Listado 1 ---
      {
          "codigo": "000000000001",
          "articulo": "SAZON LIQUIDO RANCHERO 400ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000002",
          "articulo": "GANDULES VERDES CON COCO GOYA",
          "p_compra": 2.11,
          "p_venta": 2.72,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000003",
          "articulo": "OREGANO RANCHERO EN POLVO 90GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000004",
          "articulo": "FRIJOLES NEGROS PLEBEYO 400GR",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000005",
          "articulo": "SALSA DE AJI PICANTE 200ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000006",
          "articulo": "SAZON CRIOLLO BALDOM SIN PIMIENTA",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000007",
          "articulo": "GUANDULES VERDES GOYA 425GR",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 28.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000008",
          "articulo": "SAZON SUPER COMPLETO 283GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000010",
          "articulo": "CABALLA EN SALSA DE TOMATE 425gr",
          "p_compra": 2.45,
          "p_venta": 3.30,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000011",
          "articulo": "AVENA EN HOJUELAS GOYA 500GR",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 14.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000012",
          "articulo": "SALSA CHINA DE SOJA 200ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000013",
          "articulo": "GUANDULES VERDES 822GR",
          "p_compra": 0.00,
          "p_venta": 3.14,
          "stock": -6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000014",
          "articulo": "LECHE DE COCO GOYA 500ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 25.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000015",
          "articulo": "GUANDULES VERDES PLEBEYO 425GR",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000016",
          "articulo": "CABALLA EN ACEITE DE SOYA 425GR",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000017",
          "articulo": "LECHE DE COCO AROY-D 1LT",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000018",
          "articulo": "GALLETAS WAFERS VAINILLA GOYA",
          "p_compra": 0.00,
          "p_venta": 0.82,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000019",
          "articulo": "VAINILLA DELIFRUIT 4 ONZA",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": -2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000020",
          "articulo": "COCA COLA LATA 330 ML",
          "p_compra": 0.61,
          "p_venta": 1.23,
          "stock": 61.0,
          "caducidad": "2026-06-01",
      },
      {
          "codigo": "000000000021",
          "articulo": "VAINILLA ORIENTE 16 ONZAS",
          "p_compra": 0.00,
          "p_venta": 4.95,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000022",
          "articulo": "AJINOMOTO 100GR",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 15.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000023",
          "articulo": "GALLETAS DUCALES 294GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000025",
          "articulo": "GALLETAS FESTIVALVAINILLA 12 PAQ",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000027",
          "articulo": "LONGANIZA INDUVECA 500GR",
          "p_compra": 0.00,
          "p_venta": 6.61,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000028",
          "articulo": "QUESO LATINO MI VAQUITA 30GR",
          "p_compra": 2.00,
          "p_venta": 2.72,
          "stock": 6.0,
          "caducidad": "2026-07-15",
      },
      {
          "codigo": "000000000029",
          "articulo": "AQUARIUS LIMON LATA 330ML",
          "p_compra": 0.62,
          "p_venta": 1.23,
          "stock": 31.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000030",
          "articulo": "FANTA LATA 330ML",
          "p_compra": 0.49,
          "p_venta": 1.23,
          "stock": 36.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000031",
          "articulo": "AGUA DE COCO GOYA LATA 350ML",
          "p_compra": 1.01,
          "p_venta": 1.23,
          "stock": 71.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000032",
          "articulo": "ENERGY DRINK LATA 250 ML",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 51.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000033",
          "articulo": "ALOE VERA MANGO 500ML",
          "p_compra": 1.04,
          "p_venta": 1.65,
          "stock": 28.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000034",
          "articulo": "CERVEZA CORONA 355ML",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 88.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000035",
          "articulo": "BOCADILLO DE GUAYABA 300GR",
          "p_compra": 1.43,
          "p_venta": 2.47,
          "stock": 20.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000036",
          "articulo": "CHOCOLATE CORONA 250GR",
          "p_compra": 0.00,
          "p_venta": 4.13,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000037",
          "articulo": "CHOCOLATE LUKER SIN AZUCAR 250GR",
          "p_compra": 0.00,
          "p_venta": 6.19,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000038",
          "articulo": "CERVEZA POKER 330ML",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000039",
          "articulo": "FRIJOLES ROJOS PLEBEYO EN BOLSA 500G",
          "p_compra": 0.00,
          "p_venta": 1.73,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000040",
          "articulo": "FRIJOLES NEGROS PLEBEYO BOLSA 500GR",
          "p_compra": 0.00,
          "p_venta": 1.73,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000041",
          "articulo": "CAFE AGUILA ROJA 250GR",
          "p_compra": 0.00,
          "p_venta": 4.95,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000042",
          "articulo": "COCA COLA GRANDE 2LT",
          "p_compra": 1.29,
          "p_venta": 2.47,
          "stock": 13.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000043",
          "articulo": "POSTEBON GRANDE UVA 2LT",
          "p_compra": 0.00,
          "p_venta": 3.14,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000044",
          "articulo": "COLOMBIANA GRANDE 2LT",
          "p_compra": 0.00,
          "p_venta": 3.14,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000045",
          "articulo": "POSTEBON MANZANA 2LT",
          "p_compra": 0.00,
          "p_venta": 3.14,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000046",
          "articulo": "HIT FRUTAS TROPICALES 237ML",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000047",
          "articulo": "INCA COLA PEQUEÑO",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 11.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000048",
          "articulo": "MALTA MORENA 355ML",
          "p_compra": 0.00,
          "p_venta": 1.81,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      # --- Listado 2 ---
      {
          "codigo": "000000000049",
          "articulo": "POSTEBON UVA 500ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000050",
          "articulo": "REFRESCO MERENGUE CLUB 500ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000051",
          "articulo": "ALOE VERA GOYA 500ML",
          "p_compra": 1.04,
          "p_venta": 1.65,
          "stock": 39.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000052",
          "articulo": "REFRESCO FRAMBUESA CLUB 500ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 22.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000053",
          "articulo": "MALTA INDIA 355ML",
          "p_compra": 1.00,
          "p_venta": 1.65,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000054",
          "articulo": "MALTA LOWENBRAU 355 ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000056",
          "articulo": "CERVEZA EMBRAU LATA 330ML",
          "p_compra": 0.00,
          "p_venta": 0.82,
          "stock": 68.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000057",
          "articulo": "YERBA MATE KURUPI MENTA Y BOLDO",
          "p_compra": 3.70,
          "p_venta": 4.95,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000058",
          "articulo": "YERBA MATE PAJARITO",
          "p_compra": 3.15,
          "p_venta": 4.95,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000059",
          "articulo": "AQUARIUS NARANJA LATA 330ML",
          "p_compra": 0.62,
          "p_venta": 1.23,
          "stock": 34.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000060",
          "articulo": "AGUA VIVO 50ml",
          "p_compra": 0.12,
          "p_venta": 0.82,
          "stock": 81.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000061",
          "articulo": "CERVEZA MAHOU LATA 330ML",
          "p_compra": 0.44,
          "p_venta": 1.23,
          "stock": 30.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000062",
          "articulo": "JABON REY 300GR",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000063",
          "articulo": "CERVEZA HEINEKEN LATA 330ML",
          "p_compra": 0.65,
          "p_venta": 1.23,
          "stock": 18.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000064",
          "articulo": "CERVEZA REPUBLICA 330ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000065",
          "articulo": "GUARANA LATA 330ML",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 24.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000066",
          "articulo": "LECHE CARNATION 385ML",
          "p_compra": 0.00,
          "p_venta": 2.72,
          "stock": 29.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000067",
          "articulo": "HIT LULO 237ML",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 27.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000068",
          "articulo": "PASTA DE AJI PANCA 225GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000069",
          "articulo": "PONY MALTA 330 ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 17.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000070",
          "articulo": "AJI PANQUITA SIBARITA 250GR",
          "p_compra": 2.23,
          "p_venta": 3.63,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000071",
          "articulo": "CERVEZA EMBRAU 1LT",
          "p_compra": 0.00,
          "p_venta": 1.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000072",
          "articulo": "DOÑAREPA MAIZ AMARILLO 1000GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000073",
          "articulo": "DOÑAREPA MAIZ BLANCO 1000GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000074",
          "articulo": "HARINA EL NEGRITO",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000075",
          "articulo": "HARINA PAN BLANCA 1000GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000076",
          "articulo": "GALLETAS FESTIVAL CHOCOLATE 12 PQ.",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000077",
          "articulo": "GALLETAS FESTIVAL LIMON 12 PQ DE",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000078",
          "articulo": "PLATANITO VERDES 65GR",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000079",
          "articulo": "PLATANITO MADURITOS",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000080",
          "articulo": "AJI PANCA DISECADO 100GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 26.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000081",
          "articulo": "GALLETAS FESTIVAL FRESA 12 PQ 403 GR",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000082",
          "articulo": "AZUCAR BLANCO SUCREBO 1KG",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000083",
          "articulo": "FARINHA DE MANDIOCA 500GR",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000084",
          "articulo": "FAROFA TRADICIONAL 400GR",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000085",
          "articulo": "AGUA FLORIDA",
          "p_compra": 0.00,
          "p_venta": 5.78,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000086",
          "articulo": "COCA COLA DE 1.25 LT",
          "p_compra": 0.98,
          "p_venta": 1.65,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000087",
          "articulo": "ZUMO DON SIMON MANGO 1.5LT",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000088",
          "articulo": "ZUMO DON SIMON PIÑA 1.5LT",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000089",
          "articulo": "FANTA NARANJA 2LT",
          "p_compra": 1.15,
          "p_venta": 2.47,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000090",
          "articulo": "AGUA VIVO 1.5LT",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 10.0,
          "caducidad": "2027-06-15",
      },
      # --- Listado 3 & Códigos Largos ---
      {
          "codigo": "4562589632659",
          "articulo": "OREGANO EN RAMA",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632661",
          "articulo": "PULPA DE MANGO EL DORADO",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632662",
          "articulo": "PATACONES EL PLEBEYO",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632663",
          "articulo": "PULPA DE MANGO GOYA",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 20.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632664",
          "articulo": "PULPA DE PAPAYA GOYA",
          "p_compra": 1.34,
          "p_venta": 2.89,
          "stock": 14.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632665",
          "articulo": "PULPA DE MAMEY O ZAPOTE GOYA",
          "p_compra": 5.83,
          "p_venta": 7.27,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632666",
          "articulo": "PULPA DE LULO EL DORADO",
          "p_compra": 3.14,
          "p_venta": 4.54,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632667",
          "articulo": "PULPA DE MARACUYA O CHINOLA GOYA",
          "p_compra": 1.77,
          "p_venta": 2.89,
          "stock": 73.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632668",
          "articulo": "PULPA CON PEPA DE MARACUYA GOYA",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632669",
          "articulo": "AREPA RIKAREPA",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632670",
          "articulo": "AJI AMARILLO EL PLEBEYO",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632671",
          "articulo": "YUCA GOYA 500GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 11.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632672",
          "articulo": "ROCOTO EL PLEBEYO",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632673",
          "articulo": "HOJAS DE PLATANO PLEBEYO 500GR",
          "p_compra": 0.00,
          "p_venta": 4.13,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632674",
          "articulo": "GUANDULES VERDES CONGELADO 500GR",
          "p_compra": 0.00,
          "p_venta": 3.71,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632675",
          "articulo": "MALTA ALEMANA TIEGERBRAU",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 39.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632676",
          "articulo": "PANELA GRANDE 454GR",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632677",
          "articulo": "PANELA PEQ. 454GR 4/1",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632678",
          "articulo": "COLOMBIANA PEQUEÑA 500ML",
          "p_compra": 3.05,
          "p_venta": 4.54,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632679",
          "articulo": "LECHE DE COCO GRANDE 1LT GOYA",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632681",
          "articulo": "TRIGO DOMICANO 500GR",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632682",
          "articulo": "RUFFLES JAMON",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632683",
          "articulo": "DORITOS TEX-MEX",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632684",
          "articulo": "DORITOS CHILLI",
          "p_compra": 0.00,
          "p_venta": 1.57,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632685",
          "articulo": "LAYS AL PUNTO DE SAL",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632686",
          "articulo": "RUFFLES ORIGINAL SAL",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632687",
          "articulo": "CHEETOS PELOTAZOS",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632688",
          "articulo": "CHEETOS STICKS PALITOS",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632689",
          "articulo": "CHEETOS PANDILLA",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632690",
          "articulo": "RUFFLES SABOR A YORK",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632691",
          "articulo": "CHEETOS GUSTOSINES",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632692",
          "articulo": "RUFFLES FLAMINT HOT",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 14.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632693",
          "articulo": "PULPAS DE TAMARINDO GOYA",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632694",
          "articulo": "PULPAS DE GUANABANA GOYA",
          "p_compra": 0.00,
          "p_venta": 8.26,
          "stock": 29.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632696",
          "articulo": "LEBARA TODO INCLUIDO 10",
          "p_compra": 0.00,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632697",
          "articulo": "PLATANO MACHO VERDE",
          "p_compra": 0.00,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632698",
          "articulo": "PLATANO MACHO MADURO",
          "p_compra": 0.00,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632699",
          "articulo": "YAUTIA / EDO",
          "p_compra": 0.00,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632700",
          "articulo": "CEBOLLA ROJA",
          "p_compra": 0.00,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632701",
          "articulo": "AGUACATE",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632703",
          "articulo": "SAZON LIQUIDO RANCHERO PICANTE",
          "p_compra": 0.00,
          "p_venta": 2.89,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632704",
          "articulo": "TOMATE DE ARBOL",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632705",
          "articulo": "MARACUYA EL DORADO",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632706",
          "articulo": "MANGO VERDE",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632707",
          "articulo": "SALSA CHINA FRUCO",
          "p_compra": 0.00,
          "p_venta": 0.41,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632708",
          "articulo": "SALSA CHINA KIKO",
          "p_compra": 0.00,
          "p_venta": 1.48,
          "stock": 105.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632709",
          "articulo": "AGUA VIVO PEQUEÑITA 33ML",
          "p_compra": 0.00,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632710",
          "articulo": "LAYS GRANDE",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632711",
          "articulo": "HIT MORA 237ML",
          "p_compra": 1.09,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632712",
          "articulo": "CERVEZA PRESIDENTE PEQUEÑA",
          "p_compra": 1.09,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632713",
          "articulo": "CANELA EN RAMA",
          "p_compra": 0.00,
          "p_venta": 2.27,
          "stock": -1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632714",
          "articulo": "FLOR DE JAMAICA NATURAL 100GR",
          "p_compra": 1.80,
          "p_venta": 7.14,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632715",
          "articulo": "PANELA FRACCIONADA DELI 454gr.",
          "p_compra": 1.19,
          "p_venta": 1.19,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632716",
          "articulo": "PANELA REDONDA DELI 454gr",
          "p_compra": 1.19,
          "p_venta": 5.20,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632717",
          "articulo": "LONGANIZA CARNITAS COLOMBIANA 500GR",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632719",
          "articulo": "GALLETAS GUARINA 12/1",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632720",
          "articulo": "HARINA PAN AMARILLA",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632721",
          "articulo": "BOLSA PLASTICA",
          "p_compra": 0.00,
          "p_venta": 0.08,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632722",
          "articulo": "POSTOBON DE MANZANA 500ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": -5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632723",
          "articulo": "BON BON BUM",
          "p_compra": 0.00,
          "p_venta": 0.41,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632724",
          "articulo": "NESTEA LIMON LATA 330ML",
          "p_compra": 0.64,
          "p_venta": 1.23,
          "stock": 25.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632725",
          "articulo": "YERBA MATE COLON",
          "p_compra": 3.87,
          "p_venta": 4.95,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632726",
          "articulo": "SALAMI SOSUA 1KILO",
          "p_compra": 5.90,
          "p_venta": 12.39,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632727",
          "articulo": "CHORIZO COLOMBIANO PEQUEÑO",
          "p_compra": 5.19,
          "p_venta": 6.61,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632729",
          "articulo": "MALTIN POLAR 330 ML",
          "p_compra": 0.98,
          "p_venta": 1.65,
          "stock": 51.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632730",
          "articulo": "FRIJOLES ROJOS 400G PLEBEYO",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632731",
          "articulo": "MAS MOVIL 10 INCLUIDO",
          "p_compra": 0.00,
          "p_venta": 8.26,
          "stock": 15.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632732",
          "articulo": "GUANDULES SECO COEXITO",
          "p_compra": 1.86,
          "p_venta": 2.47,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632733",
          "articulo": "HARINA DE MAIZ MAZORCA DOMINICANA",
          "p_compra": 0.97,
          "p_venta": 2.31,
          "stock": 11.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632734",
          "articulo": "GUANDULES VERDE CON COCO PLEBEYO",
          "p_compra": 1.53,
          "p_venta": 2.47,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632735",
          "articulo": "ANIS ESTRELLA VIZCAYA",
          "p_compra": 1.21,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632736",
          "articulo": "DORITOS SWEET CHILLI",
          "p_compra": 1.13,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632737",
          "articulo": "PASTA ROCOTO",
          "p_compra": 1.86,
          "p_venta": 2.47,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632738",
          "articulo": "PASTA AJI AMARILLO",
          "p_compra": 1.80,
          "p_venta": 2.47,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632739",
          "articulo": "GALLETAS FESTIVAL COCO",
          "p_compra": 2.44,
          "p_venta": 3.30,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632740",
          "articulo": "GALLETAS FESTIVAL TUTTI FRUTTI",
          "p_compra": 2.44,
          "p_venta": 7.43,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632741",
          "articulo": "SALCHICHON CERVECERO",
          "p_compra": 5.98,
          "p_venta": 1.81,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632742",
          "articulo": "AZUCAR BLANCO AZUCARERA 1KG",
          "p_compra": 0.79,
          "p_venta": 1.65,
          "stock": 10.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632743",
          "articulo": "LECHE ENTERA 1LT GALLEGA",
          "p_compra": 0.78,
          "p_venta": 4.95,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632744",
          "articulo": "ACHIOTE 50 GRAMOS COEXITO",
          "p_compra": 1.19,
          "p_venta": 4.13,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632745",
          "articulo": "CAFE SELLO ROJO",
          "p_compra": 3.90,
          "p_venta": 5.45,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632746",
          "articulo": "HOJAS DE PLATANO DORADO",
          "p_compra": 2.13,
          "p_venta": 1.23,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632747",
          "articulo": "TILAPIA ROJA",
          "p_compra": 2.93,
          "p_venta": 12.39,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632748",
          "articulo": "PLATANITOS LIMON NATUCHIPS",
          "p_compra": 10.00,
          "p_venta": 4.13,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632749",
          "articulo": "TE GUARANI 30 DIAS",
          "p_compra": 2.93,
          "p_venta": 4.096,
          "stock": 92.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632750",
          "articulo": "PELOS PARA TRENZAS",
          "p_compra": 0.90,
          "p_venta": 4.54,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632751",
          "articulo": "PAN DE QUESO YOKI",
          "p_compra": 2.93,
          "p_venta": 4.95,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632752",
          "articulo": "FECULA DE MANDIOCA",
          "p_compra": 2.84,
          "p_venta": 3.71,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632753",
          "articulo": "POLVILHO AZEDO YOKI",
          "p_compra": 2.90,
          "p_venta": 3.63,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632754",
          "articulo": "TRIGO PARA KIBE YOKI",
          "p_compra": 3.70,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632755",
          "articulo": "FARINHA MANDIOCA TORRADA YOKI",
          "p_compra": 2.40,
          "p_venta": 2.27,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632756",
          "articulo": "MAIZ AMARILLO MAZAMORRA PROCOLDIS",
          "p_compra": 2.35,
          "p_venta": 2.27,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632757",
          "articulo": "MAIZ BLANCO MAZAMORRA PROCOLDIS",
          "p_compra": 1.09,
          "p_venta": 9.81,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632758",
          "articulo": "MAIZ AMARILLO TRILLADO",
          "p_compra": 1.09,
          "p_venta": 2.06,
          "stock": 9.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632759",
          "articulo": "MAIZ BLANCO TRILLADO",
          "p_compra": 1.09,
          "p_venta": 7.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632760",
          "articulo": "LEVADURA ACTIVA SECA",
          "p_compra": 5.83,
          "p_venta": 4.54,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632761",
          "articulo": "TOSTONES PRECOCIDOS",
          "p_compra": 3.14,
          "p_venta": 1.65,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632762",
          "articulo": "REFRESCO CLUB UVA 500ML",
          "p_compra": 0.72,
          "p_venta": 3.63,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632763",
          "articulo": "SALSA DE SOJA KIKO 500ML",
          "p_compra": 1.45,
          "p_venta": 3.63,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632764",
          "articulo": "MAIZ MORADO COEXITO",
          "p_compra": 0.00,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632765",
          "articulo": "PLATANOS CHILE Y LIMON EL DORADO",
          "p_compra": 1.79,
          "p_venta": 3.90,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632766",
          "articulo": "PLATANITO ZAMBOS YUMMIES",
          "p_compra": 0.93,
          "p_venta": 3.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632767",
          "articulo": "MAIZ MOTE PLEBEYO",
          "p_compra": 2.66,
          "p_venta": 2.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632768",
          "articulo": "MAIZ DE TOSTAR COEXITO",
          "p_compra": 2.59,
          "p_venta": 1.36,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632769",
          "articulo": "DORITOS DINAMITA",
          "p_compra": 1.70,
          "p_venta": 0.59,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632770",
          "articulo": "FRUTIÑO MARACUYA",
          "p_compra": 1.14,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632771",
          "articulo": "GALLETAS LECHE GUARINA",
          "p_compra": 0.30,
          "p_venta": 1.65,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632772",
          "articulo": "FRUTIÑO MARACUPIÑA",
          "p_compra": 0.00,
          "p_venta": 3.63,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632773",
          "articulo": "AJI AMARILLIN SIBARITA",
          "p_compra": 0.30,
          "p_venta": 2.72,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632774",
          "articulo": "ANIS ESTRELLADO LATINA",
          "p_compra": 2.36,
          "p_venta": 1.81,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632775",
          "articulo": "CLAVO DULCE VIZCAYA",
          "p_compra": 2.13,
          "p_venta": 0.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632776",
          "articulo": "MILO NESTLE 20 G",
          "p_compra": 1.22,
          "p_venta": 2.72,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632777",
          "articulo": "SAZON CRIOLLO BALDOM CON PIMIENTA",
          "p_compra": 0.49,
          "p_venta": 18.18,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632778",
          "articulo": "CALDERO 22 CM",
          "p_compra": 13.70,
          "p_venta": 20.66,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632779",
          "articulo": "CALDERO 24 CM",
          "p_compra": 15.07,
          "p_venta": 1.36,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632780",
          "articulo": "LAYS SABOR A CEBOLLA",
          "p_compra": 1.09,
          "p_venta": 1.36,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632781",
          "articulo": "PATATAS FRITAS SANTA ANA",
          "p_compra": 1.13,
          "p_venta": 2.47,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632782",
          "articulo": "JABON DE RUDA TRIO",
          "p_compra": 1.54,
          "p_venta": 3.08,
          "stock": 39.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632783",
          "articulo": "REDBULL 250ML",
          "p_compra": 0.85,
          "p_venta": 33.15,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632784",
          "articulo": "AGUA SAN JOAQUIN 1.5LT",
          "p_compra": 0.22,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632785",
          "articulo": "REFRESCO SEVEN UP LIMA,2LT",
          "p_compra": 1.03,
          "p_venta": 2.47,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632786",
          "articulo": "AGUA VIVO 5 LT",
          "p_compra": 0.57,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632787",
          "articulo": "AGUA VALTORRE 5 LT",
          "p_compra": 0.63,
          "p_venta": 2.52,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632788",
          "articulo": "HIT DE MANGO",
          "p_compra": 0.75,
          "p_venta": 3.00,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632789",
          "articulo": "PANELA FRACCIONADA COEXITO",
          "p_compra": 30.14,
          "p_venta": 37.19,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632790",
          "articulo": "CALDERO 36CM UNIVERSAL",
          "p_compra": 22.61,
          "p_venta": 28.92,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "4562589632791",
          "articulo": "CALDERO 30CM UNIVERSAL",
          "p_compra": 1.04,
          "p_venta": 2.47,
          "stock": 21.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026416",
          "articulo": "REFRESCO UVA 2LT GOYA",
          "p_compra": 1.24,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026417",
          "articulo": "LAYS CAMPESINAS",
          "p_compra": 1.13,
          "p_venta": 1.81,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026418",
          "articulo": "FRIJOLES ROJO NATURAL GOYA",
          "p_compra": 1.49,
          "p_venta": 2.06,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026419",
          "articulo": "FRIJOLES ROJO GUISADO",
          "p_compra": 0.93,
          "p_venta": 2.98,
          "stock": 18.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026420",
          "articulo": "TOSTONES CHIPS AJO GOYA",
          "p_compra": 0.00,
          "p_venta": 16.74,
          "stock": 22.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026421",
          "articulo": "FRIJOLES NEGRO GOYA CARAOTA",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 20.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026422",
          "articulo": "LEBARA TODO INCLUIDO 15",
          "p_compra": 0.44,
          "p_venta": 8.26,
          "stock": 45.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026423",
          "articulo": "REFRESCO UVA GOYA 500ML",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 19.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026424",
          "articulo": "ORANGE 10 EUROS",
          "p_compra": 0.00,
          "p_venta": 8.26,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026425",
          "articulo": "LEBARA 10 TODO INCLUIDO VIEJO",
          "p_compra": 0.00,
          "p_venta": 3.30,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026426",
          "articulo": "AJI LIMO EL PLEBEYO",
          "p_compra": 0.87,
          "p_venta": 1.23,
          "stock": 28.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026427",
          "articulo": "TANG PIÑA",
          "p_compra": 1.09,
          "p_venta": 1.23,
          "stock": 27.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026428",
          "articulo": "TANG FRESA",
          "p_compra": 5.38,
          "p_venta": 4.35,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026429",
          "articulo": "TANG RIO PUNCH",
          "p_compra": 0.87,
          "p_venta": 3.48,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026430",
          "articulo": "TANG NARANJA",
          "p_compra": 0.09,
          "p_venta": 0.54,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026431",
          "articulo": "CHICLETS ADAMS",
          "p_compra": 0.12,
          "p_venta": 0.22,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026432",
          "articulo": "BOCADILLO GUAYABA COEXITO PEQ",
          "p_compra": 0.12,
          "p_venta": 0.22,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026433",
          "articulo": "BUBALOO MORA",
          "p_compra": 0.00,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026434",
          "articulo": "BUBALOO FRESA",
          "p_compra": 1.70,
          "p_venta": 0.45,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026435",
          "articulo": "PANELA REDONDA COEXITO 454G",
          "p_compra": 0.67,
          "p_venta": 1.23,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026436",
          "articulo": "CHOCOLATE EMBAJADOR 26GX1",
          "p_compra": 0.28,
          "p_venta": 4.13,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026437",
          "articulo": "CHOCLITOS LIMON 27G",
          "p_compra": 1.90,
          "p_venta": 4.95,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026438",
          "articulo": "CHORIZO ANTIOQUEÑO 250G GOYA",
          "p_compra": 3.70,
          "p_venta": 0.82,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026439",
          "articulo": "CAFE SANTO DOMINGO",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026440",
          "articulo": "CUADRADITOS DE CACAO DULCESOL",
          "p_compra": 0.00,
          "p_venta": 0.82,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026441",
          "articulo": "PALMERITAS DULCESOL",
          "p_compra": 0.66,
          "p_venta": 1.98,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026442",
          "articulo": "CHAPELA CACAO DULCESOL",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026443",
          "articulo": "CHAPELA ZEBRA DULCESOL",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026444",
          "articulo": "BROWNS RELLENO DE NATA DULCESOL 3u",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026445",
          "articulo": "BRIOCHOCO CON PEPITAS DULCESOL",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026446",
          "articulo": "PANDORINO CACAO DULCESOL 3und",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026447",
          "articulo": "NANJUS COOKIES DULCESOL",
          "p_compra": 0.66,
          "p_venta": 0.82,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026448",
          "articulo": "BOER COCO DULCESOL",
          "p_compra": 0.66,
          "p_venta": 1.23,
          "stock": 13.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026449",
          "articulo": "FLAMINGUITO SNACK PINKY DULCESOL 3u",
          "p_compra": 0.41,
          "p_venta": 3.63,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026450",
          "articulo": "KAS NARANJA LATA 330ML",
          "p_compra": 2.60,
          "p_venta": 0.90,
          "stock": 13.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026451",
          "articulo": "CERVEZA AMSTEL RADLER LIMON LATA",
          "p_compra": 0.00,
          "p_venta": 0.90,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026452",
          "articulo": "CHICHA EL CHICHERO 240ML",
          "p_compra": 0.65,
          "p_venta": 0.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026454",
          "articulo": "MILKA ALPINE MILK",
          "p_compra": 0.65,
          "p_venta": 0.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026455",
          "articulo": "MILKA AVELLANAS",
          "p_compra": 0.65,
          "p_venta": 1.18,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026456",
          "articulo": "MILKA TUC",
          "p_compra": 0.75,
          "p_venta": 1.18,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026457",
          "articulo": "MILKA LU",
          "p_compra": 0.75,
          "p_venta": 1.18,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026459",
          "articulo": "MICADO LAIT",
          "p_compra": 0.75,
          "p_venta": 1.18,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026460",
          "articulo": "MIKADO NOIR",
          "p_compra": 0.53,
          "p_venta": 0.90,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026461",
          "articulo": "MILKA COOKIES SENSATIONS",
          "p_compra": 0.53,
          "p_venta": 6.81,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026462",
          "articulo": "MILKA OREO",
          "p_compra": 4.74,
          "p_venta": 16.52,
          "stock": 23.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026463",
          "articulo": "MILKA OREO",
          "p_compra": 12.57,
          "p_venta": 3.63,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026464",
          "articulo": "AGUA AQUAFINA",
          "p_compra": 2.59,
          "p_venta": 2.89,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026465",
          "articulo": "TAMALES DE ELOTE HUMITAS GOYA",
          "p_compra": 2.16,
          "p_venta": 4.95,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026467",
          "articulo": "AGUARDIENTE ANTIOQUEÑO",
          "p_compra": 3.62,
          "p_venta": 2.52,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026468",
          "articulo": "AREPA RIKAREPA PEQUEÑA",
          "p_compra": 0.63,
          "p_venta": 5.76,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026469",
          "articulo": "YERBA MATE CAMPESINO MANZANILLA",
          "p_compra": 2.28,
          "p_venta": 4.13,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026470",
          "articulo": "ACHIOTE LA LATINA",
          "p_compra": 1.87,
          "p_venta": 3.36,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026471",
          "articulo": "CHOCLO ENTERO PLEBEYO",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026472",
          "articulo": "AREPITA 800G CARNILSA",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026473",
          "articulo": "MONSTER ENERGY ULTRA",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026474",
          "articulo": "MONSTER ENERGY LANDO NORRIS",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      # --- Listado 4 & Finales ---
      {
          "codigo": "8410199026475",
          "articulo": "MONSTER ENERGY",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026476",
          "articulo": "MONSTER RIO PUNCH",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026477",
          "articulo": "PANELA FRACCIONADA 4*1 CASTIPAR",
          "p_compra": 1.46,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026478",
          "articulo": "PLATANOS SABOR LIMON EL DORADO",
          "p_compra": 0.93,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026479",
          "articulo": "DORITOS COLLISION",
          "p_compra": 0.87,
          "p_venta": 1.36,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026480",
          "articulo": "REFRESCO MANZANA 500ML GOYA",
          "p_compra": 0.44,
          "p_venta": 1.65,
          "stock": 13.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026481",
          "articulo": "MALTA GOYA 355ML",
          "p_compra": 1.04,
          "p_venta": 8.26,
          "stock": 44.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026482",
          "articulo": "MAS MOVIL TODO INCLUIDO 15€",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 159.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026483",
          "articulo": "FRESCOLITA LATA 330ML",
          "p_compra": 1.14,
          "p_venta": 14.87,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026484",
          "articulo": "VINO LA FUERZA GRANDE",
          "p_compra": 10.49,
          "p_venta": 2.72,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026485",
          "articulo": "SAZON LIQUIDO RANCHERO VERDURAS",
          "p_compra": 1.98,
          "p_venta": 3.00,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026486",
          "articulo": "GALLETAS CLUB SOCIAL ORIGINAL",
          "p_compra": 2.18,
          "p_venta": 3.18,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026487",
          "articulo": "HARINA PAN DULCE 500G",
          "p_compra": 2.40,
          "p_venta": 3.63,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026488",
          "articulo": "CHOCOLATE EMBAJADOR CAJA ENTERA",
          "p_compra": 2.61,
          "p_venta": 2.47,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026489",
          "articulo": "REFRESCO GOYA ORO ANDINO 2LT",
          "p_compra": 0.82,
          "p_venta": 0.82,
          "stock": 3.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026490",
          "articulo": "YERBA MATE KURUPI CEDRON Y MENTA",
          "p_compra": 3.35,
          "p_venta": 5.45,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026491",
          "articulo": "CABALLA DEL PACIFICO EL PIRATA",
          "p_compra": 2.43,
          "p_venta": 3.63,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026492",
          "articulo": "AREPA DE CHOCOLO CON QUESO",
          "p_compra": 5.12,
          "p_venta": 6.81,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026493",
          "articulo": "GUANDULES VERDES CONGELADOS GOYA",
          "p_compra": 1.84,
          "p_venta": 2.88,
          "stock": 34.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026494",
          "articulo": "DORITOS BITS SWEET CHILLI",
          "p_compra": 0.74,
          "p_venta": 4.13,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026495",
          "articulo": "HOJA DE PLATANO GOYA 500GM",
          "p_compra": 4.65,
          "p_venta": 7.43,
          "stock": 22.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026497",
          "articulo": "SALAMI INDUVECA 500GR",
          "p_compra": 1.68,
          "p_venta": 2.88,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026498",
          "articulo": "AREPA DE MAIZ BLANCO GOYA",
          "p_compra": 4.15,
          "p_venta": 5.00,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026500",
          "articulo": "CHOCOLATE LUKER TRADICIONAL 112g",
          "p_compra": 2.60,
          "p_venta": 3.63,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026501",
          "articulo": "ZAMBOS PICOSITAS CON CHILE, LIMON Y",
          "p_compra": 3.95,
          "p_venta": 6.61,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026502",
          "articulo": "SALAMI SOSUA 500GR",
          "p_compra": 1.12,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026503",
          "articulo": "PLATANOS CON SAL EL DORADO",
          "p_compra": 0.19,
          "p_venta": 0.45,
          "stock": 22.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026504",
          "articulo": "BOCADILLO DE GUAYABA CASTIPAN 40g",
          "p_compra": 1.27,
          "p_venta": 1.54,
          "stock": 28.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026505",
          "articulo": "LAYS AL PUNTO DE SAL 1.70€",
          "p_compra": 1.28,
          "p_venta": 1.54,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026506",
          "articulo": "LAYS SABOR CAMPESINAS 1.70€",
          "p_compra": 1.28,
          "p_venta": 1.54,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026507",
          "articulo": "LAYS SABOR SAL Y VINAGRE 1.70€",
          "p_compra": 1.29,
          "p_venta": 1.54,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026508",
          "articulo": "DORITOS SWEET CHILLI 1.70€",
          "p_compra": 1.28,
          "p_venta": 1.54,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026509",
          "articulo": "DORITOS TEX MEX 1.70€",
          "p_compra": 1.28,
          "p_venta": 1.54,
          "stock": 9.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026510",
          "articulo": "RUFFLES SABOR A JAMON 1.70€",
          "p_compra": 1.71,
          "p_venta": 2.40,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026511",
          "articulo": "RUFFLES SABOR A YORK 1.70€",
          "p_compra": 1.28,
          "p_venta": 1.81,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026512",
          "articulo": "ARROZ SOS REDONDO 1K",
          "p_compra": 1.28,
          "p_venta": 2.06,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026513",
          "articulo": "AZUCAR BLANCO VIVO 1KG",
          "p_compra": 0.56,
          "p_venta": 3.63,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026514",
          "articulo": "AGUA SAN JOAQUIN 5LT",
          "p_compra": 1.92,
          "p_venta": 2.27,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026515",
          "articulo": "BOCADILLO GUAYABA 500gr COEXITO",
          "p_compra": 1.46,
          "p_venta": 3.63,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026516",
          "articulo": "BOCADILLO GUAYABA 200gr CASTIPAN",
          "p_compra": 4.97,
          "p_venta": 7.27,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026517",
          "articulo": "PANELA REDONDA 454g CASTIPAN",
          "p_compra": 0.98,
          "p_venta": 1.81,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026518",
          "articulo": "CHORIZO COLOMBIANO 500G CARNITAS EL",
          "p_compra": 0.98,
          "p_venta": 1.81,
          "stock": 30.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026519",
          "articulo": "TORTOLINES LIMON GOYA 100g",
          "p_compra": 0.72,
          "p_venta": 5.76,
          "stock": 19.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026520",
          "articulo": "TORTOLINES LIMON GOYA 100g (2)",
          "p_compra": 0.72,
          "p_venta": 5.76,
          "stock": 8.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026521",
          "articulo": "CONOS SABOR NATA 2u 120ml",
          "p_compra": 0.72,
          "p_venta": 5.76,
          "stock": 10.0,
          "caducidad": "2027-06-15",
      },
      # --- Listado Final ---
      {
          "codigo": "8410199026522",
          "articulo": "BOMBON NATA 3u 80ml",
          "p_compra": 0.72,
          "p_venta": 11.52,
          "stock": 16.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026523",
          "articulo": "POLO LIMON 3u 210gr",
          "p_compra": 0.53,
          "p_venta": 7.20,
          "stock": -10.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026524",
          "articulo": "CONO NATA Y FRESA 125ml",
          "p_compra": 0.53,
          "p_venta": 5.83,
          "stock": 11.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026525",
          "articulo": "CONO VAINILLA 125ml",
          "p_compra": 0.72,
          "p_venta": 10.07,
          "stock": 19.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026526",
          "articulo": "CONO VAINILLA Y CHOCOLATE 125ml",
          "p_compra": 0.72,
          "p_venta": 2.12,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026527",
          "articulo": "TARTA DE MANZANA DULCESOL 2und",
          "p_compra": 0.72,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026528",
          "articulo": "PISTACHO CAKE DULCESOL 3und",
          "p_compra": 0.72,
          "p_venta": 0.00,
          "stock": 0.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026529",
          "articulo": "BRACITOS DE AZUCAR DULCESOL 4und",
          "p_compra": 0.72,
          "p_venta": 1.44,
          "stock": 2.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026530",
          "articulo": "BRACITOS CACAO TRUFA DULCESOL 4und",
          "p_compra": 0.60,
          "p_venta": 2.88,
          "stock": 4.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026531",
          "articulo": "MILKA COOKIES SENSATIONS 2un peq.",
          "p_compra": 0.60,
          "p_venta": 7.20,
          "stock": 12.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026532",
          "articulo": "GALLETAS OREO ORIGINAL PEQ.",
          "p_compra": 0.73,
          "p_venta": 4.20,
          "stock": 7.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026533",
          "articulo": "DORITOS BITS ORIGINAL BBQ PEQ.",
          "p_compra": 1.62,
          "p_venta": 11.68,
          "stock": 16.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026534",
          "articulo": "SALSA CHINA DE SOJA ORIENTAL 400ML",
          "p_compra": 1.10,
          "p_venta": 20.90,
          "stock": 5.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026535",
          "articulo": "PONY MALTA LATA 33ML",
          "p_compra": 1.28,
          "p_venta": 1.28,
          "stock": 19.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026536",
          "articulo": "RUFFLES SABOR ASADO ARGENTINO",
          "p_compra": 0.52,
          "p_venta": 3.12,
          "stock": 1.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026537",
          "articulo": "GALLETAS WAFERS NARANJA GOYA",
          "p_compra": 0.52,
          "p_venta": 3.12,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026538",
          "articulo": "GALLETAS WAFERS LIMON GOYA",
          "p_compra": 0.72,
          "p_venta": 7.20,
          "stock": 6.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "8410199026539",
          "articulo": "BOER SABOR CHOCOLATE DULCESOL",
          "p_compra": 0.72,
          "p_venta": 7.20,
          "stock": 10.0,
          "caducidad": "2027-06-15",
      },
  ])

if "carrito" not in st.session_state:
  st.session_state.carrito = []

# --- PANTALLA DE ACCESO (LOGIN) ---
if st.session_state.rol_activo is None:
  st.markdown(
      "<h1"
      " style='text-align: center; color: #4f46e5;'>✨ Multi Servicios"
      " Ramirez ✨</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: #6b7280;'>Sistema TPV Inteligente"
      " & Dinámico</h4>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown("### 🔐 Iniciar Sesión")
    tipo_login = st.selectbox("Selecciona tu Rol:", ["Empleado", "Administrador"])
    clave = st.text_input("Clave de Acceso:", type="password")

    if st.button(
        "🚀 Acceder al Sistema", use_container_width=True, type="primary"
    ):
      if tipo_login == "Administrador" and clave == "admin123":
        st.session_state.rol_activo = "Administrador"
        st.success(
            f"¡Bienvenido, {st.session_state.admin_nombre} (Admin)!"
        )
        st.rerun()
      elif tipo_login == "Empleado" and clave == "emp123":
        st.session_state.rol_activo = "Empleado"
        st.success(f"¡Bienvenido, {st.session_state.empleado_nombre}!")
        st.rerun()
      else:
        st.error("❌ Clave incorrecta. Inténtalo de nuevo.")

else:
  # --- BARRA LATERAL MODERNA ---
  st.sidebar.markdown("### 🌟 Panel de Control")
  if st.session_state.rol_activo == "Administrador":
    st.sidebar.info(f"👑 **{st.session_state.admin_nombre}** (Admin)")
  else:
    st.sidebar.success(
        f"👤 **{st.session_state.empleado_nombre}** (Empleado)"
    )

  if st.sidebar.button(
      "🚪 Cerrar Sesión", use_container_width=True, type="secondary"
  ):
    st.session_state.rol_activo = None
    st.rerun()

  st.sidebar.markdown("---")
  opciones_menu = [
      "🛒 Caja / Venta",
      "📦 Gestión de Artículos",
      "⚠️ Alertas de Caducidad",
      "⚙️ Configuración Nombres",
  ]
  menu = st.sidebar.selectbox("Menú Principal", opciones_menu)

  # --- CAJA / VENTA ---
  if menu == "🛒 Caja / Venta":
    st.markdown(
        f"### ⚡ Caja Registradora Activa | Turno: <b>"
        f"{st.session_state.empleado_nombre}</b>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    busqueda = st.text_input(
        "🔍 Buscar producto por nombre o código...", placeholder="Escribe aquí..."
    ).lower()

    df_inv = st.session_state.inventario
    if busqueda:
      df_inv = df_inv[
          df_inv["codigo"].str.lower().str.contains(busqueda)
          | df_inv["articulo"].str.lower().str.contains(busqueda)
      ]

    for index, row in df_inv.iterrows():
      with st.container():
        c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
        with c1:
          st.write(f"**{row['articulo']}**")
          st.caption(f"Stock: {row['stock']} | Caducidad: {row['caducidad']}")
        with c2:
          st.markdown(f"**{row['p_venta']:.2f} €**")
        with c3:
          iva_sel = st.selectbox(
              "IVA",
              [21, 10, 4],
              key=f"iva_{row['codigo']}",
              label_visibility="collapsed",
          )
        with c4:
          if st.button("➕ Añadir", key=f"add_{row['codigo']}"):
            precio_con_iva = row["p_venta"] * (1 + iva_sel / 100.0)
            st.session_state.carrito.append({
                "codigo": row["codigo"],
                "articulo": f"{row['articulo']} (IVA {iva_sel}%)",
                "precio": precio_con_iva,
            })
            st.toast(f"✨ Añadido: {row['articulo']}")
      st.divider()

    # --- SECCIÓN DEL CARRITO Y FACTURACIÓN EMPRESA ---
    st.markdown("### 🧾 Ticket y Justificante para Empresa")

    if st.session_state.carrito:
      df_carrito = pd.DataFrame(st.session_state.carrito)
      st.dataframe(df_carrito[["articulo", "precio"]], use_container_width=True)

      total = df_carrito["precio"].sum()
      st.markdown(
          f"<h3 style='color: #4f46e5;'>Total a Pagar: {total:.2f} €</h3>",
          unsafe_allow_html=True,
      )

      # Opción de factura para reembolso de empresa
      with st.expander("🏢 Generar Justificante / Factura para Empresa"):
        st.markdown(
            "Introduce los datos del cliente que necesita el comprobante para"
            " su empresa:"
        )
        c_nombre = st.text_input("Nombre y Apellidos / Razón Social")
        c_nif = st.text_input("NIF / CIF de la Empresa")
        c_concepto = st.text_input("Concepto (ej. Dieta, Material Oficina)")

        if st.button("📄 Imprimir / Ver Justificante"):
          if c_nombre and c_nif:
            st.success(
                f"✅ Justificante generado correctamente para **{c_nombre}**"
                f" (NIF: {c_nif})"
            )
            st.markdown(f"""
                        > **MULTISERVICIOS RAMIREZ**
                        > -----------------------------------
                        > **Cliente:** {c_nombre}
                        > **NIF/CIF:** {c_nif}
                        > **Concepto:** {c_concepto or 'Compra habitual'}
                        > **Total Abonado:** {total:.2f} €
                        > **Atendido por:** {st.session_state.empleado_nombre}
                        > -----------------------------------
                        > *¡Gracias por su confianza!*
                        """)
          else:
            st.warning("⚠️ Por favor introduce al menos el Nombre y el NIF.")

      c1, c2 = st.columns(2)
      with c1:
        if st.button(
            "✅ Cobrar Venta", use_container_width=True, type="primary"
        ):
          st.balloons()
          st.success("🎉 ¡Venta cobrada con éxito!")
          st.session_state.carrito = []
          st.rerun()
      with c2:
        if st.button("❌ Cancelar", use_container_width=True):
          st.session_state.carrito = []
          st.rerun()
    else:
      st.info("🛒 El carrito está vacío. Selecciona productos arriba.")

  # --- GESTIÓN DE ARTÍCULOS ---
  elif menu == "📦 Gestión de Artículos":
    if st.session_state.rol_activo != "Administrador":
      st.warning(
          "⚠️ Zona exclusiva para el Administrador. Inicia sesión como Admin."
      )
    else:
      st.markdown("### 📦 Inventario y Control de Caducidades")
      st.dataframe(st.session_state.inventario, use_container_width=True)

      st.markdown("### ➕ Añadir Nuevo Producto con Caducidad")
      with st.form("form_nuevo"):
        ncod = st.text_input("Código de Barras")
        nart = st.text_input("Descripción del Producto")
        np_compra = st.number_input(
            "Precio de Compra (€)", min_value=0.0, value=0.0, step=0.01
        )
        np_venta = st.number_input(
            "Precio de Venta Base (€)", min_value=0.0, value=1.0, step=0.01
        )
        nstock = st.number_input("Existencias / Stock", value=0.0, step=1.0)
        ncad = st.date_input("Fecha de Caducidad", value=date.today())

        submitted = st.form_submit_button("Guardar en Inventario")
        if submitted and ncod and nart:
          nuevo = pd.DataFrame([{
              "codigo": ncod,
              "articulo": nart,
              "p_compra": np_compra,
              "p_venta": np_venta,
              "stock": nstock,
              "caducidad": str(ncad),
          }])
          st.session_state.inventario = pd.concat(
              [st.session_state.inventario, nuevo], ignore_index=True
          )
          st.success("🎉 ¡Artículo guardado con éxito!")
          st.rerun()

  # --- ALERTAS DE CADUCIDAD ---
  elif menu == "⚠️ Alertas de Caducidad":
    st.markdown("### ⚠️ Control de Alertas de Caducidad")
    st.markdown(
        "Aquí puedes revisar qué productos están próximos a caducar o ya han"
        " vencido."
    )

    hoy = date.today()
    inv = st.session_state.inventario.copy()

    inv["caducidad_dt"] = pd.to_datetime(inv["caducidad"]).dt.date

    caducados = inv[inv["caducidad_dt"] < hoy]
    por_caducar = inv[
        (inv["caducidad_dt"] >= hoy)
        & (inv["caducidad_dt"] <= pd.Timestamp(hoy.toordinal() + 30).date())
    ]

    st.markdown("#### 🔴 Productos Caducados")
    if not caducados.empty:
      st.error(
          "¡Atención! Hay productos que ya han superado su fecha de caducidad:"
      )
      st.dataframe(
          caducados[["codigo", "articulo", "stock", "caducidad"]],
          use_container_width=True,
      )
    else:
      st.success("✅ No hay ningún producto caducado.")

    st.markdown("#### 🟡 Productos Próximos a Caducar (Próximos 30 días)")
    if not por_caducar.empty:
      st.warning("Revisa estos artículos, caducan pronto:")
      st.dataframe(
          por_caducar[["codigo", "articulo", "stock", "caducidad"]],
          use_container_width=True,
      )
    else:
      st.success("✅ Todo en orden. No hay productos próximos a caducar.")

  # --- CONFIGURACIÓN DE NOMBRES ---
  elif menu == "⚙️ Configuración Nombres":
    if st.session_state.rol_activo != "Administrador":
      st.warning("⚠️ Solo el Administrador puede modificar los nombres.")
    else:
      st.markdown("### ⚙️ Personalizar Nombres de Turno y Administrador")
      with st.form("form_nombres"):
        nuevo_admin = st.text_input(
            "Nombre del Administrador", value=st.session_state.admin_nombre
        )
        nuevo_empleado = st.text_input(
            "Nombre del Empleado de Turno",
            value=st.session_state.empleado_nombre,
        )

        if st.form_submit_button("💾 Guardar Cambios"):
          st.session_state.admin_nombre = nuevo_admin
          st.session_state.empleado_nombre = nuevo_empleado
          st.success("🎉 ¡Nombres actualizados correctamente!")
          st.rerun()
