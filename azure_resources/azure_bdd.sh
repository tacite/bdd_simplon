#!/bin/bash

# ___VARIABLES___

# Ressource Group
RESOURCE_GROUP=RG_SADAHE
LOCATION=francecentral
# Flexible server - Database
SERVER_NAME=sadaheformationserver
SKU_SERVER=Standard_B1ms
ADMIN_PASSWORD=sad@he
ADMIN_USER=adminsadahe
DATABASE_NAME=sadaheformations
# Storage
STORAGE_NAME=formationsadahestorage
SKUNAME=Standard_LRS
CONTAINER_NAME=sadaheformationscontainer
# Datafactory - pipeline
DATAFACT_NAME=sadaheformationsdatatfact
PIPELINE_NAME=sadaheformationspipeline
# Batch - pool
BATCH_ACCOUNT_NAME=sadahescrapybatch
POOL_NAME=sadahescrapypool
# Scrapy
SCRAPY_PROJECT_DIR="../simplonscrapy"

# Erase .env if exist to renew values
if [ -f ".env" ]; then
    rm ".env"
fi

# Create resources group
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

echo "___RESSOURCES_GROUP___ finish"

# ___STORAGE___

# Create storage account
az storage account create \
    --name $STORAGE_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku $SKUNAME

# Get storage key
STORAGE_KEY=$(az storage account keys list \
    --resource-group $RESOURCE_GROUP \
    --account-name $STORAGE_NAME \
    --query '[0].value' \
    --output tsv)

# Create storage container
az storage container create \
    --name $CONTAINER_NAME \
    --account-name $STORAGE_NAME \
    --account-key $STORAGE_KEY
echo "___STORAGE___ finish"

# ___DATABASE___

# Create flexible server "Development"
az postgres flexible-server create \
    --name $SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --admin-password $ADMIN_PASSWORD \
    --admin-user $ADMIN_USER \
    --sku-name $SKU_SERVER \
    --tier Burstable \
    --version 12 \
    --database-name $DATABASE_NAME\

# Configure connexion parameters
az postgres flexible-server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --name $SERVER_NAME \
    --rule-name AllowAll \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

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

# Create PostgreSQL database
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $SERVER_NAME \
    --database-name $DATABASE_NAME


echo "___DATABASE___ finish"

# ___DATAFACTORY - PIPELINE___

# Create Azure Data Factory
az datafactory create \
    --resource-group $RESOURCE_GROUP \
    --name $DATAFACT_NAME \
    --location $LOCATION

# Create Azure Batch
az batch account create \
    --name $BATCH_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --storage-account $STORAGE_NAME

# OK jusque là !

# Associate Batch and Resource Group
az batch account login \
    --name $BATCH_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --shared-key-auth

# Get ID of the Batch
while [ -z "$NODE_AGENT_SKU_ID" ]; do
    =$(az batch pool node-agent-skus list \
    --query "[?starts_with(id, 'batch.node.ubuntu')].id" \
    --output tsv | head -n 1)
    if [ -z "$NODE_AGENT_SKU_ID" ]; then
        echo "Waiting for Batch to be ready..."
        sleep 50
    fi
done

# Create Pool
az batch pool create \
    --id $POOL_NAME \
    --vm-size Standard_D2_v2 \
    --target-dedicated-nodes 1 \
    --image canonical:ubuntuserver:18.04-LTS \
    --node-agent-sku-id $NODE_AGENT_SKU_ID

# Deploy Scrapy in Blob Container
cd $SCRAPY_PROJECT_DIR
zip -r simplonscrapy.zip .
az storage blob upload \
    --account-name $STORAGE_NAME \
    --container-name $CONTAINER_NAME \
    --name simplonscrapy.zip \
    --file simplonscrapy.zip

# Create Data Factory Pipeline in the right directory
cd ../azure_ressources
cat << EOF > pipeline.json
{
  "name": "$PIPELINE_NAME",
  "properties": {
    "activities": [
      {
        "name": "RunScrapySpider",
        "type": "ExecutePipeline",
        "dependsOn": [],
        "userProperties": [],
        "linkedServiceName": {
          "referenceName": "AzureBatchLinkedService",
          "type": "LinkedServiceReference"
        },
        "typeProperties": {
          "pipelineReference": {
            "referenceName": "ExecuteScrapySpider",
            "type": "PipelineReference"
          }
        },
        "policy": {
          "timeout": "7.00:00:00",
          "retry": 3,
          "retryIntervalInSeconds": 30,
          "secureOutput": false,
          "secureInput": false
        }
      }
    ]
  }
}
EOF

az datafactory pipeline create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name $PIPELINE_NAME \
    --pipeline-definition @pipeline.json

# Plan Pipeline every week
az datafactory trigger create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name WeeklyTrigger \
    --type ScheduleTrigger \
    --pipeline-name $PIPELINE_NAME \
    --recurrence-expression "0 0 * * 1"

echo "___DATAFACTORY-PIPELINE___ finish"

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
STORAGE_KEY=$STORAGE_KEY
CONTAINER_NAME=$CONTAINER_NAME
# ___DATAFACTORY - PIPELINE___
DATAFACT_NAME=$DATAFACT_NAME
PIPELINE_NAME=$PIPELINE_NAME
# ___BATCH - POOL___
BATCH_ACCOUNT_NAME=$BATCH_ACCOUNT_NAME
NODE_AGENT_SKU_ID=$NODE_AGENT_SKU_ID
POOL_NAME=$POOL_NAME
EOT

echo ".env file created successfully with the following content:"
cat .env
