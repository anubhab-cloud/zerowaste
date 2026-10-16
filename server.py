import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("================================================================")
    print("ZeroWasteByte Full-Stack Server")
    print(f"Web App & API: http://127.0.0.1:{port}")
    print(f"Swagger API Docs: http://127.0.0.1:{port}/docs")
    print("Database: MongoDB (zerowaste_db)")
    print("================================================================")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=port, reload=False)
