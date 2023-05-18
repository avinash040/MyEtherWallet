import httpx
import asyncio
import nest_asyncio

nest_asyncio.apply()

QUART_APP_URL = 'http://localhost:5003'
ETHEREUM_ADDRESS = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'  # Set your Ethereum address here
CONTRACT_ADDRESS = 'contract_address'  # Set your contract address here

async def test_get_balance():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/balance/{ETHEREUM_ADDRESS}')
        print(f"Status code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Response: {response.text}")
        try:
            print(response.json())
        except Exception as e:
            print(f"Error parsing JSON: {e}")



async def test_get_token_balance():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/tokenbalance/{ETHEREUM_ADDRESS}/{CONTRACT_ADDRESS}')
    print(response.json())

async def test_get_normal_transactions():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/txlist/{ETHEREUM_ADDRESS}')
    print(response.json())

async def test_get_internal_transactions():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/txlistinternal/{ETHEREUM_ADDRESS}')
    print(response.json())

async def test_get_erc20_transfer_events():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f'{QUART_APP_URL}/tokentx/{ETHEREUM_ADDRESS}')
    print(response.json())

async def test_get_erc721_transfer_events():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/tokennfttx/{ETHEREUM_ADDRESS}')
    print(response.json())

async def test_get_mined_blocks():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{QUART_APP_URL}/getminedblocks/{ETHEREUM_ADDRESS}')
    print(response.json())

async def main():
    await test_get_balance()
    #await test_get_token_balance()
    #await test_get_normal_transactions()
    #await test_get_internal_transactions()
    await test_get_erc20_transfer_events()
    #await test_get_erc721_transfer_events()
    #await test_get_mined_blocks()

if __name__ == '__main__':
    asyncio.run(main())
