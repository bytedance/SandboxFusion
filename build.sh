#!/bin/bash
#SBATCH --account=infra01
#SBATCH --nodes=1
#SBATCH --time=04:00:00

cd /iopsstor/scratch/cscs/rmachace/sandbox

# Build base
podman build -f ./scripts/Dockerfile.base.us -t code_sandbox:base .
podman save -o code_sandbox_base.tar code_sandbox:base

# Build server
podman build -f ./scripts/Dockerfile.server.us -t code_sandbox:server .
podman save -o code_sandbox_server.tar code_sandbox:server