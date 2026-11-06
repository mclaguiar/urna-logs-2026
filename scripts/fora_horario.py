"""Votos do log no dia do turno, fora de 8h–17h de Brasília.

A hora usa o fuso estadual, o mesmo da curva do dia. O exterior fica de fora.
A abertura legal das 6h no oeste do Amazonas cai em 'antes das 8h' por esse fuso;
o grosso do 1º turno está na hora das 17h em diante.
"""

from pathlib import Path

import pandas as pd

from urna_logs.config import PROJECT_ROOT, data_turno
from urna_logs.fuso import delta_local_para_brt

RAIZ = PROJECT_ROOT / "data" / "anomalias" / "2026"
DESTINO = PROJECT_ROOT / "data" / "anomalias" / "fora_horario.csv"


def contar(turno: int) -> dict:
    dia = data_turno(turno, 2026).isoformat()
    antes = desde = 0
    secoes_antes: set[str] = set()
    secoes_desde: set[str] = set()
    for path in sorted(RAIZ.glob(f"tempos_*_{turno}t.parquet")):
        uf = path.name.split("_")[1]
        if uf == "ZZ":
            continue
        delta = delta_local_para_brt(uf) or 0
        frame = pd.read_parquet(path, columns=["join_key", "t"])
        texto = frame["t"].astype(str)
        no_dia = texto.str.slice(0, 10) == dia
        hora = texto.str.slice(11, 13).astype(int) + delta
        parte = frame.loc[no_dia]
        hora = hora.loc[no_dia]
        cedo = hora < 8
        tarde = hora >= 17
        antes += int(cedo.sum())
        desde += int(tarde.sum())
        secoes_antes.update(parte.loc[cedo, "join_key"])
        secoes_desde.update(parte.loc[tarde, "join_key"])
    return {
        "turno": turno,
        "secoes_antes_8": len(secoes_antes),
        "votos_antes_8": antes,
        "secoes_desde_17": len(secoes_desde),
        "votos_desde_17": desde,
    }


def main() -> None:
    frame = pd.DataFrame([contar(1), contar(2)])
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(DESTINO, index=False)
    print(frame.to_string(index=False))
    print(f"escrito {DESTINO}")


if __name__ == "__main__":
    main()
