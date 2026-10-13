# CG VPS deployment plan

Status: PROPOSED, not executed. The VPS was inspected read-only on October 13, 2026. No app containers, ports, credentials, tenant accounts or production records were created for this fork.

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

The initial change in this fork is documentation only. It does not supply a validated deployment manifest or a production-ready servicing module. Resolve the gates in [implementation.md](implementation.md) before deploying real financial records.
