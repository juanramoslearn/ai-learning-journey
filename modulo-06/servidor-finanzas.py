import requests
from mcp.server.fastmcp import FastMCP

# Crear el servidor MCP
mcp = FastMCP("Finanzas Colombia")

@mcp.tool()
def obtener_tasa_dolar() -> dict:
    """Obtiene la tasa de cambio actual del dólar en Colombia (TRM)"""
    try:
        url = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=1&$order=vigenciadesde DESC"
        respuesta = requests.get(url, timeout=5)
        dato = respuesta.json()[0]
        return {
            "tasa": float(dato["valor"]),
            "fecha": dato["vigenciadesde"][:10],
            "fuente": "Banco de la República Colombia"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calcular_conversion(monto_cop: float) -> dict:
    """Convierte un monto en pesos colombianos a dólares usando la TRM actual"""
    tasa_info = obtener_tasa_dolar()
    if "error" in tasa_info:
        return tasa_info
    tasa = tasa_info["tasa"]
    return {
        "monto_cop": monto_cop,
        "monto_usd": round(monto_cop / tasa, 2),
        "tasa_usada": tasa
    }

@mcp.tool()
def obtener_inflacion_colombia() -> dict:
    """Retorna la inflación proyectada de Colombia según el Plan Financiero 2026"""
    return {
        "inflacion_proyectada": 5.1,
        "meta_banrep": 3.0,
        "año": 2026,
        "fuente": "Ministerio de Hacienda - Plan Financiero 2026"
    }

if __name__ == "__main__":
    mcp.run()