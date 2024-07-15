# sudo docker build -t helenedubourg/sadahescrapy:tag /home/helene/Documents/bdd_simplon/bdd_simplon/azurefunction
# sudo docker push helenedubourg/sadahescrapy:tag

# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.12.0

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot