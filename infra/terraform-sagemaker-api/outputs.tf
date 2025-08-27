output "api_invoke_url" {
  value = "${aws_api_gateway_deployment.predict_deployment.invoke_url}"
}
