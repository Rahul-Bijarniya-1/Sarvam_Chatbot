# agent/conversation_context.py - Handles conversation context management

import re
import logging
from datetime import datetime

logger = logging.getLogger('conversation_context')

class ConversationContextManager:
    """
    Manages the conversation context including tracking pending tools,
    restaurant selections, and parameter extraction.
    """
    
    def __init__(self):
        """Initialize the conversation context manager."""
        self.reset()
    
    def reset(self):
        """Reset all conversation context to initial state."""
        self.current_context = {
            "selected_restaurant_id": None,
            "selected_restaurant_name": None,
            "last_search_results": [],
            "restaurant_name_to_id_map": {},
            "pending_tool_call": None,  # Track incomplete tool calls
            "missing_parameters": []    # Track which parameters we're waiting for
        }
        return self
    
    def update_restaurant_selection(self, restaurant_id, restaurant_name):
        """
        Update the currently selected restaurant.
        
        Args:
            restaurant_id (str): ID of the selected restaurant
            restaurant_name (str): Name of the selected restaurant
            
        Returns:
            self: For method chaining
        """
        self.current_context["selected_restaurant_id"] = restaurant_id
        self.current_context["selected_restaurant_name"] = restaurant_name
        return self
    
    def store_search_results(self, restaurants):
        """
        Store search results for future reference.
        
        Args:
            restaurants (list): List of restaurant objects
            
        Returns:
            self: For method chaining
        """
        self.current_context["last_search_results"] = restaurants
        # Update restaurant name to ID mapping
        for restaurant in restaurants:
            self.current_context["restaurant_name_to_id_map"][restaurant["name"].lower()] = restaurant["id"]
        return self
    
    def get_selected_restaurant_id(self):
        """
        Get the currently selected restaurant ID.
        
        Returns:
            str: Selected restaurant ID or None
        """
        return self.current_context["selected_restaurant_id"]