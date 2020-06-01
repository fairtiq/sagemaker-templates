FROM tensorflow/tensorflow:2.2.0-gpu

RUN pip install sagemaker-containers

RUN apt-get update && apt-get install -y MY_EXTRA_LIBS

# /opt/ml and all subdirectories are used by SageMaker,
# we use the /opt/ml/code subdirectory to store our ML package code.

# copy the private dependencies that we downloaded with git clone to the container
COPY ./tmp/my-private-package /tmp/my-private-package
# I keep a separate sagemaker sub-package to separate the requirements file
COPY ./sagemaker/requirements.txt /tmp/requirements.txt

# install private and public dependencies
RUN pip install /tmp/my-private-package -r /tmp/requirements.txt

#` -- /opt/ml/code
#    `-- your-ml-package
#    |-- entrypoint_train.py

COPY ./MY_ML_PACKAGE /opt/ml/code/your-ml-package
# copy the entrypoint file to the code directory
COPY ./sagemaker/entrypoint_train.py /opt/ml/code/entrypoint_train.py
WORKDIR /opt/ml/code

# add working directory to PYTHONPATH to make imports from your ML package
ENV PYTHONPATH="/opt/ml/code:${PYTHONPATH}"

# argument to sagemaker what we want to run
ENV SAGEMAKER_PROGRAM entrypoint_train.py