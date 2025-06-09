import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# Fecha actual
FECHA = datetime.now().strftime('%d-%m-%y')

# Configuración de la página
st.set_page_config(
    page_title="DaTASA",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ruta al archivo de Excel con los proyectos
BD = './BD.xlsx'
TEMPORADAS = load_workbook(BD, read_only=True).sheetnames

# Sidebar
st.sidebar.header('Proyectos :anchor:')
selector_temporada = st.sidebar.selectbox("Seleccione Tipo de Buque:", TEMPORADAS, index=0)
df_proyecto = pd.read_excel(BD, sheet_name=selector_temporada)

selector_proyecto = st.sidebar.multiselect("Seleccione proyectos:", df_proyecto['Proyecto'].drop_duplicates())

# Título principal
st.title(":ship: Control de Proyectos")

# Lista de columnas para el primer cuadro (datos generales)
columnas_superiores = ["Manga", "Eslora", "Puntal"]

# Lista de columnas para el segundo cuadro (seguimiento u otros)
columnas_extra = ["Temporada Gestion de Astillero", "Costo Total (PEN)", "Identificador"]

if selector_proyecto:
    chata_path = 'CHATA.xlsx'

    for proyecto in selector_proyecto:
        try:
            df_historial = pd.read_excel(chata_path, sheet_name=proyecto)

            # ================== CUADRO 1 ==================
            columnas_1 = [col for col in columnas_superiores if col in df_historial.columns]
            if columnas_1:
                # Extraer una fila como Serie
                info_general = df_historial[columnas_1].iloc[0]

            st.subheader(f"📋 Información Técnica del proyecto: {proyecto}")
            for col in columnas_1:
                st.markdown(f"**{col}:** {info_general[col]}")

            # ================== CUADRO 2 ==================
            columnas_2 = [col for col in columnas_extra if col in df_historial.columns]
            if columnas_2:
                info_extra = df_historial[columnas_2].iloc[0:3].copy()

                 # Formatear columna de costos con símbolo S/.
                if "Costo Total (PEN)" in info_extra.columns:
                     info_extra["Costo Total (PEN)"] = info_extra["Costo Total (PEN)"].apply(lambda x: f"S/. {x:,.2f}")

                st.subheader(f"🧾 Seguimiento de proyecto: {proyecto}")
                st.dataframe(info_extra)

            # ================== CUADRO 3 ==================
            columnas_usadas = columnas_1 + columnas_2
            df_tecnico = df_historial.drop(columns=columnas_usadas, errors='ignore')
            st.subheader(f"📏 Historial metrado del proyecto: {proyecto}")
            st.dataframe(df_tecnico)

        except Exception as e:
            st.error(f"❌ No se pudo cargar la hoja '{proyecto}' en {chata_path}. Error: {e}")
