#!/usr/bin/env python

import argparse
import os
import tensorflow as tf


def parse_args(args=None):

    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=25)
    parser.add_argument("--dropout_rate", type=float, default=0.5)

    # data directories
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))

    # where to store model for export: SM_MODEL_DIR is always set by Sagemaker to /opt/ml/model
    parser.add_argument("--model_dir", type=str, default=os.environ.get("SM_MODEL_DIR"))

    return parser.parse_known_args(args=args)


def load_data(*args):
    raise NotImplementedError()


def get_model(filename):
    raise NotImplementedError()


def get_train_data(train_dir):
    return load_data(train_dir + "/training.ndjson")


def get_test_data(test_dir):
    return load_data(test_dir + "/validation.ndjson")


def train_model(args):
    model = get_model(args.dropout_rate, ...)

    train = get_train_data(args.train)
    val = get_test_data(args.test)

    model.fit(
        x=train,
        epochs=args.epochs,
        validation_data=val,
        verbose=2,  # print one log line per epoch -- important for parsing by sagemaker
    )

    tf.keras.models.save_model(model, args.model_dir)


if __name__ == "__main__":
    args, _ = parse_args()

    train_model(args)
