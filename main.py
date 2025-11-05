# main.py (en la raíz del repo)
import uvicorn

if __name__ == "__main__":
    # Ejecuta con: python main.py
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=False)
