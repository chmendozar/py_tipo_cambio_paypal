import logging
import variables_globales as vg
from utilidades.limpieza import cerrarProcesos as Limpieza
from modulos.bot_00_configuracion import bot_run as Bot_00_Configuracion
from modulos.bot_01_tc_bloomberg import bot_run as Bot_01_Template

logger = logging.getLogger("Main - Orquestador")

def main():
    try:

        # Configuración del bot
        cfg = Bot_00_Configuracion()

        # Limpieza de ambiente
        lista_procesos = ["chrome.exe", "firefox.exe"]
        #Limpieza(lista_procesos)

        logger.info("Inicio del proceso ...")

        # Ejecutar bot
        Bot_01_Template(cfg, mensaje="Test 01")

        # Verificar si hay excepciones de negocio
        if vg.business_exception:
            logger.info("Enviando Notificacion por Error de Negocio...")
            return
        
        # Verificar si hay excepciones de sistema
        if vg.system_exception:
            logger.info("Enviando Notificacion por Error de Sistema...")
            return


    except Exception as e:
        logger.error(f"Error en main: {e}")
    finally:
        logger.info("Fin del proceso ...")

if __name__ == "__main__":
    main()