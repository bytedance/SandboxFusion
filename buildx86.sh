docker build -f ./scripts/Dockerfile.base.x86 -t code_sandbox:base .
docker build -f ./scripts/Dockerfile.server.us -t code_sandbox:server .