locals {
  vm_tags = ["web-app", "allow-ssh"]

  vm_labels = {
    app  = "nginx"
    type = "webapp"
    env  = "dev"
  }
}
