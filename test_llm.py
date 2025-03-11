# test_llm.py - Test the AI service
from pathlib import Path
import sys
from agent.llm_service import LLMService
import time

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))


def test_simple_queries():
    ai_service = LLMService()
    
    # # Test 1: Simple greeting
    # print("\n=== Test 1: Simple greeting ===")
    # response = ai_service.process_query("Hello, I'd like to find a restaurant.")
    # print(f"AI Response: {response['response']}\n")
    
    # # Test 2: Query that should trigger a tool call
    # print("\n=== Test 2: Query that should trigger a tool call ===")
    # response = ai_service.process_query("What cuisines do you offer?")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")
    
    # Test 3: More complex query
    print("\n=== Test 3: More complex query ===")
    response = ai_service.process_query("find me French restaurants")
    print(f"AI Response: {response['response']}")
    if response.get("debug_info"):
        print(f"Tool called: {response['debug_info']['tool_name']}")
        print(f"Tool args: {response['debug_info']['tool_args']}")
        print(f"Tool response: {response['debug_info']['tool_response']}\n")
    
    # # Test 4: Follow-up query
    # print("\n=== Test 4: Follow-up query ===")
    # response = ai_service.process_query("Check availiabilty Silver Table.")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool args: {response['debug_info']['tool_args']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")

    # # Test 5: Follow-up query
    # print("\n=== Test 5: Follow-up query ===")
    # response = ai_service.process_query("Make Reservation for 4 people tomorrow at 7 PM")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool args: {response['debug_info']['tool_args']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")

    # # # Test 6: Follow-up query
    # print("\n=== Test 6: More complex query ===")
    # response = ai_service.process_query("Yes, Make Reservation.")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool args: {response['debug_info']['tool_args']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")

    # # # Test 7: Follow-up query
    # print("\n=== Test 7: Follow-up query ===")    
    # response = ai_service.process_query("I'll Choose Blue Garden for tomorrow at 7 PM for 4 people")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool args: {response['debug_info']['tool_args']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")

    # # # Test 8: Follow-up query
    # print("\n=== Test 8: Follow-up query ===")    
    # response = ai_service.process_query("Make reservation for Adam")
    # print(f"AI Response: {response['response']}")
    # if response.get("debug_info"):
    #     print(f"Tool called: {response['debug_info']['tool_name']}")
    #     print(f"Tool args: {response['debug_info']['tool_args']}")
    #     print(f"Tool response: {response['debug_info']['tool_response']}\n")
    

    # # Test 2: Query with reservation intent
    # print("\nTest 2: Query with reservation intent")
    # ai_service.reset_conversation()
    # response = ai_service.process_query("Find a resturant for tomorrow at 7 PM for 4 people")
    # print(f"AI Response: {response['response']}")
    # # print(f"Context after query: selected_restaurant_id={ai_service.current_context.get('selected_restaurant_id')}")

    # # Test 2: Query with reservation intent
    # print("\nTest 2: Query with reservation intent")
    # ai_service.reset_conversation()
    # response = ai_service.process_query("Make a reservation at Taco Fiesta for tomorrow at 7 PM for 4 people under the name Smith")
    # print(f"AI Response: {response['response']}")
    

if __name__ == "__main__":
    test_simple_queries()