#!/bin/bash
#SBATCH --account=infra01
#SBATCH --nodes=1
#SBATCH --time=04:00:00

cd /iopsstor/scratch/cscs/rmachace/sandbox

# Build base (arch is taken from the host: aarch64 on the GH200 cluster)
podman build -f ./scripts/Dockerfile.base -t code_sandbox:base .
podman save -o code_sandbox_base.tar code_sandbox:base

# Build server on top of the locally-built base
podman build -f ./scripts/Dockerfile.server --build-arg BASE_IMAGE=code_sandbox:base -t code_sandbox:server .
podman save -o code_sandbox_server.tar code_sandbox:server