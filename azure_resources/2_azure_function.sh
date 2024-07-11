#!/bin/bash

# Variables générales
RESOURCE_GROUP=RG_SADAHE
LOCATION=francecentral
SERVER_NAME=sadaheformationserver
SKU_SERVER=Standard_B1ms
ADMIN_PASSWORD=sad@he
ADMIN_USER=adminsadahe
DATABASE_NAME=sadaheformations
# Storage
STORAGE_NAME=formationsadahestorage
SKUNAME=Standard_LRS
CONTAINER_NAME=sadaheformationscontainer

DATAFACT_NAME=sadaheformationsdatatfact
PIPELINE_NAME=sadaheformationspipeline
TRIGGER_NAME=WeeklyTrigger
# Scrapy
BASE_DIR=$(pwd)
SCRAPY_PROJECT_DIR="$BASE_DIR/../simplonscrapy"
ZIP_FILE="$BASE_DIR/simplonscrapy.zip"

# # Créer le groupe de ressources
# az group create --name $RESOURCE_GROUP --location $LOCATION

# # Créer le serveur PostgreSQL flexible
# az postgres flexible-server create \
#     --name $SERVER_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --admin-password $ADMIN_PASSWORD \
#     --admin-user $ADMIN_USER \
#     --sku-name $SKU_SERVER \
#     --tier Burstable \
#     --version 12 \
#     --database-name $DATABASE_NAME

# # Attendre que le serveur PostgreSQL soit prêt
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

# # Créer la base de données PostgreSQL
# az postgres flexible-server db create \
#     --resource-group $RESOURCE_GROUP \
#     --server-name $SERVER_NAME \
#     --database-name $DATABASE_NAME

# # ___STORAGE___

# # Create storage account
# az storage account create \
#     --name $STORAGE_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --sku $SKUNAME

# Get storage key
STORAGE_KEY=$(az storage account keys list \
    --resource-group $RESOURCE_GROUP \
    --account-name $STORAGE_NAME \
    --query '[0].value' \
    --output tsv)

# # Create storage container
# az storage container create \
#     --name $CONTAINER_NAME \
#     --account-name $STORAGE_NAME \
#     --account-key $STORAGE_KEY

# echo "___STORAGE___ finish"

# Enregistrer les variables dans .env
cat <<EOT > .env
# Chemin de base
BASE_DIR=$(pwd)
# Ressource Group
RESOURCE_GROUP=$RESOURCE_GROUP
LOCATION=$LOCATION
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
STORAGE_KEY=$STORAGE_KEY
# Scraping
SCRAPY_PROJECT_DIR="$BASE_DIR/../simplonscrapy"
ZIP_FILE="$BASE_DIR/simplonscrapy.zip"
# Data Factory
DATAFACT_NAME=$DATAFACT_NAME
PIPELINE_NAME=$PIPELINE_NAME
# Trigger
TRIGGER_NAME=$TRIGGER_NAME
EOT

echo ".env file created successfully with the following content:"
cat .env

# # Create Azure Function
# az functionapp create \
#     --name SadaheFunctionApp \
#     --resource-group $RESOURCE_GROUP \
#     --consumption-plan-location $LOCATION \
#     --runtime python \
#     --runtime-version 3.8 \
#     --functions-version 4 \
#     --storage-account $STORAGE_NAME \
#     --os-type Linux

# Deploy scrapy project in Azure Function
cd $SCRAPY_PROJECT_DIR
zip -r $ZIP_FILE .
az functionapp deployment source config-zip \
    --src $ZIP_FILE \
    --name SadaheFunctionApp \
    --resource-group $RESOURCE_GROUP

# Run Azure Function
az functionapp start \
    --name SadaheFunctionApp \
    --resource-group $RESOURCE_GROUP

$FUNCTION_KEY
echo "Script executed successfully."
