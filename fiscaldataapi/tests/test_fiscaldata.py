from fiscaldataapi import get_fiscaldata, __endpoints
import pandas as pd
import pytest
import time

db = list(__endpoints.keys())


@pytest.mark.parametrize("database", db)
def test_get_fiscaldata(database):
    time.sleep(0.5)
    df = get_fiscaldata(database)
    assert (isinstance(df, pd.DataFrame) and not df.empty)
