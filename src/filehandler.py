import os
import shutil


def static_files_handler():
    if os.path.exists("./public"):
        # shutil.rmtree("./public")

        print("existe public")

    # borra public
    # crea public
    # detecta si existe static
    #
    # funcion duplicar_directorio(origen, destino)
    #   si origen está vacío
    #       return
    #
    #   elementos es igual a lista origen
    #   por cada elemento en elementos
    #       imprime origen
    #       ruta_origen = origen + elemento
    #       ruta_destino = destino + elemento
    #       si ruta_origen es directorio
    #           crea ruta_destino
    #           duplicar_directorio(ruta_origen, ruta_destino)
    #       o
    #           copiar archivo en destino

    pass
