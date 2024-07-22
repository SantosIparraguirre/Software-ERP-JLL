from ui2 import iniciar_interfaz

if __name__ == "__main__":
    try:
        iniciar_interfaz()
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(str(e))
    input("Presiona Enter para salir...")