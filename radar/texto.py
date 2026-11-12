from bs4 import BeautifulSoup


def limpar_html(html: str) -> str:
    """Tira as tags HTML e junta os espaços."""
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)