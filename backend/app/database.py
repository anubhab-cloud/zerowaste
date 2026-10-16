import logging
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

logger = logging.getLogger("zerowaste.database")

client: AsyncIOMotorClient = None
db = None

def get_database():
    return db

async def connect_to_mongo():
    global client, db
    logger.info("Connecting to MongoDB at %s", settings.MONGODB_URL)
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    # Ping
    await client.admin.command('ping')
    logger.info("Connected to MongoDB database '%s'", settings.DATABASE_NAME)
    await seed_initial_data()

async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("Closed MongoDB connection.")

async def seed_initial_data():
    """Seed initial sample data if collections are empty."""
    users_col = db["users"]
    listings_col = db["listings"]
    requests_col = db["requests"]
    
    # 1. Seed default users
    user_count = await users_col.count_documents({})
    if user_count == 0:
        logger.info("Seeding initial users...")
        sample_users = [
            {
                "id": "pg123",
                "email": "shanti@zerowaste.demo",
                "name": "Shanti Niwas PG",
                "role": "PG Owner",
                "phone": "+91 98765 43210",
                "address": "BTM Layout 2nd Stage, Bengaluru"
            },
            {
                "id": "pg124",
                "email": "paradise@zerowaste.demo",
                "name": "Paradise PG",
                "role": "PG Owner",
                "phone": "+91 98765 43211",
                "address": "Koramangala 5th Block, Bengaluru"
            },
            {
                "id": "ngo456",
                "email": "helpinghands@zerowaste.demo",
                "name": "Helping Hands Foundation",
                "role": "NGO",
                "phone": "+91 80 2345 6789",
                "address": "Indiranagar, Bengaluru"
            },
            {
                "id": "ngo999",
                "email": "foodforall@zerowaste.demo",
                "name": "Food for All",
                "role": "NGO",
                "phone": "+91 80 9876 5432",
                "address": "HSR Layout, Bengaluru"
            }
        ]
        await users_col.insert_many(sample_users)

    # 2. Seed initial surplus food listings
    listing_count = await listings_col.count_documents({})
    if listing_count == 0:
        logger.info("Seeding initial surplus food listings...")
        sample_listings = [
            {
                "id": "l1",
                "pgId": "pg123",
                "pgName": "Shanti Niwas PG",
                "foodName": "Fresh Vegetable Biryani & Raita",
                "quantity": "Feeds 20-25 people",
                "pickupTime": "Today by 9:30 PM",
                "location": "BTM Layout, Bangalore",
                "photoFilename": "11.jpg",
                "status": "Available",
                "claimedByNgoId": None,
                "claimedByNgoName": None,
                "createdAt": "2026-10-14T19:00:00Z"
            },
            {
                "id": "l2",
                "pgId": "pg124",
                "pgName": "Paradise PG",
                "foodName": "Roti, Dal Tadka & Paneer Curry",
                "quantity": "Feeds 12-15 people",
                "pickupTime": "Today by 10:00 PM",
                "location": "Koramangala 5th Block, Bangalore",
                "photoFilename": "13.jpg",
                "status": "Available",
                "claimedByNgoId": None,
                "claimedByNgoName": None,
                "createdAt": "2026-10-14T19:30:00Z"
            },
            {
                "id": "l3",
                "pgId": "pg123",
                "pgName": "Shanti Niwas PG",
                "foodName": "Idli, Vada & Sambar Breakfast Surplus",
                "quantity": "Feeds 30 people",
                "pickupTime": "Morning 10:30 AM",
                "location": "BTM Layout, Bangalore",
                "photoFilename": "12.jpeg",
                "status": "Claimed",
                "claimedByNgoId": "ngo456",
                "claimedByNgoName": "Helping Hands Foundation",
                "createdAt": "2026-10-14T08:00:00Z"
            }
        ]
        await listings_col.insert_many(sample_listings)

    # 3. Seed initial item requests
    request_count = await requests_col.count_documents({})
    if request_count == 0:
        logger.info("Seeding initial item requests...")
        sample_requests = [
            {
                "id": "r1",
                "ngoId": "ngo456",
                "ngoName": "Helping Hands Foundation",
                "itemName": "Aluminum Food Containers (Medium, 750ml)",
                "quantity": "500 units",
                "status": "Needed",
                "fulfilledByPgId": None,
                "fulfilledByPgName": None,
                "createdAt": "2026-10-14T15:00:00Z"
            },
            {
                "id": "r2",
                "ngoId": "ngo999",
                "ngoName": "Food for All",
                "itemName": "Heavy Duty Recyclable Delivery Bags",
                "quantity": "1000 units",
                "status": "Needed",
                "fulfilledByPgId": None,
                "fulfilledByPgName": None,
                "createdAt": "2026-10-14T16:00:00Z"
            },
            {
                "id": "r3",
                "ngoId": "ngo456",
                "ngoName": "Helping Hands Foundation",
                "itemName": "Insulated Meal Carriers / Thermal Boxes",
                "quantity": "10 boxes",
                "status": "Fulfilled",
                "fulfilledByPgId": "pg123",
                "fulfilledByPgName": "Shanti Niwas PG",
                "createdAt": "2026-10-13T10:00:00Z"
            }
        ]
        await requests_col.insert_many(sample_requests)
