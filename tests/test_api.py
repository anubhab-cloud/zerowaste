import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.database import connect_to_mongo, close_mongo_connection, get_database

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    await connect_to_mongo()
    yield
    await close_mongo_connection()

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_auth_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Test quick login as PG Owner
        res = await ac.post("/api/auth/login", json={"email_or_role": "pg"})
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["user"]["role"] == "PG Owner"

        # Test quick login as NGO
        res = await ac.post("/api/auth/login", json={"email_or_role": "ngo"})
        assert res.status_code == 200
        data = res.json()
        assert data["user"]["role"] == "NGO"

@pytest.mark.asyncio
async def test_listings_crud_and_claim():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Create a surplus food listing
        new_listing = {
            "foodName": "Pytest Surplus Biryani",
            "quantity": "Feeds 10 people",
            "pickupTime": "Today by 11 PM",
            "location": "BTM Layout, Bengaluru"
        }
        create_res = await ac.post("/api/listings", json=new_listing)
        assert create_res.status_code == 201
        listing_data = create_res.json()
        listing_id = listing_data["id"]
        assert listing_data["status"] == "Available"

        # 2. Get listings
        get_res = await ac.get("/api/listings?status=Available")
        assert get_res.status_code == 200
        items = get_res.json()
        assert any(i["id"] == listing_id for i in items)

        # 3. NGO Claims the food
        claim_res = await ac.put(f"/api/listings/{listing_id}/claim", json={
            "ngoId": "ngo456",
            "ngoName": "Helping Hands Foundation"
        })
        assert claim_res.status_code == 200
        assert claim_res.json()["status"] == "Claimed"

        # 4. Clean up delete
        del_res = await ac.delete(f"/api/listings/{listing_id}")
        assert del_res.status_code == 200

@pytest.mark.asyncio
async def test_requests_crud_and_pledge():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Create a supply request
        new_req = {
            "itemName": "Pytest Biodegradable Bowls",
            "quantity": "250 units"
        }
        create_res = await ac.post("/api/requests", json=new_req)
        assert create_res.status_code == 201
        req_id = create_res.json()["id"]

        # 2. PG pledges to fulfill
        pledge_res = await ac.put(f"/api/requests/{req_id}/pledge", json={
            "pgId": "pg123",
            "pgName": "Shanti Niwas PG"
        })
        assert pledge_res.status_code == 200
        assert pledge_res.json()["status"] == "Fulfilled"

        # 3. Clean up
        del_res = await ac.delete(f"/api/requests/{req_id}")
        assert del_res.status_code == 200

@pytest.mark.asyncio
async def test_donation_and_stats():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Submit a donation
        donation_res = await ac.post("/api/donations", json={
            "donorName": "Test Donor",
            "amount": 500,
            "paymentMethod": "UPI"
        })
        assert donation_res.status_code == 201
        assert "transactionId" in donation_res.json()

        # Check stats
        stats_res = await ac.get("/api/stats")
        assert stats_res.status_code == 200
        stats = stats_res.json()
        assert stats["mealsServed"] >= 3000
        assert stats["pgOwnersJoined"] >= 150
