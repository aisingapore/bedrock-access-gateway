# SEA-LION Amazon Bedrock Custom Model Import Demo

## Posts
- [Importing and Using SEA-LION in a Serverless, On-Demand Environment with Amazon Bedrock](https://sea-lion.ai/importing-and-using-sea-lion-in-a-serverless-on-demand-environment-with-amazon-bedrock/)
- [OpenAI-compatible APIs with SEA-LION and Bedrock Access Gateway](https://sea-lion.ai/openai-compatible-apis-with-sea-lion-and-bedrock-access-gateway/)

## Setup
> [!NOTE]
> At the time of writing, Amazon Bedrock Custom Model Import is available in the `us-east-1`, `us-west-2` and `eu-central-1` AWS regions. The [supported model architectures](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html#model-customization-import-model-architecture) include Llama 3 and Llama 3.1.

- Upload the [SEA-LION model](https://huggingface.co/aisingapore/Llama-SEA-LION-v3-8B-IT) to an Amazon S3 bucket.
- Navigate to **Imported models** in the Amazon Bedrock console. Click the **Import model** button.
- Fill in the **Import model** form. Include the S3 URL of the uploaded SEA-LION model.
- Click the **Import model** button to start the import.
- After the model is imported, copy the model ARN from the **Imported models** page.
- In the demo directory, copy `.env`.
  ```
  cp .env.example .env
  ```
- Update `ENDPOINT_ARN` in `.env` with the copied value.
- Update the environment variables in `.env`, if necessary.
- Initialise the virtual environment.
  ```
  python -m venv venv
  ```
- Activate the virtual environment.
  ```
  source venv/bin/activate
  ```
- Install the packages.
  ```
  pip install -r requirements.txt
  ```
- Set up the Boto3 credentials.
  - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

## Demo
- Run the demo.
  ```
  python sealion_bedrock.py
  ```

## Disclaimer
- When using Amazon Bedrock or any AWS services, please be mindful that costs can accrue based on your usage. AWS pricing varies depending on the services used, the amount of data processed, and the resources allocated. It is recommended that you monitor your AWS usage regularly and review the pricing details on the [AWS Bedrock Pricing page](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html) to avoid unexpected charges.
- For imported models, you are charged for model inference, based on the number of copies of your custom model required to service your inference volume and the duration each model copy is active, billed in 5-minute windows.
  - A model copy is a single instance of an imported model ready to serve inference requests.
  - The price per model copy per minute depends on factors such as architecture, context length, AWS Region, compute unit version (hardware generation), and is tiered by model copy size.