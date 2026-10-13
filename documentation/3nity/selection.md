# Software selection

Reviewed October 13, 2026. The requirement is a small rental portfolio plus seller-finance notes, self-hosted on an existing Linux VPS, with agent access and owner-controlled notices.

## Recommendation

Use the last MIT-licensed MicroRealEstate revision as the rental development base. It already models properties, tenants, leases, rent payments, documents, organizations, and application credentials. Add a distinct loan-servicing module and a narrowly scoped MCP interface. This is the best fit among the evaluated options for a small portfolio that already uses QuickBooks and wants to own the code. It is not an off-the-shelf solution for both rentals and notes.

The decisive limitation is maintenance: this is an older fork, not the current supported upstream release. We own security fixes, dependency upgrades, U.S. templates, servicing logic, and release testing. If maintaining a servicing engine becomes the dominant cost, reassess Frappe Lending as the servicing backend before building more financial logic.

| Option | License / state observed | Rental fit | Note servicing | Decision |
| --- | --- | --- | --- | --- |
| MicroRealEstate current `main` | Sustainable Use License v2; source available, commercial use requires a separate license | Strong | Custom work | Excluded from the open source selection |
| MicroRealEstate MIT `master` | MIT; retained December 2025 revision | Properties, tenants, leases, rent tracking, receipts and documents | Custom module required | Selected development base, conditional on hardening |
| Frappe Lending + ERPNext | Lending GPLv3; loan management on Frappe/ERPNext | Rental extension still required | Existing repayment, schedules, interest and delinquency workflows | Stronger dedicated servicing alternative; heavier accounting setup and host footprint |
| PropMS + ERPNext | Property extension targets v15; `LICENSE` only says `License: GPL`, hooks declare MIT | Property and lease billing, operations | Would need version-compatible Lending integration | Not selected until license and joint version compatibility are resolved |
| Parcelis | AGPLv3; maintainers explicitly say not production ready | Broad planned/current rental workflows | Custom work | Too early for live payment operations |
| OpenKOS | Apache 2.0; MVP/v0.1 alpha, not production hardened | Functional rental lifecycle; Indonesian boarding-house origins | Custom work | Promising, but current maturity adds risk |
| Online Rental Property Manager | MIT; generated PHP/AppGini application | Property, lease and tenant records; CSV tools | Custom work, plus collection/payment workflow gaps | Less useful foundation for the requested collections system |

## Evidence

- [MicroRealEstate retained MIT source](https://github.com/microrealestate/microrealestate/tree/479d0ad703436071b64dfdf4e48321c121d8efb5)
- [MIT license at the selected commit](https://github.com/microrealestate/microrealestate/blob/479d0ad703436071b64dfdf4e48321c121d8efb5/LICENSE)
- [Current upstream license and explicit historical MIT cutoff](https://github.com/microrealestate/microrealestate/blob/main/LICENSE.md)
- [Frappe Lending](https://github.com/frappe/lending)
- [PropMS version-15-hotfix documentation](https://github.com/Aakvatech-Limited/PropMS/tree/version-15-hotfix)
- [Parcelis project status](https://github.com/parcelis/parcelis)
- [OpenKOS project status](https://github.com/senatroxx/OpenKos)
- [Online Rental Property Manager](https://github.com/bigprof-software/online-rental-property-manager)

## Source-level findings

The selected revision exposes landlord REST routes in `services/api/src/routes.js` for `/properties`, `/tenants`, `/leases`, `/rents`, `/dashboard`, and `/emails`. Machine-to-machine sign-in exists in `services/authenticator/src/routes/landlord.js`; it returns an organization ID and a short-lived access token. Organization scoping is checked in `services/common/src/utils/middlewares.ts`.

The API's common guard excludes the tenant role; it does not establish a genuinely read-only service principal across every write endpoint. An MCP tool list alone is insufficient to create read-only credentials. Add server-side scope enforcement before giving any agent credentials. Existing rent payment updates and email sends also need an audit and approval layer before agent use.

The organization schema supports a currency and locale; actual USD formatting, U.S. lease language, date handling, and notice templates still need functional validation. The package identifies itself as an alpha revision. No full application, load, vulnerability, or loan-servicing test has been completed in this selection phase.
