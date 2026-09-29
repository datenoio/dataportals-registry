# Review: CN entries with `software: custom` — pattern analysis

Date: 2026-09-28
Scope: all 322 entries under `data/entities/CN/` with `software.id: custom`.

Method: extracted all CN custom entries, fetched homepages (199 of 322 reachable;
many gov sites block non-browser/WAF-less requests), fingerprinted HTML for shared
asset paths, CMS signatures, vendor credits, and URL-shape families.

## 1. Overview

| catalog_type | custom entries |
|---|---|
| Open data portal | 147 |
| Scientific data repository | 129 |
| Indicators catalog | 20 |
| Machine learning catalog | 12 |
| Microdata catalog | 4 |
| Data marketplace | 4 |
| Geoportal | 4 |
| Data search engine | 2 |

By folder: Federal 180, CN-AH 14, CN-HB 14, CN-SC 13, CN-JX 12, CN-JS 12, CN-HN 9,
CN-GD 8, rest smaller.

China-specific software already defined (do not recreate):
`oportal` (Inspur, 41 deployments), `gxopendata` (Guangxi, 15), `jdop` (Zhejiang, 12),
`odweb` (Inspur /odweb/, 3), `supermapiportal`, `geovis`, `tianditu`, plus many CN
indicator terminals (wind, choice, ifind, eastmoneydata, csmar, ...).

## 2. Repeating patterns found

### 2.1 Verified shared-platform clusters (fingerprint evidence)

**A. Hunan municipal data-open product — "CreatorCMS/KCUI" family (3 entries)**
- `www.yiyang.gov.cn/webapp/yiyang2019/dataPublic/index.jsp`
- `www.czs.gov.cn/webapp/czs/dataPublic/index.jsp` (Chenzhou)
- `www.yueyang.gov.cn/webapp/yydsj/index.jsp`
- Evidence: shared URL shape `/webapp/{city}/(dataPublic|index).jsp`; Yiyang page
  (GBK) loads `KCUI/KCUI3.min.js`, `/creatorCMS/statisticManage/count.page`,
  `dataDetail.jsp?id=`. KCUI + creatorCMS point to a single vendor product
  (Hunan-based gov-IT vendor, likely 科创信息/Creator). Other two blocked by WAF
  (503/NWAF) during probe — same URL shape.

**B. Anhui open-data-web family (3+ entries)**
- `www.bozhou.gov.cn/open-data-web/index/index.do`
- `www.hefei.gov.cn/open-data-web/index/index-hfs.do`
- `data.ahzwfw.gov.cn:8000/dataopen-web/index.html` (provincial platform)
- Related: `sjzyj.huainan.gov.cn/odssite/index`
- Evidence: shared `open-data-web`/`dataopen-web` Struts-style (`.do`) URL paths.
  Live pages sit behind the same WAF (identical 7,386-byte NWAF block page on Hefei
  and the provincial host), so vendor name unconfirmed.

**C. `/extranet/openportal/` product (2 entries, cross-province)**
- `data.yichun.gov.cn/extranet/openportal/pages/default/index.html` (Jiangxi)
- `kf.zjkzwfw.gov.cn/extranet/openportal/pages/default/index.html` (Zhangjiakou, Hebei)
- Distinctive identical path across two provinces → one vendor product.

**D. `/col/colNN/index.html` government-website CMS (4 entries)**
- `www.yingtan.gov.cn/col/col26/index.html`, `www.als.gov.cn/col/col130/index.html`,
  `www.hengshui.gov.cn/col/col51/index.html`, `www.hg.gov.cn/col/col7161/index.html`
- These are data-open columns inside general government portals, all on a CMS using
  the `/col/col{N}/` URL scheme (widespread Chinese gov-site CMS; vendor not yet
  confirmed — candidates include Hanweb/大汉). All four blocked direct probing.

**E. Changzhou `/statics/open/v2` family (2 entries)**
- `opendata.changzhou.gov.cn` + `www.cztn.gov.cn/opendata` (Tianning district) serve
  the identical 2,399-byte SPA shell with `/statics/open/v2` assets. Regional vendor,
  thin (city + own district).

**F. CAS Kunming institutes ASP.NET data-center app (2 entries)**
- `data.iflora.cn` and `datacenter.kiz.ac.cn` share the MVC route scheme
  `/Home/DataContent`, `/Home/...`; both are CAS Kunming institute science data
  centers. Other CAS institute centers (niglas, issas, iphy, igadc, qdio) each use
  different stacks — no CAS-wide platform evident.

### 2.2 Administrative/program clusters (NOT shared software)

- **National Science Data Centers (国家科学数据中心)** — ~20 of the 129 scientific
  entries: tpdc.ac.cn, data.earthquake.cn, mds.nmdis.org.cn, ncdc.ac.cn,
  nesdc.org.cn, forestdata.cn, noda.ac.cn, nssdc.ac.cn, nmdc.ac.cn, nhepsdc.cn,
  gscloud.cn, geodata.cn, phsciencedata.cn, corrdata.org.cn, chinare.org.cn ...
  One national *program*, many bespoke builds. Recommend a tag, not a software def.
- **CNIC-built platforms** — 中国科学院计算机网络信息中心 footer credit on 5 sites
  (scidb.cn, gscloud.cn, nesdc.org.cn, nadc.china-vo.org, opendatachain.cn). Same
  builder, distinct products. Only `scidb.cn` is a named, reusable product (see 3.1).
- **National laboratory-animal resource banks** (4): nhp.kiz.ac.cn, pla.caas.cn,
  nclarc.org.cn, nrla.nifdc.org.cn — one program family, unverified shared stack.
- **`genomics.org.cn` legacy BGI databases** (4): rise, yh, pig, chicken — same org
  and era, defunct-ish; low value as a software definition.
- **Per-lab bioinformatics database sites**: idrblab.org (DrugMAP, TTD),
  zhounan.org (eccDNAdb, FerrDb), pkumdl.cn — bespoke per lab; no definition.

### 2.3 Structural observation (data quality)

- 33 of 147 custom open-data entries are **data-open columns on general government
  websites** (`/sjkf`, `/ztzl/sjkf`, `/xxgk/sjkf`, `/content/column/...`), not
  dedicated portal software. They run on heterogeneous gov-site CMSs. The
  `governmentsitebuilder` definition covers only the German GSB, so these currently
  have no fitting software value — keep `custom`, or identify CMSs case by case.
- Single-instance ML platforms (ModelScope, OpenXLab/OpenDataLab, Tianchi, AI
  Studio, WiseModel, HeyWhale, OpenI, BAAI, DataFountain, Datatang) are each named
  vendor platforms — same situation as indicator terminals (wind/ifind/choice) that
  already have definitions.

## 3. Candidate new software definitions

Ranked by confidence × value. Registry precedent allows small/named products
(`odweb` = 3 deployments; `kaggle`/`pangaea` = single-instance named platforms).

### 3.1 Recommended

| id (proposal) | name | evidence | entries |
|---|---|---|---|
| `sciencedb` | ScienceDB (Science Data Bank) | named CNIC/CSTCloud generalist repository product, DOI minting, journal integrations | 1 (scidb.cn) |
| `creatorcms` | CreatorCMS data-open module (KCUI) | KCUI assets + `/creatorCMS/` + `/webapp/{city}/dataPublic/*.jsp` | 3 (Yiyang, Chenzhou, Yueyang) |
| `ahopendataweb` | Anhui open-data-web platform | shared `/open-data-web/*.do`, `/dataopen-web/` paths incl. provincial host | 3–4 (Bozhou, Hefei, Anhui provincial, +Huainan?) |
| `openportal` | openportal gov data platform | identical `/extranet/openportal/pages/` path across two provinces | 2 (Yichun JX, Zhangjiakou HE) |

### 3.2 Worth defining as named platforms (single-instance, low urgency)

`modelscope` (Alibaba), `opendatalab` (Shanghai AI Lab, also powers OpenXLab),
`tianchi` (Alibaba), `aistudio` (Baidu Paddle), `ngdc-cncb` stack (ngdc.cncb.ac.cn
incl. GSA — 3 entries but one org). Consistent with existing indicator-terminal and
`kaggle`-style definitions.

### 3.3 Hold — needs vendor identification first

- `/col/colNN/` gov CMS (4 entries) — identify vendor (probe via FOFA icon/hash or
  browser session; curl is WAF-blocked).
- Gansu `data.zwfw.*` family (Lanzhou, Longnan) — only 2, blocked by WAF.
- `genomics.org.cn` legacy family — historical, low value.

## 4. Suggested next steps

1. Create the 3.1 definitions (start with `sciencedb` + `creatorcms`), re-point the
   affected entries, then `sync-software-maps`, `validate-software`, `validate-yaml`.
2. For 3.3, use FOFA/Censys favicon-hash or body-hash fingerprints (`hunt.py search`
   workflow) to identify the CMS vendor and find further deployments.
3. Consider a registry tag for "National Science Data Center" program membership
   instead of a software definition.
