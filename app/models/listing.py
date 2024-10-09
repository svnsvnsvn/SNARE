# Pydantic models for request/response
# Define the structure of listings

from pydantic import BaseModel, HttpUrl, Field

# class Listing(BaseModel):
#     url: HttpUrl            # Validates that it's a valid URL
#     address: str            # The address of the listing
#     price: float = Field(..., gt=0)  # Price must be greater than zero
#     bedrooms: int           # Number of bedrooms (optional, just an example)
#     square_feet: float      # Square footage of the listing
#     description: str = None  # Optional description of the listing


class ListingRequest(BaseModel):
    url: str