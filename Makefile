# Makefile for creating an AWS Lambda execution role

ROLE_NAME := lambda-ex
POLICY_DOC := file://trust-policy.json

.PHONY: all create-role clean

all: create-role

# Create trust policy document
trust-policy.json:
	@echo 'Creating trust policy document...'
	@echo '{"Version": "2012-10-17",' > trust-policy.json
	@echo '  "Statement": [{' >> trust-policy.json
	@echo '    "Effect": "Allow",' >> trust-policy.json
	@echo '    "Principal": {"Service": "lambda.amazonaws.com"},' >> trust-policy.json
	@echo '    "Action": "sts:AssumeRole"' >> trust-policy.json
	@echo '  }]' >> trust-policy.json
	@echo '}' >> trust-policy.json

# Create IAM role for Lambda
create-role: trust-policy.json
	@echo 'Creating IAM role "$(ROLE_NAME)"...'
	aws iam create-role \
	  --role-name $(ROLE_NAME) \
	  --assume-role-policy-document $(POLICY_DOC)
	@echo 'Role "$(ROLE_NAME)" created successfully.'

# Remove temporary files
clean:
	@rm -f trust-policy.json
	@echo 'Cleaned up generated files.'
