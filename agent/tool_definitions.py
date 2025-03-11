# ai/tool_definitions.py - Tool definitions for the AI service

# Tool definitions
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_cuisines",
            "description": "Get a list of all available cuisine types",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_locations",
            "description": "Get a list of all available restaurant locations",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_features",
            "description": "Get a list of all available restaurant features",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check if a restaurant has availability for a specific date, time, and party size",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "string",
                        "description": "Unique identifier of the restaurant"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date for reservation (YYYY-MM-DD format)"
                    },
                    "time": {
                        "type": "string",
                        "description": "Time for reservation (HH:MM format, 24-hour)"
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people in the party"
                    }
                },
                "required": [
                    "restaurant_id",
                    "date",
                    "time",
                    "party_size"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_reservation",
            "description": "Create a new restaurant reservation",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "string",
                        "description": "Unique identifier of the restaurant"
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the customer"
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people in the party"
                    },
                    "reservation_date": {
                        "type": "string",
                        "description": "Date of reservation (YYYY-MM-DD format)"
                    },
                    "reservation_time": {
                        "type": "string",
                        "description": "Time of reservation (HH:MM format, 24-hour)"
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "Email address of the customer (optional)"
                    },
                    "customer_phone": {
                        "type": "string",
                        "description": "Phone number of the customer (optional)"
                    },
                    "special_requests": {
                        "type": "string",
                        "description": "Any special requests or notes for the reservation (optional)"
                    }
                },
                "required": [
                    "restaurant_id",
                    "customer_name",
                    "party_size",
                    "reservation_date",
                    "reservation_time"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_reservation",
            "description": "Cancel an existing restaurant reservation",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {
                        "type": "string",
                        "description": "Unique identifier of the reservation"
                    }
                },
                "required": [
                    "reservation_id"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_reservation",
            "description": "Get information about a specific reservation by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {
                        "type": "string",
                        "description": "Unique identifier of the reservation"
                    }
                },
                "required": [
                    "reservation_id"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "modify_reservation",
            "description": "Modify an existing restaurant reservation",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {
                        "type": "string",
                        "description": "Unique identifier of the reservation"
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "New number of people in the party (optional)"
                    },
                    "reservation_date": {
                        "type": "string",
                        "description": "New date of reservation (YYYY-MM-DD format) (optional)"
                    },
                    "reservation_time": {
                        "type": "string",
                        "description": "New time of reservation (HH:MM format, 24-hour) (optional)"
                    },
                    "special_requests": {
                        "type": "string",
                        "description": "New special requests or notes for the reservation (optional)"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status for the reservation (confirmed, pending, cancelled) (optional)"
                    }
                },
                "required": [
                    "reservation_id"
                ]
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_customer_reservations",
    #         "description": "Get all reservations for a customer by name",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "customer_name": {
    #                     "type": "string",
    #                     "description": "Name of the customer"
    #                 }
    #             },
    #             "required": [
    #                 "customer_name"
    #             ]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "recommend_restaurants",
            "description": "Search for and recommend restaurants based on user preferences with fallback options if initial search yields no results",
            "parameters": {
                "type": "object",
                "properties": {
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people in the party"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date for the reservation (YYYY-MM-DD format)"
                    },
                    "time": {
                        "type": "string", 
                        "description": "Time for the reservation (HH:MM format, 24-hour)"
                    },
                    "location": {
                        "type": "string",
                        "description": "Preferred area or neighborhood"
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Type of cuisine preferred"
                    },
                    "price_range": {
                        "type": "string",
                        "description": "Price range ($ for budget, $$ for mid-range, $$$ for high-end)"
                    },
                    "features": {
                        "type": "string", 
                        "description": "Comma-separated list of desired features (e.g., 'outdoor seating, kid-friendly')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top restaurants to return based on rating (default: 5)"
                    }
                },
                "required": []
            }
        }
    }
]