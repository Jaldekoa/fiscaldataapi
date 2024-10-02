from fiscaldataapi import get_fiscaldata, __endpoints
import pandas as pd
import random
import pytest

db = random.choices(list(__endpoints.keys()), k=5)


@pytest.mark.parametrize("database", db)
def test_get_fiscaldata(database):
    time.sleep(1)
    df = get_fiscaldata(database)
    assert (isinstance(df, pd.DataFrame) and not df.empty)
