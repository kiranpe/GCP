variable "region" {
  type = string
}

variable "zone" {
  type = string
}

variable "projectId" {
  type = string
}

variable "bucket_name" {
  type = string
}

variable "env" {
  type = list(string)
}

variable "vm" {
  type = list(string)
}

variable "client" {
  type = list(string)
}

variable "sa_id" {
  type = string
}

variable "vpc" {
  type = string
}

variable "public_subnets" {
  type = list(string)
}

variable "private_subnets" {
  type = list(string)
}

variable "file_name" {
  type = string
}
