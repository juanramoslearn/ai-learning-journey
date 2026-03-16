import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"]
)

# Las herramientas que el agente puede usar
def obtener_tasa_dolar():
    """Simula consultar la TRM actual"""
    return {"tasa": 3710.5, "fecha": "2026-03-15", "fuente": "Banco de la República"}

def calcular_conversion(monto_cop, tasa):
    """Convierte pesos colombianos a dólares"""
    return {"monto_usd": round(monto_cop / tasa, 2), "monto_cop": monto_cop, "tasa_usada": tasa}

# Definición de herramientas para el modelo
herramientas = [
    {
        "type": "function",
        "function": {
            "name": "obtener_tasa_dolar",
            "description": "Obtiene la tasa de cambio actual del dólar en Colombia (TRM)",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_conversion",
            "description": "Convierte un monto en pesos colombianos a dólares",
            "parameters": {
                "type": "object",
                "properties": {
                    "monto_cop": {"type": "number", "description": "Monto en pesos colombianos"},
                    "tasa": {"type": "number", "description": "Tasa de cambio a usar"}
                },
                "required": ["monto_cop", "tasa"]
            }
        }
    }
]

def ejecutar_herramienta(nombre, argumentos):
    if nombre == "obtener_tasa_dolar":
        return obtener_tasa_dolar()
    elif nombre == "calcular_conversion":
        return calcular_conversion(**argumentos)

def agente(pregunta):
    mensajes = [{"role": "user", "content": pregunta}]
    
    while True:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            tools=herramientas
        )
        
        mensaje = respuesta.choices[0].message
        
        # Si no hay tool calls, el agente terminó
        if not mensaje.tool_calls:
            return mensaje.content
        
        # Ejecutar cada herramienta que pidió el modelo
        mensajes.append(mensaje)
        for tool_call in mensaje.tool_calls:
            nombre = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments)
            resultado = ejecutar_herramienta(nombre, argumentos)
            
            print(f"  → Herramienta usada: {nombre}({argumentos})")
            
            mensajes.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultado)
            })

# Prueba
print('Pregunta: ¿Cuántos dólares son 500,000 pesos?')
respuesta = agente('¿Cuántos dólares son 500,000 pesos colombianos')
print(f'Respuesta: {respuesta}\n')

print('Pregunta: ¿A cuánto está el dólar hoy?')
respuesta = agente('¿A cuánto está el dólar hoy?')
print(f'Respuesta: {respuesta}')