import datetime
import json
import random
import time
import traceback
import requests
from lb_tech_handler.db_handler import execute_query_and_return_result

DEFAULT_LOG_FILE_NAME = "api_calls.log"

DEFAULT_MINIMUM_API_WAIT_TIME_IN_SECONDS = 3

DEFAULT_MAXIMUM_API_WAIT_TIME_IN_SECONDS = 5

def debug_api_response(api_response: requests.Response,application_id:int=0,user_id:int=0):
    """
    Debug an API response by collecting useful details and returning them as a structured dictionary.

    Args:
        api_response (requests.Response): The API response object to debug.

    Returns:
        dict: A dictionary containing API debugging information.
    """
    # Safely get Content-Type
    content_type = api_response.headers.get('Content-Type', 'Unknown')

    # Decode request payload if it exists
    payload = api_response.request.body
    if payload and isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    # Determine response content type and handle appropriately
    if "application/json" in content_type.lower():
        try:
            response_content = json.dumps(api_response.json(),indent=4)  # Parse JSON
        except ValueError:
            response_content = "Invalid JSON content"
    elif "text" in content_type.lower():
        response_content = api_response.text  # Plain text
    else:
        response_content = "Binary"  # Assume binary content for other types

    # Construct the API log data
    api_data = {
        "log_type": "api_log",
        "data": {
            "api_end_point": api_response.url,
            "request_method": api_response.request.method,
            "response_code": api_response.status_code,
            "response_content": response_content,  # Can be JSON, text, or "Binary"
            "response_headers": dict(api_response.headers),  # Converts headers to a dictionary
            "request_headers": dict(api_response.request.headers),
            "payload": payload,
        },
        "application_id": application_id,
        "user_id": user_id,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    }


    return api_data

def log_api_request(api_response: requests.Response,log_file_name:str=DEFAULT_LOG_FILE_NAME,log_to_database:bool=False,log_to_file:bool=True,application_id:int=0,user_id:int=0) -> int:
    """_summary_

    Example:
        api_response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
        api_log_id = log_api_request(api_response=api_response,log_file_name=log_file_name,log_to_database=True,log_to_file=True)

    Args:
        api_response (requests.Response): _description_
        log_file_name (str, optional): _description_. Defaults to DEFAULT_LOG_FILE_NAME.
        log_to_database (bool, optional): _description_. Defaults to False.
        log_to_file (bool, optional): _description_. Defaults to True.
        application_id (int, optional): _description_. Defaults to 0.
        user_id (int, optional): _description_. Defaults to 0.

    Returns:
        int: Returns the api log id , returns 0 if not logged
    """    

    api_data = debug_api_response(api_response=api_response,application_id=application_id,user_id=user_id)

    if log_to_file and log_file_name:
        try:
            with open(log_file_name, "a") as log_file:
                # Append JSON-formatted log with a newline for each log entry
                log_file.write(json.dumps(api_data, indent=4) + "\n")
            print(f"Logged API request to file: {log_file_name}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    if log_to_database:

        api_log_query = """
        INSERT INTO tech.api_call_log(
         application_id, request_triggered_by_user_id,api_end_point, api_call_method, response_code, response_headers, response_content, request_headers, request_payload, created_at, created_by, updated_at, updated_by)
        VALUES (%(application_id)s, %(user_id)s,%(api_end_point)s, %(request_method)s, %(response_code)s, %(response_headers)s, %(response_content)s, %(request_headers)s, %(payload)s, %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        RETURNING api_log_id;
        """

        args = {
            "application_id": application_id,
            "user_id": user_id,
            "request_method": api_data["data"]["request_method"],
            "response_code": api_data["data"]["response_code"],
            "response_headers": json.dumps(api_data["data"]["response_headers"]),
            "response_content": api_data["data"]["response_content"],
            "request_headers": json.dumps(api_data["data"]["request_headers"]),
            "payload": api_data["data"]["payload"],
            "created_at": "now()",
            "created_by": user_id,
            "updated_at": "now()",
            "updated_by": user_id,
            "api_end_point": api_data["data"]["api_end_point"]
        }

        print(args)

        try:
            api_call_id = execute_query_and_return_result(query=api_log_query, vars=args)

            return api_call_id
        
        except Exception as e:

            print(f"Error writing to database: {e}")

            print(traceback.format_exc())
    
    return 0

def throttle_api_call(minimum_api_wait_time_in_seconds=3, maximum_api_wait_time_in_seconds=5):
    """This is a decorator use to slow down API calls.
    SLowing down API calls by throttling to prevent overloading the server.

    Example:
        @throttle_api_call(minimum_api_wait_time_in_seconds=3,maximum_api_wait_time_in_seconds=5)
        def test_api():
            response = requests.get("https://api.learnbasics.fun/learnyst?name=test")

        @throttle_api_call
        def test_api():
            response = requests.get("https://api.learnbasics.fun/learnyst?name=test")

    Args:
        minimum_api_wait_time_in_seconds (int, optional): _description_. Defaults to 3.
        maximum_api_wait_time_in_seconds (int, optional): _description_. Defaults to 5.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Calculate delay time
            delay_time = random.randint(
                minimum_api_wait_time_in_seconds, maximum_api_wait_time_in_seconds
            )
            print(f"Throttling API call for {func.__name__} for {delay_time} seconds")
            
            # Delay execution
            time.sleep(delay_time)
            
            # Execute the actual function
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


if __name__ == "__main__":

    log_file_name = "learnyst_api.log"

    application_name = "Test Release"
    
    api_response = requests.get("https://api.learnbasics.fun/learnyst?name=johnson")

    # api_log_id = log_api_request(api_response=api_response,log_file_name=log_file_name,log_to_database=True,log_to_file=True)
    # # print(debug_api_response(api_response=api_response))

    # api_response = requests.get("https://api.learnbasics.fun/")

    # log_api_request(api_response=api_response,log_file_name=log_file_name,log_to_database=True,log_to_file=True)

    # print(debug_api_response(api_response=api_response))