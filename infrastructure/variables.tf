variable "http_proxy" {
  type      = string
  sensitive = true
}

variable "fetcher_image_tag" {
  type = string
}

variable "loader_image_tag" {
  type = string
}

variable "pg_host" {
  type      = string
  sensitive = true
}

variable "pg_db" {
  type      = string
  sensitive = true
}

variable "pg_user" {
  type      = string
  sensitive = true
}

variable "pg_pass" {
  type      = string
  sensitive = true
}
