#!/bin/bash

# Load variables
if [ -f .env ]; then
  source .env
fi

# ___VARIABLES___
UNIVERSAL_STORAGE_NAME=sadahestorage
IMAGE_NAME="helenedubourg/sadahescrapy"
ENVIRONMENT_NAME=sadaheenvironment
SUBSCRIPTION_ID="029b3537-0f24-400b-b624-6058a145efe1"
APP_FUNCTION_NAME=sadahescrapyfunction

# mettre à niveau l'extension Azure Container Apps
az extension add --name containerapp --upgrade -y
az provider register --namespace Microsoft.Web 
az provider register --namespace Microsoft.App 
az provider register --namespace Microsoft.OperationalInsights

# Créer un groupe de ressources
if ! az group show --name $RESOURCE_GROUP &>/dev/null; then
  az group create --name $RESOURCE_GROUP --location $LOCATION
fi

# Créer un environnement Azure Container App
az containerapp env create --name $ENVIRONMENT_NAME \
  --enable-workload-profiles \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Créer un groupe de stockage universel
if ! az storage account show --name $UNIVERSAL_STORAGE_NAME &>/dev/null; then
  az storage account create --name $UNIVERSAL_STORAGE_NAME \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --sku Standard_LRS
fi

# Vérifier que l'environnement est prêt
az containerapp env show -n $ENVIRONMENT_NAME \
  -g $RESOURCE_GROUP

# Créer une application de fonction
az functionapp create --name $APP_FUNCTION_NAME \
  --storage-account $STORAGE_NAME \
  --environment $ENVIRONMENT_NAME \
  --workload-profile-name "Consumption" \
  --resource-group $RESOURCE_GROUP \
  --functions-version 4 \
  --runtime dotnet-isolated \
  --image $IMAGE_NAME

# ajouter les variables d'environnement pour la connexion à la bdd pour scrapy
az functionapp config appsettings set --name $APP_FUNCTION_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "PGUSER=$ADMIN_USER" "PGPASSWORD=$ADMIN_PASSWORD" "PGHOST='$SERVER_URL'" "PGPORT=5432" "PGDATABASE=$DATABASE_NAME"


# Vérifier la fonction
az functionapp function show --resource-group $RESOURCE_GROUP \
  --name $APP_FUNCTION_NAME \
  --function-name scrapytimer \
  --query invokeUrlTemplate