#Gcp Infra end to end Automation

module "gcp_devops" {
  source = "./modules/gcp-devops"

  region          = "us-west4"
  zone            = "us-west4-b"
  projectId       = "pythonproject-335216"
  env             = ["uat", "prod"]
  vm              = ["vm1", "vm2"]
  client          = ["abc", "xyz"]
  sa_id           = "python-readonly-access"
  vpc             = "main"
  bucket_name     = "bucket1"
  public_subnets  = ["10.26.1.0/24", "10.26.2.0/24"]
  private_subnets = ["10.26.3.0/24", "10.26.4.0/24"]
  file_name       = "dummy.txt"
}
