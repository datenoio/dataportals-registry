# Каталоги данных Казахстана

Обзор инфраструктуры каталогов данных Республики Казахстан по реестру [dataportals-registry](https://github.com/datenoio/dataportals-registry) (снимок рабочих экспортов на 8 сентября 2026, таблица `catalogs` в DuckDB). Это **каталоги** (порталы, геопорталы, репозитории, витрины индикаторов), а не перечень датасетов внутри них.

## 1. Как читать этот блок

Оценки ниже сделаны **на уровне каталога**, по полям реестра (`software`, `endpoints`, `access_mode`, `api`, `rights`, `status`, описание) и по известным свойствам платформ. Внутри одного портала наборы могут отличаться по лицензии и качеству.

| Вопрос | Что считалось «да» | Ограничение |
|--------|---------------------|-------------|
| Агрегация в единый поиск | Машиночитаемый каталог/API: OAI-PMH, CSW, DCAT, REST-каталог, ArcGIS REST directory, Geonomics catalog, IPT, DSpace, OpenSDG, TAP, WFS | Наличие endpoint в реестре ≠ SLA. Viewer-only порталы в индекс попадают только карточкой источника |
| Коммерческое использование | Явная открытая лицензия, разрешающая коммерцию (CC-BY, CC0, ODbL и т.п.) | **Ни у одного** казахстанского каталога в реестре не заполнены `license_id` / `license_name`. Оценка поэтому везде «условная», кроме явно платных и режимных |
| Обучение ИИ | Bulk/API выгрузка структурированных или исследовательских данных + правовой режим, не запрещающий ML | Нет каталога с лицензией «AI training allowed». Кадастр и персональные данные исключаются |

Шкала агрегации: **высокий** — стандартный harvest; **средний** — кастомный API или только OGC-слои; **ограниченный / низкий** — витрина; **нет** — мёртвый или закрытый контур.

**Права.** `rights_type=unknown` или пусто у большинства записей. `global` у части ArcGIS означает публичную видимость сервиса, не SPDX-лицензию. `granular` — лицензия на уровне объекта (Nazarbayev University). `inapplicable` — к картографическому сервису лицензия каталога не применялась.

В выборку входят **118** записей с владельцем в Казахстане и **2** внешних каталога, покрывающих территорию РК. Из 118 в YAML `data/entities/KZ/` сейчас **112**; шесть `scheduled`-записей есть в экспорте, но ещё не лежат в `data/entities/KZ/` (`kazakhstantravel`, `mapiulytaukz`, `portalgiprozemkz`, `testgidrogharyshkz`, `tourismonlinekz`, `wwwvisitaqmolakz`).

## 2. Сводка

| Показатель | Значение |
|-----------|----------|
| Всего каталогов с владельцем в РК | 118 |
| Действующие (`active`) | 86 |
| На проверке (`scheduled`) | 29 |
| Неактивные | 2 |
| Устаревший дубль | 1 |
| С `access_mode: open` | 117 |
| С `access_mode: restricted` | 1 (Национальный картографо-геодезический фонд) |
| С заполненной лицензией (`license_id`) | **0** |
| С зарегистрированными endpoints | 55 |
| Официальные национальные каталоги типа (`is_national: true`) | 7 |
| Внешние каталоги с покрытием KZ | 2 |

### 2.1. Чего нет

В реестре **нет** казахстанских записей типов: микроданные (NSO microdata), каталог ML-моделей, маркетплейс, метаданные/MDR, поисковая система данных, API-каталог как отдельный тип. Научный ML-контур фактически представлен страницей датасетов ISSAI, а не отдельным `Machine learning catalog`.

Порталов открытых данных всего три, из них живых два: национальный `data.egov.kz` и городской Smart Almaty. Остальной ландшафт — геопорталы и статистические витрины.

## 3. Разбивка по типам каталогов

| Тип | Всего | Действующие | На проверке | Неактивные / дубли |
|-----|------:|------------:|------------:|-------------------:|
| геопортал (Geoportal) | 92 | 61 | 29 | 2 |
| каталог индикаторов (Indicators catalog) | 15 | 15 | 0 | 0 |
| научный репозиторий данных (Scientific data repository) | 8 | 8 | 0 | 0 |
| портал открытых данных (Open data portal) | 3 | 2 | 0 | 1 |

**Геопорталы (92, из них 61 действующий)** — доминирующий тип. Три технологических семьи региональных карт:

1. **Geonomics** (Alau Solutions) — областные/городские геопорталы акиматов с catalog API (`geonomics:catalog`), часто Mapbox + опциональный GeoServer. Это основной «региональный каталог слоёв».
2. **SmartMap** — 20 тенантов `{район}.smartmap.kz`, почти все в ЗКО: инвестиционные карты участков без API.
3. **RGIS / VKOMAP / KAZGISA** — региональные ГИС акиматов; у части узлов GeoServer уже 404, остался Leaflet-просмотр.

Национальный геоконтур: НИПД `map.gov.kz` (GeoNode), публичная кадастровая карта ЕГКН, АИС ГЗК, Госградкадастр, линейка Gharysh Sapary (много `scheduled` WebGIS), отраслевые ArcGIS REST (Ғарыш Сапары, GIS Center, SkyGIS, KPO, Terra Exploration, E-Geoprom).

**Каталоги индикаторов (15, все действующие)** — Бюро национальной статистики (сайт, Taldau, SDG, NSDP, гендер, дети), Нацбанк, Минфин (бюджеты), Казгидромет (климат/гидро), Qamqor, KOREM, SEDA, Enbek, AtlasSD КазНУ.

**Научные репозитории (8)** — кластер Nazarbayev University (DSpace данные, DSpace публикации, Pure, ISSAI), IPT биоразнообразия (Buketov, Wings), архив FAI (DaCHS/TAP), сейсмологический KNDC.

**Порталы открытых данных (3)** — см. выше; QIoT неактивен.

## 4. Региональные каталоги

Покрытие ISO 3166-2 (только записи с `coverage.location.subregion`). Национальные каталоги без субрегиона сюда не входят.

| Код | Регион | Каталогов (все статусы) | Действующих | Что есть |
|-----|--------|-------------------------:|------------:|----------|
| `KZ-10` | Абайская область | 1 | 1 | Геопортал Абай (VKOMAP) |
| `KZ-11` | Акмолинская область | 2 | 1 | Карта области (custom); VisitAqmola — scheduled |
| `KZ-15` | Актюбинская область | 2 | 2 | РГИС Актобе; SmartMap района Темир |
| `KZ-19` | Алматинская область | 1 | 1 | Geonomics `map.almobl.kz` |
| `KZ-23` | Атырауская область | 1 | 1 | Геопортал Атырау (KAZGISA OpenLayers, GeoServer 404) |
| `KZ-27` | Западно-Казахстанская область | 19 | 18 | Geonomics области + ArcGIS Уральска + 15 SmartMap (районы, жильё, природа); 1 inactive |
| `KZ-31` | Жамбылская область | 1 | 1 | РГИС e-jambyl.kz (карта, GeoServer 404) |
| `KZ-33` | область Жетісу | 1 | 1 | Geonomics `map.e-zhetisu.kz` |
| `KZ-35` | Карагандинская область | 3 | 3 | Geonomics области; VKOMAP Темиртау; SmartMap района Бокейхан |
| `KZ-39` | Костанайская область | 1 | 1 | Geonomics `map.ikostanay.kz` |
| `KZ-43` | Кызылординская область | 2 | 2 | Geonomics области; SmartMap «Kyzylorda District» |
| `KZ-47` | Мангистауская область | 1 | 1 | Geonomics `map.e-mangistau.kz` |
| `KZ-55` | Павлодарская область | 1 | 1 | РГИС Павлодар (живой GeoServer/OGC) |
| `KZ-59` | Северо-Казахстанская область | 1 | 1 | РГИС e-sqo.kz (карта, GeoServer 404) |
| `KZ-61` | Туркестанская область | 1 | 1 | Geonomics `map.iturkistan.kz` |
| `KZ-62` | Улытауская область | 1 | 0 | Geonomics `map.iulytau.kz` — только scheduled |
| `KZ-63` | Восточно-Казахстанская область | 1 | 1 | Геопортал ВКО (VKOMAP) |
| `KZ-71` | город Астана | 1 | 1 | ArcGIS `gis.esaulet.kz` |
| `KZ-75` | город Алматы | 2 | 2 | Geonomics `alag.kz` **и** портал открытых данных Smart Almaty |
| `KZ-79` | город Шымкент | 1 | 1 | РГИС Шымкент (WMS) |

**Наблюдения**

- Самая плотная региональная сетка — **Западно-Казахстанская область (KZ-27)**: областной Geonomics (`map.e-batys.kz`), городской ArcGIS Уральска, жилой/природный SmartMap и **15 районных инвестиционных карт**. Это не 15 разных платформ, а один SaaS.
- Областные Geonomics закрывают Алматы (город и область), Караганду, Костанай, Кызылорду, Туркестан, ЗКО, Мангистау, Жетісу. **Улытау** (`map.iulytau.kz`) в экспорте ещё `scheduled`.
- RGIS/VKOMAP: Абай, ВКО, Темиртау, Актобе, Павлодар, Шымкент; Атырау — старый OpenLayers; СКО и Жамбыл — карта без живого GeoServer.
- **Городской портал открытых данных** есть только у Алматы. Астана — геопортал `gis.esaulet.kz`, не open data.
- Туристические карты Акмолы и нацтуроператора — scheduled, не верифицированы.

Регионы с действующим **областным/городским** геопорталом (не считая только районный SmartMap): Абай, Акмола, Актобе, Алматинская, Атырау, ЗКО, Жамбыл, Жетісу, Караганда, Костанай, Кызылорда, Мангистау, Павлодар, СКО, Туркестан, ВКО, Астана, Алматы, Шымкент. Улытау — только неверифицированная запись.

## 5. Типы владельцев

| Тип владельца | Всего | Действующие |
|---------------|------:|------------:|
| центральное правительство | 36 | 23 |
| региональная власть (акимат области / города республиканского значения) | 24 | 22 |
| местная власть (акимат района / города) | 19 | 18 |
| бизнес | 17 | 12 |
| академия / научная организация | 13 | 10 |
| государственное агентство / нацкомпания | 5 | 0 |
| прочее | 2 | 0 |
| некоммерческая организация | 1 | 0 |
| гражданское общество | 1 | 1 |

Центральное правительство и нацагентства держат национальную статистику, открытые данные, кадастр, НИПД и отраслевые Gharysh-карты. Региональная и местная власть — почти исключительно геопорталы акиматов. Бизнес — ГИС-операторы и недропользователи (Gharysh Sapary, GIS Center, SkyGIS, KPO, Terra, E-Geoprom, SmartForest, Kaztoll, Minerals e-Qazyna). Академия — NU, КазНУ, Buketov, FAI, КазНИИЖиК, KNDC. Гражданское общество — IPT фонда Wings; НКО — Экокарта (scheduled).

`State agency` в схеме реестра — не канонический `owner.type` (синоним к central/business); в выгрузке так помечены тенанты Gharysh Sapary и Казтуризм.

## 6. Программные платформы

| ПО | Записей | Роль в агрегации |
|----|--------:|------------------|
| Custom software (`custom`) | 36 | кастом / зависит от сайта |
| SmartMap (`smartmap`) | 20 | витрина / слои, слабый каталог |
| ArcGIS Server (`arcgisserver`) | 14 | высокий / средний harvest |
| Geonomics (`geonomics`) | 10 | высокий / средний harvest |
| ArcGIS Web AppBuilder (`webappbuilder`) | 10 | витрина / слои, слабый каталог |
| KAZGISA RGIS (`rgis`) | 5 | витрина / слои, слабый каталог |
| VKOMAP (`vkomap`) | 3 | витрина / слои, слабый каталог |
| GeoServer (`geoserver`) | 3 | высокий / средний harvest |
| GeoNode (`geonode`) | 2 | высокий / средний harvest |
| Gharysh Geoportal Platform (`gharyshgeoportal`) | 2 | витрина / слои, слабый каталог |
| GBIF Integrated Publishing Toolkit (IPT) (`ipt`) | 2 | высокий / средний harvest |
| DSpace (`dspace`) | 2 | высокий / средний harvest |
| KAZGISA OpenLayers WebGIS (`kazgisaopenlayers`) | 1 | витрина / слои, слабый каталог |
| CoGIS (`cogis`) | 1 | витрина / слои, слабый каталог |
| Wis 2.0 Box (`wis20box`) | 1 | высокий / средний harvest |
| NextGIS Web (`nextgisweb`) | 1 | высокий / средний harvest |
| ArcGIS Hub (`arcgishub`) | 1 | средний |
| OpenSDG (`opensdg`) | 1 | высокий / средний harvest |
| IMF National Summary Data Page (`imfnsdp`) | 1 | высокий / средний harvest |
| DaCHS (`dachs`) | 1 | высокий / средний harvest |
| Pure (`pure`) | 1 | средний |

## 7. Агрегация в единый каталог и поиск

Имеется в виду возможность **собрать метаданные (и при наличии — записи/слои) в один поисковый индекс**, а не наличие кнопки «скачать» на сайте.

### 7.1. Что реально стыкуется

| Контур | Интерфейсы | Рекомендация для единого поиска |
|--------|-----------|----------------------------------|
| `data.egov.kz` | REST v4 | Ядро национального индекса открытых данных. Обходить API, не HTML |
| НИПД `map.gov.kz` | CSW 2.0.2, OAI-PMH, GeoNode datasets API, WMS/WFS/WCS | Лучшая точка сборки **гео**-метаданных. Приоритет №1 среди геопорталов |
| Областные Geonomics | `geonomics:catalog` (+ иногда WMS) | Второй слой: региональные слои земли/градостроительства. Нужен коннектор под Geonomics, не DCAT |
| ArcGIS REST-фермы | `arcgis:rest:services` | Индексировать **сервисы/слои**, не «портал». Несколько хостов Gharysh — один оператор |
| Научные IR | OAI-PMH (DSpace), IPT/DCAT TTL, TAP, Pure export | Отдельная научная коллекция; фильтровать публикации vs datasets |
| SDG / NSDP | OpenSDG catalog+data, IMF NSDP | Индикаторы ЦУР и макросводка — отдельная схема (indicator, не dataset) |
| Kazhydromet WIS2 | pygeoapi collections/OpenAPI | Погодные коллекции в OGC API, стыкуется с международным WIS |
| SmartMap, RGIS без GeoServer, Web AppBuilder | нет / только карта | **Не harvestить как каталог**. Карточка источника + ссылка |

Действующие каталоги по оценке агрегации:

| Оценка | Число действующих |
|--------|------------------:|
| высокий | 38 |
| средний | 6 |
| ограниченный | 3 |
| низкий | 39 |

Практический вывод: **единый поиск по Казахстану нельзя строить одним коннектором**. Минимум четыре адаптера: (1) REST data.egov.kz, (2) CSW/OAI GeoNode, (3) Geonomics catalog, (4) ArcGIS REST. Статистика БНС в основном HTML/витрина — Taldau без API в реестре; исключение — OpenSDG и NSDP.

## 8. Коммерческий потенциал данных

**Главный риск: лицензионный вакуум.** 0 из 118 каталогов имеют `license_id`. `access_mode: open` в реестре означает «публично смотрится», не «можно продавать производные продукты».

| Сегмент | Потенциал | Комментарий |
|---------|-----------|-------------|
| Национальные открытые данные | средний, условный | data.egov.kz заточен под повторное использование; без SPDX всё равно нужна оферта портала |
| Официальная статистика / Нацбанк / бюджет | условный | Цитирование и аналитика — обычная практика; redistributable bulk — проверить |
| Научные репозитории NU / GBIF | средний по наборам с CC-BY/CC0 | Единственное место, где лицензия бывает на объекте (`granular`) |
| Инвестиционные SmartMap | низкий | Маркетинг территорий, не открытый кадастр на продажу |
| Кадастр ЕГКН / АИС ГЗК / НКГФ | низкий / закрытый | Режимные и правовые сведения, ЭЦП, не open data |
| Minerals e-Qazyna | платный продукт | Коммерция уже встроена оператором |
| Нефтегаз KPO, геологоразведка | условный / договорной | Публичный REST ≠ право встроить в коммерческий ГИС-продукт |
| Мёртвые / scheduled | не использовать | |

Для коммерческого продукта разумная стратегия: (а) data.egov.kz + статистика как справочный слой с атрибуцией; (б) научные наборы с явной CC; (в) геослои — только после письменных условий оператора. Не строить продукт на ЕГКН/SmartMap/Gharysh-витринах без договора.

## 9. Применимость для обучения ИИ

| Задача ИИ | Лучшие источники | Почему |
|-----------|------------------|--------|
| Табличный ML, RAG по госданным | data.egov.kz, Taldau/stat, SDG, Нацбанк | Машиночитаемые таблицы и индикаторы |
| Геомодели (сегментация, land use) | map.gov.kz WFS, живые GeoServer/ArcGIS | Вектор/растр, если скачивание легально |
| Климат / гидрология | климатический кадастр, hydro DB, WIS2 | Ряды наблюдений |
| Биоразнообразие | IPT Buketov, Wings | GBIF-совместимые occurrence |
| Астрономия | FAI DaCHS TAP | Стандартный VO-доступ |
| Речь / vision / NLP (казахский) | ISSAI NU datasets | Прямо заявленные ML-датасеты |
| Сейсмология | KNDC | Бюллетени событий |
| Pretraining LLM на «всём Казахстане» | нет | Нет крупного открытого текстового/мультимодального корпуса в этих каталогах |
| Обучение на кадастре/персональных данных | не рекомендуется | Правовой и этический стоп |

ISSAI — единственная витрина, которая **задумана** как датасеты для ИИ. Остальное — побочный эффект открытых данных и науки. Почти нигде нет явного разрешения на training; для коммерческих моделей это отдельное юридическое решение, не «раз открыто — можно учить».

## 10. Национальные якоря (`is_national: true`)

| Каталог | Тип | Замечание |
|---------|-----|-----------|
| Open Data Portal (`data.egov.kz`) | открытые данные | Да, официальный портал |
| Бюро нацстатистики (`stat.gov.kz`) | индикаторы | Витрина НСУ |
| Taldau (`taldau.stat.gov.kz`) | индикаторы | Флаг `is_national` в выгрузке не проставлен; по сути это рабочая система рядов БНС |
| SDG, NSDP, Gender, Bala | индикаторы | Национальные статистические продукты |
| Геопортал НКГФ | геопортал | Фонд, не публичный NSDI |
| `map.gov.kz` | геопортал | По описанию — НИПД, флаг national не проставлен |

## 11. Карточки каталогов

Ниже — все 118 записей с владельцем в РК, сгруппированные по типу. Сначала действующие, затем проблемные и scheduled.

## Порталы открытых данных

Записей: **3**.

### Open Data Portal of the Republic of Kazakhstan

- **id / uid:** `dataegovkz` / `cdi00001085`
- **URL:** https://data.egov.kz/
- **Тип:** портал открытых данных
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** JSC National Information Technologies — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** RU, KZ
- **Темы:** Government and public sector, Transport, Environment, Society, Economy, Geoscientific Information, Location
- **Интерфейсы (endpoints):** rest

Official Open Data portal of Kazakhstan, publishing machine-readable datasets from central state bodies, regional akimats and other organizations, with search, download (Excel/JSON) and a documented v4 API.

Ключевой национальный каталог открытых данных (is_national=true). Кастомный стек НИТ, не CKAN. API v4 `/api/v4/dataset`.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: rest. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный (лучший среди госданных). Национальный портал открытых данных с API v4 и выгрузкой Excel/JSON. Формально access_mode=open, но license_id в реестре пустой (rights_type=unknown). Коммерческое использование типично допускается политикой открытых данных РК, однако без явной лицензии (CC-BY / аналог) юридический риск остаётся: проверять условия data.egov.kz и паспорта набора.

**Обучение ИИ:** средний. Машиночитаемые госданные (JSON/Excel) и API v4 — лучший вход в табличный training/RAG по Казахстану (транспорт, госуслуги, экология и т.д.). Объём и качество наборов неравномерны; много мелких таблиц. Для LLM — скорее knowledge/RAG, не pretraining. Лицензия не зафиксирована.

### Open Data Smart Almaty

- **id / uid:** `opendatasmartalmatykz` / `cdi00001081`
- **URL:** https://opendata.smartalmaty.kz/
- **Тип:** портал открытых данных
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Akimat of the city of Almaty — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** город Алматы (`KZ-75`)
- **Доступ:** open; API: None / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Government and public sector, Transport, Environment, Education, culture and sport, Economy and finance, Health, Science and technology
- **Интерфейсы (endpoints):** нет в реестре

Almaty city open data portal (Smart Almaty), publishing municipal datasets for public reuse.

Единственный выделенный городской портал открытых данных. API в реестре не подтверждён.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Water resources data portal (Kazakhstan)

- **id / uid:** `dataqiotkz` / `cdi00005208`
- **URL:** https://data.qiot.kz
- **Тип:** портал открытых данных
- **Статус:** неактивный
- **ПО:** Custom software (`custom`)
- **Владелец:** QIoT — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Environment, Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Former water-resources data portal on data.qiot.kz. The hostname no longer accepts connections (connection reset, August 2026).

Мёртвый хост (connection reset, август 2026).

**Агрегация в единый каталог/поиск:** нет. Каталог недоступен, машинная агрегация невозможна.

**Коммерческое использование:** нет. Источник не работает; коммерческое использование актуальных данных невозможно.

**Обучение ИИ:** нет. Источник недоступен.

## Каталоги индикаторов

Записей: **15**.

### AtlasSD socio-demographic atlas of Kazakhstan

- **id / uid:** `atlassdkaznukz` / `cdi99995352`
- **URL:** https://atlassd.kaznu.kz/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Al-Farabi Kazakh National University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ, EN
- **Темы:** Population and society, Society
- **Интерфейсы (endpoints):** нет в реестре

Public AtlasSD electronic atlas of socio-demographic development of Kazakhstan's regions, with yearly indicator reports and thematic maps compiled by Al-Farabi Kazakh National University.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### Bureau of National Statistics (stat.gov.kz)

- **id / uid:** `statgovkz` / `cdi00012000`
- **URL:** https://stat.gov.kz
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** KZ, RU, EN
- **Темы:** Population and society, Economy and finance, Society
- **Интерфейсы (endpoints):** нет в реестре

Main website of the Bureau of National Statistics, sharing population, inflation, labor market and other official indicators for Kazakhstan along with announcements and methodological materials.

Витрина БНС, не API-каталог.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

### Gender Statistics of Kazakhstan

- **id / uid:** `genderstatgovkz` / `cdi00022387`
- **URL:** https://gender.stat.gov.kz
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** KZ, RU, EN
- **Темы:** Population and society, Education, culture and sport, Health, Economy and finance, Society, Economy
- **Интерфейсы (endpoints):** нет в реестре

Official gender statistics portal of the Bureau of National Statistics, presenting the national gender indicator system and publications on the situation of women and men in Kazakhstan across population, family, health, education, employment, human rights and politics.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

### Kazakhstan Indicators for the Sustainable Development Goals

- **id / uid:** `sdgdatastatgovkz` / `cdi00022385`
- **URL:** https://sdgdata.stat.gov.kz/en/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** OpenSDG (`opensdg`)
- **Владелец:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** KZ, RU, EN
- **Темы:** Population and society, Economy and finance, Government and public sector, Environment, Health, Education, culture and sport, Society, Economy
- **Интерфейсы (endpoints):** opensdg:catalog, opensdg:data

National platform for reporting on the Sustainable Development Goals, publishing official global and national SDG indicators for Kazakhstan. Operated by the Bureau of National Statistics as the central coordinator of SDG reporting, with 280 indicators including 205 global and 75 national indicators.

OpenSDG: редкий для РК случай стандартного индикаторного API (catalog+data).

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: opensdg:catalog, opensdg:data. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

### Kazakhstan National Summary Data Page

- **id / uid:** `nsdpstatgovkz` / `cdi00037477`
- **URL:** https://stat.gov.kz/en/standard/national/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** IMF National Summary Data Page (`imfnsdp`)
- **Владелец:** Bureau of National Statistics of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** RU, EN
- **Темы:** Economy and finance, Population and society, Government and public sector, Economy, Society
- **Интерфейсы (endpoints):** imfnsdp:catalog

IMF SDDS National Summary Data Page for Kazakhstan, hosted by Bureau of National Statistics of Kazakhstan. Disseminates macroeconomic and financial summary indicators with SDMX downloads linked from the IMF Dissemination Standards Bulletin Board.

IMF SDDS / NSDP — макросводка со ссылками на SDMX.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: imfnsdp:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

### Kazhydromet hydrological database

- **id / uid:** `meteokazhydrometkzdatabasehydrokz` / `cdi00024676`
- **URL:** https://meteo.kazhydromet.kz/database_hydro_kz/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Kazhydromet — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU, EN
- **Темы:** Environment, Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Surface-water hydrological observation database of Kazhydromet, covering water levels, discharge, ice and related measurements from monitoring stations across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (климат/гидро). Ряды наблюдений и WIS 2.0 collections. Ценны для climate/hydro ML. Климатический кадастр — после регистрации. Не текстовый корпус.

### KOREM electricity market analytics portal

- **id / uid:** `portalkoremkz` / `cdi99995354`
- **URL:** https://portal.korem.kz/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** KOREM JSC — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ
- **Темы:** Energy, Economy and finance, Economy
- **Интерфейсы (endpoints):** нет в реестре

Public analytics portal of KOREM, the operator of Kazakhstan's wholesale electricity and capacity market, with interactive dashboards of centralized trades, prices, volumes and balancing indicators. Embedded from korem.kz.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### Open Budgets of Kazakhstan

- **id / uid:** `budgetegovkz` / `cdi99995355`
- **URL:** https://budget.egov.kz/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Ministry of Finance of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU
- **Темы:** Government and public sector, Economy and finance, Economy
- **Интерфейсы (endpoints):** нет в реестре

Open Budgets portal of Kazakhstan's e-government, publishing budget program passports, income and expenditure execution, republican and local budget reports, and National Fund figures for public use.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### Open Data Repository of the National Bank of the Republic of Kazakhstan

- **id / uid:** `datanationalbankkz` / `cdi00005207`
- **URL:** https://data.nationalbank.kz
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** National Bank of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, EN, KZ
- **Темы:** Economy and finance, Economy
- **Интерфейсы (endpoints):** rest

Open data repository of the National Bank of Kazakhstan, publishing monetary, banking, balance-of-payments and other financial statistics. A REST API is present but requires authentication.

REST есть, но с аутентификацией.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: rest. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Официальная финансовая статистика НБРК. REST требует аутентификации. Коммерческие аналитические продукты обычно допустимы как использование опубликованной статистики, но лицензия в реестре не зафиксирована — нужна проверка правил портала.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### Qamqor Legal Statistics Portal

- **id / uid:** `qamqorgovkz` / `cdi00039816`
- **URL:** https://qamqor.gov.kz/crimestat/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Committee on Legal Statistics and Special Accounts, Prosecutor General's Office of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU
- **Темы:** Justice, legal system and public safety
- **Интерфейсы (endpoints):** нет в реестре

Official crime and legal statistics portal of the Committee on Legal Statistics and Special Accounts of the Prosecutor General's Office: public interactive dashboards on registered crimes, road traffic accidents and other legal statistics indicators.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### SEDA System for Education Data Analysis

- **id / uid:** `sedaiackz` / `cdi99995351`
- **URL:** https://seda.iac.kz/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Information-Analytic Center — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ
- **Темы:** Education, culture and sport, Society
- **Интерфейсы (endpoints):** нет в реестре

SEDA publishes school-quality and access indicators from Kazakhstan's National Educational Database (NOBD), with an indicator list and an interactive map. The TLS certificate on seda.iac.kz was expired when last probed.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### Socio-labor indicators dashboard (ERDO Enbek)

- **id / uid:** `erdoenbekkz` / `cdi99995353`
- **URL:** https://erdo.enbek.kz/analitics
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Workforce Development Center (Center for Development of Labor Resources) — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ
- **Темы:** Population and society, Economy and finance, Society, Economy
- **Интерфейсы (endpoints):** нет в реестре

Public dashboard of socio-labor indicators for Kazakhstan (employment, wages, vacancies, pensions, social payments and labor-force forecasts), published by the Workforce Development Center. The older iac.enbek.kz host redirects here.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** ограниченный. Дашборды и индикаторы: мало строк, много визуализации. Для RAG — да; для обучения больших моделей — нет.

### State Climate Cadastre of Kazakhstan

- **id / uid:** `meteokazhydrometkzclimatekadastr` / `cdi00024672`
- **URL:** https://meteo.kazhydromet.kz/climate_kadastr/
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Kazhydromet — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU, EN
- **Темы:** Environment, Climatology / Meteorology / Atmosphere
- **Интерфейсы (endpoints):** нет в реестре

State Climate Cadastre of Kazhydromet, providing monthly and annual meteorological observation series and climate normals for Kazakhstan after user registration.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (климат/гидро). Ряды наблюдений и WIS 2.0 collections. Ценны для climate/hydro ML. Климатический кадастр — после регистрации. Не текстовый корпус.

### Statistics on Children of Kazakhstan (Bala)

- **id / uid:** `balastatgovkz` / `cdi00022384`
- **URL:** https://bala.stat.gov.kz
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** KZ, RU, EN
- **Темы:** Population and society, Education, culture and sport, Health, Society
- **Интерфейсы (endpoints):** нет в реестре

Official child statistics portal of the Bureau of National Statistics, bringing together indicators and publications on children of Kazakhstan at national, regional and district levels, with disaggregation by age, gender and urban or rural residence across areas such as demography, health, education and living standards.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

### Taldau information-analytical system of the Bureau of National Statistics

- **id / uid:** `taldaustatgovkz` / `cdi00001084`
- **URL:** https://taldau.stat.gov.kz
- **Тип:** каталог индикаторов
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: None / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Population and society, Society
- **Интерфейсы (endpoints):** нет в реестре

Official statistical platform managed by the Bureau of National Statistics, offering demographic and other official statistics for Kazakhstan, including population, gender, age groups, and more.

Основная аналитическая витрина рядов БНС; машиночитаемый API в реестре не описан.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. Официальные индикаторы. Цитирование и аналитика обычно допустимы; перепродажа «как датасет» и скрытие источника — нет. Лицензия в реестре не указана.

**Обучение ИИ:** средний (табличный / RAG). Официальная статистика: ряды индикаторов, SDMX/OpenSDG у части узлов. Отлично для табличных моделей, nowcasting, RAG-справки. Мало для обучения больших моделей «с нуля». Лицензия неизвестна; для детей (Bala) — осторожность с чувствительной статистикой.

## Научные репозитории данных

Записей: **8**.

### FAI archives

- **id / uid:** `dachsfaikz` / `cdi00039817`
- **URL:** https://dachs.fai.kz/
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** DaCHS (`dachs`)
- **Владелец:** Fesenkov Astrophysical Institute — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** EN
- **Темы:** Science and technology
- **Интерфейсы (endpoints):** tap:capabilities

Archive of photometric and spectral observations, digitized astronomical plates, and simulation results from the Fesenkov Astrophysical Institute.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: tap:capabilities. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний–высокий (астрономия). Архив фотометрии, спектров и оцифрованных пластинок FAI. TAP — стандартный интерфейс виртуальной обсерватории. Пригоден для астрономических моделей; не общий LLM-корпус.

### Institute of Smart Systems and Artificial Intelligence. Nazarbayev University datasets

- **id / uid:** `issainuedukz` / `cdi00002051`
- **URL:** https://issai.nu.edu.kz/issai-datasets/
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Institute of Smart Systems and Artificial Intelligence. Nazarbayev University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Science and technology, Education, culture and sport
- **Интерфейсы (endpoints):** sitemap

Collection of datasets by the Institute of Smart Systems and Artificial Intelligence (ISSAI), including speech, image, and text datasets.

**Агрегация в единый каталог/поиск:** ограниченный. Есть только вспомогательное обнаружение (sitemap/RSS). Для агрегации нужен разбор HTML или недокументированный фронтенд-API.

**Коммерческое использование:** условный. Исследовательские датасеты ISSAI (речь, изображение, текст). Часто публикуются для исследований; коммерческое ML-использование нужно сверять с карточкой каждого датасета (не с лицензией каталога).

**Обучение ИИ:** высокий (целевой). Единственный явный ML/AI-ориентированный каталог: датасеты речи, изображений и текста от ISSAI NU. Пригодны для обучения моделей при соблюдении лицензии каждого набора. Каталожного API нет (sitemap), выгрузка — по карточкам.

### Karaganda Biodiversity Information Network

- **id / uid:** `gbifbuketovedukz` / `cdi00010618`
- **URL:** https://gbif.buketov.edu.kz
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** GBIF Integrated Publishing Toolkit (IPT) (`ipt`)
- **Владелец:** Karaganda Buketov University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Biota, Environment, Science and technology
- **Интерфейсы (endpoints):** dcat:ttl, ipt:dataset, rss

IPT installation publishing biodiversity datasets for Kazakhstan and Central Asia.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: ipt:dataset. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. GBIF IPT. Наборы обычно уходят в GBIF под стандартными условиями (CC0/CC-BY/CC-BY-NC). Коммерция зависит от лицензии конкретного IPT-ресурса; NC-лицензии коммерцию закрывают.

**Обучение ИИ:** средний–высокий (биоразнообразие). Occurrence-данные IPT/GBIF — сильный источник для моделей биоразнообразия, ареалов, citizen science. Объём обычно тысячи–сотни тысяч наблюдений, не web-scale корпус. Лицензия набора критична (CC-BY vs CC-BY-NC).

### Kazakhstan National Data Center (KNDC)

- **id / uid:** `kndckz` / `cdi00039818`
- **URL:** https://kndc.kz/
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Institute of Geophysical Research, National Nuclear Center of Kazakhstan — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Science and technology
- **Интерфейсы (endpoints):** нет в реестре

Seismological data center of the Institute of Geophysical Research (NNC RK): urgent and interactive seismic event bulletins, seismic and infrasound station network catalog for Kazakhstan and Central Asia.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (сейсмология). Бюллетени событий и каталог станций. Полезны для seismology ML; объём ограничен. API в реестре не описан.

### Nazarbayev University Repository

- **id / uid:** `nurnuedukz` / `cdi99991626`
- **URL:** https://nur.nu.edu.kz
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** DSpace (`dspace`)
- **Владелец:** Nazarbayev University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** EN, KZ, RU
- **Темы:** Science and technology, Education, culture and sport
- **Интерфейсы (endpoints):** dspace, dspace:objects, oaipmh20

Institutional DSpace archive of Nazarbayev University theses, research publications, institute outputs, journals, and conference materials. Distinct from the NU Research Data Repository at nurdata.nu.edu.kz.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: dspace, dspace:objects, oaipmh20. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. DSpace с тезисами и публикациями: текст для RAG/NLP, но это IR смешанного типа (статьи ≠ открытые датасеты). OAI-PMH есть. Не путать с nurdata.

### NU Research Data Repository

- **id / uid:** `nurdatanuedukz` / `cdi00024675`
- **URL:** https://nurdata.nu.edu.kz
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** DSpace (`dspace`)
- **Владелец:** Nazarbayev University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=granular; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** EN, KZ, RU
- **Темы:** Science and technology, Education, culture and sport, Society
- **Интерфейсы (endpoints):** dspace, dspace:objects, sitemap, oaipmh20

Institutional research data repository of Nazarbayev University for storing, managing, preserving and providing access to research datasets of the NU community, with persistent DOIs for citation and reuse.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: dspace, dspace:objects, oaipmh20. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный (по набору). Научный репозиторий с granular-лицензиями: права задаются на уровне датасета (часто CC). Коммерция возможна только там, где лицензия набора это разрешает; смесь публикаций и данных.

**Обучение ИИ:** высокий. Институциональный research data repository (DSpace) с DOI и OAI-PMH. Пригоден для сбора исследовательских датасетов. Смесь дисциплин; не все объекты — train-ready таблицы. Лицензии granular.

### NU Research Portal - Nazarbayev University

- **id / uid:** `researchnuedukz` / `cdi00002052`
- **URL:** https://research.nu.edu.kz
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** Pure (`pure`)
- **Владелец:** Nazarbayev University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=granular; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** EN
- **Темы:** Science and technology
- **Интерфейсы (endpoints):** rss, pure:export_excel, sitemap

Portal hosting information about research projects, publications, datasets, grant opportunities, and collaboration activities for over 400 researchers and faculty at Nazarbayev University, promoting interdisciplinary research and innovation.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (pure:export_excel), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный (по набору). Научный репозиторий с granular-лицензиями: права задаются на уровне датасета (часто CC). Коммерция возможна только там, где лицензия набора это разрешает; смесь публикаций и данных.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Wings PF IPT installation

- **id / uid:** `iptwingedsworld` / `cdi00010619`
- **URL:** https://ipt.wingeds.world
- **Тип:** научный репозиторий данных
- **Статус:** действующий
- **ПО:** GBIF Integrated Publishing Toolkit (IPT) (`ipt`)
- **Владелец:** Wings Animal and Plant Conservation and Protection Fund — гражданское общество
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Biota, Environment, Science and technology
- **Интерфейсы (endpoints):** dcat:ttl, ipt:dataset, rss

GBIF IPT of the Wings Animal and Plant Conservation and Protection Fund, used to publish bird and other biodiversity monitoring datasets for Kazakhstan.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: ipt:dataset. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. GBIF IPT. Наборы обычно уходят в GBIF под стандартными условиями (CC0/CC-BY/CC-BY-NC). Коммерция зависит от лицензии конкретного IPT-ресурса; NC-лицензии коммерцию закрывают.

**Обучение ИИ:** средний–высокий (биоразнообразие). Occurrence-данные IPT/GBIF — сильный источник для моделей биоразнообразия, ареалов, citizen science. Объём обычно тысячи–сотни тысяч наблюдений, не web-scale корпус. Лицензия набора критична (CC-BY vs CC-BY-NC).

## Геопорталы

Записей: **92**.

### Abai region geoportal

- **id / uid:** `abaimapkz` / `cdi00022386`
- **URL:** https://abaimap.kz/Kaz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** VKOMAP (`vkomap`)
- **Владелец:** Department of Architecture, Urban Planning and Land Relations of Abai Region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Абайская область (`KZ-10`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Regions and cities, Transport, Government and public sector, Boundaries, Planning / Cadastre, Structure, Transportation, Location
- **Интерфейсы (endpoints):** customapi, customapi

Regional geoinformation system of Abai Region for spatial data and electronic maps, including land plots, buildings, street networks, utilities, master plans, and cadastral land valuation.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: customapi. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Akmola Regional Map Portal

- **id / uid:** `mapakmolkz` / `cdi00002037`
- **URL:** http://map.akmol.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Akimat of Akmola region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Акмолинская область (`KZ-11`)
- **Доступ:** open; API: None / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Environment, Elevation, Geoscientific Information, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** нет в реестре

Interactive map portal of Akmola Region (Интерактивная карта Акмолинской области), publishing geographic and spatial data for the oblast. HTTP only; the HTTPS certificate does not match.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Aktobe city geoportal

- **id / uid:** `geoportalaktkz` / `cdi00002033`
- **URL:** https://eaqtobe.kz/map/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA RGIS (`rgis`)
- **Владелец:** Communal State Institution Urban Planning Centre — местная власть (акимат района / города)
- **Покрытие:** Актюбинская область (`KZ-15`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=inapplicable; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Location
- **Интерфейсы (endpoints):** wms111, wms130, wfs110, wfs200, wcs100, wcs110, wcs111, wcs11, wcs201, wps100, tms100, wms-c111, wmts100

Regional GIS (RGIS) geoportal of Aktobe (title РГИС Актобе). The former geoportal.akt.kz GeoServer host no longer resolves; the public Leaflet map is at eaqtobe.kz/map.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (tms100, wcs100, wcs11, wcs110, wcs111, wcs201, wfs110, wfs200, wms-c111, wms111), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Akzhaik District investment geoportal

- **id / uid:** `aqjaiyqsmartmapkz` / `cdi99995365`
- **URL:** https://aqjaiyq.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Akzhaik District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Akzhaik District (West Kazakhstan, centre Chapaev) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Almaty region geoportal

- **id / uid:** `mapalmoblkz` / `cdi00002038`
- **URL:** https://map.almobl.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Almaty region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Алматинская область (`KZ-19`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Government and public sector, Environment, Transport, Boundaries
- **Интерфейсы (endpoints):** geonomics:catalog

Geoportal of the Almaty Region akimat, powered by Geonomics.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### ArcGIS server of the Committee on the legal statistics and special accounts of the state office of public prosecutor of Republic of Kazakhstan

- **id / uid:** `giskgpkz` / `cdi00001078`
- **URL:** https://gis.kgp.kz/server/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Committee on the legal statistics and special accounts of the state office of public prosecutor of Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Justice, legal system and public safety, Location
- **Интерфейсы (endpoints):** arcgis:portals:self, arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

ArcGIS Enterprise of the Committee on Legal Statistics and Special Accounts of the Prosecutor General's Office, with Experience Builder apps and REST services.

Живой ArcGIS Enterprise прокуратуры; deprecated-дубль — giskgparcgisrestservices.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:portals:self, arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### ArcGIS server of the JSC "National company "Kazakhstan Gharysh Sapary"

- **id / uid:** `gisgharyshkz` / `cdi00001077`
- **URL:** https://gis.gharysh.kz/server/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** JSC "National company "Kazakhstan Gharysh Sapary" — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

Geoportal. managed by JSC National company Kazakhstan Gharysh Sapary, powered by ArcGIS Server.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### ArcGIS server of the Kazakhstan Center for Geographic Information Systems

- **id / uid:** `arcgisgiscenterkz` / `cdi00001075`
- **URL:** https://arcgis.gis-center.kz/server/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Kazakhstan Center for Geographic Information Systems — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Location, Boundaries
- **Интерфейсы (endpoints):** arcgis:rest:services

Listing of ArcGIS REST services provided by the GIS Center in Kazakhstan, intended for mapping, spatial analysis, and geodata sharing.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Atyrau region geoportal

- **id / uid:** `geoeatyraukz` / `cdi00002030`
- **URL:** http://eatyrau.kz/map/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA OpenLayers WebGIS (`kazgisaopenlayers`)
- **Владелец:** Akimat of Atyrau region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Атырауская область (`KZ-23`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=inapplicable; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Geoscientific Information
- **Интерфейсы (endpoints):** нет в реестре

Regional geoportal of Atyrau Region (title Геопортал Атырау). The former GeoServer at geo.eatyrau.kz/geoserver returns HTTP 404; the public map is at eatyrau.kz/map.

**Агрегация в единый каталог/поиск:** низкий. Стандартных harvest-интерфейсов в метаданных нет.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Bayterek District investment geoportal

- **id / uid:** `baitereksmartmapkz` / `cdi99995366`
- **URL:** https://baiterek.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Bayterek District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Bayterek District (West Kazakhstan, centre Peremyotnoye) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Bokey Orda District investment geoportal

- **id / uid:** `bokeyordasmartmapkz` / `cdi99991645`
- **URL:** https://bokeyorda.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Bokey Orda District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Bokey Orda District (West Kazakhstan) with rural okrug polygons, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Burlin District investment geoportal

- **id / uid:** `burlinsmartmapkz` / `cdi99991646`
- **URL:** https://burlin.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Burlin District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Burlin District (West Kazakhstan), including Aksai, with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Chingirlau District investment geoportal

- **id / uid:** `chingirlausmartmapkz` / `cdi99991647`
- **URL:** https://chingirlau.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Chingirlau District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Chingirlau District (West Kazakhstan) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### City of Almaty geoportal

- **id / uid:** `alagkz` / `cdi00002028`
- **URL:** https://alag.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of the city of Almaty — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** город Алматы (`KZ-75`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Government and public sector, Boundaries
- **Интерфейсы (endpoints):** geonomics:catalog

Geonomics geoportal of Almaty city for administrative-territorial divisions and other municipal spatial layers, with export APIs.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### E-Geoprom geological ArcGIS Server

- **id / uid:** `stixgeologykz` / `cdi00001083`
- **URL:** https://stix.geology.kz:6443/arcgis/rest/services/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** LLP Geological platform E-Geoprom — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:services

A web-based data catalog for geological data, hosted on ArcGIS REST services.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### East Kazakhstan region geoportal

- **id / uid:** `vkomapkz` / `cdi00002050`
- **URL:** https://vkomap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** VKOMAP (`vkomap`)
- **Владелец:** Akimat of East Kazakhstan region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** KZ-63 (`KZ-63`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Transport, Environment, Economy and finance, Government and public sector, Transportation, Inland Waters, Economy
- **Интерфейсы (endpoints):** customapi, customapi

Geo-spatial portal for East Kazakhstan region, providing maps, land relations, construction regulations, and technical specifications.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: customapi. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### EGIZ ArcGIS Server

- **id / uid:** `egizkz` / `cdi00013539`
- **URL:** https://egiz.kz/server/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** EGIZ — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

ArcGIS REST Services Directory providing access to orthophoto imagery, administrative boundaries, population data, and other geospatial services for Kazakhstan.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### GIS portal of the National Spatial Data Infrastructure of Kazakhstan

- **id / uid:** `mapgovkz` / `cdi00001079`
- **URL:** https://map.gov.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** GeoNode (`geonode`)
- **Владелец:** National Centre of Geodesy and Spatial Information — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Environment, Elevation
- **Интерфейсы (endpoints):** geonode:datasets, geonode:documents, wms111, wfs110, wcs111, csw202, oaipmh20, opensearch, wms130, wfs100, wfs200, wcs100, wcs110, wcs11, wcs201, wps100, geoserver:version, geoserver:settings, geoserver:layers, opensearch

Official government GeoNode portal for the National Spatial Data Infrastructure of Kazakhstan (НИПД), with GeoServer OGC services.

Фактический узел НИПД на GeoNode: лучший набор интерфейсов в стране (CSW, OAI-PMH, WMS/WFS/WCS). Флаг is_national в выгрузке не проставлен, но по смыслу это национальный геопортал.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: csw202, geonode:datasets, oaipmh20. Дополнительно есть OGC/картографические сервисы (geonode:documents, geoserver:layers, opensearch, wcs100, wcs11, wcs110, wcs111, wcs201). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Karachaganak Petroleum Operating B.V. geoportal

- **id / uid:** `mapskpokz` / `cdi00001080`
- **URL:** https://maps.kpo.kz/arcgis/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Karachaganak Petroleum Operating B.V. — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Environment, Energy, Geoscientific Information
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

Official mapping portal of Karachaganak Petroleum Operating B.V. (KPO), providing access to spatial and environmental data related to the Karachaganak field and its operations in Kazakhstan.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Karaganda Alikhan Bokeikhan District geoportal

- **id / uid:** `karagandasmartmapkz` / `cdi99995361`
- **URL:** https://karaganda.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** State Revenue Department for Alikhan Bokeikhan District — центральное правительство
- **Покрытие:** Карагандинская область (`KZ-35`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap geoportal for Alikhan Bokeikhan District in Karaganda, publishing tax, business, and urban map objects in a Leaflet plus Google Maps viewer.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Karaganda region geoportal

- **id / uid:** `geoqaroblkz` / `cdi00002034`
- **URL:** https://geo.qarobl.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Karaganda region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Карагандинская область (`KZ-35`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities
- **Интерфейсы (endpoints):** geonomics:catalog, wms130

Geonomics geoportal of Karaganda Region for land, urban-planning and administrative-territorial spatial data, with an optional GeoServer WMS backend.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Дополнительно есть OGC/картографические сервисы (wms130). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Karatobe District investment geoportal

- **id / uid:** `qaratobesmartmapkz` / `cdi99995364`
- **URL:** https://qaratobe.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Karatobe District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Karatobe District (West Kazakhstan) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Kazakh research institute of livestock and fodder production geoserver

- **id / uid:** `pastureskazniizhikkz` / `cdi00001082`
- **URL:** https://pastures.kazniizhik.kz:8443/geoserver
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** GeoServer (`geoserver`)
- **Владелец:** Kazakh research institute of livestock and fodder production — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=inapplicable; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** wms111, wms130, wfs100, wfs110, wfs200, wcs100, wcs110, wcs111, wcs11, wcs201, wps100, tms100, wms-c111

GeoServer of the Kazakh Research Institute of Livestock and Fodder Production, publishing pasture and related agricultural spatial layers.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (tms100, wcs100, wcs11, wcs110, wcs111, wcs201, wfs100, wfs110, wfs200, wms-c111), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Kazakhstan - WIS 2.0 in a box

- **id / uid:** `wis2boxkazhydrometkz` / `cdi00005100`
- **URL:** https://wis2box.kazhydromet.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Wis 2.0 Box (`wis20box`)
- **Владелец:** Kazhydromet — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** EN
- **Темы:** Climatology / Meteorology / Atmosphere, Environment
- **Интерфейсы (endpoints):** pygeoapi:openapi, pygeoapi:collections

WIS 2.0 in a Box node of Kazhydromet, publishing meteorological and hydrological collections to the WMO Information System.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: pygeoapi:collections. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (климат/гидро). Ряды наблюдений и WIS 2.0 collections. Ценны для climate/hydro ML. Климатический кадастр — после регистрации. Не текстовый корпус.

### Kaztal District investment geoportal

- **id / uid:** `kaztalovsmartmapkz` / `cdi99991644`
- **URL:** https://kaztalov.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Kaztal District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Kaztal District (West Kazakhstan) with rural okrug boundaries, land plots, mineral occurrences, and business/infrastructure map objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Kostanay region geoportal

- **id / uid:** `mapikostanaykz` / `cdi00002043`
- **URL:** https://map.ikostanay.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Kostanay region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Костанайская область (`KZ-39`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities
- **Интерфейсы (endpoints):** geonomics:catalog

Data catalog for Kostanay region, Kazakhstan

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### KPO CoGIS catalog

- **id / uid:** `giskpoelitegisrestservices` / `cdi00013538`
- **URL:** https://gis.kpo.kz/cogis
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** CoGIS (`cogis`)
- **Владелец:** Karachaganak Petroleum Operating B.V. — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Environment, Energy, Geoscientific Information
- **Интерфейсы (endpoints):** arcgis:rest:services

Public CoGIS Portal catalog for Karachaganak Petroleum Operating (Экомонитор / ГИС-КПО). Map services remain on eLiteGIS at /elitegis/rest/services.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Kyzylorda District investment geoportal

- **id / uid:** `kyzylordasmartmapkz` / `cdi99995367`
- **URL:** https://kyzylorda.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Kyzylorda — местная власть (акимат района / города)
- **Покрытие:** Кызылординская область (`KZ-43`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap geoportal titled Kyzylorda District, with the same Leaflet plus Google Maps investment-viewer stack as other smartmap.kz tenants.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Kyzylorda region geoportal

- **id / uid:** `ordageoportalkz` / `cdi00002046`
- **URL:** https://orda.geoportal.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Kyzylorda region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Кызылординская область (`KZ-43`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Geoscientific Information
- **Интерфейсы (endpoints):** geonomics:catalog

Geonomics geoportal of Kyzylorda Region for collecting, visualizing and analysing land, urban-planning and administrative-territorial spatial data.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Moraine Lakes Ile Alatau

- **id / uid:** `morainelakeskz` / `cdi00021355`
- **URL:** https://morainelakes.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** GeoNode (`geonode`)
- **Владелец:** Moraine Lakes Ile Alatau Project — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** EN, RU, KZ
- **Темы:** Environment, Inland Waters
- **Интерфейсы (endpoints):** geonode:datasets, wms130

GeoNode catalog of the Moraine Lakes Ile Alatau project (IRN BR21882365), publishing remote-sensing and field-survey layers used to assess glacial lake outburst risk in Ile-Alatau.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonode:datasets. Дополнительно есть OGC/картографические сервисы (wms130). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### National Spatial Data Fund portal

- **id / uid:** `geoportalnkgfkz` / `cdi00024674`
- **URL:** https://geoportal.nkgf.kz/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** National Cartographic and Geodetic Fund, National Centre of Geodesy and Spatial Information — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** restricted; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** да
- **Языки:** KZ, RU
- **Темы:** Government and public sector, Imagery / Base Maps / Earth Cover, Elevation, Location, Geoscientific Information
- **Интерфейсы (endpoints):** нет в реестре

Spatial data web portal of the National Cartographic and Geodetic Fund, cataloguing digital topographic maps and plans, orthophotos, analog maps and geodetic network materials. Access requires a Kazakhstan electronic digital signature.

Официальный фонд пространственных данных (is_national=true) с доступом по ЭЦП — не путать с публичным map.gov.kz.

**Агрегация в единый каталог/поиск:** низкий. Доступ по ЭЦП, публичных harvest-интерфейсов в реестре нет. В единый открытый поиск не включается без отдельного соглашения.

**Коммерческое использование:** низкий. Национальный картографо-геодезический фонд: доступ по ЭЦП РК, режим restricted. Коммерческое переиспользование фондовных карт/ортофото вне установленного порядка маловероятно.

**Обучение ИИ:** низкий. Фондовые карты за ЭЦП. Для открытого обучения ИИ не подходит.

### North Kazakhstan region geoportal

- **id / uid:** `geoesqokz` / `cdi00002032`
- **URL:** https://e-sqo.kz/map/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA RGIS (`rgis`)
- **Владелец:** Akimat of North Kazakhstan region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Северо-Казахстанская область (`KZ-59`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Location, Elevation
- **Интерфейсы (endpoints):** нет в реестре

Regional map portal of North Kazakhstan Region (E-SQO). The former geo.e-sqo.kz host returns HTTP 404; the public Leaflet map is at e-sqo.kz/map.

**Агрегация в единый каталог/поиск:** ограниченный. RGIS (KAZGISA): публичная карта на Leaflet. OGC-сервисы у части инсталляций отвалились (404 на geo.*). Агрегация слоёв возможна только если жив GeoServer; иначе — только ручная витрина.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Oral maslikhat geoportal

- **id / uid:** `maslihatsmartmapkz` / `cdi99995362`
- **URL:** https://maslihat.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Maslikhat of Oral — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Government and public sector, Boundaries, Location, Society
- **Интерфейсы (endpoints):** нет в реестре

Live SmartMap city geoportal for Oral (Uralsk) with electoral-district layers. Distinct from the inactive uralsk.smartmap.kz city-development tenant.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Pavlodar region geoportal

- **id / uid:** `geopavlodarkz` / `cdi00002042`
- **URL:** https://geopavlodar.kz/map/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA RGIS (`rgis`)
- **Владелец:** Pavlodar region Digital department — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Павлодарская область (`KZ-55`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Transport, Population and society, Government and public sector, Environment, Education, culture and sport, Health, Economy and finance
- **Интерфейсы (endpoints):** wms111, wms130, wfs100, wfs110, wfs200, wcs100, wcs110, wcs111, wcs11, wcs201, wps100, tms100, wms-c111, wmts100

Regional GIS (RGIS) geoportal of Pavlodar Region, with a public Angular Leaflet map viewer and GeoServer OGC services for regional spatial data.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (tms100, wcs100, wcs11, wcs110, wcs111, wcs201, wfs100, wfs110, wfs200, wms-c111), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Public cadastral map of Kazakhstan (EGKN)

- **id / uid:** `mapgov4ckz` / `cdi00024673`
- **URL:** https://map.gov4c.kz/egkn/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Non-profit JSC Government for Citizens — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU
- **Темы:** Government and public sector, Regions and cities, Planning / Cadastre, Boundaries, Location
- **Интерфейсы (endpoints):** нет в реестре

Public cadastral map of the Unified State Cadastre of Real Estate (EGKN), displaying land, legal and urban-planning cadastre information for plots across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** низкий. Публичная кадастровая карта ЕГКН. Содержит сведения о правах на недвижимость. Просмотр для информирования — да; массовая выгрузка и коммерческие продукты по персональным/правовым данным — высокий юридический риск без отдельного правового основания.

**Обучение ИИ:** низкий. Кадастр и права на землю: персональные и режимные сведения. Не использовать для открытого обучения моделей без правового основания.

### QAJ Kaztoll geoportal

- **id / uid:** `geoportalkaztollkz` / `cdi00024678`
- **URL:** https://geoportal.kaztoll.kz/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** GeoServer (`geoserver`)
- **Владелец:** NC KazAvtoZhol (QAJ) — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=inapplicable; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Transport, Transportation, Location, Structure
- **Интерфейсы (endpoints):** wms111, wms130, wfs100, wfs110, wfs200

GeoServer geoportal of the Kazakhstan toll-road operator QAJ, publishing geospatial layers for the national paid-road network.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (wfs100, wfs110, wfs200, wms111, wms130), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Second ArcGIS server of the JSC "National company Kazakhstan Gharysh Sapary"

- **id / uid:** `argissrvgharyshkz` / `cdi00002029`
- **URL:** https://argissrv.gharysh.kz/arcgis/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** JSC "National company "Kazakhstan Gharysh Sapary" — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

ArcGIS REST Services Directory listing published GIS services.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Shymkent city geoportal

- **id / uid:** `geoshymkz` / `cdi00002045`
- **URL:** https://geo-shym.kz/map
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA RGIS (`rgis`)
- **Владелец:** Akimat of Shymkent city — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** город Шымкент (`KZ-79`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Location, Planning / Cadastre
- **Интерфейсы (endpoints):** wms130

Regional GIS (RGIS) geoportal of Shymkent city, with a public map viewer and GeoServer WMS layers for municipal spatial data.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (wms130), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### SkyGIS ArcGIS tile server

- **id / uid:** `tileskygiskz` / `cdi00002047`
- **URL:** https://tile.skygis.kz/arcgis/rest/services
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** SkyGIS — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Location, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:services

ArcGIS Server tile services operated by SkyGIS, including topographic and regional map caches for Kazakhstan and neighbouring coverage folders.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### SmartForest Web GIS

- **id / uid:** `gissmartforestkz` / `cdi00025853`
- **URL:** https://gis.smartforest.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** NextGIS Web (`nextgisweb`)
- **Владелец:** SmartForest — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Agriculture, fisheries, forestry and food, Environment, Biota, Imagery / Base Maps / Earth Cover, Location
- **Интерфейсы (endpoints):** nextgisweb:api, nextgisweb:pkg-version, nextgisweb:routes

Kazakhstan SmartForest NextGIS Web geoportal with public forest, collector, and imagery resource groups.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: nextgisweb:api. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Syrym District investment geoportal

- **id / uid:** `syrymsmartmapkz` / `cdi99991651`
- **URL:** https://syrym.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Syrym District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Syrym District (West Kazakhstan) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Taskala District investment geoportal

- **id / uid:** `taskalasmartmapkz` / `cdi99991649`
- **URL:** https://taskala.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Taskala District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Taskala District (West Kazakhstan) with rural okrug boundaries, land plots, mineral occurrences, and mapped investment objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Temir District investment geoportal

- **id / uid:** `temirsmartmapkz` / `cdi99995360`
- **URL:** https://temir.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Temir District — местная власть (акимат района / города)
- **Покрытие:** Актюбинская область (`KZ-15`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Temir District (Aktobe Region, centre Shubarkuduk) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Temirstroy housing geoportal

- **id / uid:** `temirstroysmartmapkz` / `cdi99999742`
- **URL:** https://temirstroy.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Construction Department of West Kazakhstan Region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Population and society, Government and public sector, Structure, Planning / Cadastre, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap housing and construction geoportal (Найти новое жилье) on temirstroy.smartmap.kz, with the same Leaflet plus Google Maps and stylse.css stack as other smartmap.kz tenants. Linked to the West Kazakhstan Construction Department (stroy-bko.gov.kz) for developer and buyer housing layers.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Temirtau city geoportal

- **id / uid:** `temirmapkz` / `cdi99991643`
- **URL:** https://temirmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** VKOMAP (`vkomap`)
- **Владелец:** Akimat of the city of Temirtau — местная власть (акимат района / города)
- **Покрытие:** Карагандинская область (`KZ-35`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** customapi, customapi

City geoportal of Temirtau (Karaganda Region) for urban-planning and cadastral map layers, including buildings, addresses, and land objects. Layer list is published at /Public/GetLayers.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: customapi. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Terekti District investment geoportal

- **id / uid:** `terektismartmapkz` / `cdi99991652`
- **URL:** https://terekti.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Terekti District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Terekti District (West Kazakhstan) with rural okrug boundaries, land plots, mineral occurrences, and mapped infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Terra Exploration ArcGIS Server

- **id / uid:** `gisportalkz` / `cdi00002036`
- **URL:** https://gis-portal.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** LLP Terra Exploration — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Location, Geoscientific Information, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** arcgis:rest:services

ArcGIS Server of LLP Terra Exploration, publishing geospatial REST services used for mineral exploration mapping in Kazakhstan.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Turkestan region geoportal

- **id / uid:** `mapiturkistankz` / `cdi00002044`
- **URL:** https://map.iturkistan.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Turkestan region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Туркестанская область (`KZ-61`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Transport, Boundaries, Elevation, Environment, Economy
- **Интерфейсы (endpoints):** geonomics:catalog

Geonomics geoportal of Turkestan Region for land, urban-planning and administrative-territorial spatial data.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Unified Subsoil Use Platform (Minerals)

- **id / uid:** `mineralseqazynakz` / `cdi00024677`
- **URL:** https://minerals.e-qazyna.kz/en/start
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** JSC Information and Accounting Center — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** KZ, RU, EN
- **Темы:** Economy and finance, Environment, Geoscientific Information, Economy
- **Интерфейсы (endpoints):** нет в реестре

Unified Subsoil Use Platform providing an interactive map and reference data on mineral deposits, licenses, contracts, applications and geological reports in Kazakhstan. Public browsing is free; full access is paid.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** ограниченный / платный. Публичный просмотр справочника недр бесплатный, полный доступ платный. Это ближе к коммерческой витрине недр, чем к открытым данным. Для продуктов нужна лицензия оператора (АО «ИУЦ»).

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Uralsk city geoportal

- **id / uid:** `uralskmapgenplankz` / `cdi00002048`
- **URL:** https://uralskmap.genplan.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Akimat of the city Uralsk — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Regions and cities
- **Интерфейсы (endpoints):** arcgis:rest:services

Uralsk city geoportal powered by ArcGIS Server.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### West Kazakhstan housing geoportal

- **id / uid:** `zkosmartmapkz` / `cdi99999743`
- **URL:** https://zko.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Construction Department of West Kazakhstan Region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Population and society, Government and public sector, Structure, Planning / Cadastre, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap regional housing and construction geoportal (Найти новое жилье) on zko.smartmap.kz for West Kazakhstan Region, with Leaflet plus Google Maps and stylse.css. Linked to the West Kazakhstan Construction Department for developer, buyer, and general-plan layers.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### West Kazakhstan natural resources geoportal

- **id / uid:** `uprsmartmapkz` / `cdi99995363`
- **URL:** https://upr.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Department of Natural Resources and Environmental Regulation of West Kazakhstan Region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Environment and energy, Government and public sector, Environment, Planning / Cadastre, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap geoportal of the West Kazakhstan Department of Natural Resources and Environmental Regulation, with land-plot lookup and regional scheme layers.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### West-Kazakhstan region geoportal

- **id / uid:** `mapebatyskz` / `cdi00002039`
- **URL:** https://map.e-batys.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of West-Kazakhstan region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities
- **Интерфейсы (endpoints):** geonomics:catalog

Геоинформационная платформа для сбора, хранения, визуализации, анализа и обработки большого объема геоданных и геоинформации. Западно-Казахстанская область

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Zhambyl region geoportal

- **id / uid:** `geoejambylkz` / `cdi00002031`
- **URL:** https://e-jambyl.kz/map/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** KAZGISA RGIS (`rgis`)
- **Владелец:** Akimat of Zhambyl region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Жамбылская область (`KZ-31`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Environment, Transport, Agriculture, fisheries, forestry and food, Boundaries, Elevation, Imagery / Base Maps / Earth Cover, Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Regional map portal of Zhambyl Region (E-JAMBYL). The former geo.e-jambyl.kz host returns HTTP 404; the public Leaflet map is at e-jambyl.kz/map.

**Агрегация в единый каталог/поиск:** ограниченный. RGIS (KAZGISA): публичная карта на Leaflet. OGC-сервисы у части инсталляций отвалились (404 на geo.*). Агрегация слоёв возможна только если жив GeoServer; иначе — только ручная витрина.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Zhangala District investment geoportal

- **id / uid:** `janaqalasmartmapkz` / `cdi99991648`
- **URL:** https://janaqala.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Zhangala District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Zhangala District (West Kazakhstan) with rural okrug boundaries, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Zhanibek District investment geoportal

- **id / uid:** `janibeksmartmapkz` / `cdi99991650`
- **URL:** https://janibek.smartmap.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of Zhanibek District — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Economy and finance, Government and public sector, Boundaries, Planning / Cadastre, Economy, Location
- **Интерфейсы (endpoints):** нет в реестре

SmartMap investment geoportal of Zhanibek District (West Kazakhstan) with rural okrug polygons, land plots, and mapped investment and infrastructure objects.

**Агрегация в единый каталог/поиск:** низкий. Платформа SmartMap — публичный Leaflet/Google Maps просмотрщик без зарегистрированного каталожного API, CSW, WFS или DCAT. В единый поиск попадает только как витрина/карточка портала, не как harvestable источник наборов.

**Коммерческое использование:** низкий. Инвестиционные карты районов: границы, участки, объекты инфраструктуры. Нет лицензии, нет bulk API. Пригодно как ориентир для due diligence, не как перепродаваемый датасет.

**Обучение ИИ:** низкий. Витрина инвестиционных объектов без bulk-выгрузки. Для обучения геомоделей почти непригодна.

### Геоинформационный портал города Астана

- **id / uid:** `gisesauletkz` / `cdi00001076`
- **URL:** https://gis.esaulet.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Akimat of the city of Astana — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** город Астана (`KZ-71`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Regions and cities, Geoscientific Information, Location, Boundaries
- **Интерфейсы (endpoints):** arcgis:portals:self, arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

Official geoinformation portal of Astana city (ArcGIS Experience Builder), with ArcGIS Server REST services for municipal maps and layers.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:portals:self, arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:kmz, arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Геопортал Мангистауской Области

- **id / uid:** `mapemangistaukz` / `cdi00002040`
- **URL:** https://map.e-mangistau.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Mangystau region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Мангистауская область (`KZ-47`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Transport, Environment, Boundaries, Health, Location, Planning / Cadastre, Society
- **Интерфейсы (endpoints):** geonomics:catalog

Геоинформационная платформа для сбора, хранения, визуализации, анализа и обработки большого объема геоданных и геоинформации по Мангистауской области.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Геопортал области Жетісу

- **id / uid:** `mapezhetisukz` / `cdi00002041`
- **URL:** https://map.e-zhetisu.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Jetisu region government — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** область Жетісу (`KZ-33`)
- **Доступ:** open; API: True / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Regions and cities, Agriculture, fisheries, forestry and food, Transport, Boundaries, Elevation, Environment, Inland Waters, Location
- **Интерфейсы (endpoints):** geonomics:catalog

Геоинформационная платформа для сбора, хранения, визуализации, анализа и обработки большого объема геоданных и геоинформации

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: geonomics:catalog. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** средний (гео-ИИ). Пространственные слои (WFS/REST/GeoJSON) пригодны для segmentation, land-use, basemap-моделей, если удаётся легально скачать вектор/растр. Это не текстовый корпус. Лицензия слоёв не задана.

### Геопортал РГП «Госградкадастр»

- **id / uid:** `ggkkz` / `cdi00002035`
- **URL:** https://ggk.kz
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** RGP Gosgradkadastr — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: None / active
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN, KZ
- **Темы:** Boundaries, Elevation, Planning / Cadastre
- **Интерфейсы (endpoints):** нет в реестре

Геопортал РГП «Госградкадастр» — инструмент предоставления информации о текущем и планируемом развитии населенных пунктов, карты, рельеф, административные объекты, генеральные и детальные планы.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** низкий. Земельный / градостроительный кадастр. Публичная карта не равна открытой лицензии на коммерческую переработку кадастра.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Картографическая основа Управления Земельного кадастра и Автоматизированной информационной системы государственного земельного кадастра

- **id / uid:** `aisgzkkz` / `cdi00001074`
- **URL:** https://aisgzk.kz/aisgzk/ru/content/maps/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Department of the Land Cadastre and Automated Information System of the State Land Cadastre. Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Geoscientific Information
- **Интерфейсы (endpoints):** arcgis:rest:services

Public cadastral map viewer of the Automated Information System of the State Land Cadastre (AIS GZK). Map services are exposed through a proxy rather than a full ArcGIS REST directory.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** низкий. Земельный / градостроительный кадастр. Публичная карта не равна открытой лицензии на коммерческую переработку кадастра.

**Обучение ИИ:** низкий. Кадастр и права на землю: персональные и режимные сведения. Не использовать для открытого обучения моделей без правового основания.

### Uralsk in development geoportal

- **id / uid:** `uralsksmartmapkz` / `cdi00002049`
- **URL:** https://uralsk.smartmap.kz
- **Тип:** геопортал
- **Статус:** неактивный
- **ПО:** SmartMap (`smartmap`)
- **Владелец:** Akimat of the city Uralsk — местная власть (акимат района / города)
- **Покрытие:** Западно-Казахстанская область (`KZ-27`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=unknown; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ, EN
- **Темы:** Regions and cities, Transport, Environment, Boundaries, Elevation, Imagery / Base Maps / Earth Cover, Inland Waters, Location
- **Интерфейсы (endpoints):** нет в реестре

Former Uralsk city-development geoportal on uralsk.smartmap.kz. The host currently returns HTTP 503 from the hosting control panel (August 2026).

**Агрегация в единый каталог/поиск:** нет. Каталог недоступен, машинная агрегация невозможна.

**Коммерческое использование:** нет. Источник не работает; коммерческое использование актуальных данных невозможно.

**Обучение ИИ:** нет. Источник недоступен.

### Committee on the legal statistics and special accounts ArcGIS Server (arcgis endpoint)

- **id / uid:** `giskgparcgisrestservices` / `cdi00013537`
- **URL:** https://gis.kgp.kz/arcgis/rest/services
- **Тип:** геопортал
- **Статус:** устаревший (дубль)
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** Committee on the legal statistics and special accounts of the state office of public prosecutor of Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=global; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Justice, legal system and public safety, Location
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap, arcgis:kmz

Duplicate ArcGIS REST alias of gis.kgp.kz (/arcgis vs /server). Use giskgpkz as the keeper record.

**Агрегация в единый каталог/поиск:** не использовать. Дублирующая точка входа; для агрегации брать основную запись.

**Коммерческое использование:** условный. Публичные ArcGIS REST-сервисы (rights_type=global). Технически слои открыты для чтения. Коммерческое включение в продукты упирается в отсутствие license_id и возможные ограничения владельца (нацкомпании, недропользователи, прокуратура).

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Archaeology.kz Heritage Map

- **id / uid:** `archaeologykz` / `temp00000010`
- **URL:** https://archaeology.kz/ru/heritages
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Archaeology.kz — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Population and society, Society
- **Интерфейсы (endpoints):** нет в реестре

Searchable national catalog and interactive map of archaeological and cultural heritage monuments across Kazakhstan, with regional and object-level records.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### HydroGOV Kazakhstan Water Resources Platform

- **id / uid:** `testgidrogharyshkz` / `temp00000026`
- **URL:** https://test-gidro.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Gharysh Geoportal Platform (`gharyshgeoportal`)
- **Владелец:** Ministry of Water Resources and Irrigation of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Live deployment of Kazakhstan’s interactive water-resources platform, integrating mapped water bodies, water-management basins, hydrological stations, reservoirs, dams, canals and other hydraulic infrastructure.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### JerKarta Returned State Land Map

- **id / uid:** `jerkartagharyshkz` / `temp00000022`
- **URL:** https://jerkarta.gharysh.kz/ru/map
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Ministry of Agriculture of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Planning / Cadastre
- **Интерфейсы (endpoints):** нет в реестре

Public interactive map and statistics portal showing land plots returned to state ownership across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakh Invest Interactive Map

- **id / uid:** `investgovkz` / `temp00000006`
- **URL:** https://invest.gov.kz/en/map/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** KAZAKH INVEST National Company JSC — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN, ZH
- **Темы:** Economy and finance, Regions and cities
- **Интерфейсы (endpoints):** custom:invest-projects, custom:investment-categories

National interactive investment map cataloging investment projects, industrial and special economic zones, infrastructure, natural resources and regional information across Kazakhstan.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: custom:invest-projects, custom:investment-categories. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Agricultural Land Quality Geoportal

- **id / uid:** `portalgiprozemkz` / `temp00000005`
- **URL:** https://portal.giprozem.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** State Institute for Land Survey Work — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Agriculture, fisheries, forestry and food, Farming
- **Интерфейсы (endpoints):** нет в реестре

National GIS portal for monitoring, analysis and accounting of agricultural land quality, including soil, geobotanical, agrochemical and cadastral assessment information.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Agricultural Satellite Monitoring Geoportal

- **id / uid:** `agrogharyshkz` / `temp00000017`
- **URL:** https://agro.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Ministry of Agriculture of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Farming
- **Интерфейсы (endpoints):** нет в реестре

Sectoral WebGIS presenting satellite monitoring of Kazakhstan agricultural land, including crop areas, crop classification and vegetation-condition assessments.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Emergency Situations Geoportal

- **id / uid:** `mchsgharyshkz` / `temp00000019`
- **URL:** https://mchs.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Ministry of Emergency Situations of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Environment
- **Интерфейсы (endpoints):** arcgis:rest:layer

Government WebGIS for emergency prevention, forecasting and monitoring using Earth-observation data, including hazard maps, incident information and emergency-response layers.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (arcgis:rest:layer), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Flood Monitoring Geoservice

- **id / uid:** `floodgharyshkz` / `temp00000020`
- **URL:** https://flood.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Committee for Water Resources of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Public geoinformation service for flood monitoring and water infrastructure, providing mapped information on reservoirs, dams, hydraulic structures and related flood-risk features.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Forest Resources Monitoring Geoportal

- **id / uid:** `forestgharyshkz` / `temp00000018`
- **URL:** https://forestopen.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Committee of Forestry and Wildlife of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Biota
- **Интерфейсы (endpoints):** нет в реестре

Government WebGIS presenting satellite-based monitoring of forest resources, burned areas, fire risk, logging and construction within the state forest fund.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Gharysh Sapary ArcGIS Server

- **id / uid:** `arcgisgharyshkz` / `temp00000001`
- **URL:** https://arcgis.gharysh.kz/server/rest/services
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Server (`arcgisserver`)
- **Владелец:** JSC National Company Kazakhstan Gharysh Sapary — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Location, Environment
- **Интерфейсы (endpoints):** arcgis:rest:info, arcgis:rest:services, arcgis:soap, arcgis:sitemap, arcgis:geositemap

Public ArcGIS Server catalog publishing national and thematic spatial services for emergency management, forestry, water, agriculture, land use and other domains.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:rest:services. Дополнительно есть OGC/картографические сервисы (arcgis:soap). Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan National Water Resources Information System

- **id / uid:** `qazsugovkz` / `temp00000007`
- **URL:** https://qazsu.gov.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Ministry of Water Resources and Irrigation of the Republic of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Environment, Inland waters
- **Интерфейсы (endpoints):** нет в реестре

National geospatial platform for searching, monitoring and managing Kazakhstan water resources, including rivers, lakes, canals, dams and other hydraulic infrastructure.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Pasture Monitoring Open Map

- **id / uid:** `pastureopengharyshkz` / `temp00000025`
- **URL:** https://pastureopen.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Kazakhstan Gharysh Sapary — государственное агентство / нацкомпания
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Farming
- **Интерфейсы (endpoints):** нет в реестре

Public WebGIS presenting satellite-monitoring data for pasture lands across Kazakhstan, with searchable layers and attribute tables.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Public Environmental Monitoring Map

- **id / uid:** `ecokartakz` / `temp00000009`
- **URL:** https://ecokarta.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Association of Environmental Organizations of Kazakhstan — некоммерческая организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Environment
- **Интерфейсы (endpoints):** sitemap

Interactive public environmental monitoring map cataloging regional environmental problems, industrial impacts, pollution indicators and government response measures across Kazakhstan.

**Агрегация в единый каталог/поиск:** ограниченный. Есть только вспомогательное обнаружение (sitemap/RSS). Для агрегации нужен разбор HTML или недокументированный фронтенд-API.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Tourism Routes and Attractions Map

- **id / uid:** `tourismonlinekz` / `temp00000012`
- **URL:** https://tourismonline.kz/maps
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Kazakh Tourism National Company JSC — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Regions and cities, Transport
- **Интерфейсы (endpoints):** нет в реестре

National interactive tourism geoportal cataloging 50 routes and hundreds of attractions, accommodation sites, transport terminals, service facilities and other points across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Unauthorized Land Occupation Monitoring Map

- **id / uid:** `geokgsopengharyshkz` / `temp00000023`
- **URL:** https://geokgsopen.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Kazakhstan Gharysh Sapary — государственное агентство / нацкомпания
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Planning / Cadastre
- **Интерфейсы (endpoints):** нет в реестре

Public satellite-monitoring WebGIS showing unauthorized occupation of land within populated areas across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Waste Monitoring Open Map

- **id / uid:** `wasteopengharyshkz` / `temp00000016`
- **URL:** https://wasteopen.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Ministry of Ecology and Natural Resources of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Environment
- **Интерфейсы (endpoints):** arcgis:rest:layer

Public WebGIS showing production and consumption waste sites identified through satellite monitoring, including licensed and unauthorized waste locations and their changes.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (arcgis:rest:layer), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Water Bodies Satellite Monitoring Open Map

- **id / uid:** `wateropengharyshkz` / `temp00000024`
- **URL:** https://wateropen.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Kazakhstan Gharysh Sapary — государственное агентство / нацкомпания
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Public WebGIS presenting satellite-monitoring data for Kazakhstan water bodies through searchable map layers and attribute tables.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan Water Resources Geoservice

- **id / uid:** `gidrogharyshkz` / `temp00000021`
- **URL:** https://gidro.gharysh.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Committee for Water Resources of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Inland Waters
- **Интерфейсы (endpoints):** нет в реестре

Government WebGIS for water resources and water bodies, publishing hydrological infrastructure and monitoring layers including reservoirs, dams, canals and water-protection boundaries.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazakhstan.travel Explore Map

- **id / uid:** `kazakhstantravel` / `temp00000028`
- **URL:** https://kazakhstan.travel/ru/explore
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Kazakh Tourism National Company — государственное агентство / нацкомпания
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Society
- **Интерфейсы (endpoints):** нет в реестре

Official national tourism catalog providing map and list discovery of destinations, attractions, routes and tour operators across Kazakhstan.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### KazGeo GeoServer

- **id / uid:** `kazgeokayakz` / `temp00000002`
- **URL:** https://kazgeo.kaya.kz/geoserver
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** GeoServer (`geoserver`)
- **Владелец:** KazGeo — прочее
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Location, Boundaries
- **Интерфейсы (endpoints):** wms111, wms130, wfs100, wfs110, wfs200

Public GeoServer catalog publishing Kazakhstan spatial layers used by the national spatial data infrastructure, including settlements, monuments, cemeteries and water-protection layers.

**Агрегация в единый каталог/поиск:** средний. Есть картографические сервисы (wfs100, wfs110, wfs200, wms111, wms130), но нет полноценного каталожного API (DCAT/CSW/OAI-PMH/пакетный REST). Слои можно подтянуть в геопоиск, но не как полноценный каталог наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Kazhydromet Interactive Maps and Databases

- **id / uid:** `wwwkazhydrometkz` / `temp00000013`
- **URL:** https://www.kazhydromet.kz/ru/interactive_cards
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** RSE Kazhydromet — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU
- **Темы:** Environment, Climatology, meteorology and atmosphere
- **Интерфейсы (endpoints):** нет в реестре

Catalog of Kazakhstan environmental monitoring maps and databases covering air quality, surface water, meteorology, hydrology, radiation and soil quality.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Minerals.AI ArcGIS Enterprise Portal

- **id / uid:** `mineralaikz` / `temp00000008`
- **URL:** https://mineral-ai.kz/portal/home/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Hub (`arcgishub`)
- **Владелец:** Minerals.AI Project — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Geology
- **Интерфейсы (endpoints):** arcgis:portals:self, arcgis:rest:search, arcgis:rest:services

Public ArcGIS Enterprise portal for viewing geological data, maps and modelling results produced by the Kazakhstan Minerals.AI research project.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: arcgis:portals:self, arcgis:rest:search, arcgis:rest:services. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Orman Forest Planting Monitoring Map

- **id / uid:** `ormangharyshkz` / `temp00000015`
- **URL:** https://orman.gharysh.kz/ru/map
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** ArcGIS Web AppBuilder (`webappbuilder`)
- **Владелец:** Kazakhstan Gharysh Sapary — государственное агентство / нацкомпания
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Biota
- **Интерфейсы (endpoints):** нет в реестре

Official public interactive map for monitoring forest planting across Kazakhstan, with layers for forestry institutions, compartments, planting areas, tree species, nurseries and implementation plans.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### OSMANOV.KZ Property and Land Map

- **id / uid:** `osmanovkz` / `temp00000011`
- **URL:** https://osmanov.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** OSMANOV.KZ — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU
- **Темы:** Regions and cities, Planning cadastre
- **Интерфейсы (endpoints):** sitemap

Public Kazakhstan property and land geoportal combining cadastral search with planning, red-line, water-protection, building and Almaty seismic layers from documented official sources.

**Агрегация в единый каталог/поиск:** ограниченный. Есть только вспомогательное обнаружение (sitemap/RSS). Для агрегации нужен разбор HTML или недокументированный фронтенд-API.

**Коммерческое использование:** низкий. Частный агрегатор кадастра и слоёв из официальных источников. Коммерция ограничена условиями сайта и правами первоисточников (ЕГКН и др.).

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Qazaqstan.Space Open Data and Atlas

- **id / uid:** `qazaqstanspace` / `temp00000004`
- **URL:** https://qazaqstan.space/data
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Qazaqstan.Space — прочее
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, EN
- **Темы:** Location, Environment
- **Интерфейсы (endpoints):** custom:data-index

Public geospatial data registry and interactive atlas for Kazakhstan, with documented layers, dataset indexes, provenance, freshness and machine-readable files.

**Агрегация в единый каталог/поиск:** высокий. Есть машиночитаемый каталожный/поисковый интерфейс: custom:data-index. Пригоден как источник для единого индекса при условии стабильности API и лицензионной проверки наборов.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Tabigat Interactive Natural Resources Map

- **id / uid:** `tabigatgovkz` / `temp00000029`
- **URL:** https://tabigat.gov.kz/
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Gharysh Geoportal Platform (`gharyshgeoportal`)
- **Владелец:** Ministry of Ecology and Natural Resources of Kazakhstan — центральное правительство
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** RU, KZ
- **Темы:** Environment, Biota
- **Интерфейсы (endpoints):** нет в реестре

Official interactive natural-resources map providing public geographic data about ecology, forests, wildlife, fisheries, protected areas, water resources, resort zones and related environmental themes.

**Агрегация в единый каталог/поиск:** низкий. Отраслевой WebGIS (ArcGIS Web AppBuilder / Gharysh). Публичный просмотр слоёв есть, но каталожный harvest в реестре не зафиксирован или неполный. Для агрегации нужен ArcGIS REST того же контура (часто gis.gharysh.kz / arcgis.gharysh.kz).

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### Ulytau Region Geoportal

- **id / uid:** `mapiulytaukz` / `temp00000003`
- **URL:** https://map.iulytau.kz
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Geonomics (`geonomics`)
- **Владелец:** Akimat of Ulytau Region — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Улытауская область (`KZ-62`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Regions and cities, Government and public sector
- **Интерфейсы (endpoints):** нет в реестре

Official geoportal of Ulytau Region, providing searchable regional maps, administrative features, land use, infrastructure, planning, environmental and public-service layers.

**Агрегация в единый каталог/поиск:** низкий. Стандартных harvest-интерфейсов в метаданных нет.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### VisitAqmola Tourist Geoportal

- **id / uid:** `wwwvisitaqmolakz` / `temp00000027`
- **URL:** https://www.visitaqmola.kz/ru/map
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Akmola Region Akimat — региональная власть (акимат области / города республиканского значения)
- **Покрытие:** Акмолинская область (`KZ-11`)
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Society
- **Интерфейсы (endpoints):** нет в реестре

Official multilingual tourist geoportal of Akmola Region, providing a searchable catalog and interactive map of attractions, accommodation, routes and tourism infrastructure.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

### WaterBalance Kazakhstan Open Geoportal

- **id / uid:** `waterbalanceorgkz` / `temp00000014`
- **URL:** https://waterbalance.org.kz/index_kz.html
- **Тип:** геопортал
- **Статус:** на проверке (не верифицирован)
- **ПО:** Custom software (`custom`)
- **Владелец:** Astana National Laboratory, Nazarbayev University — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** KZ, RU, EN
- **Темы:** Inland waters
- **Интерфейсы (endpoints):** нет в реестре

Open multilingual geoportal and spatial data catalog for hydrological analysis of Kazakhstan water basins, providing downloadable vector, raster and time-series datasets.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** не оценивать как продукт. Запись ещё не верифицирована. Не строить коммерческий контур на scheduled-каталоге до проверки ToS и стабильности.

**Обучение ИИ:** не подтверждён. Потенциал можно оценить только после верификации (есть ли выгрузка, не только карта).

## Приложение. Каталоги с покрытием Казахстана, владелец не в РК

Эти две записи не казахстанские по владельцу, но покрывают территорию РК и полезны в страновом обзоре.

### Электронный атлас Каспийского моря

- **id / uid:** `degeogrmsurucasp` / `cdi00041801`
- **URL:** http://de.geogr.msu.ru/casp/
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** Custom software (`custom`)
- **Владелец:** Географический факультет Московского государственного университета имени М. В. Ломоносова — академия / научная организация
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: False / uncertain
- **Права:** rights_type=не указан; license_id не задан
- **Национальный каталог типа:** нет
- **Языки:** RU
- **Темы:** Environment, Science and technology, Location, Oceans
- **Интерфейсы (endpoints):** нет в реестре

Public thematic atlas of the Caspian Sea and surrounding countries, published by the MSU Faculty of Geography with Russian Geographical Society support. Provides map collections and downloadable map PDFs covering climate, oceanography, hydrology, ecosystems, population, land use and environmental hazards.

**Агрегация в единый каталог/поиск:** низкий. Кастомный сайт/карта без зарегистрированных endpoints. Для единого каталога — только карточка источника, не автоматический harvest.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

### Central Asia and Caucasus GeoPortal

- **id / uid:** `cacgeoportalcom` / `cdi00004969`
- **URL:** https://www.cacgeoportal.com
- **Тип:** геопортал
- **Статус:** действующий
- **ПО:** ArcGIS Hub (`arcgishub`)
- **Владелец:** Esri — бизнес
- **Покрытие:** национальный / без субрегиона
- **Доступ:** open; API: True / active
- **Права:** rights_type=granular; license_id не задан
- **Национальный каталог типа:** не задан
- **Языки:** EN
- **Темы:** Location, Boundaries, Imagery / Base Maps / Earth Cover
- **Интерфейсы (endpoints):** dcatap201, dcatus11, rss, ogcrecordsapi, sitemap

Dedicated to empowering students, educators, and GIS professionals by providing free access to geospatial resources. Our mission is to enhance understanding and engagement in critical regional and global issues through the power of GIS technology.

**Агрегация в единый каталог/поиск:** ограниченный. Есть только вспомогательное обнаружение (sitemap/RSS). Для агрегации нужен разбор HTML или недокументированный фронтенд-API.

**Коммерческое использование:** условный. access_mode=open, но ни у одного казахстанского каталога в реестре не заполнены license_id / license_name. Коммерческое использование нельзя считать разрешённым «по умолчанию»: нужна проверка ToS портала и, для кадастра/недр/персональных данных, отраслевого режима.

**Обучение ИИ:** ограниченный. Открытый просмотр есть, но нет ни явной лицензии на обучение моделей, ни гарантированного bulk-доступа. Пригодно скорее как метаданные источника, чем как train set.

## Приложение. Источник и оговорки

- Источник: `data/datasets/datasets.duckdb`, `owner.location.country.id = 'KZ'` (118) плюс покрытие KZ при ином владельце (2).
- Экспорт может отставать от YAML; шесть scheduled-записей есть в DuckDB, но не в `data/entities/KZ/`.
- `status` — кураторский, не live-probe. Liveness отдельных хостов могла измениться после последней проверки.
- Оценки коммерции и ИИ — экспертные, не юридическое заключение. Перед продуктом проверять ToS, закон об информации РК и лицензию набора.
