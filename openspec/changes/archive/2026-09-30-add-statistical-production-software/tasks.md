## 1. Schema and validation

- [x] Add non-catalog category and directory mapping without changing existing category semantics.
- [x] Add tests for schema-valid production definitions and invalid catalog masquerading.
- [x] Update software map sync and validation to include the new group.

## 2. Verified definitions

- [x] Add CSPro using the U.S. Census Bureau product documentation.
- [x] Add DataSHIELD using project documentation; describe it as controlled federated analysis, not download access.
- [x] Validate license claims against each product's primary license source.

## 3. Documentation and downstream

- [x] Exempt only non-catalog production products from catalog discovery/harvest recipe headings; provide a product-information index entry instead.
- [x] Regenerate and validate software maps, index, and software exports.
- [x] Add downstream `statskb` cards and update coverage audit.
- [x] Run focused tests, software validation/export, and an isolated full registry build. The complete test suite was also run: 652 passed; remaining failures concern pre-existing `llms.txt` copies, quality baseline, and 24 unrelated unmapped software IDs in this dirty worktree. The two new IDs are explicitly classified as having no public catalog probe.

Software-only export was refreshed against the current YAML tree on 27 September 2026: 700 definitions and 700 JSONL records, with no missing, extra, or content-drifted IDs. This did not rebuild the unrelated catalog datasets.
