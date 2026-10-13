# 3nity Ventures development fork

This folder defines the rental-management and seller-finance servicing extension to MicroRealEstate. It is a development plan, not evidence of an installed application, implemented MCP server, or live loan servicing. No tenant, borrower, bank, contract, or payment data belongs in this public repository.

## Current state

- Base: MicroRealEstate `master`, commit `479d0ad703436071b64dfdf4e48321c121d8efb5`, December 9, 2025.
- License: MIT at that exact commit; the original `LICENSE` is retained.
- Fork default branch: `main`, reset to this same MIT commit.
- Newer upstream `main` uses the Sustainable Use License and must not be merged into this fork without a separate licensing decision.
- GitHub Actions are disabled until inherited workflows have been reviewed.
- This initial change adds documentation and development guardrails only. No runtime code changes.

## Documents

- [Selection and tradeoffs](selection.md)
- [MCP, servicing, and collection workflows](architecture.md)
- [Implementation sequence and acceptance criteria](implementation.md)
- [VPS deployment plan](deployment.md)

## Ownership of records

3nity is a separate legal and operating context. Sharing a host with CG does not grant CG agents access to 3nity. Use a dedicated database, network, service credentials, backups, and restricted document store. The source documents live in a separate Google account; connection and migration are deferred at the owner's request. Historical copies in another company's Drive must not seed production.

QuickBooks remains the accounting source during migration. Verify the connected company's identity and reconcile posted payments before deriving delinquency. Open invoices alone do not establish an unpaid obligation. Choose one system to issue each recurring charge before enabling billing, so the new app does not duplicate QuickBooks invoices.

## Development starting point

The repository contains the upstream code and developer instructions at the pinned MIT revision. Its Dockerfiles and dependencies require security and compatibility review before production. Build from this source, rather than using upstream `latest` container images. See [deployment.md](deployment.md) before running any installer or Compose stack on a shared host.
