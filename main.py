#main.py
import subprocess
import sys

def main():
    print("Iniciando aplicación Streamlit...")
    
    # Usamos Popen en lugar de run para poder controlar el proceso hijo
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "ui/app.py"
    ])
    
    try:
        # Esperamos a que el proceso de Streamlit termine por sí solo
        process.wait()
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C, capturamos la excepción aquí
        print("\n\n⚠️ Interrupción detectada. Cerrando Streamlit...")
        
        # Terminamos el proceso hijo (Streamlit)
        process.terminate() 
        
        # Esperamos a que el proceso hijo muera completamente
        process.wait() 
        print("✅ Streamlit cerrado correctamente. ¡Adiós!")

if __name__ == "__main__":
    main()