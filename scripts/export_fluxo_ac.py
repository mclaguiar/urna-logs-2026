"""Margens balanceadas das seções do AC para os três modelos de transferência."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "reports" / "comparar_turnos_AC_1t_2t.parquet"
OUT = ROOT / "reports" / "fluxo_ac_margens.csv"

ORIGEM = {
    "o_13": "votos_fa_1t",
    "o_22": "votos_fb_1t",
    "o_elim": "votos_eliminados_1t",
    "o_branco": "branco_1t",
    "o_nulo": "nulo_1t",
    "o_abst": "abstencao_1t",
}
DESTINO = {
    "d_13": "votos_fa_2t",
    "d_22": "votos_fb_2t",
    "d_branco": "branco_2t",
    "d_nulo": "nulo_2t",
    "d_abst": "abstencao_2t",
}


def main() -> None:
    df = pd.read_parquet(SRC)
    df = df.loc[df["status"] == "ambos"].copy()
    out = df[["join_key", "municipio", "zona", "secao"]].copy()
    for nome, col in {**ORIGEM, **DESTINO}.items():
        out[nome] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(lower=0)
    so = out[list(ORIGEM)].sum(axis=1)
    sd = out[list(DESTINO)].sum(axis=1)
    n = so.combine(sd, max)
    out["ajuste_1t"] = (n - so).round(0)
    out["ajuste_2t"] = (n - sd).round(0)
    out["o_abst"] = out["o_abst"] + out["ajuste_1t"]
    out["d_abst"] = out["d_abst"] + out["ajuste_2t"]
    out["n"] = n
    out = out.loc[out["n"] > 0].copy()
    for col in list(ORIGEM) + list(DESTINO) + ["ajuste_1t", "ajuste_2t", "n"]:
        out[col] = out[col].round(0).astype(int)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"{len(out)} seções → {OUT}")
    print(
        "ajuste 1º",
        int((out["ajuste_1t"] != 0).sum()),
        "ajuste 2º",
        int((out["ajuste_2t"] != 0).sum()),
    )


if __name__ == "__main__":
    main()
