# Route53 CNAME record pointing to the Load Balancer
resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.hosted_zone.zone_id
  name    = "${var.record_name}.${var.domain_name}"
  type    = "CNAME"
  ttl     = 60
  records = [aws_elastic_beanstalk_environment.main.endpoint_url]
}
