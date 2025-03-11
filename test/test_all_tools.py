# test_restaurant_tools.py - Test suite for restaurant operations functions

import unittest
import sys
from pathlib import Path
import datetime
import json
import os

# Add parent directory to path to import required modules
sys.path.append(str(Path(__file__).parent.parent))

# Import the functions to test
from tools.restaurant_tools import (
    search_restaurants, 
    get_cuisines, 
    get_locations, 
    get_features,
    check_availability, 
    recommend_restaurants, 
    create_reservation,
    get_reservation, 
    cancel_reservation, 
    modify_reservation
)

# Import configuration
from config import RESTAURANTS_FILE, RESERVATIONS_FILE

class TestRestaurantTools(unittest.TestCase):
    """Test suite for restaurant tools module"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test data before running tests"""
        # Create backup of existing data files if they exist
        cls._backup_data_files()
        
        # Create test restaurant data
        cls.test_restaurants = [
            {
                "id": "rest1",
                "name": "Test Italian Place",
                "cuisine": "Italian",
                "location": "Downtown",
                "price_range": "$$",
                "rating": 4.5,
                "capacity": 50,
                "features": ["Outdoor Seating", "Vegetarian Options", "Vegan Options"],
                "hours": {"open": "11:00", "close": "22:00"},
                "tables": {
                    "small": {"count": 5, "capacity": 2},
                    "medium": {"count": 8, "capacity": 4},
                    "large": {"count": 3, "capacity": 8}
                }
            },
            {
                "id": "rest2",
                "name": "Test Sushi Bar",
                "cuisine": "Japanese",
                "location": "Midtown",
                "price_range": "$$$",
                "rating": 4.8,
                "capacity": 30,
                "features": ["Takeout", "Vegan Options"],
                "hours": {"open": "12:00", "close": "23:00"},
                "tables": {
                    "small": {"count": 4, "capacity": 2},
                    "medium": {"count": 5, "capacity": 4},
                    "large": {"count": 2, "capacity": 8}
                }
            },
            {
                "id": "rest3",
                "name": "Test Steakhouse",
                "cuisine": "American",
                "location": "Downtown",
                "price_range": "$$$",
                "rating": 4.3,
                "capacity": 60,
                "features": ["Outdoor Seating", "Bar", "Takeout"],
                "hours": {"open": "16:00", "close": "23:00"},
                "tables": {
                    "small": {"count": 0, "capacity": 2},  # No small tables
                    "medium": {"count": 10, "capacity": 4},
                    "large": {"count": 5, "capacity": 8}
                }
            }
        ]
        
        # Create test reservation data
        cls.test_reservations = [
            {
                "id": "res1",
                "restaurant_id": "rest1",
                "restaurant_name": "Test Italian Place",
                "customer_name": "John Doe",
                "party_size": 2,
                "reservation_date": "2025-05-15",
                "reservation_time": "19:00",
                "table_type": "small",
                "status": "confirmed",
                "customer_email": "john@example.com",
                "customer_phone": "555-1234",
                "created_at": "2025-03-10T10:00:00",
                "updated_at": "2025-03-10T10:00:00"
            }
        ]
        
        # Write test data to files
        with open(RESTAURANTS_FILE, 'w') as f:
            json.dump(cls.test_restaurants, f)
        
        with open(RESERVATIONS_FILE, 'w') as f:
            json.dump(cls.test_reservations, f)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls._restore_data_files()
    
    @classmethod
    def _backup_data_files(cls):
        """Create backups of existing data files"""
        cls.restaurants_backup = None
        cls.reservations_backup = None
        
        if os.path.exists(RESTAURANTS_FILE):
            with open(RESTAURANTS_FILE, 'r') as f:
                cls.restaurants_backup = f.read()
        
        if os.path.exists(RESERVATIONS_FILE):
            with open(RESERVATIONS_FILE, 'r') as f:
                cls.reservations_backup = f.read()
    
    @classmethod
    def _restore_data_files(cls):
        """Restore original data files from backups"""
        if cls.restaurants_backup is not None:
            with open(RESTAURANTS_FILE, 'w') as f:
                f.write(cls.restaurants_backup)
        elif os.path.exists(RESTAURANTS_FILE):
            os.remove(RESTAURANTS_FILE)
        
        if cls.reservations_backup is not None:
            with open(RESERVATIONS_FILE, 'w') as f:
                f.write(cls.reservations_backup)
        elif os.path.exists(RESERVATIONS_FILE):
            os.remove(RESERVATIONS_FILE)
    
    def test_search_restaurants(self):
        """Test searching restaurants with various criteria"""
        # Test search by location
        results = search_restaurants(location="Downtown")
        self.assertEqual(len(results), 2)
        
        # Test search by cuisine
        results = search_restaurants(cuisine="Italian")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Test Italian Place")
        
        # Test search by features
        results = search_restaurants(features="Outdoor Seating")
        self.assertEqual(len(results), 2)
        
        # Test search by price range
        results = search_restaurants(price_range="$$$")
        self.assertEqual(len(results), 2)
        
        # Test search with multiple criteria
        results = search_restaurants(location="Downtown", cuisine="American")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Test Steakhouse")
        
        # Test search with no matching results
        results = search_restaurants(location="Suburb")
        self.assertEqual(len(results), 0)
    
    def test_get_cuisines(self):
        """Test retrieving all cuisine types"""
        cuisines = get_cuisines()
        self.assertEqual(sorted(cuisines), sorted(["Italian", "Japanese", "American"]))
    
    def test_get_locations(self):
        """Test retrieving all locations"""
        locations = get_locations()
        self.assertEqual(sorted(locations), sorted(["Downtown", "Midtown"]))
    
    def test_get_features(self):
        """Test retrieving all features"""
        features = get_features()
        expected_features = sorted([
            "Outdoor Seating", "Vegetarian Options", 
            "Vegan Options", "Takeout", "Bar"
        ])
        self.assertEqual(sorted(features), expected_features)
    
    def test_check_availability(self):
        """Test checking restaurant availability"""
        # Test valid availability for small table
        result = check_availability("rest1", "2025-05-15", "19:30", 2)
        self.assertTrue(result["available"])
        self.assertEqual(result["table_type"], "small")
        
        # Test valid availability for medium table
        result = check_availability("rest1", "2025-05-15", "19:30", 4)
        self.assertTrue(result["available"])
        self.assertEqual(result["table_type"], "medium")
        
        # Test restaurant with no small tables
        result = check_availability("rest3", "2025-05-15", "19:30", 2)
        self.assertFalse(result["available"])
        
        # Test outside of opening hours
        result = check_availability("rest1", "2025-05-15", "10:30", 2)
        self.assertFalse(result["available"])
        self.assertIn("not open", result["error"])
        
        # Test invalid inputs
        result = check_availability("rest1", "invalid-date", "19:30", 2)
        self.assertFalse(result["available"])
        
        result = check_availability("rest1", "2025-05-15", "invalid-time", 2)
        self.assertFalse(result["available"])
    
    def test_recommend_restaurants(self):
        """Test restaurant recommendations"""
        # Test basic recommendations
        result = recommend_restaurants()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result["restaurants"]), 3)  # All restaurants (limited to 5)
        
        # Test recommendations with criteria
        result = recommend_restaurants(location="Downtown", cuisine="Italian")
        self.assertEqual(len(result["restaurants"]), 1)
        self.assertEqual(result["restaurants"][0]["name"], "Test Italian Place")
        
        # Test with fallback search
        result = recommend_restaurants(cuisine="Mexican", fallback_search=True)
        self.assertTrue(result["fallback_applied"])
        self.assertEqual(len(result["restaurants"]), 3)  # All restaurants (fallback)
        
        # Test with availability
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        result = recommend_restaurants(
            date=today, 
            time="19:00", 
            party_size=2, 
            location="Downtown"
        )
        self.assertTrue(result["filtered_by_availability"])
        
        # Test with no results
        result = recommend_restaurants(cuisine="Mexican", fallback_search=False)
        self.assertEqual(len(result["restaurants"]), 0)
    
    def test_create_reservation(self):
        """Test creating a reservation"""
        # Test creating a valid reservation
        result = create_reservation(
            restaurant_id="rest1",
            customer_name="Jane Smith",
            party_size=4,
            reservation_date="2025-05-20",
            reservation_time="18:00",
            customer_email="jane@example.com",
            customer_phone="555-5678",
            special_requests="Window seat please"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["reservation"]["customer_name"], "Jane Smith")
        self.assertEqual(result["reservation"]["table_type"], "medium")
        
        # Test creating a reservation outside of hours
        result = create_reservation(
            restaurant_id="rest1",
            customer_name="Test Person",
            party_size=2,
            reservation_date="2025-05-20",
            reservation_time="09:00",  # Outside opening hours
            customer_email="test@example.com"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("not open", result["error"])
    
    def test_get_reservation(self):
        """Test retrieving a reservation"""
        # Test retrieving an existing reservation
        result = get_reservation("res1")
        self.assertTrue(result["success"])
        self.assertEqual(result["reservation"]["customer_name"], "John Doe")
        
        # Test retrieving a non-existent reservation
        result = get_reservation("nonexistent")
        self.assertFalse(result["success"])
    
    def test_cancel_reservation(self):
        """Test cancelling a reservation"""
        # First create a reservation to cancel
        create_result = create_reservation(
            restaurant_id="rest2",
            customer_name="Cancel Test",
            party_size=2,
            reservation_date="2025-06-01",
            reservation_time="20:00"
        )
        
        reservation_id = create_result["reservation"]["id"]
        
        # Now cancel it
        result = cancel_reservation(reservation_id)
        self.assertTrue(result["success"])
        self.assertEqual(result["reservation"]["status"], "cancelled")
        
        # Test cancelling a non-existent reservation
        result = cancel_reservation("nonexistent")
        self.assertFalse(result["success"])
    
    def test_modify_reservation(self):
        """Test modifying a reservation"""
        # First create a reservation to modify
        create_result = create_reservation(
            restaurant_id="rest1",
            customer_name="Modify Test",
            party_size=2,
            reservation_date="2025-07-01",
            reservation_time="19:00"
        )
        
        reservation_id = create_result["reservation"]["id"]
        
        # Modify the reservation
        result = modify_reservation(
            reservation_id=reservation_id,
            party_size=4,
            reservation_time="20:00",
            special_requests="Anniversary dinner"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["reservation"]["party_size"], 4)
        self.assertEqual(result["reservation"]["reservation_time"], "20:00")
        self.assertEqual(result["reservation"]["special_requests"], "Anniversary dinner")
        self.assertEqual(result["reservation"]["table_type"], "medium")  # Updated for new party size
        
        # Test modifying a non-existent reservation
        result = modify_reservation("nonexistent", party_size=4)
        self.assertFalse(result["success"])
        
        # Test modifying to invalid time
        result = modify_reservation(reservation_id, reservation_time="invalid")
        self.assertFalse(result["success"])

if __name__ == "__main__":
    unittest.main()