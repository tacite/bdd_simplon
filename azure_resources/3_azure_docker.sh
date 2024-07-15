#!/bin/bash

# Load variables
if [ -f .env ]; then
  source .env
fi

# ___VARIABLES___
IMAGE_NAME="j30v/spider-demo"
ENVIRONMENT_NAME=sadaheenvironm
CONTAINERAPP_NAME=sadahefunccontainerapp

# Create environment for the azure container
az containerapp env create \
    --name $ENVIRONMENT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION

# Check the status of the environment creation
STATUS=""
while [ "$STATUS" != "Succeeded" ]; do
  echo "Checking environment status..."
  STATUS=$(az containerapp env show \
      --name $ENVIRONMENT_NAME \
      --resource-group $RESOURCE_GROUP \
      --query "properties.provisioningState" \
      --output tsv)
  
  if [ "$STATUS" == "Failed" ]; then
    echo "Environment creation failed."
    exit 1
  fi

  if [ "$STATUS" != "Succeeded" ]; then
    echo "Current status: $STATUS. Waiting for 10 seconds before checking again."
    sleep 10
  fi
done

echo "Environment creation succeeded. Proceeding with Docker image deployment."

# Deploy Docker image
func azurecontainerapps deploy \
    --name $CONTAINERAPP_NAME \
    --environment $ENVIRONMENT_NAME \
    --storage-account $STORAGE_NAME \
    --resource-group $RESOURCE_GROUP \
    --image-name $IMAGE_NAME\
    --location $LOCATION
