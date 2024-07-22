#!/bin/bash

# Load variables
source .env

# Delete resource group
az group delete --resource-group $RESOURCE_GROUP
# az group delete --resource-group RG_SADAHE