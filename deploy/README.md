# Private staging deployment

One Compose project operates the application, local MongoDB, Redis and persistent document volumes. It contains several containers. This is internal staging, not approved live servicing. Source starts at the retained MIT baseline; application images are built locally from the feature branch.

```sh
python3 deploy/init-env.py
docker compose --parallel 1 --env-file deploy/.env -f deploy/compose.yaml build api landlord tenant
docker compose --env-file deploy/.env -f deploy/compose.yaml up -d --no-build
python3 deploy/bootstrap.py
docker compose --env-file deploy/.env -f deploy/compose.yaml --profile mcp build mcp
```

Secrets are generated on the host, never committed. Bootstrap refuses to overwrite an existing organization or credential file. Public signup and external sending are disabled. No SMTP credentials are provided. Operator credentials live in `../operator-credentials.json` outside the Git checkout with mode 0600; read them locally through SSH. Rotate the initial operator password in the app before active use.

The gateway binds only to `127.0.0.1:8088`. Open a local tunnel:

```sh
ssh -N -L 8088:127.0.0.1:8088 cg-hermes
```

Then visit `http://localhost:8088/landlord`. Use the verified CG host; SSH alias names alone do not prove company identity. There is no public website or database port.

For private MCP stdio access, launch through SSH with an agent/client that supports a subprocess transport:

```sh
ssh cg-hermes 'cd /opt/3nity/property-manager && docker compose --env-file deploy/.env -f deploy/compose.yaml --profile mcp run --rm --no-deps -T mcp'
```

Current MCP tools are read-only. The API's machine-reader role rejects writes, configuration, email and document routes before controller execution. Tool output is bounded and the configured organization is verified at sign-in. MCP writes, draft/approval workflows and loan servicing are future work; this transport has not been wired into the existing fleet automatically.

Stop/start with `docker compose ... stop` / `start`. Never use `down -v` on data you intend to retain. Named volumes preserve MongoDB, Redis, templates, uploads and generated documents across container recreation. Keep backups separately and prove restore before importing real records.

Node 22 replaces the obsolete Node 20 runtime in this deployment. Next.js is patched to 14.2.35, with selected backend dependency patches. This is not a completed dependency/security audit; broader framework and legacy dependency maintenance remains a production gate.
