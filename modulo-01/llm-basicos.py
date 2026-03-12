import os
from openai import OpenAI

client = OpenAI(
base_url='https://models.inference.ai.azure.com',
api_key=os.environ["GITHUB_TOKEN"]
)

respuesta = client.chat.completions.create(
model='gpt-4o-mini',
messages=[
{'role':'user','content':'¿Qué es un token en el contexto de los LLMs? Explícalo en 3 líneas.'}
]
)

print(respuesta.choices[0].message.content)
