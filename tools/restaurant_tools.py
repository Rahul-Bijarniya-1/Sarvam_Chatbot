# tools/restaurant_tools.py - Functions for restaurant operations

import json
import datetime
from pathlib import Path
import sys

# Add parent directory to path so we can import from other modules
sys.path.append(str(Path(__file__).parent.parent))

from config import RESTAURANTS_FILE, RESERVATIONS_FILE
from utils.helpers import load_json_file, save_json_file, generate_id, is_valid_date_format, is_valid_time_format

def search_restaurants(location=None, cuisine=None, min_capacity=None, features=None, price_range=None):
    """
    Search for restaurants matching the given criteria.
    
    Args:
        location (str, optional): Area or neighborhood
        cuisine (str, optional): Type of cuisine
        min_capacity (int, optional): Minimum seating capacity required
        features (str, optional): Comma-separated list of desired features
        price_range (str, optional): Price range (e.g., "$", "$$", "$$$")
        
    Returns:
        list: Matching restaurants
    """
    restaurants = load_json_file(RESTAURANTS_FILE)
    results = []
    
    # Convert min_capacity to int if provided
    if min_capacity is not None:
        try:
            min_capacity = int(min_capacity)
        except ValueError:
            min_capacity = None
    
    # Parse features into a list if provided
    feature_list = []
    if features:
        feature_list = [f.strip().lower() for f in features.split(',')]
    
    for restaurant in restaurants:
        # Check if restaurant matches all provided criteria
        location_match = not location or restaurant["location"].lower() == location.lower()
        cuisine_match = not cuisine or restaurant["cuisine"].lower() == cuisine.lower()
        capacity_match = not min_capacity or restaurant["capacity"] >= min_capacity
        price_match = not price_range or restaurant["price_range"] == price_range
        
        # Check features if any were specified
        features_match = True
        if feature_list:
            rest_features = [f.lower() for f in restaurant["features"]]
            features_match = all(feature in rest_features for feature in feature_list)
        
        # Include restaurant if it matches all criteria
        if location_match and cuisine_match and capacity_match and price_match and features_match:
            results.append(restaurant)
    
    return results

def get_cuisines():
    """
    Get a list of all available cuisine types.
    
    Returns:
        list: All unique cuisines
    """
    restaurants = load_json_file(RESTAURANTS_FILE)
    cuisines = set()
    
    for restaurant in restaurants:
        cuisines.add(restaurant["cuisine"])
    
    return sorted(list(cuisines))

def get_locations():
    """
    Get a list of all available restaurant locations.
    
    Returns:
        list: All unique locations
    """
    restaurants = load_json_file(RESTAURANTS_FILE)
    locations = set()
    
    for restaurant in restaurants:
        locations.add(restaurant["location"])
    
    return sorted(list(locations))

def get_features():
    """
    Get a list of all available restaurant features.
    
    Returns:
        list: All unique features
    """
    restaurants = load_json_file(RESTAURANTS_FILE)
    features = set()
    
    for restaurant in restaurants:
        for feature in restaurant["features"]:
            features.add(feature)
    
    return sorted(list(features))

def check_availability(restaurant_id, date, time, party_size):
    """
    Check if a restaurant has availability for a party.
    
    Args:
        restaurant_id (str): ID of the restaurant
        date (str): Date in YYYY-MM-DD format
        time (str): Time in HH:MM format
        party_size (int): Number of people
        
    Returns:
        dict: Result with availability status and details
    """
    # Input validation
    if not is_valid_date_format(date):
        return {"available": False, "error": "Invalid date format. Use YYYY-MM-DD."}
    
    if not is_valid_time_format(time):
        return {"available": False, "error": "Invalid time format. Use HH:MM in 24-hour format."}
    
    try:
        party_size = int(party_size)
    except ValueError:
        return {"available": False, "error": "Party size must be a number."}
    
    # Load restaurants
    restaurants = load_json_file(RESTAURANTS_FILE)
    
    # Find the requested restaurant
    restaurant = None
    for r in restaurants:
        if r["id"] == restaurant_id:
            restaurant = r
            break
    
    if not restaurant:
        return {"available": False, "error": f"Restaurant with ID {restaurant_id} not found."}
    
    # Check restaurant hours
    restaurant_open = restaurant["hours"]["open"]
    restaurant_close = restaurant["hours"]["close"]
    
    if time < restaurant_open or time > restaurant_close:
        return {
            "available": False, 
            "error": f"Restaurant is not open at {time}. Hours: {restaurant_open} - {restaurant_close}"
        }
    
    # For this simplified version, we'll just check if party size fits in any table
    # In a real system, you'd check against existing reservations
    
    # Find appropriate table size
    table_type = None
    if party_size <= 2:
        table_type = "small"
    elif party_size <= 4:
        table_type = "medium"
    elif party_size <= 8:
        table_type = "large"
    else:
        return {"available": False, "error": "Party size exceeds maximum table capacity."}
    
    # Check if that table type is available
    if restaurant["tables"][table_type]["count"] > 0:
        return {
            "available": True,
            "restaurant_name": restaurant["name"],
            "table_type": table_type,
            "party_size": party_size,
            "date": date,
            "time": time
        }
    else:
        return {"available": False, "error": "No tables available for this party size."}
    
def recommend_restaurants(party_size=None, date=None, time=None, location=None, 
                         cuisine=None, price_range=None, features=None, limit=5,
                         fallback_search=True):
    """
    Recommend restaurants based on user preferences and requirements.
    
    Args:
        party_size (int, optional): Number of people in the party
        date (str, optional): Date in YYYY-MM-DD format
        time (str, optional): Time in HH:MM format
        location (str, optional): Preferred area or neighborhood
        cuisine (str, optional): Type of cuisine preferred
        price_range (str, optional): Price range (e.g., "$", "$$", "$$$")
        features (str, optional): Comma-separated list of desired features
        limit (int, optional): Number of top restaurants to return (default: 5)
        fallback_search (bool, optional): Whether to try alternative searches if no results (default: True)
        
    Returns:
        dict: Search results and metadata
    """
    # First, search for restaurants matching the criteria
    results = search_restaurants(
        location=location,
        cuisine=cuisine,
        min_capacity=party_size,
        features=features,
        price_range=price_range
    )
    
    # If no results and fallback is enabled, try alternative searches
    original_query = {
        "location": location,
        "cuisine": cuisine, 
        "party_size": party_size,
        "features": features,
        "price_range": price_range
    }
    
    fallback_applied = False
    fallback_message = None
    
    if not results and fallback_search:
        # First fallback: Try without location constraint
        if features:
            fallback_results = search_restaurants(
                location=location,
                cuisine=cuisine,
                min_capacity=party_size,
                features=None,
                price_range=price_range
            )
            if fallback_results:
                results = fallback_results
                fallback_applied = True
                fallback_message = f"No restaurants found in {location} with {features if features else ''} features. Showing results without features."
        
        # Second fallback: Try without cuisine constraint if still no results
        if not results and cuisine:
            fallback_results = search_restaurants(
                location=location,
                cuisine=None,
                min_capacity=party_size,
                features=features,
                price_range=price_range
            )
            if fallback_results:
                results = fallback_results
                fallback_applied = True
                fallback_message = f"No {cuisine} cuisine restaurants found. Showing all cuisines in {location if location else 'all locations'}."
    
    # If still no results, return empty list with explanation
    if not results:
        return {
            "restaurants": [],
            "count": 0,
            "original_query": original_query,
            "message": "No restaurants found matching your criteria."
        }
    
    # If date and time are provided, filter by availability
    available_restaurants = []
    if date and time and party_size:
        for restaurant in results:
            # Check availability
            availability = check_availability(
                restaurant_id=restaurant["id"],
                date=date,
                time=time,
                party_size=party_size
            )
            
            # Add to available restaurants if available
            if availability.get("available", False):
                restaurant["available"] = True
                available_restaurants.append(restaurant)
    
    # Use available restaurants if filtering was applied and returned results
    filtered_by_availability = False
    if date and time and party_size:
        filtered_by_availability = True
        if available_restaurants:
            results = available_restaurants
    
    # Sort results by rating (highest first)
    results.sort(key=lambda x: x.get("rating", 0), reverse=True)
    
    # Limit the number of results
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 5
    
    recommendations = results[:limit]
    
    # Return a more comprehensive response
    return {
        "restaurants": recommendations,
        "count": len(recommendations),
        "total_matches": len(results),
        "original_query": original_query,
        "fallback_applied": fallback_applied,
        "fallback_message": fallback_message,
        "filtered_by_availability": filtered_by_availability,
        "available_count": len(available_restaurants) if filtered_by_availability else None
    }    
    
def create_reservation(restaurant_id, customer_name, party_size, reservation_date, 
                     reservation_time, customer_email=None, customer_phone=None, 
                     special_requests=None):
    """
    Create a new restaurant reservation.
    
    Args:
        restaurant_id (str): ID of the restaurant
        customer_name (str): Name of the customer
        party_size (int): Number of people
        reservation_date (str): Date in YYYY-MM-DD format
        reservation_time (str): Time in HH:MM format
        customer_email (str, optional): Customer's email
        customer_phone (str, optional): Customer's phone number
        special_requests (str, optional): Special requests
        
    Returns:
        dict: The created reservation or error information
    """
    # First check availability
    availability = check_availability(restaurant_id, reservation_date, reservation_time, party_size)
    
    if not availability["available"]:
        return {"success": False, "error": availability.get("error", "No availability")}
    
    # Find the restaurant to get its name
    restaurants = load_json_file(RESTAURANTS_FILE)
    restaurant_name = ""
    for r in restaurants:
        if r["id"] == restaurant_id:
            restaurant_name = r["name"]
            break
    
    # Determine table type
    if int(party_size) <= 2:
        table_type = "small"
    elif int(party_size) <= 4:
        table_type = "medium"
    else:
        table_type = "large"
    
    # Create reservation object
    now = datetime.datetime.now().isoformat()
    reservation = {
        "id": generate_id("res"),
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant_name,
        "customer_name": customer_name,
        "party_size": int(party_size),
        "reservation_date": reservation_date,
        "reservation_time": reservation_time,
        "table_type": table_type,
        "status": "confirmed",
        "created_at": now,
        "updated_at": now
    }
    
    # Add optional fields if provided
    if customer_email:
        reservation["customer_email"] = customer_email
    if customer_phone:
        reservation["customer_phone"] = customer_phone
    if special_requests:
        reservation["special_requests"] = special_requests
    
    # Save the reservation
    reservations = load_json_file(RESERVATIONS_FILE)
    if not reservations:
        reservations = []
    
    reservations.append(reservation)
    success = save_json_file(RESERVATIONS_FILE, reservations)
    
    return {"success": True, "reservation": reservation}

def get_reservation(reservation_id):
    """
    This is a placeholder. In a real application, this would retrieve a reservation from storage.
    For this simplified example, we'll just return a dummy reservation.
    
    Args:
        reservation_id (str): ID of the reservation
        
    Returns:
        dict: The reservation information
    """
    reservations = load_json_file(RESERVATIONS_FILE)
    
    if not reservations:
        return {"success": False, "error": "No reservations found."}
    
    for reservation in reservations:
        if reservation["id"] == reservation_id:
            return {"success": True, "reservation": reservation}
    
    return {"success": False, "error": f"Reservation {reservation_id} not found."}

def cancel_reservation(reservation_id):
    """
    Cancel a reservation by ID.
    
    Args:
        reservation_id (str): ID of the reservation
        
    Returns:
        dict: Result of the cancellation
    """
     # Simply call modify_reservation with status="cancelled"
    result = modify_reservation(reservation_id, status="cancelled")
    
    if result["success"]:
        return {
            "success": True,
            "message": f"Reservation {reservation_id} has been cancelled.",
            "reservation": result["reservation"]
        }
    else:
        return result

def modify_reservation(reservation_id, party_size=None, reservation_date=None, 
                      reservation_time=None, special_requests=None, status=None):
    """
    Modify an existing reservation.
    
    Args:
        reservation_id (str): ID of the reservation
        party_size (int, optional): New party size
        reservation_date (str, optional): New date (YYYY-MM-DD)
        reservation_time (str, optional): New time (HH:MM)
        special_requests (str, optional): New special requests
        status (str, optional): New status (confirmed, pending, cancelled)
        
    Returns:
        dict: Result of the modification
    """
    # Input validation
    if reservation_date and not is_valid_date_format(reservation_date):
        return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD."}
    
    if reservation_time and not is_valid_time_format(reservation_time):
        return {"success": False, "error": "Invalid time format. Use HH:MM in 24-hour format."}
    
    if party_size:
        try:
            party_size = int(party_size)
        except ValueError:
            return {"success": False, "error": "Party size must be a number."}
    
    # Load all reservations
    reservations = load_json_file(RESERVATIONS_FILE)
    
    if not reservations:
        return {"success": False, "error": "No reservations found."}
    
    # Find the reservation to modify
    reservation_index = None
    for i, reservation in enumerate(reservations):
        if reservation["id"] == reservation_id:
            reservation_index = i
            break
    
    if reservation_index is None:
        return {"success": False, "error": f"Reservation {reservation_id} not found."}
    
    # Get the current reservation
    current_reservation = reservations[reservation_index]
    
    # Check availability if changing date, time, or party size
    if (reservation_date or reservation_time or party_size) and current_reservation["status"] != "cancelled":
        check_date = reservation_date or current_reservation["reservation_date"]
        check_time = reservation_time or current_reservation["reservation_time"]
        check_party = party_size or current_reservation["party_size"]
        
        availability = check_availability(
            current_reservation["restaurant_id"],
            check_date,
            check_time,
            check_party
        )
        
        if not availability["available"]:
            return {"success": False, "error": availability.get("error", "No availability for the requested changes.")}
    
    # Apply modifications
    if party_size:
        current_reservation["party_size"] = party_size
        # Update table type
        if party_size <= 2:
            current_reservation["table_type"] = "small"
        elif party_size <= 4:
            current_reservation["table_type"] = "medium"
        else:
            current_reservation["table_type"] = "large"
    
    if reservation_date:
        current_reservation["reservation_date"] = reservation_date
    
    if reservation_time:
        current_reservation["reservation_time"] = reservation_time
    
    if special_requests is not None:  # Allow empty string to clear special requests
        current_reservation["special_requests"] = special_requests
    
    if status:
        current_reservation["status"] = status
    
    # Update the timestamp
    current_reservation["updated_at"] = datetime.datetime.now().isoformat()
    
    # Save the updated reservations
    success = save_json_file(RESERVATIONS_FILE, reservations)
    
    if success:
        return {"success": True, "reservation": current_reservation}
    else:
        return {"success": False, "error": "Failed to save reservation changes."}