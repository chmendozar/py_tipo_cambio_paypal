import logging
from utilidades.excepciones import BusinessException
import variables_globales as vg
import requests
from bs4 import BeautifulSoup
from lxml import html

logger = logging.getLogger("Bot 01 - Tipo cambio bloomberg")

def extrer_tipo_cambio_bloomberg(cfg):
    """
    Función para extraer el tipo de cambio de Bloomberg utilizando XPath y BeautifulSoup como fallback.
    """
    tipo_cambio = None
    try:
        url = cfg["url"]["url_bloomberg"]
        # Usar un User-Agent menos común para evitar detección de actividad inusual
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Método 1: Usando XPath con lxml
        try:
            tree = html.fromstring(response.content)
            xpath_selector = "//main//*[@data-component='sized-price']"
            elementos = tree.xpath(xpath_selector)
            
            if elementos and len(elementos) > 0:
                tipo_cambio = elementos[0].text_content().strip()
                logger.info(f"Tipo de cambio obtenido con XPath: {tipo_cambio}")
                return tipo_cambio
        except Exception as xpath_error:
            logger.warning(f"Error al usar XPath: {xpath_error}, intentando con BeautifulSoup...")
        
        # Método 2: Usando BeautifulSoup como fallback
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Intento 1: Selector específico dentro de main
        tipo_cambio_element = soup.select_one("main [data-component='sized-price']")
        
        if tipo_cambio_element:
            tipo_cambio = tipo_cambio_element.text.strip()
            logger.info(f"Tipo de cambio obtenido con BeautifulSoup (selector específico): {tipo_cambio}")
            return tipo_cambio
        
        # Intento 2: Selector más genérico
        tipo_cambio_element = soup.select_one("[data-component='sized-price']")
        
        if tipo_cambio_element:
            tipo_cambio = tipo_cambio_element.text.strip()
            logger.info(f"Tipo de cambio obtenido con BeautifulSoup (selector genérico): {tipo_cambio}")
            return tipo_cambio
        
        # Intento 3: Buscar por clase que contiene "Price"
        tipo_cambio_element = soup.select_one("[class*='Price']")
        
        if tipo_cambio_element:
            tipo_cambio = tipo_cambio_element.text.strip()
            logger.info(f"Tipo de cambio obtenido con BeautifulSoup (clase Price): {tipo_cambio}")
            return tipo_cambio
            
        # Si llegamos aquí, ningún método funcionó
        raise BusinessException("No se encontró el tipo de cambio en la página de Bloomberg con ningún método")
            
    except requests.exceptions.RequestException as req_error:
        logger.error(f"Error en la solicitud HTTP: {req_error}")
        raise BusinessException(f"Error al conectar con Bloomberg: {str(req_error)}")
    except BusinessException as be:
        # Reenviar excepciones de negocio
        logger.error(f"Error de negocio: {be}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al extraer el tipo de cambio de Bloomberg: {e}")
        raise BusinessException(f"Error inesperado al extraer el tipo de cambio: {str(e)}")
    finally:
        # Si llegamos aquí sin encontrar el tipo de cambio, será None
        return tipo_cambio

def limpiar_tipo_cambio(tipo_cambio_str):
    """
    Limpia el string del tipo de cambio para convertirlo a un número flotante.
    """
    if not tipo_cambio_str:
        return None
        
    try:
        # Elimina caracteres no numéricos excepto el punto decimal
        import re
        numero_limpio = re.sub(r'[^\d.]', '', tipo_cambio_str)
        return float(numero_limpio)
    except ValueError:
        logger.error(f"No se pudo convertir '{tipo_cambio_str}' a un número")
        return None

def bot_run(cfg, mensaje="Bot 01 - Tipo cambio bloomberg"):
    resultado = False
    try:
        logger.info(f"Iniciando {mensaje}")
        tipo_cambio_str = extrer_tipo_cambio_bloomberg(cfg)
        
        if tipo_cambio_str:
            # Convertir a número si es necesario
            tipo_cambio_num = limpiar_tipo_cambio(tipo_cambio_str)
            logger.info(f"Tipo de cambio de Bloomberg extraído con éxito: {tipo_cambio_num}")
            vg.tipo_cambio_bloomberg = tipo_cambio_num
            resultado = True
        else:
            logger.warning("No se pudo obtener el tipo de cambio")
            resultado = False
        
    except BusinessException as be:
        logger.error(f"Error de negocio en bot_run: {be}")
        mensaje = f"Error de negocio: {be}"
        resultado = False
    except Exception as e:
        logger.error(f"Error inesperado en bot_run: {e}")
        mensaje = f"Error inesperado: {e}"
        resultado = False
    finally:
        logger.info("Fin del proceso ...")
        return resultado, mensaje