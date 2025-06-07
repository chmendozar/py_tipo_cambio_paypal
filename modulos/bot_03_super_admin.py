import logging
import configparser
import requests
from utilidades.excepciones import BusinessException
import variables_globales as vg

logger = logging.getLogger("Bot 03 - Super Admin")

def bot_run(cfg, mensaje="Bot 03 - Super Admin"):
    resultado = False
    try:
        # Leer configuración
        config = configparser.ConfigParser()
        config.read(cfg)
        username = ""
        password = ""
        compra = vg.tipo_cambio_compra
        venta = vg.tipo_cambio_venta
    
        # Leer URLs desde el archivo de configuración
        base_url = cfg["url"]["url_superadmin"]
        login_url = f"{base_url}{cfg['url'] ['url_login']}"
        exchange_rate_get_url = f"{base_url}{cfg['url']['url_tc_paypal_get']}"
        exchange_rate_save_url = f"{base_url}{cfg['url']['url_tc_paypal_post']}"

        # Crear una sesión para mantener las cookies
        session = requests.Session()

        # Datos del formulario de inicio de sesión
        login_data = {
            "usuario": username, 
            "password": password 
        }

        # Encabezados de la solicitud
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Realizar la solicitud POST para iniciar sesión
        login_response = session.post(login_url, data=login_data, headers=headers)

        # Verificar si el inicio de sesión fue exitoso
        if login_response.status_code == 200:
            login_result = login_response.json()
            if login_result.get("respuesta") == "00":
                logger.info(f"Inicio de sesión exitoso. Bienvenido {login_result.get('nombres')}!")

                # Validar si ya existen datos en el endpoint
                exchange_rate_get_response = session.get(exchange_rate_get_url, headers=headers)

                if exchange_rate_get_response.status_code == 200:
                    existing_data = exchange_rate_get_response.json()
                    logger.info("Datos existentes en el servidor: %s", existing_data)

                    # Verificar si los datos existentes coinciden con los valores deseados
                    if (
                        existing_data.get("status") == 1 and
                        existing_data.get("buy") == vg.tipo_cambio_compra and
                        existing_data.get("sell") == vg.tipo_cambio_venta
                    ):
                        compra = existing_data.get("buy")
                        venta = existing_data.get("sell")

                # Datos a enviar (ajusta los valores de 'buy' y 'sell' según sea necesario)
                exchange_rate_data = {
                    "buy": compra,  # Tipo de cambio de compra
                    "sell": venta  # Tipo de cambio de venta
                }

                # Realizar la solicitud POST para guardar el tipo de cambio
                exchange_rate_response = session.post(exchange_rate_save_url, data=exchange_rate_data, headers=headers)

                # Verificar si la solicitud fue exitosa
                if exchange_rate_response.status_code == 200:
                    response_json = exchange_rate_response.json()
                    logger.info("Respuesta del servidor: %s", response_json)

                    # Manejar la respuesta según el estado
                    if response_json.get("status") == 0:
                        logger.error("Error: %s", response_json.get("message"))
                    elif response_json.get("status") == 1:
                        logger.info("Correcto: %s", response_json.get("message"))
                        resultado = True
                    elif response_json.get("status") == 2:
                        logger.info("Información: %s", response_json.get("message"))
                else:
                    logger.error(f"Error al guardar el tipo de cambio: {exchange_rate_response.status_code}")
            else:
                raise BusinessException(f"Inicio de sesión fallido. Mensaje: {login_result.get('mensaje')}")
        else:
            raise BusinessException(f"Error en la solicitud de inicio de sesión: {login_response.status_code}")

    except BusinessException as be:
        logger.error(f"Error de negocio en bot_run: {be}")
        mensaje = f"Error de negocio: {be}"
    except Exception as e:
        logger.error(f"Error inesperado en bot_run: {e}")
        mensaje = f"Error inesperado: {e}"
    finally:
        logger.info("Fin del bot: %s", mensaje)
        return resultado, mensaje