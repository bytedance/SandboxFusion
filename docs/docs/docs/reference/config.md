---
sidebar_position: 3
---

# Configuration File

The runtime configuration file is controlled by the environment variable SANDBOX_CONFIG. The corresponding file path is `sandbox/configs/{SANDBOX_CONFIG}.yaml`. By default, the configuration is set to `sandbox/configs/local.yaml`.

```yaml
online_judge:
  database:
    backend:
      type: mysql  # or none
      user: mysql_user
      password: mysql_password
      host: mysql_host
      port: mysql_port
    cache:  # optional cache, remove to disable
      path: memory  # sqlite database path, file address or memory
      sources:
      - type: mysql  # cache data source, mysql for online database, local for local folder
        tables:
        - name: table_name
          columns: [id, labels, content, test]
  # Maximum concurrency when requesting the sandbox
  max_runner_concurrency: 5
runner:
  isolation: none  # Isolation level when running code, none (no isolation), lite (overlayfs+cgroups+namespace, recommended for use within docker to avoid affecting the host machine) or foil (foil run --strict, no root needed)
  cleanup_process: false  # Kill all processes unrelated to the sandbox service after each request, use with caution locally
  restore_bash: true  # Check bash binary integrity and attempt to restore after each request
  max_concurrency: 0  # Maximum concurrency, 0 for no limit
common:
  logging_color: false  # Whether to include color in log output
```

Below are examples of configuration files for different scenarios.

local.yaml for local development:

```yaml
online_judge:
  database:
    backend:
      type: none  # Don't connect to online database
    cache:
      path: memory  # Location of local cache sqlite database, here it's in memory
      sources:
        - type: local  # Read jsonl files from local folder as cache
          path: sandbox/tests/datasets/samples
  max_runner_concurrency: 3
runner:
  isolation: none
  cleanup_process: false
  restore_bash: false
  max_concurrency: 34
common:
  logging_color: true
```

ci.yaml for integration testing environment:

The integration testing environment uses all local information

```yaml
online_judge:
  database:
    backend:
      type: none
    cache:
      path: memory
      sources:
        - type: local
          path: sandbox/tests/datasets/samples
  max_runner_concurrency: 3
runner:
  isolation: lite
  cleanup_process: false
  restore_bash: false
  max_concurrency: 0  # concurrency in ci is limited by pytest-xdist
common:
  logging_color: true
```
