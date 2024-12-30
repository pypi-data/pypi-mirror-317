Kaizen-Deploy is an open-source tool that can be used for deploying KIMS(Kubernetes Incident Management System). This is an open-source project however, authorization rights and confidential modules belongs to the owner itself. Self written modules based on Python3 works with the tool.


[![PyPi Version Alt](https://badge.fury.io/py/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)  
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)

[![kaizen-deploy](https://img.shields.io/static/v1?label=gandalf-cmt&message=v1.1.0&color=yellowgreen)](https://pypi.org/project/kaizen-deploy/)
[![release](https://img.shields.io/static/v1?label=release&message=v1.1.0&color=orange)](https://pypi.org/project/kaizen-deploy/1.1.0/)




## Prerequisite: 

##### Linux
In the case of Linux based systems, set environment variable path and provide execution permission: 
```Shell
PATH=$PATH:/usr/local/Lib/kaizen-deploy/
chmod 774 /usr/local/Lib/kaizen-deploy/main
```

## Command usage:
`kaizen-deploy --scroll [yaml file]`

## Requirements
* Python >= 3.9.6

## Parameters
 

[![OS](https://img.shields.io/static/v1?label=OS&message=Linux&color=red)](https://pypi.org/project/kaizen-deploy/)
[![Stage](https://img.shields.io/static/v1?label=Stage&message=Stable&color=blue)](https://pypi.org/project/kaizen-deploy/)

|**Parameter**|**Choices/Defaults**|**Comments**|
|-------------|--------------------|------------|
|**clusterName** |Any| Name of the Kubernetes cluster.
|**jutsu/database/username** |Any| Name of the database user. This username can be used to login to the KIMS PostgreSQL server to check data feeds.
|**jutsu/database/password** |Any| Password for the database user. This password can be used to login to the KIMS PostgreSQL server to check data feeds.
|**jutsu/AICloudProvisioner** |**Choices:** **azure** or  **aws** or **anthropic**| Name of the AI Cloud provisioner. OpenAi in Azure or Bedrock in AWS or Anthropic can be used.
|**jutsu/azureOpenAI/deploymentEndpoint** |If Azure is used as the AI Cloud provisioner| OpenAi deployment endpoint URL.
|**jutsu/azureOpenAI/apiKey** |If Azure is used as the AI Cloud provisioner| OpenAi deployment API key.
|**jutsu/azureOpenAI/apiVersion** |If Azure is used as the AI Cloud provisioner| OpenAi deployment API version..
|**jutsu/azureOpenAI/deploymentName** |If Azure is used as the AI Cloud provisioner| OpenAi deployment name (Eg: gpt-4).
|**jutsu/alertManager/teamsWebhookURL** |Any| The Microsoft Webhook URL/Workflow URL for sending Kubernetes incident notification.
|**jutsu/alertManager/kimsUIURL** |Any| The Microsoft Webhook URL/Workflow URL for sending Kubernetes incident notification.

  
  
### Example
  
```YAML
---

clusterName: docker-desktop

jutsu:
  database:
    username: postgres
    password: postgres
  AICloudProvisioner: azure
  azureOpenAI:
    deploymentEndpoint: "https://test.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview"
    apiKey: "DWFDF7832bDQDds8wQwc23SQsfdsqd23sdQW"
    apiVersion: "2024-02-01"
    deploymentName: "gpt-4"
  alertManager:
    teamsWebhookURL: "https://prod-13.centralindia.logic.azure.com:443/workflows/34nkjb34b3b141/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&si3wqqwlfMZpiQsfds_sdbqs1h-ZqcY"
    kimsUIURL: "http://kims-incident-dashboard-v1.eastus.cloudapp.azure.com:31000/incidents"
```
  



