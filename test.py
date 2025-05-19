import json

import requests

# Replace with the actual URL where your FastAPI app is running locally
LOCAL_API_URL = "http://127.0.0.1:8000/classify"

def test_classify_endpoint(email_body):
    """
    Sends a POST request to the /classify endpoint of the local FastAPI app.

    Args:
        email_body (str): The email content to be classified.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"input_email_body": email_body}

    try:
        response = requests.post(LOCAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

if __name__ == "__main__":
    # Example email bodies to test
    test_emails = [
        "Hello, my name is Alice Smith and my email is alice.smith@example.com. I'm having trouble with my account.",
        "Urgent: My credit card number is 1234-5678-9012-3456 and the expiry is 03/27. I was overcharged.",
        "Subject: Network down - Office B1 floor. Please investigate.",
        "Request for new software installation on my laptop.",
        "Regarding invoice INV-2023-10-01. The total seems incorrect.",
        "My date of birth is 01/15/1990 and my phone number is 987-654-3210.",
        "Is there a problem with the server?",
        "I need to change my registered address.",
        "Subject: Unplanned system outage affecting database access.",
        "Can I get access to the premium features?"
    ]

    print("Testing the /classify endpoint on localhost:")
    for i, email in enumerate(test_emails):
        print(f"\n--- Test Email {i+1} ---")
        print(f"Input Email Body: {email}")
        response_data = test_classify_endpoint(email)
        if response_data:
            print("API Response:")
            print(json.dumps(response_data, indent=4))
        else:
            print("Failed to get a valid response from the API.")

    print("\nTesting complete.")