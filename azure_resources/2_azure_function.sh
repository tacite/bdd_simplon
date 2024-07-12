#!/bin/bash

# Variables générales
# Resources
RESOURCE_GROUP=RG_SADAHE
LOCATION=francecentral
BASE_DIR=$(pwd)
# Database
SERVER_NAME=sadaheformationserver2
SKU_SERVER=Standard_B1ms
ADMIN_PASSWORD=sad@he
ADMIN_USER=adminsadahe
DATABASE_NAME=sadaheformations
# Storage
STORAGE_NAME=formationsadahestorage
SKUNAME=Standard_LRS
CONTAINER_NAME=sadaheformationscontainer
# Datafactory
DATAFACT_NAME=sadaheformationsdatatfact
PIPELINE_NAME=sadaheformationspipeline
TRIGGER_NAME=WeeklyTrigger
# Scrapy
SCRAPY_PROJECT_DIR="$BASE_DIR/../simplonscrapy"
ZIP_FILE="$BASE_DIR/simplonscrapy.zip"
# Function
FUNC_APP_NAME=SadaheFunctionApp

# Erase .env if exist to renew values
if [ -f ".env" ]; then
    rm ".env"
fi

# Créer le groupe de ressources
# az group create --name $RESOURCE_GROUP --location $LOCATION

# ___DATABASE___
# Créer le serveur PostgreSQL flexible
# az postgres flexible-server create \
#     --name $SERVER_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --admin-password $ADMIN_PASSWORD \
#     --admin-user $ADMIN_USER \
#     --public all\
#     --storage-size 32 \
#     --sku-name $SKU_SERVER \
#     --tier Burstable \
#     --version 13

# # Get server URL
# while [ -z "$SERVER_URL" ]; do
#     SERVER_STATE=$(az postgres flexible-server show --name $SERVER_NAME --resource-group $RESOURCE_GROUP --query 'state' --output tsv)
#     if [ "$SERVER_STATE" == "Ready" ]; then
#         SERVER_URL=$(az postgres flexible-server show --name $SERVER_NAME --resource-group $RESOURCE_GROUP --query 'fullyQualifiedDomainName' --output tsv)
#     fi

#     if [ -z "$SERVER_URL" ]; then
#         echo "Waiting for PostgreSQL server to be ready... Current state: $SERVER_STATE"
#         sleep 50
#     fi
# done

# Create PostgreSQL database
# az postgres flexible-server db create \
#     --resource-group $RESOURCE_GROUP \
#     --server-name $SERVER_NAME \
#     --database-name $DATABASE_NAME

# echo "___DATABASE___ finish"

# ___STORAGE___

# Create storage account
# az storage account create \
#     --name $STORAGE_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --sku $SKUNAME

# Get storage key
# while [ -z "$STORAGE_KEY" ]; do
#     STORAGE_KEY=$(az storage account keys list \
#     --resource-group $RESOURCE_GROUP \
#     --account-name $STORAGE_NAME \
#     --query '[0].value' \
#     --output tsv)
    
#     if [ -z "$STORAGE_KEY" ]; then
#         echo "La clé de stockage n'a pas pu être récupérée. Nouvelle tentative dans 5 secondes..."
#         sleep 5
#     fi
# done

# Create storage container
# az storage container create \
#     --name $CONTAINER_NAME \
#     --account-name $STORAGE_NAME \
#     --account-key $STORAGE_KEY

# echo "___STORAGE___ finish"

# ___DATAFACTORY___

# Create Azure Data Factory
# az datafactory create \
#     --resource-group $RESOURCE_GROUP \
#     --name $DATAFACT_NAME \
#     --location $LOCATION

# echo "___DATAFACTORY___ finish"

# ___FUNCTION___

# # Create Azure Function
# az functionapp create \
#     --name $FUNC_APP_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --consumption-plan-location $LOCATION \
#     --runtime python \
#     --runtime-version 3.11 \
#     --functions-version 4 \
#     --storage-account $STORAGE_NAME \
#     --os-type Linux

# # Wait for Azure Function to be ready
# while true; do
#     FUNC_APP_STATE=$(az functionapp show --resource-group $RESOURCE_GROUP --name $FUNC_APP_NAME --query 'state' --output tsv)
#     if [ "$FUNC_APP_STATE" == "Running" ]; then
#         break
#     fi
#     echo "Waiting for Function App to be ready... Current state: $FUNC_APP_STATE"
#     sleep 10
# done

# echo "___AZURE FUNCTION___ finish"

# # Get functionapp key
# while [ -z "$FUNCTION_KEY" ]; do
#     FUNCTION_KEY=$(az functionapp keys list \
#         --resource-group $RESOURCE_GROUP \
#         --name $FUNC_APP_NAME \
#         --query 'functionKeys.default' \
#         --output tsv)
    
#     if [ -z "$FUNCTION_KEY" ]; then
#         echo "La clé de la Function App n'a pas pu être récupérée. Nouvelle tentative dans 5 secondes..."
#         sleep 5
#     fi
# done

# echo "___FUNCTION KEY___ finish"

# Deploy functionapp
func azure functionapp publish $FUNC_APP_NAME --python \
    --settings DB_HOST=$SERVER_URL \
    --settings DB_USER=$ADMIN_USER \
    --settings DB_PASSWORD=$ADMIN_PASSWORD \
    --settings DB_DATABASE=$DATABASE_NAME \

echo "___DEPLOY___ finish"

# Remplacement des variables dans le JSON
sed -e "s|{{FUNCTION_APP_NAME}}|$FUNC_APP_NAME|g" \
    -e "s|{{FUNCTION_KEY}}|$FUNCTION_KEY|g" \
    function_properties_template.json > function_properties.json
    
FunctionLinkedServiceName="FunctionLinkedService"
Functionjsonpath="json/function_properties.json"

# /!\ jq must be installed
FunctionServiceContent=$(cat $Functionjsonpath | jq -c '.')

# Create linked service
az datafactory linked-service create \
    --factory-name $DATAFACT_NAME \
    --properties "$FunctionServiceContent" \
    --name $FunctionLinkedServiceName \
    --resource-group $RESOURCE_GROUP

# ___PIPELINE___

PipelineName="PythonPipeline"
Pipelinejsonpath="json/pipeline_properties.json"

# /!\ jq must be installed
PipelineContent=$(cat $Pipelinejsonpath | jq -c '.')

# Create linked service
az datafactory pipeline create \
    --factory-name $DATAFACT_NAME \
    --pipeline "$PipelineContent" \
    --name $PipelineName \
    --resource-group $RESOURCE_GROUP

# ___TRIGGER___

TriggerName="TriggerPythonPipeline"
Triggerjsonpath="json/trigger_properties.json"

# /!\ jq must be installed
TriggerContent=$(cat $Triggerjsonpath | jq -c '.')

# Create Trigger
az datafactory trigger create \
    --factory-name $DATAFACT_NAME \
    --properties "$TriggerContent" \
    --name $TriggerName \
    --resource-group $RESOURCE_GROUP

# Start trigger
az datafactory trigger start \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name $TriggerName

# Save variables in .env
cat <<EOT > .env
# Ressource Group
RESOURCE_GROUP=$RESOURCE_GROUP
LOCATION=$LOCATION
BASE_DIR=$(pwd)
# PostgreSQL
PGHOST=$SERVER_URL
PGUSER=$ADMIN_USER
PGPORT=5432
PGDATABASE=$DATABASE_NAME
PGPASSWORD=$ADMIN_PASSWORD
DATABASE_URL="postgresql+psycopg2://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_URL:5432/$DATABASE_NAME"
# Storage
STORAGE_NAME=$STORAGE_NAME
SKUNAME=$SKUNAME
CONTAINER_NAME=$CONTAINER_NAME
STORAGE_KEY="$STORAGE_KEY"
# Datafactory
DATAFACT_NAME=$DATAFACT_NAME
PIPELINE_NAME=$PIPELINE_NAME
# Function
FUNC_APP_NAME=$FUNC_APP_NAME
FUNCTION_KEY="$FUNCTION_KEY"
EOT

echo ".env file created successfully with the following content:"
cat .env
