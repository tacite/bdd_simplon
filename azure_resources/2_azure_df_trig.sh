#!/bin/bash

# ___VARIABLES___

source .env

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

# Associate Batch and Resource Group
az batch account login \
    --name $BATCH_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --shared-key-auth

# Create Pool
az batch pool create \
    --id $POOL_NAME \
    --image canonical:0001-com-ubuntu-server-focal:20_04-lts \
    --node-agent-sku-id "batch.node.ubuntu 20.04" \
    --target-dedicated-nodes 1 \
    --vm-size Standard_A1_v2 \

# Deploy Scrapy in Blob Container
cd $SCRAPY_PROJECT_DIR
zip -r $ZIP_FILE .
az storage blob upload \
    --account-name $STORAGE_NAME \
    --container-name $CONTAINER_NAME \
    --name simplonscrapy.zip \
    --file $ZIP_FILE \
    --overwrite

# Create Linked Service for Azure Storage
az datafactory linked-service create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name AzureStorageLinkedService \
    --properties '{
      "type": "AzureBlobStorage",
      "typeProperties": {
        "connectionString": "DefaultEndpointsProtocol=https;AccountName='$STORAGE_NAME';AccountKey='$STORAGE_KEY';EndpointSuffix=core.windows.net"
      }
    }'

# Create Azure Batch Linked Service for Data Factory
az datafactory linked-service create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name AzureBatchLinkedService \
    --properties '{
        "type": "AzureBatch",
        "typeProperties": {
            "accountName": "'"$BATCH_ACCOUNT_NAME"'",
            "batchUri": "'"https://$BATCH_URL"'",
            "poolName": "'"$POOL_NAME"'",
            "linkedServiceName": {
                "referenceName": "AzureStorageLinkedService",
                "type": "LinkedServiceReference"
            }
        }
    }'
  
# Create Data Factory Pipeline
cd $BASE_DIR
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

Pipelinejsonpath="pipeline.json"

# jq must be add to your computer
PipelineContent=$(cat $Pipelinejsonpath | jq -c '.')

az datafactory pipeline create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name $PIPELINE_NAME \
    --pipeline "$PipelineContent" \

# Plan Pipeline every week
az datafactory trigger create \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name $TRIGGER_NAME \
    --properties '{
      "type": "ScheduleTrigger",
      "pipelines": [
        {
          "pipelineReference": {
            "referenceName": "'"${PIPELINE_NAME}"'",
            "type": "PipelineReference"
          }
        }
      ],
      "typeProperties": {
        "recurrence": {
          "frequency": "Week",
          "interval": 1,
          "startTime": "2023-07-01T00:00:00Z"
        }
      }
    }'

# Start Trigger
az datafactory trigger start \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --name $TRIGGER_NAME

# Execute the trigger manuelly just after creation
az datafactory pipeline create-run \
    --resource-group $RESOURCE_GROUP \
    --factory-name $DATAFACT_NAME \
    --pipeline-name $PIPELINE_NAME
echo "___DATAFACTORY-PIPELINE___ finish"

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
