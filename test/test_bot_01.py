import modulos.bot_01_tc_bloomberg as Bot_01

# pytest -v <- Ejecutar todos los tests
# pytest -v test/test_bot_01.py <- Ejecutar tests del archivo
# pytest -v test/test_bot_01.py::test_hola_mundo <- Ejecutar unico test

def test_hola_mundo():
    assert Bot_01.hola_mundo() == "Hola mundo"

def test_hola_error():
    try:
        Bot_01.hola_error()
    except Exception as e:
        assert str(e) == "Error de negocio - Hola error"

def test_hola_api():
    # Validar estado 200 de la API
    res, status = Bot_01.hola_api("https://api.nationalize.io/?name=nathaniel")
    assert status == 200