#!/bin/bash
az webapp up --name my-energy-analytics-app --resource-group myResourceGroup --runtime "PYTHON:3.10"
az webapp remote-connection create --name my-energy-analytics-app --resource-group myResourceGroup
