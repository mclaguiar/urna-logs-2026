# Três estimadores publicados da matriz de transferência, só no AC.
# Brown e Payne (1986): matriz homogênea, mínimos quadrados nas contagens.
# Rosen, Jiang, King e Tanner (2001): ei.MD.bayes do pacote eiPack.
# lphom (Pavía), cenário simultaneous: dois turnos com o mesmo total por seção.

args_lib <- Sys.getenv("R_LIBS_USER", unset = "")
if (!nzchar(args_lib)) {
  args_lib <- file.path(Sys.getenv("USERPROFILE"), "R", "win-library", "4.6")
}
dir.create(args_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(args_lib, .libPaths()))

need <- c("lphom", "eiPack")
missing <- need[!vapply(need, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  install.packages(missing, repos = "https://cloud.r-project.org")
}
library(lphom)
library(eiPack)

cmd <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", cmd, value = TRUE)
script_dir <- dirname(normalizePath(sub("^--file=", "", file_arg[[1]])))
root <- normalizePath(file.path(script_dir, ".."), winslash = "/")
csv <- file.path(root, "reports", "fluxo_ac_margens.csv")
md_path <- file.path(root, "reports", "fluxo_modelos_AC.md")

df <- read.csv(csv, stringsAsFactors = FALSE)
o_cols <- c("o_13", "o_22", "o_elim", "o_branco", "o_nulo", "o_abst")
d_cols <- c("d_13", "d_22", "d_branco", "d_nulo", "d_abst")
o_lab <- c("13", "22", "Eliminados", "Branco", "Nulo", "Abstenção")
d_lab <- c("13", "22", "Branco", "Nulo", "Abstenção")
X <- as.matrix(df[o_cols])
Y <- as.matrix(df[d_cols])
storage.mode(X) <- "double"
storage.mode(Y) <- "double"

softmax_P <- function(theta) {
  M <- matrix(theta, nrow = 6, ncol = 4)
  P <- matrix(0, 6, 5)
  for (i in seq_len(6)) {
    e <- exp(pmin(M[i, ], 20))
    s <- sum(e) + 1
    P[i, 1:4] <- e / s
    P[i, 5] <- 1 / s
  }
  P
}

theta_from_P <- function(P) {
  P <- pmax(P, 1e-8)
  P <- P / rowSums(P)
  as.vector(log(P[, 1:4] / P[, 5]))
}

sse <- function(P) sum((Y - X %*% P)^2)

fit_brown_payne <- function() {
  dest_share <- colSums(Y) / sum(Y)
  indep <- matrix(rep(dest_share, each = 6), nrow = 6)
  leal <- indep
  leal[1, ] <- c(1, 0, 0, 0, 0)
  leal[2, ] <- c(0, 1, 0, 0, 0)
  leal[4, ] <- c(0, 0, 1, 0, 0)
  leal[5, ] <- c(0, 0, 0, 1, 0)
  leal[6, ] <- c(0, 0, 0, 0, 1)
  starts <- list(indep, leal)
  set.seed(20261030)
  for (k in seq_len(6)) {
    R <- matrix(rexp(30), 6, 5)
    starts[[length(starts) + 1]] <- R / rowSums(R)
  }
  best <- NULL
  for (P0 in starts) {
    opt <- optim(
      theta_from_P(P0),
      function(th) sse(softmax_P(th)),
      method = "BFGS",
      control = list(maxit = 400, reltol = 1e-12)
    )
    P <- softmax_P(opt$par)
    if (is.null(best) || opt$value < best$value) {
      best <- list(P = P, value = opt$value, conv = opt$convergence)
    }
  }
  sst <- sum((Y - matrix(colMeans(Y), nrow(Y), 5, byrow = TRUE))^2)
  best$r2 <- 1 - best$value / sst
  best
}

fmt_pct <- function(P) {
  shown <- round(100 * P, 1)
  apply(shown, 1, function(row) paste(sprintf("%.1f", row), collapse = " | "))
}

linha_md <- function(nome, P) {
  paste0("| ", nome, " | ", paste(fmt_pct(P), collapse = " |\n|  | "), " |")
}

pred_secao <- function(P, i) {
  as.vector(X[i, ] %*% P)
}

cat("Brown e Payne...\n")
bp <- fit_brown_payne()

cat("lphom...\n")
lp <- lphom(
  votes_election1 = as.data.frame(X),
  votes_election2 = as.data.frame(Y),
  new_and_exit_voters = "simultaneous",
  integers = FALSE,
  verbose = FALSE
)
P_lp <- as.matrix(lp$VTM) / 100
if (!all(dim(P_lp) == c(6, 5))) {
  stop("lphom devolveu dimensão ", paste(dim(P_lp), collapse = "x"))
}

cat("RxC ei.MD.bayes...\n")
rxc <- ei.MD.bayes(
  cbind(d_13, d_22, d_branco, d_nulo, d_abst) ~
    cbind(o_13, o_22, o_elim, o_branco, o_nulo, o_abst),
  data = df,
  sample = 400,
  burnin = 400,
  thin = 1,
  verbose = 0,
  ret.beta = "d",
  ret.mcmc = FALSE
)
cells <- rxc$draws$Cell.count
if (is.null(dim(cells))) stop("eiPack não devolveu Cell.count")
origens <- colSums(X)
# array R x C x sample, ou matriz (R*C) x sample
if (length(dim(cells)) == 3) {
  fluxo <- apply(cells, c(1, 2), mean)
} else {
  medias <- rowMeans(cells)
  cand <- list(
    matrix(medias, nrow = 6, ncol = 5),
    matrix(medias, nrow = 6, ncol = 5, byrow = TRUE)
  )
  erro <- vapply(cand, function(M) sum((rowSums(M) - origens)^2), numeric(1))
  fluxo <- cand[[which.min(erro)]]
}
cat(
  "RxC somas de linha", paste(round(rowSums(fluxo)), collapse = " "),
  " origens", paste(round(origens), collapse = " "), "\n"
)
P_rx <- fluxo / origens
P_rx <- P_rx / rowSums(P_rx)

idx <- which(df$municipio == 1120 & df$zona == 8 & df$secao == 8)
if (length(idx) != 1) stop("seção de Acrelândia não encontrada")
i <- idx[[1]]

bloco <- function(titulo, P) {
  pred <- pred_secao(P, i)
  real <- Y[i, ]
  c(
    paste0("### ", titulo),
    "",
    "| Origem no 1º | 13 | 22 | Branco | Nulo | Abstenção |",
    "|---|---:|---:|---:|---:|---:|",
    paste0(
      mapply(
        function(lab, k) {
          sprintf(
            "| %s | %s |",
            lab,
            paste(sprintf("%.1f", 100 * P[k, ]), collapse = " | ")
          )
        },
        o_lab,
        seq_along(o_lab)
      ),
      collapse = "\n"
    ),
    "",
    sprintf(
      "Acrelândia, zona 8, seção 8. Votos previstos no 2º turno por esta taxa: 13 = %.1f, 22 = %.1f, branco = %.1f, nulo = %.1f, abstenção = %.1f.",
      pred[1], pred[2], pred[3], pred[4], pred[5]
    ),
    sprintf(
      "Totais observados nessa seção: 13 = %.0f, 22 = %.0f, branco = %.0f, nulo = %.0f, abstenção = %.0f.",
      real[1], real[2], real[3], real[4], real[5]
    ),
    ""
  )
}

r2_lp <- 1 - sse(P_lp) / sum((Y - matrix(colMeans(Y), nrow(Y), 5, byrow = TRUE))^2)
r2_rx <- 1 - sse(P_rx) / sum((Y - matrix(colMeans(Y), nrow(Y), 5, byrow = TRUE))^2)

linhas <- c(
  "# Transferência 1º→2º — AC",
  "",
  sprintf(
    "Seções nos dois turnos: **%s**. O total de cada seção foi fechado na abstenção quando os dois turnos não batiam (%s seções no 1º, %s no 2º).",
    format(nrow(df), big.mark = "."),
    format(sum(df$ajuste_1t != 0), big.mark = "."),
    format(sum(df$ajuste_2t != 0), big.mark = ".")
  ),
  "",
  "As células são a taxa, em %, de quem votou na origem no 1º turno e foi para aquele destino no 2º. Cada linha soma 100.",
  "",
  sprintf(
    "Ajuste aos totais do 2º turno no estado (R² das contagens): Brown e Payne **%.3f**, lphom **%.3f**, R×C **%.3f**.",
    bp$r2, r2_lp, r2_rx
  ),
  "",
  bloco("Brown e Payne (1986), matriz única", bp$P),
  bloco("lphom, cenário simultaneous", P_lp),
  bloco("R×C, ei.MD.bayes (Rosen, Jiang, King e Tanner, 2001)", P_rx),
  "## O que a seção de Acrelândia obriga",
  "",
  "Intervalo de Duncan–Davis, sem modelo: dos 32 do 13, entre 0 e 32 podem ter ficado no 13. Dos 130 do 22 para o 13, entre 0 e 34. Dos 130 do 22 para o 22, entre 39 e 123.",
  "",
  sprintf("Convergência do mínimos quadrados: código %s.", bp$conv),
  ""
)
writeLines(linhas, md_path, useBytes = TRUE)
saveRDS(
  list(brown_payne = bp$P, lphom = P_lp, rxc = P_rx, r2 = c(bp = bp$r2, lphom = r2_lp, rxc = r2_rx)),
  file.path(root, "reports", "fluxo_modelos_AC.rds")
)
cat("relatório:", md_path, "\n")
