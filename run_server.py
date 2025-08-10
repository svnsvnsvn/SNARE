#!/usr/bin/env python3
"""
SNARE Backend Server Startup Script
Starts the FastAPI server with configuration from environment variables.
"""

import uvicorn
from app.config import get_server_config, get_settings

def main():
    """Start the SNARE backend server."""
    settings = get_settings()
    server_config = get_server_config()
    
    print(f"Starting SNARE Backend Server...")
    print(f"Server will run at: http://{server_config['host']}:{server_config['port']}")
    print(f"Environment: {'Development' if server_config['reload'] else 'Production'}")
    print(f"CORS Origins: {settings.cors_allow_origins}")
    
    uvicorn.run(
        "app.main:app",
        **server_config
    )

if __name__ == "__main__":
    main()
