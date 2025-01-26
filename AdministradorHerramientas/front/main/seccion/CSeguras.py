import string
import random
import os
import subprocess

def contraseña_segura(longitud, incluir_minusculas=False, incluir_mayusculas=False, incluir_numeros=False, incluir_simbolos=False, nombre="Contraseña segura"):
    """Genera una contraseña segura de longitud especificada."""
    # Validar longitud
    if not isinstance(longitud, int) or longitud <= 0:
        raise ValueError("La longitud de la contraseña debe ser un número positivo.")

    # Definir caracteres permitidos
    caracteres = ""
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Debe incluir al menos un tipo de caracteres en la contraseña.")

    folder_name = "Contraseñas seguras"
    base_name = nombre
    extension = ".txt"

    # Generar y validar contraseña
    while True:
        contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
        if not caracteres_repetidos(contraseña):
            continue  # Generar otra si tiene demasiados caracteres repetidos
        return generar_archivo_contraseña(contraseña, folder_name, base_name, extension)

def caracteres_repetidos(contraseña):
    """Verifica si una contraseña tiene demasiados caracteres repetidos."""
    return len(set(contraseña)) >= len(contraseña) * 0.6

def generar_archivo_contraseña(contraseña, folder_name="Contraseñas seguras", base_name="Contraseña_segura", extension=".txt"):
    """Genera un archivo de texto con la contraseña."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    i = 1
    while os.path.exists(os.path.join(folder_name, f"{base_name}{i}{extension}")):
        i += 1
    filename = os.path.join(folder_name, f"{base_name}{i}{extension}")
    with open(filename, "w") as file:
        file.write(f"Su contraseña generada con el nombre {base_name} es: {contraseña}")

    # Abrir el archivo de manera automatica
    try:
        if os.name == "nt": #Para Windows
            os.startfile(filename)
        else:#Para otros sistemas operativos
            subprocess.call(["open", filename] if os.name == "posix" else ["xdg-open", filename])
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
    return filename
