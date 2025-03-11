# generate_restaurants.py - Generate a larger set of restaurant data

import json
import random
from datetime import datetime, timedelta

# Define data sets for random generation
CUISINES = ['Italian', 'Japanese', 'Mexican', 'Chinese', 'American', 'Indian', 'Thai', 'French', 'Greek', 'Korean', 'Vietnamese', 'Spanish', 'Mediterranean', 'Brazilian', 'Lebanese']
LOCATIONS = ['Downtown', 'Riverfront', 'Westside', 'Eastside', 'Northend', 'Southside', 'Midtown', 'Uptown', 'Oceanview', 'Lakeside', 'Central District', 'Financial District']
FEATURES = ['outdoor seating', 'kid-friendly', 'wheelchair accessible', 'takeout', 'delivery', 'bar', 'live music', 'vegetarian options', 'vegan options', 'gluten-free options', 'private dining', 'romantic', 'trendy', 'casual', 'fine dining', 'pet-friendly']
PRICE_RANGES = ['$', '$$', '$$$', '$$$$']
RESTAURANT_PREFIXES = ['The', 'Little', 'Golden', 'Royal', 'Blue', 'Green', 'Red', 'Silver', 'Grand', 'Classic', 'Urban', 'Village', 'Rustic', 'Modern', 'Vintage']
RESTAURANT_SUFFIXES = ['Bistro', 'Kitchen', 'Grill', 'Restaurant', 'Cafe', 'Diner', 'Eatery', 'House', 'Bar & Grill', 'Steakhouse', 'Trattoria', 'Palace', 'Garden', 'Lounge', 'Table']

def generate_restaurant_name(cuisine):
    """Generate a random restaurant name, optionally using the cuisine type."""
    if random.random() < 0.3:  # 30% chance to use cuisine in name
        return f"{random.choice(RESTAURANT_PREFIXES)} {cuisine} {random.choice(RESTAURANT_SUFFIXES)}"
    else:
        return f"{random.choice(RESTAURANT_PREFIXES)} {random.choice(RESTAURANT_SUFFIXES)}"

def generate_restaurants(count=30):
    """Generate a specified number of random restaurant entries."""
    restaurants = []
    
    for i in range(count):
        # Generate basic details
        cuisine = random.choice(CUISINES)
        location = random.choice(LOCATIONS)
        price_range = random.choice(PRICE_RANGES)
        
        # Generate random name
        name = generate_restaurant_name(cuisine)
        
        # Generate random capacity
        small_tables = random.randint(3, 12)
        medium_tables = random.randint(3, 10)
        large_tables = random.randint(1, 5)
        total_capacity = (small_tables * 2) + (medium_tables * 4) + (large_tables * 8)
        
        # Generate random features (2-5 features per restaurant)
        feature_count = random.randint(2, 5)
        restaurant_features = random.sample(FEATURES, feature_count)
        
        # Generate random rating (3.0-5.0)
        rating = round(random.uniform(3.0, 5.0), 1)
        
        # Generate random hours
        open_hour = random.randint(7, 12)
        close_hour = random.randint(20, 23)
        open_time = f"{open_hour:02d}:00"
        close_time = f"{close_hour:02d}:00"
        
        # Create restaurant object
        restaurant = {
            "id": f"rest{i+1:03d}",
            "name": name,
            "location": location,
            "cuisine": cuisine,
            "capacity": total_capacity,
            "tables": {
                "small": {"capacity": 2, "count": small_tables},
                "medium": {"capacity": 4, "count": medium_tables},
                "large": {"capacity": 8, "count": large_tables}
            },
            "hours": {"open": open_time, "close": close_time},
            "price_range": price_range,
            "features": restaurant_features,
            "description": f"A {price_range} {cuisine.lower()} restaurant located in {location}.",
            "rating": rating
        }
        
        restaurants.append(restaurant)
    
    return restaurants

def save_restaurants(restaurants, file_path="data/restaurants.json"):
    """Save the generated restaurants to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(restaurants, file, indent=2)
        print(f"Successfully saved {len(restaurants)} restaurants to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving restaurants: {e}")
        return False

if __name__ == "__main__":
    # Generate 30 random restaurants
    restaurants = generate_restaurants(30)
    
    # Save to the data file
    save_restaurants(restaurants)
    
    # Print a summary
    print("\nRestaurant Summary:")
    print(f"Generated {len(restaurants)} restaurants")
    
    # Print cuisine distribution
    cuisine_counts = {}
    for restaurant in restaurants:
        cuisine_counts[restaurant["cuisine"]] = cuisine_counts.get(restaurant["cuisine"], 0) + 1
    
    print("\nCuisine Distribution:")
    for cuisine, count in sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {cuisine}: {count} restaurants")