locals {
  tags = ["allow-ssh", "web-app"]
  vm_labels = {
    app  = "nginx"
    env  = "dev"
    type = "webapp"
  }
}
