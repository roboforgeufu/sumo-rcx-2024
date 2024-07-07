def ir_read_to_mm(percentage):
    """(tentativa de) conversão da leitura do InfraVermelho para uma distância em cm"""
    # Parábola obtida através da interpolação dos pontos (https://www.geogebra.org/m/qPAebsAc)
    # 0, 40
    # 50, 440
    # 100, 1200
    return (9 / 125) * percentage**2 + (22 / 5) * percentage + 40
