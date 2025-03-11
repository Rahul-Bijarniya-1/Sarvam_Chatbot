# test_tools.py - Test the restaurant tools functions

from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))


from tools.restaurant_tools import recommend_restaurants, get_cuisines, get_locations, get_features, check_availability
from tools.restaurant_tools import create_reservation, get_reservation, cancel_reservation

def test_search_restaurants():
    print("\n=== Testing search_restaurants ===")
    
    # Test 1: Search by cuisine
    print("\nTest 1: Searching for Italian restaurants")
    results = recommend_restaurants(cuisine="Italian", location="Downtown", features="bar")
    print(f"Found {len(results)} Italian restaurants:")
    print(f"\n Type :{type(results)} Result:",results, "\n")
    # for r in results:
    #     print(f"- {r['name']} in {r['location']}")
    
    # Test 2: Search by location
    print("\nTest 2: Searching for restaurants in Downtown")
    results = recommend_restaurants(cuisine="Thai", location="Downtown", features="bar")
    print(f"Found {len(results)} restaurants in Downtown:")
    print(f"\n Type :{type(results)} Result:",results, "\n")

    # for r in results:
    #     print(f"- {r['name']} ({r['cuisine']})")
    
    # Test 3: Search by feature
    print("\nTest 3: Searching for restaurants with outdoor seating")
    results = recommend_restaurants(features="outdoor seating")
    print(f"Found {len(results)} restaurants with outdoor seating:")
    # for r in results:
    #     print(f"- {r['name']} ({r['cuisine']})")

def test_get_functions():
    print("\n=== Testing get functions ===")
    
    # Test get_cuisines
    cuisines = get_cuisines()
    print("\nAvailable cuisines:")
    print(", ".join(cuisines))
    
    # Test get_locations
    locations = get_locations()
    print("\nAvailable locations:")
    print(", ".join(locations))
    
    # Test get_features
    features = get_features()
    print("\nAvailable features:")
    print(", ".join(features))

def test_check_availability():
    print("\n=== Testing check_availability ===")
    
    # Test 1: Valid reservation
    print("\nTest 1: Checking availability for 2 people")
    result = check_availability("rest001", "2025-03-10", "18:00", 3)
    print("Result:", result)
    
    # Test 2: Invalid time
    print("\nTest 2: Checking availability with invalid time")
    result = check_availability("rest001", "2025-03-10", "25:00", 2)
    print("Result:", result)
    
    # Test 3: Large party
    print("\nTest 3: Checking availability for large party")
    result = check_availability("rest001", "2025-03-10", "18:00", 12)
    print("Result:", result)

def test_reservation_functions():
    print("\n=== Testing reservation functions ===")
    
    # Test 1: Create reservation
    print("\nTest 1: Creating a reservation")
    result = create_reservation(
        restaurant_id="rest001",
        customer_name="Jane Smith",
        party_size=4,
        reservation_date="2025-03-12",
        reservation_time="19:30",
        customer_email="jane@example.com",
        customer_phone="555-123-4567",
        special_requests="Window table if possible"
    )
    print("Result:", result)
    
    if result["success"]:
        reservation_id = result["reservation"]["id"]
        
        # Test 2: Get reservation
        print("\nTest 2: Getting reservation details")
        get_result = get_reservation(reservation_id)
        print("Result:", get_result)
        
        # Test 3: Cancel reservation
        print("\nTest 3: Cancelling reservation")
        cancel_result = cancel_reservation(reservation_id)
        print("Result:", cancel_result)

if __name__ == "__main__":
    test_search_restaurants()
    test_get_functions()
    test_check_availability()
    test_reservation_functions