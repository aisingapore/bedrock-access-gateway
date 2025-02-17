import argparse
import boto3
import logging
import os
import sys
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from openai import OpenAI
from typing import Any, Dict, List

# Load the environment variables
load_dotenv()

try:
    # Load the endpoint ARN and configuration settings
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    endpoint_arn = os.environ["ENDPOINT_ARN"]
    max_tokens = int(os.environ.get("MAX_TOKENS", 1024))
    openai_base_url = os.environ["API_URL"]
    temperature = float(os.environ.get("TEMPERATURE", 0.0))
    top_k = int(os.environ.get("TOP_K", 250))
except KeyError as e:
    logging.error(f"The environment variable {e} is not defined.")
    sys.exit(1)

# Set the chatbot name
chatbot_name = "SEA-LION"


def stream_openai_response(openai_client, conversation: List[Dict[str, Any]]):
    """
    Stream the response from the OpenAI API.

    Args:
        openai_client: The OpenAI client.
        conversation (List[Dict[str, Any]]): The conversation history.
    """
    try:
        stream = openai_client.chat.completions.create(
            model=endpoint_arn,
            messages=conversation,
            stream=True,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except (ClientError, Exception) as e:
        logging.error(f"Exception: {e}")
        sys.exit(1)

    # Process the stream
    assistant_message = ""
    for part in stream:
        # Get the content from the stream
        content = part.choices[0].delta.content or ""

        # Filter out new lines and line feeds
        filtered_content = content.replace("\n", "").replace("\r", "")

        # Append to the assistant's message
        assistant_message += filtered_content

        # Print the filtered content
        print(filtered_content, end="", flush=True)

    print()

    # Append the assistant's reply to the conversation
    conversation.append({"role": "assistant", "content": assistant_message})


def stream_bedrock_response(bedrock_client, conversation: List[Dict[str, Any]]):
    """
    Stream the response from Bedrock.

    Args:
        bedrock_client: The Bedrock client.
        conversation (List[Dict[str, Any]]): The conversation history.
    """
    # Format the conversation messages appropriately for Bedrock
    formatted_conversation = [
        {"role": message["role"], "content": [{"text": message["content"]}]}
        for message in conversation
    ]

    # Get the streaming response
    try:
        streaming_response = bedrock_client.converse_stream(
            modelId=endpoint_arn,
            messages=formatted_conversation,
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": temperature,
            },
            additionalModelRequestFields={
                "parameters": {
                    "top_k": top_k,
                }
            },
        )
    except (ClientError, Exception) as e:
        logging.error(f"Exception: {e}")
        sys.exit(1)

    assistant_message = ""
    for chunk in streaming_response["stream"]:
        if "contentBlockDelta" in chunk:
            text = chunk["contentBlockDelta"]["delta"]["text"]
            if not all(char in "\n\r" for char in text):
                print(text, end="", flush=True)
                assistant_message += text
    print()

    # Append the assistant's reply to the conversation
    conversation.append({"role": "assistant", "content": assistant_message})


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="SEA-LION Bedrock Chatbot")
    parser.add_argument(
        "--api", action="store_true", help="Use the OpenAI-compatible API"
    )
    args = parser.parse_args()
    if args.api:
        print("Using the OpenAI-compatible API.")
        openai_client = OpenAI(base_url=openai_base_url, api_key="bedrock")
    else:
        print("Using the Amazon Bedrock Runtime (https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html).")
        bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)

    print("Welcome! Type your message or /bye to end.")

    # Initialize the conversation history
    conversation = []

    while True:
        # Get the input
        user_message = input("You: ").strip()

        # Check for the termination condition
        if user_message.lower() == "/bye" or user_message == "":
            print(f"{chatbot_name}: Goodbye!")
            break

        # Append the user's message to the conversation history
        conversation.append({"role": "user", "content": user_message})

        print(f"{chatbot_name}: ", end="")
        if args.api:
            # Use the OpenAI compatible endpoint
            stream_openai_response(openai_client, conversation)
        else:
            # Use the Bedrock endpoint
            stream_bedrock_response(bedrock_client, conversation)


if __name__ == "__main__":
    main()
