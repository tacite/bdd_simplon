#!/bin/bash

# ___VARIABLES___

# Ressource Group
RESOURCE_GROUP=RG_SADAHE2
LOCATION=francecentral
# Flexible server - Database
SERVER_NAME=sadaheformationserver2
SKU_SERVER=Standard_B1ms
ADMIN_PASSWORD=SadaHe111
ADMIN_USER=adminsadahe
DATABASE_NAME=sadaheformations
# Storage
# STORAGE_NAME=formationsadahestorage2
SKUNAME=Standard_LRS
CONTAINER_NAME=sadaheformationscontainer
UNIVERSAL_STORAGE_NAME=sadahestorage
IMAGE_NAME="helenedubourg/sadahescrapy"
ENVIRONMENT_NAME=sadaheenvironment
# SUBSCRIPTION_ID="029b3537-0f24-400b-b624-6058a145efe1"
APP_FUNCTION_NAME=sadahescrapyfunction

# Erase .env if exist to renew values
if [ -f ".env" ]; then
    rm ".env"
fi

# Create resources group
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

echo "___RESSOURCES_GROUP___ finish"

# # ___STORAGE___

# # Create storage account
# az storage account create \
#     --name $STORAGE_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --sku $SKUNAME

# # Get storage key
# STORAGE_KEY=$(az storage account keys list \
#     --resource-group $RESOURCE_GROUP \
#     --account-name $STORAGE_NAME \
#     --query '[0].value' \
#     --output tsv)

# # Create storage container
# az storage container create \
#     --name $CONTAINER_NAME \
#     --account-name $STORAGE_NAME \
#     --account-key $STORAGE_KEY

# echo "___STORAGE___ finish"

# ___DATABASE___

# Create flexible server "Development"
# az postgres flexible-server create \
#     --name $SERVER_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --location $LOCATION \
#     --admin-password $ADMIN_PASSWORD \
#     --admin-user $ADMIN_USER \
#     --sku-name $SKU_SERVER \
#     --tier Burstable \
#     --version 12 \
#     --database-name $DATABASE_NAME\

# Configure connexion parameters
# az postgres flexible-server firewall-rule create \
#     --resource-group $RESOURCE_GROUP \
#     --name $SERVER_NAME \
#     --rule-name AllowAll \
#     --start-ip-address 0.0.0.0 \
#     --end-ip-address 0.0.0.0

# Wait for the PostgreSQL server to be available and retrieve "SERVER_URL="
while [ -z "$SERVER_URL" ]; do
    # Check server status
    SERVER_STATE=$(az postgres flexible-server show \
        --name $SERVER_NAME \
        --resource-group $RESOURCE_GROUP \
        --query 'state' \
        --output tsv)
    
    if [ "$SERVER_STATE" == "Ready" ]; then
        SERVER_URL=$(az postgres flexible-server show \
            --name $SERVER_NAME \
            --resource-group $RESOURCE_GROUP \
            --query 'fullyQualifiedDomainName' \
            --output tsv)
    fi

    if [ -z "$SERVER_URL" ]; then
        echo "Waiting for PostgreSQL server to be ready... Current state: $SERVER_STATE"
        sleep 50
    fi
done

echo "PostgreSQL server is ready with URL: $SERVER_URL"

# Create PostgreSQL database
# az postgres flexible-server db create \
#     --resource-group $RESOURCE_GROUP \
#     --server-name $SERVER_NAME \
#     --database-name $DATABASE_NAME

echo "___DATABASE___ finish"

# ___FUNCTION___

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
# az containerapp env create --name $ENVIRONMENT_NAME \
#   --enable-workload-profiles \
#   --resource-group $RESOURCE_GROUP \
#   --location $LOCATION

# Créer un groupe de stockage universel
# if ! az storage account show --name $UNIVERSAL_STORAGE_NAME &>/dev/null; then
#   az storage account create --name $UNIVERSAL_STORAGE_NAME \
#     --location $LOCATION \
#     --resource-group $RESOURCE_GROUP \
#     --sku Standard_LRS
# fi

# Vérifier que l'environnement est prêt
az containerapp env show -n $ENVIRONMENT_NAME \
  -g $RESOURCE_GROUP

# Créer une application de fonction
az functionapp create --name $APP_FUNCTION_NAME \
  --storage-account $UNIVERSAL_STORAGE_NAME \
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

# Save variables in .env file
cat <<EOT > .env
# ___RESSOURCE_GROUP___
RESOURCE_GROUP=$RESOURCE_GROUP
LOCATION=$LOCATION
# ___DATABASE___
PGHOST=$SERVER_URL
PGUSER=$ADMIN_USER
PGPORT=5432
PGDATABASE=$DATABASE_NAME
PGPASSWORD=$ADMIN_PASSWORD
DATABASE_URL="postgresql+psycopg2://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_URL:5432/$DATABASE_NAME"
SKU_SERVER=$SKU_SERVER
SERVER_NAME=$SERVER_NAME
# ___STORAGE___
STORAGE_NAME=$STORAGE_NAME
SKUNAME=$SKUNAME
#STORAGE_KEY="$STORAGE_KEY"
CONTAINER_NAME=$CONTAINER_NAME
EOT

echo ".env file created successfully with the following content:"
cat .env
