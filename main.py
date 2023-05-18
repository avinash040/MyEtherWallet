import quart
import quart_cors
from quart import request, jsonify
import httpx

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
#app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")

import os

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

headers = {'Content-Type': 'application/json'}


@app.route('/balance/<address>', methods=['GET'])
async def get_balance(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}', headers=headers)
    return jsonify(response.json())

@app.route('/tokenbalance/<address>/<contract_address>', methods=['GET'])
async def get_token_balance(address, contract_address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.route('/txlist/<address>', methods=['GET'])
async def get_normal_transactions(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.route('/txlistinternal/<address>', methods=['GET'])
async def get_internal_transactions(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=txlistinternal&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.route('/tokentx/<address>', methods=['GET'])
async def get_erc20_transfer_events(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.route('/tokennfttx/<address>', methods=['GET'])
async def get_erc721_transfer_events(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=tokennfttx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.route('/getminedblocks/<address>', methods=['GET'])
async def get_mined_blocks(address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ETHERSCAN_API_URL}?module=account&action=getminedblocks&address={address}&blocktype=blocks&apikey={ETHERSCAN_API_KEY}')
    return jsonify(response.json())

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5003)
