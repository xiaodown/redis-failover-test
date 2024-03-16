from time import sleep
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.client import Redis
from redis.exceptions import (
   BusyLoadingError,
   ConnectionError,
   TimeoutError
)
import sys
import curses

retry = Retry(ExponentialBackoff(), 3)

def redis_tester(redis_client):
    try:
        print("\n\nRunning test loop, fail over redis at will, ^C to exit...\n")
        sleep(2)
        loopcount=0
        while True:
            test_key = f'test_key{loopcount}'
            test_value = f'test_value{loopcount}'
            print(f"\nSetting {test_key} to {test_value}")
            redis_client.set(test_key, test_value)
            print(f"Getting {test_key}: ", redis_client.get(test_key))
            print(f"Deleting {test_key}")
            redis_client.delete(test_key)
            sleep(0.2) 
            loopcount += 1
    except Exception as e:
        print("Error: ", e)
        print("Exiting...")
        sys.exit(0)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        menu()

def menu():
    try:
        print("\n1. Run redis test loop with retry and backoff logic")
        print("2. Run redis test loop without retry")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            redis_client = Redis(host='localhost', port=6379, retry=retry, retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
            redis_tester(redis_client)
        if choice == '2':
            redis_client = Redis(host='localhost', port=6379)
            redis_tester(redis_client)
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1 or 2.")
    except KeyboardInterrupt:
        print("keyboard interrupt")
        sys.exit(0)

menu()