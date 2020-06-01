import os
from sagemaker.estimator import Estimator
import sagemaker

# TODO: change bucket name
sess = sagemaker.Session(default_bucket="MY_BUCKET")
role = os.environ["SAGEMAKER_ROLE"]
tag = os.environ.get("CIRCLE_BRANCH") or "latest"
account_url = os.environ["AWS_ECR_ACCOUNT_URL"]

tf_estimator = Estimator(
    role=role,
    train_instance_count=1,
    train_instance_type="ml.m5.large",
    sagemaker_session=sess,
    output_path="s3://MY_BUCKET/sagemaker/model",
    image_name=f"{account_url}/REPO_NAME:{tag}",
    hyperparameters={"epochs": 200, "batch_size": 25, "dropout_rate": 0.5}
)

# creates ENV variables based on keys -- SM_CHANNEL_XXX
tf_estimator.fit(
    inputs={
        "train": "s3://MY_BUCKET/sagemaker/train",
        "test": "s3://MY_BUCKET/sagemaker/validation",
    },
    wait=False  # for CI deployment
)
