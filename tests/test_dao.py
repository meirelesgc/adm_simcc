from adm_simcc.dao import Connection

test_adm_simcc = Connection(database="test_adm_simcc")


def test_db_is_created():
    registry = test_adm_simcc.select("SELECT 'STATUS OK'")
    assert registry == [("STATUS OK",)]


