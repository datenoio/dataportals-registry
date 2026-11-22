"""Characterization tests for dpr.geo.infer_country_from_link.

The expected values pin the behaviour of the version that promote_scheduled.py
used before the helper moved to dpr.geo (task 3.1 of the OpenSpec change
refactor-shared-script-library). hunt.py ingest and promotion depend on it.
"""

import pytest

from constants import COUNTRIES
import fix_important_issues
import promote_scheduled
from dpr.geo import infer_country_from_link


@pytest.mark.unit
@pytest.mark.parametrize(
    "link, expected",
    [
        ("https://data.gov.uk/dataset", "GB"),
        ("https://www.data.gov.au", "AU"),
        ("data.gov.sg", "SG"),
        ("https://catalog.data.gov", "US"),
        ("https://www.census.gov/data", "US"),
        ("https://www.trnava.sk", "SK"),
        ("https://opendata.paris.fr/explore", "FR"),
        ("https://data.europa.eu", "EU"),
        ("https://open.canada.ca/en", "CA"),
        ("https://dados.gov.br", "BR"),
        ("https://example.org", None),
        ("https://zenodo.org/communities/x", None),
        ("https://www.wider.unu.edu", None),
        ("", None),
        (None, None),
        ("not a url", None),
    ],
)
def test_infer_country_from_link(link, expected):
    assert infer_country_from_link(link) == expected


@pytest.mark.unit
def test_promote_scheduled_uses_shared_helper():
    assert promote_scheduled.infer_country_from_link is infer_country_from_link


@pytest.mark.unit
@pytest.mark.parametrize(
    "owner_link, code",
    [
        ("https://www.gov.uk/government/organisations/dsit", "GB"),
        # The old fix_important_issues.py table wrote "Ivory Coast" here,
        # not the registry name from constants.COUNTRIES.
        ("https://data.gov.ci", "CI"),
    ],
)
def test_fix_owner_location_uses_registry_country_names(owner_link, code):
    record = {
        "owner": {
            "name": "Ministry",
            "link": owner_link,
            "location": {"country": {"id": "Unknown", "name": "Unknown"}, "level": 0},
        },
        "coverage": [],
    }
    changed, message = fix_important_issues.fix_owner_location(record, "x.yaml")
    assert changed
    assert record["owner"]["location"]["country"] == {"id": code, "name": COUNTRIES[code]}
    assert record["owner"]["location"]["level"] == 20
    assert COUNTRIES[code] in message
