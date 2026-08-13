# Proyecto: Servicio de Soporte Técnico en la Nube

## 1. Objetivo del Proyecto
Desarrollar y desplegar una aplicación web ligera en la nube utilizando Python y Streamlit que permita a los usuarios reportar incidencias técnicas. El sistema valida los datos ingresados y notifica automáticamente al administrador mediante correo electrónico sin almacenar información de manera permanente.


## 3. Tecnologías Utilizadas
* **Lenguaje:** Python 3.10+
* **Framework Web:** Streamlit
* **Envío de Correo:** Módulo nativo `smtplib` y `email.mime`
* **Despliegue:** Streamlit Community Cloud

## 4. Funcionamiento de la Aplicación
1. El usuario accede al formulario web e ingresa sus datos (Nombre, Correo, Tipo de problema, Prioridad y Descripción).
2. El sistema valida en tiempo real que todos los campos requeridos estén llenos y que el correo cumpla con la estructura válida.
3. Si los datos son válidos, se genera un mensaje formateado y se envía por protocolo SMTP al administrador.
4. Se muestra un mensaje de confirmación en pantalla ("¡Reporte enviado correctamente!...").
5. La información no se guarda en bases de datos ni archivos locales.

## 5. Gestión Segura de Credenciales
Las credenciales del servidor de correo SMTP (usuario, contraseña de aplicación, puerto y servidor) no están escritas en el código fuente. Se gestionan mediante el mecanismo de **Secrets** de Streamlit (`.streamlit/secrets.toml` en entorno local y la sección *Secrets* del panel de control de Streamlit Community Cloud).

## 6. Procedimiento de Ejecución Local
```bash
pip install -r requirements.txt
streamlit run app.py
