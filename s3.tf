resource "aws_s3_bucket" "test_tf_review_bucket" {
  bucket = "${terraform.env}-tf-review-bucket"
  acl = "private"
}

resource "aws_s3_bucket" "test_tf_review_bucket2" {
  bucket = "${terraform.env}-tf-review-bucket2"
  acl = "private"

  logging {
    target_bucket = "${terraform.env}-tf-review-bucket-log"
    target_prefix = "${terraform.env}-tf-review-bucket/"
  }

  lifecycle_rule {
    id = "cap-s3bucket-lifecycle-rule"
    prefix = ""
    enabled = true
    abort_incomplete_multipart_upload_days = 7
  }

  tags {
    Name = "${terraform.env}-tf-review-bucket"
    Env = "dev"
  }
}
