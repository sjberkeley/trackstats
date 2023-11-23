from js import document
#import scrape
#import numpy
#import matplotlib
#import boto3
#import requests
import json

def handle_click():
    display("Starting calculation ...", target="output")

    eventMenu = document.querySelector("#menu2")
    selectedOption = eventMenu.selectedOptions[0]
    eventText = selectedOption.textContent

    display(eventText, target="output")

    genderMenu = document.querySelector("#menu1")
    selectedOption = genderMenu.selectedOptions[0]
    genderText = selectedOption.textContent

    display(genderText, target="output")






    # AWS Lambda API endpoint
    lambda_endpoint = 'https://lambda.us-east-1.amazonaws.com'  # Replace with the correct endpoint for your region
    
    # AWS credentials (configure these)
    access_key = 'your-access-key'
    secret_key = 'your-secret-key'
    session_token = 'your-session-token'  # Required if using temporary security credentials
    
    # Specify the name of the Lambda function and the input payload
    function_name = 'your-lambda-function-name'
    input_payload = {
        'key1': 'value1',
        'key2': 'value2'
    }
    
    # Create the API request headers
    headers = {
        'X-Amz-Date': '20221231T000000Z',  # Replace with the current date and time
        'Content-Type': 'application/json',
        'X-Amz-Security-Token': session_token  # Include this if using temporary security credentials
    }
    
    # Create the API request data
    data = {
        'FunctionName': function_name,
        'InvocationType': 'RequestResponse',  # Use 'Event' for asynchronous invocation
        'Payload': json.dumps(input_payload)
    }
    
    # Make the API request
    response = requests.post(f"{lambda_endpoint}/2015-03-31/functions/{function_name}/invocations", data=json.dumps(data), headers=headers, auth=(access_key, secret_key))
    
    # Extract the response from the Lambda function
    response_payload = json.loads(response.content.decode('utf-8'))
    print(response_payload)








    # Create a boto3 client for AWS Lambda
    lambda_client = boto3.client('lambda')

    # Specify the name of the Lambda function and the input payload
    function_name = 'trackstats'
    input_payload = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
        Payload=json.dumps(input_payload)
    )

    # Extract the response from the Lambda function
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    display(response_payload, target="output")

    #scrape.build_csv(genderText, eventText)

    display("... not done!", target="output")
