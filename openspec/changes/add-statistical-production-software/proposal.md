# Change: Register statistical production software separately from catalog platforms

## Why

The software registry currently classifies every product using a catalog category. CSPro (census and survey processing) and DataSHIELD (controlled analysis of sensitive data) are relevant to statistical knowledge bases but are not microdata catalogs. Misclassifying them as such would make the registry misleading.

## What Changes

- Add a `Statistical production software` category for non-catalog collection, processing, and protected-analysis products.
- Keep existing catalog categories and records unchanged.
- Permit production-software definitions without catalog discovery/harvest recipes when the product has no public catalog to discover; require a product documentation link instead.
- Add verified CSPro and DataSHIELD definitions after the schema and documentation rule are approved.
- Let downstream knowledge bases reference the new category and distinguish primary product function from data-publication components.

## Impact

- Affected specs: new `statistical-production-software`; modified `documentation-site`.
- Affected code/data: `data/schemes/software.json`, software validation and map sync, `data/software/statistical/`, documentation coverage guard, generated software exports, downstream `statskb` registry-group allowlist and software cards.
- No change to catalog records or public catalog APIs is proposed.
