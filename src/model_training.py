import sagemaker
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
import boto3
# Session & bucket
session = sagemaker.Session()
iam=boto3.client("iam")
role = iam.get_role(RoleName="sagemaker")["Role"]["Arn"]  # or replace with your IAM role ARN

bucket = "salesforce-models"  # replace with your bucket name
prefix = "xgboost-50features-5classes"

# Upload training data (CSV without headers, first column = label 0–4)
train_path = session.upload_data("../data/train.csv", bucket=bucket, key_prefix=prefix + "/train")
validation_path = session.upload_data("../data/validation.csv", bucket=bucket, key_prefix=prefix + "/validation")

# XGBoost image
container = sagemaker.image_uris.retrieve("xgboost", session.boto_region_name, version="1.7-1")

# Estimator
xgb = Estimator(
    image_uri=container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    volume_size=5,
    output_path=f"s3://{bucket}/{prefix}/models/",
    sagemaker_session=session,
)

# Hyperparameters for multi-class
xgb.set_hyperparameters(
    objective="multi:softmax",  # probability output for multi-class
    num_class=5,                 # 5 classes
    num_round=20,               # boosting rounds
    max_depth=6,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.8,
    verbosity=1,
    eval_metric="mlogloss"
)

# Data channels
train_input = TrainingInput(train_path, content_type="text/csv")
validation_input = TrainingInput(validation_path, content_type="text/csv")

# Launch training
xgb.fit({"train": train_input, "validation": validation_input})
# s3_client = boto3.client("s3")
print(xgb.model_data)

