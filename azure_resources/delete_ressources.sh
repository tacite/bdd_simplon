#!/bin/bash

# Load variables
source ../simplonscrapy/.env

# Delete resource group
az group delete --resource-group $RESOURCE_GROUP