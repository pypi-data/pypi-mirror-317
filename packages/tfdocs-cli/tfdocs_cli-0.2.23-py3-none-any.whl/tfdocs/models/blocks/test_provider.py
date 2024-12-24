import pytest
import logging
from unittest.mock import patch
from tfdocs.db.test_handler import MockDb
from tfdocs.models.blocks.provider import Provider

log = logging.getLogger()


class MockProvider(Provider):
    _db = MockDb()


@pytest.mark.parametrize(
    "case, exp",
    [
        ("registry.terraform.io/hashicorp/archive", "3c09cf2d1f63e6886c1ff5bd2a9fa49d"),
        ("registry.terraform.io/hashicorp/null", "b68b2e47df542636676cf4c527b75aa0"),
        ("registry.terraform.io/hashicorp/time", "85c7eb5ef45cc843ad01660e75695dce"),
    ],
)
def test_from_name(case, exp):
    subject = MockProvider.from_name(case)
    assert subject.id == exp


def test_list_providers():
    exp = {
        "registry.terraform.io/hashicorp/archive",
        "registry.terraform.io/hashicorp/null",
        "registry.terraform.io/hashicorp/time",
    }
    subjects = MockProvider.list_providers()
    assert {s.name for s in subjects} == exp


@pytest.mark.parametrize(
    "case, exp",
    {
        "85c7eb5ef45cc843ad01660e75695dce": {  # hashicorp/time's ID
            "79308e46475d463658c5e9bcd37ccfe2",  # time_offset Resource
            "1f3b97524b1efacbbd2b77679940710d",  # time_rotating Resource
            "8cbde6725c88f9474cf8acaf239114c7",  # time_sleep Resource
            "8f26c13e667a269ac45e8cd1909aaebf",  # time_static Resource
        },
        "3c09cf2d1f63e6886c1ff5bd2a9fa49d": {  # hashicorp/archive's ID
            "d56975289b6c16e3e49a10e308ef58c3",  # archive_file Resource
            "743e19765c5244e08afe83dca406e244",  # archive_file DataSource
        },
        "b68b2e47df542636676cf4c527b75aa0": {  # hashicorp/null's ID
            "e832cce309a19eb2d126e41ac2f54997",  # null_resource Resource
            "48052ad9e3ae785a9030b2c8628b6b54",  # null_data_source DataSource
        },
    }.items(),
)
def test_list_all(case, exp):
    subjects = MockProvider(type="Provider", hash=case).list_all()
    assert {s.id for s in subjects} == exp


@pytest.mark.parametrize(
    "case, exp",
    {
        "85c7eb5ef45cc843ad01660e75695dce": {  # hashicorp/time's ID
            "79308e46475d463658c5e9bcd37ccfe2",  # time_offset Resource
            "1f3b97524b1efacbbd2b77679940710d",  # time_rotating Resource
            "8cbde6725c88f9474cf8acaf239114c7",  # time_sleep Resource
            "8f26c13e667a269ac45e8cd1909aaebf",  # time_static Resource
        },
        "3c09cf2d1f63e6886c1ff5bd2a9fa49d": {  # hashicorp/archive's ID
            "d56975289b6c16e3e49a10e308ef58c3",  # archive_file Resource
        },
        "b68b2e47df542636676cf4c527b75aa0": {  # hashicorp/null's ID
            "e832cce309a19eb2d126e41ac2f54997",  # null_resource Resource
        },
    }.items(),
)
def test_list_resources(case, exp):
    subjects = MockProvider(type="Provider", hash=case).list_resources()
    assert {s[0] for s in subjects} == exp


@pytest.mark.parametrize(
    "case, exp",
    {
        "85c7eb5ef45cc843ad01660e75695dce": set(),  # hashicorp/time's ID
        "3c09cf2d1f63e6886c1ff5bd2a9fa49d": {  # hashicorp/archive's ID
            "743e19765c5244e08afe83dca406e244",  # archive_file DataSource
        },
        "b68b2e47df542636676cf4c527b75aa0": {  # hashicorp/null's ID
            "48052ad9e3ae785a9030b2c8628b6b54",  # null_data_source DataSource
        },
    }.items(),
)
def test_list_data_sources(case, exp):
    subjects = MockProvider(type="Provider", hash=case).list_datasources()
    assert {s[0] for s in subjects} == exp
