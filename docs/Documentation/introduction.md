# Documentation Database Simplon

## Introduction

This programm create a database to compare its training programs with those of other training centers.

To achieve this, the program retrieves training courses from the France Compétences website through its API. Then, the program scrapes the Simplon website to gather information on training courses currently being offered.

The API allows querying the created database to find the sought training courses based on the information source (Simplon or France Compétences), the region where the training takes place, and the formacodes.

## Code Structure

**azure_resources**: creates and deletes Azure resources.

**azurefunction**: this folder contains the various parts of the automation of data retrieval from the France Compétences and Simplon websites.

**bdd_structure**: this folder contains the database schemas.

### Authentification


## Endpoints
