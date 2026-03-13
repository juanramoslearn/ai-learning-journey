import os
from openai import OpenAI

def crear_cliente():
    return OpenAI(
        base_url='https://models.github.ai/inference',
        api_key=os.environ['GITHUB_TOKEN']
    )

def llamar_modelo(client, conversacion, modelo='gpt-4o-mini', max_tokens=200):
    respuesta = client.chat.completions.create(
        model=modelo,
        messages=conversacion,
        max_tokens=max_tokens
    )

    if respuesta.choices[0].finish_reason == 'length':
        print('Advertencia: respuesta cortada')
    
    return respuesta.choices[0].message.content

# Prueba básica
client = crear_cliente()

conversacion = []
prompt_1 = '¿Cuál es la capital de Colombia'
conversacion.append({'role':'user','content':prompt_1})

respuesta_1 = llamar_modelo(client, conversacion)
print(respuesta_1)
conversacion.append({'role':'assistant','content':respuesta_1})

prompt_2 = '¿Y la de Brasil?'
conversacion.append({'role':'user','content':prompt_2})

respuesta_2 = llamar_modelo(client, conversacion)
print(respuesta_2)