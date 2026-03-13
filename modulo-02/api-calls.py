import os
from openai import OpenAI

def crear_cliente():
    return OpenAI(
        base_url='https://models.github.ai/inference',
        api_key=os.environ['GITHUB_TOKEN']
    )

def llamar_modelo(client, conversacion, modelo='gpt-4o-mini', max_tokens=200):
    try:
        respuesta = client.chat.completions.create(
            model=modelo,
            messages=conversacion,
            max_tokens=max_tokens
        )

        if respuesta.choices[0].finish_reason == 'length':
            print('Advertencia: respuesta cortada')
        
        return respuesta.choices[0].message.content
    
    except Exception as e:
        print(f'Error al llamar al modelo: {e}')
        return None

def llamar_modelo_stream(client, conversacion, modelo='gpt-4o-mini'):
    stream = client.chat.completions.create(
        model=modelo,
        messages=conversacion,
        stream=True
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='', flush=True)
    print()

# Prueba básica
client = crear_cliente()

# conversacion = []
# prompt_1 = '¿Cuál es la capital de Colombia'
# conversacion.append({'role':'user','content':prompt_1})

# respuesta_1 = llamar_modelo(client, conversacion)
# print(respuesta_1)
# conversacion.append({'role':'assistant','content':respuesta_1})

# prompt_2 = '¿Y la de Brasil?'
# conversacion.append({'role':'user','content':prompt_2})

# respuesta_2 = llamar_modelo(client, conversacion)
# print(respuesta_2)
# conversacion.append({'role':'assistant','content':respuesta_2})

# # Error simple
# resultado = llamar_modelo(client, conversacion, modelo='modelo inventado')
# print(f'Resultado con error: {resultado}')

# Probar modelo stream
conversacion = [{'role':'user','content':'Explícame qué es el streaming en APIs en 3 líneas'}]
llamar_modelo_stream(client, conversacion)