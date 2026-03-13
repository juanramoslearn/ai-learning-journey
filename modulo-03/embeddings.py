import os
from openai import OpenAI
import math
import json

client = OpenAI(
    base_url='https://models.github.ai/inference',
    api_key=os.environ['GITHUB_TOKEN']
)

def obtener_embedding(texto, modelo='text-embedding-3-small'):
    respuesta = client.embeddings.create(
        input=texto,
        model=modelo
    )
    return respuesta.data[0].embedding

def similitud_coseno(vec1, vec2):
    producto_punto = sum(a * b for a,b in zip(vec1, vec2))
    magnitud1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitud2 = math.sqrt(sum(a ** 2 for a in vec2))
    return producto_punto / (magnitud1 * magnitud2)

def buscar(consulta, documentos, top_n=2):
    embedding_consulta = obtener_embedding(consulta)
    resultados = []

    for doc in documentos:
        embedding_doc = obtener_embedding(doc)
        score = similitud_coseno(embedding_consulta, embedding_doc)
        resultados.append((score, doc))
    
    resultados.sort(reverse=True)
    return resultados[:top_n]

def guardar_embeddings(documentos, archivo='embeddings.json'):
    datos = []
    for doc in documentos:
        embedding = obtener_embedding(doc)
        datos.append({'texto':doc, 'embedding': embedding})
    
    with open(archivo, 'w') as f:
        json.dump(datos, f)
    print(f'Guardados {len(datos)} embeddings en {archivo}')

def cargar_y_buscar(consulta, archivo='embeddings.json', top_n=2):
    with open(archivo, 'r') as f:
        datos = json.load(f)

    embedding_consulta = obtener_embedding(consulta)
    resultados = []

    for item in datos:
        score = similitud_coseno(embedding_consulta, item['embedding'])
        resultados.append((score, item['texto']))

    resultados.sort(reverse=True)
    return resultados[:top_n]

# # Primera prueba
# embedding = obtener_embedding('error en el procesamiento de nómina')
# print(f'Tipo: {type(embedding)}')
# print(f'Dimensiones: {len(embedding)}')
# print(f'Primeros 5 números: {embedding[:5]}')

# # Comparar frases
# frases = [
#     "error en el procesamiento de nómina",
#     "fallo al calcular el pago de empleados",
#     "el clima de Bogotá hoy"
# ]

# consulta = 'problema con la nómina'
# embedding_consulta = obtener_embedding(consulta)

# for frase in frases:
#     embedding_frase = obtener_embedding(frase)
#     similitud = similitud_coseno(embedding_consulta, embedding_frase)
#     print(f'{similitud:.4f} -> {frase}')

# Mini base de conocimiento
documentos = [
    'El proceso de nómina falla cuando hay empleados sin contrato activo',
    'Los errores de isolved se registran en el log de Azure Functions',
    'Para resetear una contraseña contactar al equipo de soporte',
    'El archivo Excel debe tener la columna employee_id en la primera hoja',
    'Los pagos se procesan los viernes antes de las 3 pm'
]

# # Prueba
# consulta = 'hay un problema procesando el pago'
# print(f"\nConsulta: '{consulta}'")
# for score, doc in buscar(consulta, documentos):
#     print(f'{score:.4f} -> {doc}')

# Guardar una vez
guardar_embeddings(documentos)

# Buscar y recalcular
consulta = 'hay un problema procesando el pago'
print(f'\nConsulta: "{consulta}"')
for score, doc in cargar_y_buscar(consulta):
    print(f'{score:.4f} -> {doc}')