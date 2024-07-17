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
APP_FUNCTION_NAME=sadahescrapyfunction

# mettre à niveau l'extension Azure Container Apps
az extension add --name containerapp --upgrade -y
az provider register --namespace Microsoft.Web 
az provider register --namespace Microsoft.App 
az provider register --namespace Microsoft.OperationalInsights

# Créer un groupe de ressources
az group create --name AzureFunctionsContainers-rg --location $LOCATION

# Créer un environnement Azure Container App
az containerapp env create --name MyContainerappEnvironment --enable-workload-profiles --resource-group AzureFunctionsContainers-rg --location $LOCATION

# Créer un groupe de stockage universel
az storage account create --name $STORAGE_NAME --location $LOCATION --resource-group AzureFunctionsContainers-rg --sku Standard_LRS

# Vérifier que l'environnement est prêt
az containerapp env show -n MyContainerappEnvironment -g AzureFunctionsContainers-rg

# Créer une application de fonction
az functionapp create --name $APP_FUNCTION_NAME --storage-account $STORAGE_NAME --environment MyContainerappEnvironment --workload-profile-name "Consumption" --resource-group AzureFunctionsContainers-rg --functions-version 4 --runtime dotnet-isolated --image $IMAGE_NAME

# Vérifier la fonction
az functionapp function show --resource-group AzureFunctionsContainers-rg --name $APP_FUNCTION_NAME --function-name scrapytimer --query invokeUrlTemplate