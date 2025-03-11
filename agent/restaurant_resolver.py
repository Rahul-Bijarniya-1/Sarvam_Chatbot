# agent/restaurant_resolver.py - Handles restaurant ID resolution and matching

import re
import logging
from config import RESTAURANTS_FILE
from tools.restaurant_tools import load_json_file

logger = logging.getLogger('restaurant_resolver')

class RestaurantResolver:
    """
    Handles resolution of restaurant names to IDs and detection of restaurant
    mentions in user queries.
    """
    
    def __init__(self):
        """Initialize the restaurant resolver with preloaded data."""
        self.restaurants = []
        self.name_to_id_map = {}
        self.word_to_restaurants_map = {}
        self._load_restaurant_data()
        
    def _load_restaurant_data(self):
        """Load restaurant data once at initialization for efficient lookups."""
        try:
            self.restaurants = load_json_file(RESTAURANTS_FILE)
            if self.restaurants:
                # Build name-to-id mapping for exact matches
                for restaurant in self.restaurants:
                    self.name_to_id_map[restaurant["name"].lower()] = restaurant["id"]
                
                # Build word-to-restaurants mapping for fuzzy matches
                for restaurant in self.restaurants:
                    name_words = restaurant["name"].lower().split()
                    for word in name_words:
                        if len(word) > 3:  # Only consider significant words (longer than 3 chars)
                            if word not in self.word_to_restaurants_map:
                                self.word_to_restaurants_map[word] = []
                            self.word_to_restaurants_map[word].append(restaurant)
                
                logger.info(f"Loaded {len(self.name_to_id_map)} restaurant name mappings")
        except Exception as e:
            logger.error(f"Error loading restaurant data: {str(e)}", exc_info=True)
    
    def resolve_restaurant_from_query(self, query):
        """
        Extract and resolve restaurant name from a query to its ID.
        
        Args:
            query (str): User query potentially containing restaurant name
            
        Returns:
            tuple: (restaurant_id, restaurant_name) if found, otherwise (None, None)
        """
        if not self.restaurants:
            return None, None
        
        # Try exact name matches first (most reliable)
        for name, id in self.name_to_id_map.items():
            if name in query.lower():
                for restaurant in self.restaurants:
                    if restaurant["id"] == id:
                        return id, restaurant["name"]
        
        # Try word-by-word matching with confidence scoring
        query_words = query.lower().split()
        potential_matches = {}
        
        for word in query_words:
            if len(word) > 3 and word in self.word_to_restaurants_map:  # Only consider significant words
                for restaurant in self.word_to_restaurants_map[word]:
                    restaurant_id = restaurant["id"]
                    if restaurant_id not in potential_matches:
                        potential_matches[restaurant_id] = {"score": 1, "restaurant": restaurant}
                    else:
                        potential_matches[restaurant_id]["score"] += 1
        
        # Find the best match with a minimum threshold
        if potential_matches:
            best_match_id = max(potential_matches, key=lambda id: potential_matches[id]["score"])
            if potential_matches[best_match_id]["score"] >= 2:  # Require at least 2 word matches for confidence
                restaurant = potential_matches[best_match_id]["restaurant"]
                return restaurant["id"], restaurant["name"]
        
        return None, None
    
    def resolve_id_from_name(self, restaurant_name):
        """
        Lookup restaurant ID from name with exact and fuzzy matching.
        
        Args:
            restaurant_name (str): Name of the restaurant
            
        Returns:
            str: Restaurant ID if found, otherwise None
        """
        # Check for exact match first
        restaurant_name = restaurant_name.lower()
        if restaurant_name in self.name_to_id_map:
            return self.name_to_id_map[restaurant_name]
        
        # Try fuzzy matching
        name_words = restaurant_name.split()
        potential_matches = {}
        
        for word in name_words:
            if len(word) > 3 and word in self.word_to_restaurants_map:
                for restaurant in self.word_to_restaurants_map[word]:
                    restaurant_id = restaurant["id"]
                    if restaurant_id not in potential_matches:
                        potential_matches[restaurant_id] = {"score": 1, "name": restaurant["name"]}
                    else:
                        potential_matches[restaurant_id]["score"] += 1
        
        # Find the best match with a minimum threshold
        if potential_matches:
            best_match_id = max(potential_matches, key=lambda id: potential_matches[id]["score"])
            if potential_matches[best_match_id]["score"] >= 2:  # Require at least 2 word matches
                return best_match_id
        
        return None