# Portfolio visuals and demos

The screenshots show actual project interfaces, not generated product mockups. The hero is AI-generated decorative artwork. No badges assert proficiency or completed certifications.

## DuckDuckGov

Source: [Hackathon-16-9 at 8704c48](https://github.com/DKAA04/Hackathon-16-9/tree/8704c48f1e27a6e6fa0ccd2f08bcdbba112350ea).

The portfolio variant uses the existing React interface with twelve invented records (`duck-fixture.json`). It replaces the registry snapshot, disables external enrichment, uses reserved `.invalid` email addresses and blocks network API requests with a Content Security Policy. Calls and email delivery remain unavailable. OpenStreetMap provides public map tiles. Corrections and drafts are local demo state. The displayed confidence values are the application's heuristics applied to synthetic data, not verified claims about real businesses.

`duck-portfolio.patch` records the source changes for this separate build. To reproduce: check out the source commit, apply the patch, install frontend dependencies and run `VITE_DATA_MODE=demo npm run build -- --base ./`. `package_demos.py` bundles the build into `duck.html`; only the synthetic build is published here.

## InvoiceAgent

Source: [Stripe_hackathon_Einvoicing at 77941e4](https://github.com/DKAA04/Stripe_hackathon_Einvoicing/tree/77941e4ce35ca710ff01d3c7a1701e00b8a2b164), with the subsequently published transport-security fix.

`invoice-fixtures.json` contains responses captured with FastAPI TestClient from the four built-in scenarios. Every example starts with an empty in-memory ledger. Gemini is not configured and real transmission is disabled. Sample bank, address, VAT and Peppol identifiers are replaced by explicit test placeholders. `invoice.html` preserves the original interface and reads those embedded responses; it does not call a backend. Selecting examples does not accumulate a live ledger. PDF uploads and arbitrary prompts require running the source locally. This replay is not a compliance certificate or accounting service.

## Activity graphics

`update_visuals.py` uses GitHub's public contribution grid and repository-language API. Language shares measure code bytes, including boilerplate; they do not measure skill or individual authorship. The profile repository and forks are excluded from the language chart. Contribution colors preserve GitHub's reported activity levels. The animated scan line is decorative and creates no contribution events. A weekly GitHub Actions job refreshes these two SVG files using only public data.

## Remaining boundaries

Code the Sky has no public inference demo because the authorized raw dataset and trained model are not included. Historical performance is labeled accordingly. Private/client projects remain outside the portfolio until their contents and redistribution rights are reviewed.
