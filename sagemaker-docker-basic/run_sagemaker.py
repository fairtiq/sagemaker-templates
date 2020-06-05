import os
from sagemaker.estimator import Estimator
import sagemaker

# TODO: change me
BUCKET_NAME = "MY_BUCKET"
REPO_NAME = "REPO_NAME"


sess = sagemaker.Session(default_bucket=BUCKET_NAME)
role = os.environ["SAGEMAKER_ROLE"]
tag = os.environ.get("CIRCLE_BRANCH") or "latest"
account_url = os.environ["AWS_ECR_ACCOUNT_URL"]

tf_estimator = Estimator(
    role=role,
    train_instance_count=1,
    train_instance_type="ml.m5.large",
    base_job_name=tag,
    sagemaker_session=sess,
    output_path=f"s3://{BUCKET_NAME}/sagemaker/{REPO_NAME}",
    image_name=f"{account_url}/{REPO_NAME}:{tag}",
    hyperparameters={"epochs": 200, "batch_size": 25, "dropout_rate": 0.5}
)

# creates ENV variables based on keys -- SM_CHANNEL_XXX
tf_estimator.fit(
    inputs={
        "train": f"s3://{BUCKET_NAME}/sagemaker/train",
        "test": f"s3://{BUCKET_NAME}/sagemaker/validation",
    },
    wait=False  # for CI deployment
)
