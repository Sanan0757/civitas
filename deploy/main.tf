provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "nova_etm" {
  function_name = "my_container_lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/my-lambda-container:latest"
  timeout       = 10
  memory_size   = 256
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
