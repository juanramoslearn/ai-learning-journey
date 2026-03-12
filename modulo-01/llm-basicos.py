import os
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

conversacion = [
    {"role": "system", "content": "Eres un asistente que explica conceptos de IA de forma simple."},
    {"role": "user", "content": "¿Qué es un token?"},
    {"role": "assistant", "content": "Un token es la unidad básica de texto que procesa un LLM."},
    {"role": "user", "content": "¿Y cuántos tokens tiene una palabra en español?"}
]

respuesta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversacion,
    max_tokens=20
)

print(respuesta.choices[0].message.content)
print(f"\nTokens totales: {respuesta.usage.total_tokens}")
print(f'Tokens enviados: {respuesta.usage.prompt_tokens}')
print(f'Razón de finalización: {respuesta.choices[0].finish_reason}')