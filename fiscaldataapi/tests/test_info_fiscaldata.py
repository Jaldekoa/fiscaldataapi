from fiscaldataapi import info_fiscaldata, __endpoints
import pandas as pd
import random
import pytest

db = random.choices(list(__endpoints.keys()), k=10)


@pytest.mark.parametrize("database", db)
def test_info_fiscaldata(database):
    df = info_fiscaldata(database)
    assert (isinstance(df, pd.DataFrame) and not df.empty)
