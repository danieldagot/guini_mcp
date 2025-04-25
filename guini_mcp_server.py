from mcp.server.fastmcp import FastMCP
import httpx
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("guini-mcp-server")

# Create an MCP server with a descriptive name
mcp = FastMCP("Guini MCP Server")

# Define base URL for API endpoints
BASE_URL = "https://cloudrun.guini.io/v1"

# Add tools with proper error handling

@mcp.tool()
async def list_partners() -> Dict[str, Any]:
    """
    Get services requests from Guini API.
    
    Returns:
        Dict containing services request data from the Guini API
    """
    try:
        logger.info("Fetching partners from Guini API")
        # Request body with null values for startDatetime, participants, and location
        body = {"startDatetime": None, "participants": None, "location": None}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{BASE_URL}/events/services-requests/",
                json=body
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return {"error": f"API returned error code: {e.response.status_code}", "details": e.response.text}
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {str(e)}")
        return {"error": "Failed to connect to API", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "Unexpected error occurred", "details": str(e)}

# @mcp.tool()
# async def get_partner_details(partner_id: str) -> Dict[str, Any]:
#     """
#     Get detailed information about a specific partner by ID.
    
#     Args:
#         partner_id: The unique identifier for the partner
        
#     Returns:
#         Dict containing detailed partner information
#     """
#     try:
#         logger.info(f"Fetching details for partner ID: {partner_id}")
#         async with httpx.AsyncClient(timeout=30.0) as client:
#             response = await client.get(f"{BASE_URL}/partners/{partner_id}")
#             response.raise_for_status()
#             return response.json()
#     except httpx.HTTPStatusError as e:
#         logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
#         return {"error": f"API returned error code: {e.response.status_code}", "details": e.response.text}
#     except httpx.RequestError as e:
#         logger.error(f"Request error occurred: {str(e)}")
#         return {"error": "Failed to connect to API", "details": str(e)}
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         return {"error": "Unexpected error occurred", "details": str(e)}

# @mcp.tool()
# async def search_services(query: str, category: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
#     """
#     Search for services based on a query string and optional filters.
    
#     Args:
#         query: Search term to find services
#         category: Optional category to filter results
#         limit: Maximum number of results to return (default: 10)
        
#     Returns:
#         Dict containing search results
#     """
#     try:
#         logger.info(f"Searching services with query: '{query}', category: '{category}', limit: {limit}")
#         params = {"q": query, "limit": limit}
#         if category:
#             params["category"] = category
            
#         async with httpx.AsyncClient(timeout=30.0) as client:
#             response = await client.get(f"{BASE_URL}/services/search", params=params)
#             response.raise_for_status()
#             return response.json()
#     except httpx.HTTPStatusError as e:
#         logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
#         return {"error": f"API returned error code: {e.response.status_code}", "details": e.response.text}
#     except httpx.RequestError as e:
#         logger.error(f"Request error occurred: {str(e)}")
#         return {"error": "Failed to connect to API", "details": str(e)}
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         return {"error": "Unexpected error occurred", "details": str(e)}

if __name__ == "__main__":
    mcp.run()