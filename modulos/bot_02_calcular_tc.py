import logging
import variables_globales as vg
from utilidades.excepciones import BusinessException
from decimal import Decimal

logger = logging.getLogger("Bot 02 - Calcular TC")

def bot_run(cfg, mensaje="Bot 02 - Tipo cambio bloomberg"):
    resultado = False
    try:
        logger.info("Inicio del bot: %s", mensaje)
        logger.debug("Configuración recibida: %s", cfg)
        logger.debug("Tipo de cambio Bloomberg: %s", vg.tipo_cambio_bloomberg)

        # Obtener valores de las variables necesarias
        valor_inicial = cfg['valores']['inicial']
        valor_final = cfg['valores']['final']
        valor_brecha = cfg['valores'].get('brecha', 0)
        logger.debug("Rango inicial: %s, Rango final: %s, Brecha: %s", valor_inicial, valor_final, valor_brecha)

        # Cálculos de tipo de cambio compra y venta
        vg.tipo_cambio_compra = round(Decimal(vg.tipo_cambio_bloomberg) * (1 - Decimal(valor_brecha) / 100), 4)
        vg.tipo_cambio_venta = round(Decimal(vg.tipo_cambio_bloomberg) * (1 + Decimal(valor_brecha) / 100), 4)
        logger.debug("Tipo de cambio compra: %s, Tipo de cambio venta: %s", vg.tipo_cambio_compra, vg.tipo_cambio_venta)

        # Validar rangos de tipos de cambio
        if ((vg.tipo_cambio_compra < 3 or vg.tipo_cambio_compra > 5) or (vg.tipo_cambio_venta < 3 or vg.tipo_cambio_venta > 5)):
            logger.warning("Error de negocio: Tipo de cambio fuera de rango permitido.")

        # Verificar condiciones para TC Compra
        if Decimal(vg.tipo_cambio_compra) > Decimal(valor_inicial) and Decimal(vg.tipo_cambio_compra) < Decimal(valor_final):
            mensaje = f'Se cumple la condición para tc Compra: {valor_inicial} < {vg.tipo_cambio_compra} < {valor_final}'
            resultado = True
            logger.info("Condición cumplida para TC Compra.")
        else:
            mensaje = f'No se cumple la condición para tc Compra: {valor_inicial} < {vg.tipo_cambio_compra} < {valor_final}'
            logger.info("Condición no cumplida para TC Compra.")

        # Verificar condiciones para TC Venta
        if Decimal(vg.tipo_cambio_venta) > Decimal(valor_inicial) and Decimal(vg.tipo_cambio_venta) < Decimal(valor_final) and resultado:
            mensaje += f' - Se cumple la condición para tc Venta: {valor_inicial} < {vg.tipo_cambio_venta} < {valor_final}'
            resultado = True
            logger.info("Condición cumplida para TC Venta.")
        else:
            mensaje += f' - No se cumple la condición para tc Venta: {valor_inicial} < {vg.tipo_cambio_venta} < {valor_final}'
            logger.info("Condición no cumplida para TC Venta.")

        logger.debug("Resultados guardados en variables globales: %s", {
            'boo_respuesta': resultado,
            'out_str_mensaje': mensaje,
        })

    except BusinessException as be:
        logger.error(f"Error de negocio en bot_run: {be}")
        resultado, mensaje = False, f"Error de negocio: {be}"

    except Exception as e:
        logger.error(f"Error inesperado en bot_run: {e}")
        resultado, mensaje =  False, f"Error inesperado: {e}"

    finally:
        logger.info("Fin del proceso ...")
        return resultado, mensaje