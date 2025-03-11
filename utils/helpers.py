# utils/helpers.py - Helper functions for the application

import json
import datetime

def load_json_file(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict or list: The loaded JSON data
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON.")
        return []
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def save_json_file(file_path, data):
    """
    Save data to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        data (dict or list): Data to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def is_valid_date_format(date_str):
    """
    Check if a string is in valid YYYY-MM-DD format.
    
    Args:
        date_str (str): Date string to check
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_time_format(time_str):
    """
    Check if a string is in valid HH:MM format.
    
    Args:
        time_str (str): Time string to check
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def generate_id(prefix=""):
    """
    Generate a unique ID based on timestamp.
    
    Args:
        prefix (str): Prefix for the ID
        
    Returns:
        str: Unique ID
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return f"{prefix}{timestamp}"