import os
import faiss
import numpy as np
from openai import OpenAI
import json

client = OpenAI(
    base_url='https://models.github.ai/inference',
    api_key=os.environ['GITHUB_TOKEN']
)

# Base de conocimiento
documentos = [
    'El Banco de la República subió la tasa de interés en 100 puntos básicos a 10.25% en enero de 2026, sorprendiendo a los mercados.',
    'BTG Pactual proyecta que el Banco de la República subirá la tasa hasta 11.25% en 2026, siendo Colombia el único país de América Latina subiendo tasas este año.',
    'La TRM del dólar en Colombia el 11 de marzo de 2026 es de COP 3,710.5. En el último mes el dólar pasó de 3,668 a más de 3,750.',
    'El conflicto en Oriente Medio tiene cerrado el estrecho de Ormuz, por donde pasa el 20% del petróleo mundial, lo que aumenta la volatilidad del dólar.',
    'El Plan Financiero 2026 del Ministerio de Hacienda proyecta inflación del 5.1% para 2026, lejos de la meta del 3% del Banco de la República.',
    'El gobierno de Petro revisó a la baja el precio del petróleo esperado a 68 dólares por barril, por debajo de los 74 dólares proyectados antes.',
    'La economía colombiana creció 2.6% en 2025 y se proyecta un cecimiento en 2.8% del PIB en 2026, sustentado en consumo y remesas.',
    'El peso colombiano se valorizó 15% en 2025, cerrando en 3,744 pesos por dólar, impulsado por debilidad global del dólar y flujo de remesas.'
]

def obtener_embedding(texto):
    respuesta = client.embeddings.create(
        input=texto,
        model='text-embedding-3-small'
    )
    return respuesta.data[0].embedding

# Construir índice
print('Construyendo índice...')
embeddings = [obtener_embedding(doc) for doc in documentos]
matriz = np.array(embeddings, dtype='float32')
indice = faiss.IndexFlatL2(matriz.shape[1])
indice.add(matriz)
print(f'Índice listo con {indice.ntotal} documentos\n')

def rag(pregunta, top_k=2):
    embedding_pregunta = np.array([obtener_embedding(pregunta)], dtype='float32')
    _, indices = indice.search(embedding_pregunta, k=top_k)
    chunks = [documentos[i] for i in indices[0]]

    contexto = '\n'.join(f'- {chunk}' for chunk in chunks)
    prompt = f'''Eres un asistente de finanzas personales especializado en Colombia.
    Responde SOLO con base en el contexto proporcionado. Si la información no está en el contexto, dilo claramente.

    Contexto:
    {contexto}

    Pregunta: {pregunta}'''

    respuesta = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role':'user','content':prompt}],
        max_tokens=200
    )

    return respuesta.choices[0].message.content, contexto, respuesta.usage.total_tokens, respuesta.choices[0].finish_reason

# Pruebas
preguntas = [
    '¿Conviene comprar dólares ahora?',
    '¿Cómo está la inflación en Colombia?',
    '¿Qué pasó con el petróleo?'
]

for pregunta in preguntas:
    respuesta, fuentes, uso, terminacion = rag(pregunta)
    print(f'Pregunta: {pregunta}')
    print(f'Respuesta: {respuesta}')
    print(f'Fuentes:\n{fuentes}')
    print(f'Tokens Totales: {uso}')
    print(f'Terminación: {terminacion}')
    print()

# Persistir índice y documentos
faiss.write_index(indice, 'indice-finanzas.faiss')
with open('documentos.json', 'w') as f:
    json.dump(documentos, f, ensure_ascii=False)

print('Índice y documentos guardados')