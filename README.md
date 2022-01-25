# Sample program for ping monitoring of Soracom IoT SIM

## Prerequisites

- Serverless: [Serverless Getting Started Guide](https://www.serverless.com/framework/docs/getting-started)

## How to deploy

1. Setup `.env` file refering `sample.env`. You need to prepare following:
   - Soracom API auth key and auth secret
   - SIM ID of Soracom IoT SIM
   - (If you want to post to Slack) Slack Incoming Webhook URL
2. Invoke `serverless deploy` in the project directory
   