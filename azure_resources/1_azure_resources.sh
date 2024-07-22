#!/bin/bash

# When change Dockerfile, build and push new image, deploy the function and restart
# az functionapp deployment container config --enable-cd true -n sadahescrapyfunction -g RG_SADAHE
# az functionapp restart -n sadahescrapyfunction -g RG_SADAHE

# ___VARIABLES___

# Ressource Group
RESOURCE_GROUP=RG_SADAHE
LOCATION=francecentral
# Flexible server - Database
SERVER_NAME=sadaheformationserver
SKU_SERVER=Standard_B1ms
ADMIN_PASSWORD=SadaHe111
ADMIN_USER=adminsadahe
DATABASE_NAME=sadaheformations
# Function
SKUNAME=Standard_LRS
UNIVERSAL_STORAGE_NAME=sadahestorage
IMAGE_NAME="helenedubourg/sadahescrapy"
ENVIRONMENT_NAME=sadaheenvironment
APP_FUNCTION_NAME=sadahescrapyfunction
FUNCTION_NAME=sadahescrapytimer

# Erase .env if exist to renew values
if [ -f ".env" ]; then
    rm ".env"
fi

# Create resources group is does not exist
if ! az group show --name $RESOURCE_GROUP &>/dev/null; then
  az group create --name $RESOURCE_GROUP --location $LOCATION
fi

echo "___RESSOURCES_GROUP___ finish"

# ___DATABASE___

# Create flexible server "Development" if does not exist
if ! az postgres flexible-server show --name $SERVER_NAME --resource-group $RESOURCE_GROUP &>/dev/null; then
  az postgres flexible-server create \
      --name $SERVER_NAME \
      --resource-group $RESOURCE_GROUP \
      --location $LOCATION \
      --admin-password $ADMIN_PASSWORD \
      --admin-user $ADMIN_USER \
      --sku-name $SKU_SERVER \
      --tier Burstable \
      --version 12 \
      --database-name $DATABASE_NAME
fi

# Configure connexion parameters if does not exist
if ! az postgres flexible-server firewall-rule show --resource-group $RESOURCE_GROUP --name $SERVER_NAME --rule-name AllowAll &>/dev/null; then
  az postgres flexible-server firewall-rule create \
      --resource-group $RESOURCE_GROUP \
      --name $SERVER_NAME \
      --rule-name AllowAll \
      --start-ip-address 0.0.0.0 \
      --end-ip-address 255.255.255.255
fi

# Wait for the PostgreSQL server to be available and retrieve "SERVER_URL="
SERVER_URL=""
while [ -z "$SERVER_URL" ]; do
    # Vérifier l'état du serveur
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

# Create PostgreSQL database if does not exist
if ! az postgres flexible-server db show --resource-group $RESOURCE_GROUP --server-name $SERVER_NAME --database-name $DATABASE_NAME &>/dev/null; then
  az postgres flexible-server db create \
      --resource-group $RESOURCE_GROUP \
      --server-name $SERVER_NAME \
      --database-name $DATABASE_NAME
fi

echo "___DATABASE___ finish"

# ___FUNCTION___

# Upgrade the Azure Container Apps extension
az extension add --name containerapp --upgrade -y
az provider register --namespace Microsoft.Web 
az provider register --namespace Microsoft.App 
az provider register --namespace Microsoft.OperationalInsights

# Create Azure Container App environment if it does not exist
if ! az containerapp env show --name $ENVIRONMENT_NAME --resource-group $RESOURCE_GROUP &>/dev/null; then
  az containerapp env create --name $ENVIRONMENT_NAME \
    --enable-workload-profiles \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION
fi

# Create universal storage group if does not exist
if ! az storage account show --name $UNIVERSAL_STORAGE_NAME &>/dev/null; then
  az storage account create --name $UNIVERSAL_STORAGE_NAME \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --sku $SKUNAME
fi

# Check if environment is ready
az containerapp env show -n $ENVIRONMENT_NAME \
  -g $RESOURCE_GROUP

# Create function app if it does not exist
if ! az functionapp show --name $APP_FUNCTION_NAME --resource-group $RESOURCE_GROUP &>/dev/null; then
  az functionapp create --name $APP_FUNCTION_NAME \
    --storage-account $UNIVERSAL_STORAGE_NAME \
    --environment $ENVIRONMENT_NAME \
    --workload-profile-name "Consumption" \
    --resource-group $RESOURCE_GROUP \
    --functions-version 4 \
    --runtime dotnet-isolated \
    --image $IMAGE_NAME
fi

# Add env variables for scrapy
az functionapp config appsettings set --name $APP_FUNCTION_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "PGUSER=$ADMIN_USER" "PGPASSWORD=$ADMIN_PASSWORD" "PGHOST='$SERVER_URL'" "PGPORT=5432" "PGDATABASE=$DATABASE_NAME"


# Check function
az functionapp function show --resource-group $RESOURCE_GROUP \
  --name $APP_FUNCTION_NAME \
  --function-name $FUNCTION_NAME \
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
# ___FUNCTION___
UNIVERSAL_STORAGE_NAME=$UNIVERSAL_STORAGE_NAME
IMAGE_NAME=$IMAGE_NAME
ENVIRONMENT_NAME=$ENVIRONMENT_NAME
APP_FUNCTION_NAME=$APP_FUNCTION_NAME
FUNCTION_NAME=$FUNCTION_NAME
EOT

echo ".env file created successfully with the following content:"
cat .env
