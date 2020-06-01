#!/usr/bin/env python

import os
import json
import sys
import traceback


# TODO: change me
from MY_ML_PACKAGE.train import train_model, parse_args

# These are the paths to where SageMaker mounts interesting things in your container.
prefix = "/opt/ml/"
output_path = os.path.join(prefix, "output")
param_path = os.path.join(prefix, "input/config/hyperparameters.json")


def _hyperparameters_to_cmd_args(hyperparameters):
    """
    Converts our hyperparameters, in json format, into key-value pair suitable for passing to our training
    algorithm.
    """
    cmd_args_list = []

    for key, value in hyperparameters.items():
        cmd_args_list.append("--{}".format(key))
        cmd_args_list.append(value)

    return cmd_args_list


if __name__ == "__main__":
    try:
        # Amazon SageMaker makes our specified hyperparameters available within the
        # /opt/ml/input/config/hyperparameters.json.
        # https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html#your-algorithms-training-algo-running-container
        with open(param_path, "r") as tc:
            training_params = json.load(tc)

        cmd_args = _hyperparameters_to_cmd_args(training_params)

        train_model(parse_args(cmd_args)[0])
        print("Training complete.")

        # A zero exit code causes the job to be marked a Succeeded.
        sys.exit(0)
    except Exception as e:
        # Write out an error file. This will be returned as the failureReason in the
        # DescribeTrainingJob result.
        trc = traceback.format_exc()
        with open(os.path.join(output_path, "failure"), "w") as s:
            s.write("Exception during training: " + str(e) + "\n" + trc)
        # Printing this causes the exception to be in the training job logs, as well.
        print("Exception during training: " + str(e) + "\n" + trc, file=sys.stderr)
        # A non-zero exit code causes the training job to be marked as Failed.
        sys.exit(255)
