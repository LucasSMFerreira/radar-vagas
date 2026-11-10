from radar.texto import limpar_html


def test_limpar_html():
    assert limpar_html("<p>Olá <b>mundo</b></p>") == "Olá mundo"