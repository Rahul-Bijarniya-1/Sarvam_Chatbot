import json
import requests
from pathlib import Path
import sys
import logging
import time
import random
from typing import List, Dict, Any, Optional

# Add parent directory to path so we can import from other modules
sys.path.append(str(Path(__file__).parent.parent))

from config import GROQ_API_KEYS  # Modified to support multiple API keys
from agent.prompt import get_system_prompt
from agent.restaurant_resolver import RestaurantResolver
from agent.conversation_context import ConversationContextManager

from tools.restaurant_tools import (
    get_cuisines, get_locations, get_features,
    check_availability, create_reservation, get_reservation, cancel_reservation,
    recommend_restaurants, modify_reservation, load_json_file
)
from config import RESTAURANTS_FILE

# Tool definitions
from .tool_definitions import TOOL_DEFINITIONS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('llm_service')

# Constants for retry logic
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds
RETRY_JITTER = 1  # seconds


class LLMService:
    """Service to handle communication with the Groq API using direct REST calls."""
    
    def __init__(self):
        """Initialize the AI service with separate components for different concerns."""
        self.api_keys = GROQ_API_KEYS  # Now a list of API keys
        self.current_key_index = 0
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
        self.system_prompt = get_system_prompt()
        self.tool_definitions = TOOL_DEFINITIONS
        self.conversation_history = []

        self.restaurant_resolver = RestaurantResolver()
        self.context_manager = ConversationContextManager()

        # Headers will be set dynamically for each request
        self.update_headers()

    def update_headers(self):
        """Update headers with the current API key."""
        self.headers = {
            "Authorization": f"Bearer {self.api_keys[self.current_key_index]}",
            "Content-Type": "application/json"
        }

    def rotate_api_key(self):
        """Rotate to the next available API key."""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Rotating to API key index {self.current_key_index}")
        self.update_headers()

    def make_api_request(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an API request with retry logic for rate limiting.
        
        Args:
            url (str): The API endpoint URL
            payload (dict): The request payload
            
        Returns:
            dict: The API response data
            
        Raises:
            Exception: If all retries fail
        """
        retries = 0
        tried_keys = set()
        
        while retries < MAX_RETRIES * len(self.api_keys):
            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30  # Add timeout
                )
                
                # Log response code
                logger.info(f"LLM API Response Status: {response.status_code}")
                
                # Handle rate limiting (429) errors
                if response.status_code == 429:
                    tried_keys.add(self.current_key_index)
                    
                    # If we've tried all keys, wait and retry
                    if len(tried_keys) == len(self.api_keys):
                        retry_delay = RETRY_DELAY_BASE * (2 ** retries) + random.uniform(0, RETRY_JITTER)
                        logger.warning(f"Rate limited on all API keys. Retrying in {retry_delay:.2f} seconds...")
                        time.sleep(retry_delay)
                        retries += 1
                    
                    # Try the next API key
                    self.rotate_api_key()
                    continue
                
                # Handle other errors
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                # For network errors, retry with backoff
                retries += 1
                retry_delay = RETRY_DELAY_BASE * (2 ** retries) + random.uniform(0, RETRY_JITTER)
                
                if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429:
                    # For rate limiting, try a different key first
                    tried_keys.add(self.current_key_index)
                    if len(tried_keys) < len(self.api_keys):
                        self.rotate_api_key()
                        retry_delay = 0  # No delay when switching keys
                
                logger.warning(f"API request failed: {str(e)}. Retrying in {retry_delay:.2f} seconds...")
                print("\nError - MESSAGE:", e.response.json(), "\n")
                time.sleep(retry_delay)
                
                # If we've exhausted all retries, raise the exception
                if retries >= MAX_RETRIES * len(self.api_keys):
                    raise Exception(f"Failed after {retries} retries: {str(e)}")

    def process_query(self, user_query):
        """
        Process a user query through the LLM and execute any tool calls.
        
        Args:
            user_query (str): The user's query
            
        Returns:
            dict: The AI response and any tool results
        """

        # Extract restaurant ID if mentioned in the query
        restaurant_id, restaurant_name = self.restaurant_resolver.resolve_restaurant_from_query(user_query)

        # print("RESOLVED RESTAURANT : ", restaurant_id, restaurant_name, "\n")

        if restaurant_id:
            self.context_manager.update_restaurant_selection(restaurant_id, restaurant_name)
            logger.info(f"Resolved restaurant '{restaurant_name}' with ID '{restaurant_id}'")

        # Add user query to conversation history
        self.conversation_history.append({"role": "user", "content": user_query})

        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ],
                "tools": self.tool_definitions,
                "tool_choice": "auto"
            }

            # print("\nFirst_PAYLOAD : ", payload, "\n")
            
            # Make the API call with retry logic
            response_data = self.make_api_request(self.api_url, payload)
            
            # print("LLM_RESPONSE : ", response_data, "\n")
            
            # Extract the assistant's message
            assistant_message = response_data["choices"][0]["message"]

            # Check if the LLM wants to call a tool
            if "tool_calls" in assistant_message and assistant_message["tool_calls"]:
                # Process each tool call
                for tool_call in assistant_message["tool_calls"]:
                    # Extract tool information
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])

                    # Preprocess the arguments to correct restaurant identification
                    function_args = self._preprocess_tool_args(function_name, function_args)

                    # print("\nTOOL_CALL : ", function_name, function_args, "\n")
                    
                    # Execute the appropriate tool
                    tool_response = self._execute_tool(function_name, function_args)
                    
                    # Add the tool call and response to conversation history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call["id"],
                                "type": "function",
                                "function": {
                                    "name": function_name,
                                    "arguments": tool_call["function"]["arguments"]
                                }
                            }
                        ]
                    })
                    
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(tool_response)
                    })

                    # If recommend_restaurants was called, store the results
                    if function_name == "recommend_restaurants" and tool_response.get("restaurants"):
                        self.context_manager.store_search_results(tool_response.get("restaurants", []))


                # Make a second API call to get a response based on the tool results
                second_payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        *self.conversation_history
                    ],
                    "max_tokens": 1024
                }

                # print("\n SECOND_PAYLOAD : ", self.conversation_history, "\n")
                
                # Make the second API call with retry logic
                second_response_data = self.make_api_request(self.api_url, second_payload)
                
                # Add the final assistant response to history
                final_response = second_response_data["choices"][0]["message"]["content"]
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                return {
                    "response": final_response,
                    "tool_calls": True,
                    "debug_info": {
                        "tool_name": function_name,
                        "tool_args": function_args,
                        "tool_response": tool_response
                    }
                }
                
            else:
                # No tool calls, just return the normal response
                response_text = assistant_message["content"]
                
                # Add the assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                return {
                    "response": response_text,
                    "tool_calls": False
                }
                
        except Exception as e:
            error_message = f"Error communicating with AI service: {str(e)}"
            logger.error(error_message, exc_info=True)
            return {"response": error_message, "tool_calls": False, "error": True}
        
    def _execute_tool(self, tool_name, args):
        """
        Execute a tool based on the AI's request.
        
        Args:
            tool_name (str): Name of the tool to execute
            args (dict): Arguments for the tool
            
        Returns:
            dict: Result of the tool execution
        """
        try:    
            if tool_name == "get_cuisines":
                return get_cuisines()
                
            elif tool_name == "get_locations":
                return get_locations()
                
            elif tool_name == "get_features":
                return get_features()
                
            elif tool_name == "check_availability":
                return check_availability(
                    restaurant_id=args.get("restaurant_id"),
                    date=args.get("date"),
                    time=args.get("time"),
                    party_size=args.get("party_size")
                )
                
            elif tool_name == "create_reservation":
                return create_reservation(
                    restaurant_id=args.get("restaurant_id"),
                    customer_name=args.get("customer_name"),
                    party_size=args.get("party_size"),
                    reservation_date=args.get("reservation_date"),
                    reservation_time=args.get("reservation_time"),
                    customer_email=args.get("customer_email"),
                    customer_phone=args.get("customer_phone"),
                    special_requests=args.get("special_requests")
                )
                
            elif tool_name == "get_reservation":
                return get_reservation(
                    reservation_id=args.get("reservation_id")
                )
                
            elif tool_name == "cancel_reservation":
                return cancel_reservation(
                    reservation_id=args.get("reservation_id")
                )
                
            elif tool_name == "recommend_restaurants":
                return recommend_restaurants(
                    party_size=args.get("party_size"),
                    date=args.get("date"),
                    time=args.get("time"),
                    location=args.get("location"),
                    cuisine=args.get("cuisine"),
                    price_range=args.get("price_range"),
                    features=args.get("features"),
                    limit=args.get("limit", 5)
                )
                
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            logger.error(f"Error executing {tool_name}: {str(e)}", exc_info=True)
            return {"error": f"Error executing {tool_name}: {str(e)}"}
        

    def _preprocess_tool_args(self, function_name, args):
        """
        Preprocess tool arguments to ensure consistent restaurant ID handling.
        
        Args:
            function_name (str): Name of the function being called
            args (dict): Arguments to the function
            
        Returns:
            dict: Processed arguments with corrected restaurant IDs
        """
        # Create a copy of the args to avoid modifying the original
        processed_args = args.copy()
        
        # Functions that use restaurant_id
        if function_name in ["check_availability", "create_reservation"]:
            # Check if restaurant_id is provided
            if "restaurant_id" in processed_args:
                restaurant_id = processed_args["restaurant_id"]
                
                # If it's not in the correct format (not starting with "rest"), it might be a name
                if not str(restaurant_id).startswith("rest"):
                    # Check if it's a name we recognize
                    restaurant_name = str(restaurant_id).lower()
                    resolved_id = self.restaurant_resolver.resolve_id_from_name(restaurant_name)
                    
                    if resolved_id:
                        # Replace with the correct ID
                        processed_args["restaurant_id"] = resolved_id
                        logger.info(f"Preprocessed: Replaced restaurant name '{restaurant_name}' with ID '{processed_args['restaurant_id']}'")
                    elif self.context_manager.get_selected_restaurant_id():
                        # Fallback to the selected restaurant ID
                        processed_args["restaurant_id"] = self.context_manager.get_selected_restaurant_id()
                        logger.info(f"Preprocessed: Using selected restaurant ID '{processed_args['restaurant_id']}' for '{restaurant_name}'")
            # If no restaurant_id is provided but we have one in context, use it
            elif self.context_manager.get_selected_restaurant_id():
                processed_args["restaurant_id"] = self.context_manager.get_selected_restaurant_id()
                logger.info(f"Preprocessed: Using restaurant ID '{processed_args['restaurant_id']}' from context")
        
        return processed_args

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        self.context_manager.reset()