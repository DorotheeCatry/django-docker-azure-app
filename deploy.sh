#!/bin/bash

# Variables
RESOURCE_GROUP="dcatryRG"
CONTAINER_NAME="django-app"
ACR_NAME="dcatryregistry"
ACR_IMAGE="django-app"
ACR_URL="$ACR_NAME.azurecr.io"
CPU="1"
MEMORY="4"
PORT="8000"
IP_ADDRESS="Public"
DNS_LABEL="elite-loans"  # ⚠ Azure DNS only accepts lowercase letters!
OS_TYPE="Linux"

# Check and load environment variables
if [ -f .env ]; then
    echo "✅ .env file found. Loading environment variables..."
    set -o allexport
    source .env
    set +o allexport
else
    echo "❌ .env file not found!"
    exit 1
fi

# Retrieve ACR credentials
echo "🔑 Retrieving ACR credentials..."
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

# Check if the container exists and delete if it does
EXISTING_CONTAINER=$(az container show --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --query "name" -o tsv 2>/dev/null)
if [ "$EXISTING_CONTAINER" == "$CONTAINER_NAME" ]; then
    echo "🗑️  Deleting existing container..."
    az container delete --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --yes
fi

# Deploy the container to Azure Container Instances
echo "🚀 Deploying container to Azure Container Instances..."
az container create \
    --name "$CONTAINER_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$ACR_URL/$ACR_IMAGE" \
    --cpu "$CPU" \
    --memory "$MEMORY" \
    --registry-login-server "$ACR_URL" \
    --registry-username "$ACR_USERNAME" \
    --registry-password "$ACR_PASSWORD" \
    --ports "$PORT" \
    --ip-address "$IP_ADDRESS" \
    --dns-name-label "$DNS_LABEL" \
    --os-type "$OS_TYPE" \
    --environment-variables DJANGO_DEBUG="$DJANGO_DEBUG" \
    ALLOWED_HOSTS="$ALLOWED_HOSTS" \
    SECRET_KEY="$SECRET_KEY" \
    API_USERNAME="$API_USERNAME" \
    API_PASSWORD="$API_PASSWORD" \
    API_BASE_URL="$API_BASE_URL" \
    API_AUTH_URL="$API_AUTH_URL" \
    API_LOANREQUEST_URL="$API_LOANREQUEST_URL" \
    API_HIST_URL="$API_HIST_URL" \
    DB_ENGINE="$DB_ENGINE" \
    DB_USERNAME="$DB_USERNAME" \
    DB_PASSWORD="$DB_PASSWORD" \
    DB_SERVER="$DB_SERVER" \
    DB_NAME="$DB_NAME" \
    DB_PORT="$DB_PORT" \
    DB_DRIVER="$DB_DRIVER"

# Check if the deployment was successful
if [ $? -eq 0 ]; then
    # Retrieve the application region
    LOCATION=$(az container show --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --query "location" -o tsv)
    echo "✅ Deployment succeeded!"
    echo "🌍 Container URL: http://$DNS_LABEL.$LOCATION.azurecontainer.io:$PORT"
else
    echo "❌ Deployment failed!"
    exit 1
fi
