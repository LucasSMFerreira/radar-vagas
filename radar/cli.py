import argparse

from radar import banco
from radar.coletores import COLETORES


def main() -> None:
    parser = argparse.ArgumentParser(prog="radar")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_coletar = sub.add_parser("coletar", help="Coleta uma fonte e salva no banco")
    p_coletar.add_argument("fonte", choices=sorted(COLETORES))

    args = parser.parse_args()

    if args.comando == "coletar":
        vagas = COLETORES[args.fonte]()
        novas = banco.salvar_vagas(vagas)
        print(f"{args.fonte}: {len(vagas)} recebidas, {novas} novas")


if __name__ == "__main__":
    main()