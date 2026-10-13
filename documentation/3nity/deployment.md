# CG VPS deployment plan

Status: private staging deployed October 13, 2026, after Oscar authorized implementation and VPS installation. See [runtime-status.md](runtime-status.md) and [deploy/README.md](../../deploy/README.md). Earlier host findings below were the preparation snapshot. No real portfolio records have been imported.

## Owner's deployment preference

October 13 clarification: this application is for internal management of the owner's properties. All application data must be stored locally on the VPS, and the owner prefers a simple Docker container installation. No managed/cloud database is required by the selected baseline.

MicroRealEstate currently uses local MongoDB and Redis plus multiple application services. Its stock Compose manifest is a multi-container stack, not an all-in-one image. A single Compose project provides one install/start/stop interface while preserving separate service lifecycles. A literal one-container package would require a custom image, process supervision, localhost service configuration, graceful database shutdown, health checks and backup/restore validation. That packaging is not implemented in this fork. Do not describe a Compose stack as one container or substitute it silently for the stated preference.

Required persistence: keep MongoDB files, relevant Redis state, documents and backups in persistent volumes or protected host directories outside the container's writable layer. Recreating or updating a container must preserve records. Revisit the software choice if achieving a tested single-container package adds more maintenance than the rental foundation saves.

## Host findings

The verified CG host is `srv1985448`. At inspection it had approximately 7.9 GiB reported RAM, 2.7 GiB available, no swap and approximately 64 GiB disk free. Existing services include Hermes agents, Paperclip, Traefik and a webhook receiver. Resource availability is transient; repeat the check before deployment. No application footprint or load test has been performed.

The local SSH alias `cg-hermes` reached the verified CG host. Another alias named `cg-vps` currently points to a different server. Never infer company identity from an alias; check host identity and existing workloads before any mutation. Older brain records using `cg-vps` are not sufficient deployment evidence.

## Deployment shape

- A dedicated Compose project, private Docker network, database and persistent volumes rooted at `/opt/3nity/property-manager`; restrict permissions to authorized administrators.
- Initially access through an authenticated SSH tunnel to a loopback-only gateway port. Use the existing reverse proxy only after choosing an authorized domain and verifying TLS/access controls. Do not start the upstream Caddy proxy on ports already owned by the host.
- Build application images from the fork's reviewed MIT source and tag with the exact commit. Verify every deployed service image derives from that source. Do not use upstream app `latest` images, which may contain restricted-license code.
- MongoDB and Redis remain internal and unpublished. Generate secrets outside Git. Use a dedicated document store and backup key, separate from CG records and agent mounts.
- Mail sending disabled and no external SMTP credentials in staging. Provision only authorized operator accounts, then disable public registration. Tenant portal activation is a separate step after records and access have been verified.
- Cap resource use and build concurrency; monitor CG service latency and memory. The current free-memory snapshot does not establish that the full stack can coexist reliably. If the staging footprint crowds existing workloads, obtain approval for more capacity before production.

## Release and rollback

1. Record host identity, baseline health/resource use, image digests and application version.
2. Back up persistent data and verify a restore into a separate isolated instance.
3. Run the synthetic rental and MCP acceptance suite and servicing fixtures.
4. Deploy a reviewed release with outbound communication still disabled.
5. Check landlord UI, service health, private network bindings, account access, ledger integrity and existing CG services.
6. Retain the prior images and restore point. Roll back app code together with compatible schema/data state; do not assume downgrading an image reverses a database migration.

The deployment manifest is implemented and tested for staging. It does not supply a production-ready servicing module. Resolve the remaining gates in [implementation.md](implementation.md) before importing real financial records or enabling collection workflows.
