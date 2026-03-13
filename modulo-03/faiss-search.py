import os
import json
import numpy as np
import faiss
from openai import OpenAI

client = OpenAI(
    base_url='https://models.github.ai/inference',
    api_key=os.environ['GITHUB_TOKEN']
)

def obtener_embeddings(texto, modelo='text-embedding-3-small'):
    respuesta = client.embeddings.create(
        input=texto,
        model=modelo
    )
    return respuesta.data[0].embedding

# Base de conocimiento
documentos = [
    'El proceso de nómina falla cuando hay empleados sin contrato activo',
    'Los errores de isolved se registran en el log de Azure Functions',
    'Para resetear una contraseña contactar al equipo de soporte',
    'El archivo Excel debe tener la columna employee_id en la primera hoja',
    'Los pagos se procesan los viernes antes de las 3pm'
]

# Construir índice FAISS
print('Construyendo índice...')
embeddings = [obtener_embeddings(doc) for doc in documentos]
matriz = np.array(embeddings, dtype='float32')

indice = faiss.IndexFlatL2(matriz.shape[1])
indice.add(matriz)
print(f'Índice construido con {indice.ntotal} vectores')

# Buscar
consulta = 'hay un problema procesando el pago'
embedding_consulta = np.array([obtener_embeddings(consulta)], dtype='float32')

distancias, indices = indice.search(embedding_consulta, k=2)

print(f'\nConsulta: "{consulta}"')
for i, idx in enumerate(indices[0]):
    print(f'{distancias[0][i]:.4f} -> {documentos[idx]}')