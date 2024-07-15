#!/bin/bash

# Load variables
if [ -f .env ]; then
  source .env
fi

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

# # # Wait for Azure Function to be ready
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


