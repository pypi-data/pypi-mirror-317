from lb_tech_handler import common_methods,api_handler

@api_handler.throttle_api_call(minimum_api_wait_time_in_seconds=7,maximum_api_wait_time_in_seconds=12)
def test_api():
    print("hello")

if __name__ == "__main__":

    test_api()