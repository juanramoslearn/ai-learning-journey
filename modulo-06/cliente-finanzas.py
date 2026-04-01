import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["servidor-finanzas.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Ver qué herramientas ofrece el servidor
            herramientas = await session.list_tools()
            print("Herramientas disponibles:")
            for h in herramientas.tools:
                print(f"  - {h.name}: {h.description}")

            # Llamar una herramienta
            print("\nConsultando TRM...")
            resultado = await session.call_tool("obtener_tasa_dolar", {})
            print(f"Resultado: {resultado.content[0].text}")

asyncio.run(main())