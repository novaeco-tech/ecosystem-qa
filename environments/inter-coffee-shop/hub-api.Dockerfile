# This is the artifact file that will be injected
ARG ARTIFACT_PATH

# 1. Start from your private, hardened base runtime
FROM ghcr.io/circular-engineering/runtime-api:latest

# 2. Copy the downloaded artifact into the image [10, 11]
COPY $ARTIFACT_PATH /app/artifact.tar.gz

# 3. Unpack the artifact and install its dependencies
RUN tar -xzf /app/artifact.tar.gz -C /app && \
    rm /app/artifact.tar.gz && \
    pip install -r /app/requirements.txt

# The base 'runtime-api' image's CMD will start the application