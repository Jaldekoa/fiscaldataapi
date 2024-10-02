from fiscaldataapi import info_fiscaldata, __endpoints
import pandas as pd
import random
import pytest

db = random.choices(list(__endpoints.keys()), k=5)


@pytest.mark.parametrize("database", db)
def test_info_fiscaldata(database):
    data_format, total_pages, total_count = info_fiscaldata(database)
    assert isinstance(data_format, dict) and isinstance(total_pages, int) and isinstance(total_count, int)
