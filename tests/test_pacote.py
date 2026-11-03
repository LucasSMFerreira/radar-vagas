import radar


def test_pacote_tem_versao():
    assert radar.__version__.count(".") == 2