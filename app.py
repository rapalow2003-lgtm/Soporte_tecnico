import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="Soporte Técnico en la Nube",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Centro de Soporte Técnico en la Nube")
st.subheader("Sistema de Reportes de Incidencias")
st.markdown("Por favor, complete el siguiente formulario para enviar una incidencia al equipo de administración.")

def es_correo_valido(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def enviar_correo(nombre, correo_usuario, tipo_problema, prioridad, descripcion):
    try:
        smtp_server = st.secrets["smtp"]["server"]
        smtp_port = int(st.secrets["smtp"]["port"])
        sender_email = st.secrets["smtp"]["email"]
        sender_password = st.secrets["smtp"]["password"]
        admin_email = st.secrets["smtp"]["admin_email"]

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = admin_email
        msg['Subject'] = f"Nueva Incidencia [{prioridad}]: {tipo_problema} - {nombre}"

        cuerpo_mensaje = f"""
        Se ha registrado un nuevo reporte de soporte técnico:

        --------------------------------------------------
        DATOS DEL USUARIO
        --------------------------------------------------
        Nombre: {nombre}
        Correo de Contacto: {correo_usuario}

        --------------------------------------------------
        DETALLES DE LA INCIDENCIA
        --------------------------------------------------
        Tipo de Problema: {tipo_problema}
        Nivel de Prioridad: {prioridad}

        Descripción detallada:
        {descripcion}
        --------------------------------------------------
        Este mensaje fue generado automáticamente por la aplicación de Soporte Técnico en la Nube.
        """
        
        msg.attach(MIMEText(cuerpo_mensaje, 'plain', 'utf-8'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True, None
    except Exception as e:
        return False, str(e)

with st.form(key="formulario_soporte", clear_on_submit=False):
    nombre = st.text_input("Nombre completo *")
    correo = st.text_input("Correo electrónico de contacto *")
    
    opciones_problema = [
        "Seleccione una opción...",
        "Fallo de Acceso / Autenticación",
        "Error de Rendimiento / Lenteza",
        "Problema de Red / Conectividad",
        "Error en la Interfaz de Usuario",
        "Otro"
    ]
    tipo_problema = st.selectbox("Tipo de problema *", opciones_problema)
    
    prioridad = st.radio(
        "Nivel de prioridad *",
        ["Baja", "Media", "Alta", "Crítica"],
        horizontal=True
    )
    
    descripcion = st.text_area("Descripción detallada del problema *", height=150)
    
    boton_enviar = st.form_submit_button(label="Enviar reporte")

if boton_enviar:
    errores = []

    if not nombre.strip():
        errores.append("El campo 'Nombre completo' es obligatorio.")
        
    if not correo.strip():
        errores.append("El campo 'Correo electrónico' es obligatorio.")
    elif not es_correo_valido(correo):
        errores.append("El formato del correo electrónico ingresado no es válido.")

    if tipo_problema == "Seleccione una opción...":
        errores.append("Debe seleccionar un 'Tipo de problema'.")

    if not descripcion.strip():
        errores.append("Debe ingresar una 'Descripción detallada' de la incidencia.")

    if errores:
        for error in errores:
            st.error(f"❌ {error}")
    else:
        with st.spinner("Enviando reporte al administrador..."):
            exito, mensaje_error = enviar_correo(nombre, correo, tipo_problema, prioridad, descripcion)
            
            if exito:
                st.success("¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador.")
                st.balloons()
            else:
                st.error(f"Error al enviar el correo: {mensaje_error}")
