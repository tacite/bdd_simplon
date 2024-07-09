#!/bin/bash

# ___VARIABLES___

# Ressource Group
RESOURCE_GROUP=RG_SADAHE
LOCATION=francecentral
# Flexible server - Database
SERVER_NAME=formationserver
SKU_SERVER=Standard_D2s_v3
ADMIN_PASSWORD=sad@he
ADMIN_USER=adminsadahe
DATABASE_NAME=formations
# Storage
STORAGE_NAME=formationsadahestorage
SKUNAME=Standard_LRS
CONTAINER_NAME=formationscontainer
# # Datafactory - pipeline
# DATAFACT_NAME=formationsdatatfact
# PIPELINE_NAME=formationspipeline
# # Batch - pool
# BATCH_ACCOUNT_NAME=scrapybatch
# BATCH_RESOURCE_GROUP=RG_BATCH
# POOL_NAME=scrapypool

# Erase .env if exist to renew values
if [ -f ".env" ]; then
    rm ".env"
fi

# Create resources group
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

echo "___RESSOURCES_GROUP___ finish"

# ___DATABASE___

# Create flexible server
az postgres flexible-server create \
    --name $SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --admin-password $ADMIN_PASSWORD \
    --admin-user $ADMIN_USER \
    --sku-name $SKU_SERVER \
    --database-name $DATABASE_NAME

# Wait for the PostgreSQL server to be available and retrieve "SERVER_URL="
while [ -z "$SERVER_URL" ]; do
    SERVER_URL=$(az postgres flexible-server show \
        --name $SERVER_NAME \
        --resource-group $RESOURCE_GROUP \
        --query 'fullyQualifiedDomainName' \
        --output tsv)
    if [ -z "$SERVER_URL" ]; then
        echo "Waiting for PostgreSQL server to be ready..."
        sleep 50
    fi
done

echo "___DATABASE___ finish"

# Save variables in .env fils
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
DATABASE_URL=postgresql+psycopg2://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_URL:5432/$DATABASE_NAME
SKU_SERVER=$SKU_SERVER
SERVER_NAME=$SERVER_NAME
# ___STORAGE___
STORAGE_NAME=$STORAGE_NAME
SKUNAME=$SKUNAME
CONTAINER_NAME=$CONTAINER_NAME
# ___DATAFACTORY - PIPELINE___
# DATAFACT_NAME=$DATAFACT_NAME
# PIPELINE_NAME=$PIPELINE_NAME
# ___BATCH - POOL___
# BATCH_ACCOUNT_NAME=$BATCH_ACCOUNT_NAME
# BATCH_RESOURCE_GROUP=$BATCH_RESOURCE_GROUP
# POOL_NAME=$POOL_NAME
EOT

echo ".env file created successfully with the following content:"
cat .env
