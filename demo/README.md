# SEA-LION Amazon Bedrock Custom Model Import Demo

## Setup
> [!NOTE]
> At the time of writing, Amazon Bedrock Custom Model Import is available in the `us-east-1` and `us-west-2` AWS regions.

- Upload the [SEA-LION model](https://huggingface.co/aisingapore/llama3.1-8b-cpt-sea-lionv3-instruct) to an Amazon S3 bucket.
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