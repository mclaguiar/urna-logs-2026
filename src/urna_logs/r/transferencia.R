# Matriz de transferência por grupo de seções.
# Brown e Payne (1986): uma matriz, mínimos quadrados nas contagens, uma linha por seção.
# lphom, cenário simultaneous: a seção, até max_linhas linhas.
# Acima disso, soma as seções da mesma zona. O programa linear cresce com o quadrado das linhas.
# Args: entrada.csv saida.csv min_secoes max_linhas

args_lib <- Sys.getenv("R_LIBS_USER", unset = "")
if (!nzchar(args_lib)) {
  args_lib <- file.path(Sys.getenv("USERPROFILE"), "R", "win-library", "4.6")
}
dir.create(args_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(args_lib, .libPaths()))

suppressPackageStartupMessages({
  library(lphom)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) stop("uso: transferencia.R entrada.csv saida.csv min_secoes [max_linhas]")
entrada <- args[[1]]
saida <- args[[2]]
min_secoes <- as.integer(args[[3]])
max_linhas_lphom <- if (length(args) >= 4) as.integer(args[[4]]) else 2500L

df <- read.csv(entrada, stringsAsFactors = FALSE)
o_cols <- c("o_13", "o_22", "o_eliminados", "o_branco", "o_nulo", "o_abstencao")
d_cols <- c("d_13", "d_22", "d_branco", "d_nulo", "d_abstencao")
faltam <- setdiff(c(o_cols, d_cols, "municipio", "zona"), names(df))
if (length(faltam)) stop(paste("colunas ausentes:", paste(faltam, collapse = ", ")))
o_lab <- c("13", "22", "eliminados", "branco", "nulo", "abstencao")
d_lab <- c("13", "22", "branco", "nulo", "abstencao")

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

fit_brown_payne <- function(X, Y, seed) {
  set.seed(seed)
  sse <- function(P) sum((Y - X %*% P)^2)
  dest_share <- colSums(Y) / sum(Y)
  indep <- matrix(rep(dest_share, each = 6), nrow = 6)
  leal <- indep
  leal[1, ] <- c(1, 0, 0, 0, 0)
  leal[2, ] <- c(0, 1, 0, 0, 0)
  leal[4, ] <- c(0, 0, 1, 0, 0)
  leal[5, ] <- c(0, 0, 0, 1, 0)
  leal[6, ] <- c(0, 0, 0, 0, 1)
  starts <- list(indep, leal)
  for (k in seq_len(4)) {
    R <- matrix(rexp(30), 6, 5)
    starts[[length(starts) + 1]] <- R / rowSums(R)
  }
  best <- NULL
  for (P0 in starts) {
    opt <- optim(
      theta_from_P(P0),
      function(th) sse(softmax_P(th)),
      method = "BFGS",
      control = list(maxit = 300, reltol = 1e-10)
    )
    if (is.null(best) || opt$value < best$value) {
      best <- list(
        P = softmax_P(opt$par),
        theta = opt$par,
        value = opt$value,
        conv = opt$convergence
      )
    }
  }
  centro <- matrix(colMeans(Y), nrow(Y), 5, byrow = TRUE)
  best$r2 <- 1 - best$value / sum((Y - centro)^2)
  best$se <- erro_padrao_bp(best$theta, X, Y)
  best
}

erro_padrao_bp <- function(theta, X, Y) {
  vazio <- rep(NA_real_, 30)
  fn <- function(th) sum((Y - X %*% softmax_P(th))^2)
  opt <- tryCatch(
    optim(theta, fn, method = "BFGS", hessian = TRUE, control = list(maxit = 0)),
    error = function(e) NULL
  )
  if (is.null(opt) || is.null(opt$hessian)) return(vazio)
  H <- (opt$hessian + t(opt$hessian)) / 2
  ev <- eigen(H, symmetric = TRUE)
  positivo <- ev$values > 1e-8 * max(ev$values[1], 0)
  if (!any(positivo)) return(vazio)
  invH <- ev$vectors %*% diag(ifelse(positivo, 1 / ev$values, 0), length(ev$values)) %*% t(ev$vectors)
  P0 <- softmax_P(theta)
  resid <- Y - X %*% P0
  eps <- 1e-5
  S <- matrix(0, nrow(X), length(theta))
  for (k in seq_along(theta)) {
    th <- theta
    th[k] <- th[k] + eps
    dmu <- X %*% ((softmax_P(th) - P0) / eps)
    S[, k] <- rowSums(resid * (-dmu))
  }
  n <- nrow(X)
  meat <- (n / (n - 1)) * (t(S) %*% S)
  bread <- 2 * invH
  vtheta <- bread %*% meat %*% t(bread)
  G <- matrix(0, 30, length(theta))
  p0 <- as.vector(t(P0))
  for (k in seq_along(theta)) {
    th <- theta
    th[k] <- th[k] + eps
    G[, k] <- (as.vector(t(softmax_P(th))) - p0) / eps
  }
  se <- sqrt(pmax(diag(G %*% vtheta %*% t(G)), 0))
  se[!is.finite(se)] <- NA_real_
  # Célula presa em 0 ou 1: o intervalo normal não vale.
  se[p0 < 1e-3 | p0 > 1 - 1e-3] <- NA_real_
  se
}

fit_lphom <- function(X, Y) {
  lp <- lphom(
    votes_election1 = as.data.frame(X),
    votes_election2 = as.data.frame(Y),
    new_and_exit_voters = "simultaneous",
    integers = FALSE,
    verbose = FALSE
  )
  P <- as.matrix(lp$VTM)
  if (max(P) > 1.5) P <- P / 100
  if (!all(dim(P) == c(6, 5))) stop("dimensão ", paste(dim(P), collapse = "x"))
  P <- pmax(P, 0)
  P / rowSums(P)
}

somar_contagens <- function(sub, chave) {
  cols <- c(o_cols, d_cols)
  agg <- stats::aggregate(sub[cols], by = list(chave = chave), FUN = sum)
  agg[rowSums(agg[o_cols]) > 0, , drop = FALSE]
}

preparar_lphom <- function(sub) {
  n <- nrow(sub)
  if (n <= max_linhas_lphom) {
    return(list(dados = sub, grao = "secao", n_unidades = n))
  }
  chave_zona <- paste(sub$municipio, sub$zona, sep = ":")
  n_zona <- length(unique(chave_zona))
  if (n_zona > 1L && n_zona <= max_linhas_lphom) {
    dados <- somar_contagens(sub, chave_zona)
    return(list(dados = dados, grao = "zona", n_unidades = nrow(dados)))
  }
  n_mun <- length(unique(sub$municipio))
  if (n_mun > 1L && n_mun <= max_linhas_lphom) {
    dados <- somar_contagens(sub, as.character(sub$municipio))
    return(list(dados = dados, grao = "municipio", n_unidades = nrow(dados)))
  }
  bloco <- ceiling(seq_len(n) / ceiling(n / max_linhas_lphom))
  dados <- somar_contagens(sub, as.character(bloco))
  list(dados = dados, grao = "bloco", n_unidades = nrow(dados))
}

longo <- function(P, nivel, chave, modelo, n_secoes, r2, conv, grao, n_unidades, se, confianca) {
  taxa <- as.vector(t(P))
  if (length(se) != length(taxa)) se <- rep(NA_real_, length(taxa))
  z <- stats::qnorm(0.975)
  lo <- pmax(0, taxa - z * se)
  hi <- pmin(1, taxa + z * se)
  lo[is.na(se)] <- NA_real_
  hi[is.na(se)] <- NA_real_
  data.frame(
    nivel = nivel,
    municipio = chave,
    modelo = modelo,
    origem = rep(o_lab, each = 5),
    destino = rep(d_lab, times = 6),
    taxa = taxa,
    se = se,
    taxa_lo = lo,
    taxa_hi = hi,
    confianca = confianca,
    n_secoes = n_secoes,
    r2 = r2,
    convergencia = conv,
    grao = grao,
    n_unidades = n_unidades,
    stringsAsFactors = FALSE
  )
}

ajustar <- function(sub, nivel, chave) {
  X <- as.matrix(sub[o_cols])
  Y <- as.matrix(sub[d_cols])
  storage.mode(X) <- "double"
  storage.mode(Y) <- "double"
  prep <- preparar_lphom(sub)
  rotulo <- if (nivel == "estado") "estado" else paste("município", chave)
  cat(rotulo, nrow(sub), "seções", "lphom", prep$grao, prep$n_unidades, "\n")
  seed <- if (nivel == "estado") 20261030 else 20261030 + as.integer(chave)
  out <- list()
  bp <- tryCatch(fit_brown_payne(X, Y, seed), error = function(e) e)
  if (inherits(bp, "error")) {
    cat("Brown e Payne falhou", nivel, chave, conditionMessage(bp), "\n")
  } else {
    out[[length(out) + 1]] <- longo(
      bp$P, nivel, chave, "brown_payne", nrow(sub), bp$r2, bp$conv, "secao", nrow(sub),
      bp$se, 0.95
    )
  }
  Xl <- as.matrix(prep$dados[o_cols])
  Yl <- as.matrix(prep$dados[d_cols])
  storage.mode(Xl) <- "double"
  storage.mode(Yl) <- "double"
  lp <- tryCatch(fit_lphom(Xl, Yl), error = function(e) e)
  if (inherits(lp, "error")) {
    cat("lphom falhou", nivel, chave, conditionMessage(lp), "\n")
  } else {
    centro <- matrix(colMeans(Y), nrow(Y), 5, byrow = TRUE)
    r2 <- 1 - sum((Y - X %*% lp)^2) / sum((Y - centro)^2)
    out[[length(out) + 1]] <- longo(
      lp, nivel, chave, "lphom", nrow(sub), r2, NA, prep$grao, prep$n_unidades,
      NA_real_, NA_real_
    )
  }
  if (!length(out)) return(NULL)
  do.call(rbind, out)
}

partes <- list(ajustar(df, "estado", ""))
muns <- sort(unique(df$municipio))
for (mun in muns) {
  sub <- df[df$municipio == mun, , drop = FALSE]
  if (nrow(sub) < min_secoes) next
  partes[[length(partes) + 1]] <- ajustar(sub, "municipio", mun)
}
taxas <- do.call(rbind, partes)
write.csv(taxas, saida, row.names = FALSE, fileEncoding = "UTF-8")
cat("taxas", nrow(taxas), "->", saida, "\n")
