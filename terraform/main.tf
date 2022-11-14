resource "azurerm_resource_group" "DevOps_rg" {
  name = "DevOps"
  location = "eastus"
}

resource "azurerm_container_group" "appcg"{
  name = "app-contable"
  location = azurerm_resource_group.DevOps_rg.location
  resource_group_name = azurerm_resource_group.DevOps_rg.name
  
  ip_address_type = "public"
  dns_name_label = "app-contable"
  os_type = "Linux"

  container {
    name = "app-contable"
    image = "santithedev/app-contable:0.0.1"
    cpu = "1"
    memory = "1"

    ports {
      port = "80"
      protocol = "TCP"
    }
  }
}