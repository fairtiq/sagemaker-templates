import os
from sagemaker.estimator import Estimator
import sagemaker


from sagemaker.debugger import (
    TensorBoardOutputConfig,
    DebuggerHookConfig,
    CollectionConfig,
)

# TODO: change me
BUCKET_NAME = "MY_BUCKET"
REPO_NAME = "REPO_NAME"

s3_output_location = f"s3://{BUCKET_NAME}/sagemaker/{REPO_NAME}"

tensorboard_output_config = TensorBoardOutputConfig(
    s3_output_path=f"{s3_output_location}/tensorboard",
    container_local_output_path="/opt/ml/output/tensorboard",
)

hook_config = DebuggerHookConfig(
    s3_output_path=s3_output_location,
    collection_configs=[CollectionConfig("weights"),
                        CollectionConfig("gradients"),
                        CollectionConfig("biases")],
)

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
    output_path=s3_output_location,
    image_name=f"{account_url}/{REPO_NAME}:{tag}",
    hyperparameters={"epochs": 200, "batch_size": 25, "dropout_rate": 0.3},
    metric_definitions=[
        {"Name": "train:loss", "Regex": "loss: (.*?) "},
        {"Name": "val:loss", "Regex": "val_loss: (.*?) "},
    ],
    tensorboard_output_config=tensorboard_output_config,
    debugger_hook_config=hook_config,
    train_use_spot_instances=True, # save $$ on AWS
    train_max_wait=3600,  # 1 hour
    train_max_run=3600,
)

# will create ENV variables based on keys -- SM_CHANNEL_XXX
tf_estimator.fit(
    inputs={
        "train": f"s3://{BUCKET_NAME}/sagemaker/train",
        "test": f"s3://{BUCKET_NAME}/sagemaker/validation",
    },
    wait=False,
)
