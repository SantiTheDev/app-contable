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
    storage_account_name = "tearraformstatefiles"
    container_name       = "tfstate"
    key                  = "remote.terraform.tfstate"
  }
}

provider "azurerm" {
    features {}
}
