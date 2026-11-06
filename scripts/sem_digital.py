"""Total de eleitores sem digital no boletim.

Sem digital = biografia + sem biometria. Brasil, sem o exterior.
A coluna das seções marcadas soma só as seções em que o percentual
se afastou das outras seções do mesmo local.
"""

from pathlib import Path

import pandas as pd

from urna_logs.config import PROJECT_ROOT

RAIZ = PROJECT_ROOT / "data" / "anomalias" / "2026"
DESTINO = PROJECT_ROOT / "data" / "anomalias" / "sem_digital.csv"


def main() -> None:
    alertas = pd.read_csv(
        PROJECT_ROOT / "data" / "anomalias" / "alertas.csv",
        usecols=["teste", "turno", "join_key"],
        low_memory=False,
    )
    marcadas = {
        turno: set(alertas[(alertas.teste == "sem_digital") & (alertas.turno == turno)].join_key)
        for turno in (1, 2)
    }
    linhas = []
    for turno in (1, 2):
        bio = sem = comp = nas = 0
        chaves = marcadas[turno]
        for path in sorted(RAIZ.glob(f"secao_*_{turno}t.parquet")):
            if path.name.split("_")[1] == "ZZ":
                continue
            df = pd.read_parquet(path, columns=["join_key", "biografia", "sem_biometria", "bu_comparecimento"])
            biografia = pd.to_numeric(df.biografia, errors="coerce").fillna(0)
            sem_bio = pd.to_numeric(df.sem_biometria, errors="coerce").fillna(0)
            total = biografia + sem_bio
            bio += int(biografia.sum())
            sem += int(sem_bio.sum())
            comp += int(pd.to_numeric(df.bu_comparecimento, errors="coerce").fillna(0).sum())
            nas += int(total[df.join_key.isin(chaves)].sum())
        linhas.append(
            {
                "turno": turno,
                "comparecimento": comp,
                "biografia": bio,
                "sem_biometria": sem,
                "votos_sem_digital": bio + sem,
                "votos_nas_secoes": nas,
                "secoes": len(chaves),
            }
        )
    frame = pd.DataFrame(linhas)
    frame.to_csv(DESTINO, index=False)
    print(frame.to_string(index=False))
    print(f"escrito {DESTINO}")


if __name__ == "__main__":
    main()
