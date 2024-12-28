"""
Test suite for the Web module.
"""

import pytest
import aiohttp
import json
from jdevtools.jweb import HTTPClient, WebSocket, APIClient, Response

@pytest.mark.asyncio
async def test_http_client():
    """Test HTTP client functionality."""
    async with HTTPClient("https://httpbin.org") as client:
        response = await client.get("/get")
        assert response.status == 200
        assert isinstance(response.data, dict)

@pytest.mark.asyncio
async def test_post_request():
    """Test POST request."""
    data = {"test": "data"}
    async with HTTPClient("https://httpbin.org") as client:
        response = await client.post("/post", data)
        assert response.status == 200
        assert response.data["json"] == data

@pytest.mark.asyncio
async def test_websocket():
    """Test WebSocket functionality."""
    # Start test WebSocket server
    async def echo(websocket):
        async for message in websocket:
            await websocket.send(message)
    
    server = await websockets.serve(echo, "localhost", 8765)
    
    # Test client
    ws = WebSocket("ws://localhost:8765")
    await ws.connect()
    
    test_data = {"message": "test"}
    await ws.send(test_data)
    response = await ws.receive()
    
    assert response == test_data
    
    await ws.close()
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_api_client():
    """Test API client functionality."""
    client = APIClient("https://httpbin.org")
    
    # Test GET
    response = await client.request("GET", "/get")
    assert response.status == 200
    
    # Test POST
    data = {"test": "data"}
    response = await client.request("POST", "/post", data=data)
    assert response.status == 200
    assert response.data["json"] == data

def test_response_object():
    """Test Response object creation."""
    response = Response(
        status=200,
        data={"test": "data"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status == 200
    assert response.data == {"test": "data"}
    assert response.headers["Content-Type"] == "application/json"

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in requests."""
    client = APIClient("https://nonexistent.example.com")
    
    with pytest.raises(Exception):
        await client.request("GET", "/")

@pytest.mark.asyncio
async def test_timeout():
    """Test request timeout."""
    client = HTTPClient(timeout=1)
    
    with pytest.raises(aiohttp.ClientTimeout):
        await client.get("https://httpbin.org/delay/2")
