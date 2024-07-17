#!/bin/bash

# Load variables
if [ -f .env ]; then
  source .env
fi

# ___VARIABLES___
STORAGE_NAME=sadahestorage
IMAGE_NAME="helenedubourg/sadahescrapy"
ENVIRONMENT_NAME=sadaheenvironm
CONTAINERAPP_NAME=sadahefunccontainerapp
SUBSCRIPTION_ID="029b3537-0f24-400b-b624-6058a145efe1"
FUNCTION_NAME=sadahescrapyfunction

az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file template.json \
  --parameters subscriptionId=$SUBSCRIPTION_ID \
  name=$FUNCTION_NAME \
  location=$LOCATION \
  use32BitWorkerProcess=false \
  ftpsState=<state> \
  storageAccountName=$STORAGE_NAME \
  linuxFxVersion=<linux-version> \
  environmentName=<environment-name> \
  workspaceName=<workspace-name> \
  workspaceLocation=<workspace-location> \
  managedEnvironmentId=<managed-environment-id> \
  workloadProfileName=<workload-profile-name> \
  resourceConfig=<resource-config>

