import pytest
import pandas as pd
from src.bollinger_bands import BollingerBands

def test_bollinger_calculation():
    """
    Verifica que las Bandas de Bollinger se calculen correctamente con suficientes datos.
    """
    # Crear datos de ejemplo con más de 20 filas
    data = {'Close': [10, 12, 13, 15, 17, 20, 21, 19, 18, 17, 22, 23, 25, 24, 27, 30, 29, 28, 26, 25, 24]}
    df = pd.DataFrame(data)

    # Calcular Bandas de Bollinger
    BollingerBands.calculate(df)

    # Verificar que las columnas se crean
    assert 'Bol_Up' in df.columns, "La columna Bol_Up no fue creada."
    assert 'Bol_Down' in df.columns, "La columna Bol_Down no fue creada."
    assert 'EMA20' in df.columns, "La columna EMA20 no fue creada."

    # Verificar que las Bandas de Bollinger no están vacías
    assert not df['Bol_Up'].isna().all(), "Bol_Up está vacío."
    assert not df['Bol_Down'].isna().all(), "Bol_Down está vacío."

def test_bollinger_insufficient_data():
    """
    Verifica que se manejen correctamente los casos con datos insuficientes.
    """
    # Crear datos insuficientes (menos de 20 filas)
    data = {'Close': [10, 12, 13, 15, 17]}
    df = pd.DataFrame(data)

    # Verificar que se lanza un error
    with pytest.raises(ValueError, match="Se requieren al menos 20 datos"):
        BollingerBands.calculate(df)
