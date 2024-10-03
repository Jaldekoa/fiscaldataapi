from fiscaldataapi import info_fiscaldata, __endpoints
import random
import pytest
import time

db = random.choices(list(__endpoints.keys()), k=2)


@pytest.mark.parametrize("database", db)
def test_info_fiscaldata(database):
    time.sleep(1)
    data_format, total_pages, total_count = info_fiscaldata(database)
    assert isinstance(data_format, dict) and isinstance(total_pages, int) and isinstance(total_count, int)
