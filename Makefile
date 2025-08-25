# ===== Configuration =====
S3_BUCKET = your-bucket
S3_PREFIX = xgboost
MODEL_NAME = xgb-local-model
MODEL_FILE = model/xgboost_model.ubj
TAR_FILE = model.tar.gz
ROLE_ARN = arn:aws:iam::<account-id>:role/<sagemaker-execution-role>
INSTANCE_TYPE = ml.m5.large
INSTANCE_COUNT = 1
FRAMEWORK_VERSION = 1.7-1

# ===== Default target =====
all: package upload deploy

# 1️⃣ Package model into tar.gz
package:
	@echo "Packaging model..."
	tar -czvf $(TAR_FILE) -C model xgboost_model.ubj
	@echo "Model packaged as $(TAR_FILE)"

# 2️⃣ Upload model to S3
upload:
	@echo "Uploading $(TAR_FILE) to s3://$(S3_BUCKET)/$(S3_PREFIX)/"
	aws s3 cp $(TAR_FILE) s3://$(S3_BUCKET)/$(S3_PREFIX)/

# 3️⃣ Deploy to SageMaker
deploy:
	@echo "Deploying model to SageMaker..."
	python deploy.py

# 4️⃣ Clean local tar.gz
clean:
	@echo "Cleaning up..."
	rm -f $(TAR_FILE)
