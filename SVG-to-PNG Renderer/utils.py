def normalize_value(value, canvas_dim):
    """
    Normalizează o valoare bazată pe dimensiunile canvas-ului și pe unități.

    Args:
        value (str | int): Valoarea ce trebuie normalizată (de ex., '50%', '100px').
        canvas_dim (float): Dimensiunea canvas-ului pentru normalizare.

    Returns:
        int: Valoarea normalizată, ca număr întreg.
    """
    if isinstance(value, str):
        value = value.strip().lower()

        if value.endswith('%'):
            return int(float(value[:-1]) * canvas_dim / 100)
        elif value.endswith('px'):
            return int(value[:-2])
        elif value.endswith('em'):
            return int(float(value[:-2]) * 16)
        elif value.endswith('pt'):
            return int(float(value[:-2]) * 1.333)
        elif value.endswith('cm'):
            return int(float(value[:-2]) * 37.795)
        elif value.endswith('mm'):
            return int(float(value[:-2]) * 3.7795)
        elif value.endswith('in'):
            return int(float(value[:-2]) * 96)
        else:
            return int(value)
    return int(value)

