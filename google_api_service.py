import requests
import logging

def get_google_maps_clients(keyword: str, location: str) -> list:
    # KEEP YOUR ACTUAL API KEY HERE
    API_KEY = "AIzaSyBt3CtlcEptvsgSxaD8i7Nkt99VQEV1e2k"
    
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        "query": f"{keyword} manufacturers and suppliers in {location}",
        "key": API_KEY
    }

    vendors = []
    try:
        response = requests.get(search_url, params=search_params)
        results = response.json().get("results", [])

        for place in results: 
            place_id = place.get("place_id")
            
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "name,formatted_address,formatted_phone_number,website",
                "key": API_KEY
            }
            
            detail_res = requests.get(details_url, params=details_params)
            detail_data = detail_res.json().get("result", {})
            
            vendors.append({
                "company": detail_data.get("name", "Unknown"),
                "product": keyword,
                "city": detail_data.get("formatted_address", "Unknown Location"),
                "phone": detail_data.get("formatted_phone_number", "No Number Listed"),
                "email": detail_data.get("website", "No Website") 
            })
            
    except Exception as e:
        logging.error(f"Google API Error: {e}")

    return vendors