from fiscaldataapi import get_fiscaldata, __endpoints
import pandas as pd
import pytest

db = list(__endpoints.keys())


@pytest.mark.parametrize("database", db)
def test_get_fiscaldata(database):
    df = get_fiscaldata(database)
    assert (isinstance(df, pd.DataFrame) and not df.empty)
