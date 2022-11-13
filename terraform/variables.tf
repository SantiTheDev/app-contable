terraform {

  required_version = ">=0.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "DevOps"
    storage_account_name = "santiagoremotefiles"
    container_name       = "tfstate"
    key                  = "codelab.microsoft.tfstate"
  }
}

provider "azurerm" {
    tenant_id = "ea649e50-27d2-4318-9cb9-2fcffe16fd41"
    subscription_id = "7e5a743d-1f65-4bfc-afcb-1f0595d664ed"
    features {}
}
