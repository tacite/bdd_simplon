# faire les manip pour ne plus avoir à mettre sudo
# docker build -t helenedubourg/sadahescrapy:latest /home/helene/Documents/bdd_simplon/bdd_simplon/azurefunction
# docker push helenedubourg/sadahescrapy:latest
# buid et push à chaque modification de function_app

# az functionapp deployment container config --enable-cd true -n sadahescrapyfunction -g RG_SADAHE
# az functionapp restart -n sadahescrapyfunction -g RG_SADAHE

# /home/site/wwwroot mène au dossier de l'azure function

# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot