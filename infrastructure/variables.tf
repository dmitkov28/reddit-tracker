variable "image_tag" {
  type = string
}

variable "http_proxy" {
  type      = string
  sensitive = true
}
