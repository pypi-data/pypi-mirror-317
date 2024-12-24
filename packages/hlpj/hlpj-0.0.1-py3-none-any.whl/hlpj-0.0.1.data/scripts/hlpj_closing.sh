#!/bin/bash
# -*- mode: sh; sh-shell: bash; -*-
set -e

YEAR_CLOSING="${1?:Informe o ano}"
YEAR_OPENING="$((YEAR_CLOSING + 1))"

DIR="${2?:Informe dir}"
TXNS_DIR="$DIR/transacoes"
STAGING_DIR="$DIR/new_txns"

CURRENT_JOURNAL_CLOSING="$TXNS_DIR/$YEAR_CLOSING.journal"
CURRENT_JOURNAL_OPENING="$TXNS_DIR/$YEAR_OPENING.journal"

TMP_JOURNAL_CLOSING="$(mktemp --suffix=.journal)"
TMP_JOURNAL_OPENING="$(mktemp --suffix=.journal)"

STAGING_JOURNAL_CLOSING="$STAGING_DIR/$YEAR_CLOSING.journal"
STAGING_JOURNAL_OPENING="$STAGING_DIR/$YEAR_OPENING.journal"

DIRECTIVES_END='; end_directives'


echo "Verificando arquivos"
if [ -f "$CURRENT_JOURNAL_OPENING" ]; then
  read -rp "Erro: Ano seguinte existente. Continua (y/n)?" answer
  [ "$answer" != "y" ] && exit 1
fi

if ! grep "$DIRECTIVES_END" "$CURRENT_JOURNAL_CLOSING" > /dev/null; then
    echo "Erro: Falta $DIRECTIVES_END no ano anterior"
    exit 1
fi

echo "Verificando se há transacoes do ano anterior"
if [ "$(hledger -f "$CURRENT_JOURNAL_CLOSING" print --unmarked -e "$YEAR_CLOSING-01-01")" != "" ]; then
  echo "Erro: Há transacoes antes do ano anterior"
  exit 1
fi

echo "Verificacao ok"

echo "Iniciando new dir"
[ -d "$STAGING_DIR" ] && rm -r "$STAGING_DIR"
mkdir -p "$STAGING_DIR"
cp -r "$DIR/transacoes/." "$STAGING_DIR" 


echo "Iniciando com directives"
sed "/$DIRECTIVES_END/G; /$DIRECTIVES_END/q" "$CURRENT_JOURNAL_CLOSING" \
    > "$STAGING_JOURNAL_CLOSING"

cp "$STAGING_JOURNAL_CLOSING" \
   "$STAGING_JOURNAL_OPENING"  # Tanto ano anterior quanto ano atual devem ter DIRECTIVES

echo "Adicionando somente confirmadas em ano anterior"
hledger -f "$CURRENT_JOURNAL_CLOSING" \
	print --unmarked \
	-p "$YEAR_CLOSING" \
	>> "$STAGING_JOURNAL_CLOSING"

echo "Copiando pendentes em ano atual"
hledger -f "$CURRENT_JOURNAL_CLOSING" \
	print --pending \
	>> "$STAGING_JOURNAL_OPENING"

echo "Copiando confirmadas posterior para ano atual"
hledger -f "$CURRENT_JOURNAL_CLOSING" \
	print --unmarked \
	-b "$YEAR_OPENING-01-01" \
	>> "$STAGING_JOURNAL_OPENING"


# Fechamento Lucro
echo -e "\nFechando Lucros Acumulados do ano anterior"
hledger -f "$STAGING_JOURNAL_CLOSING" close  \
	--retain \
	--close-desc "#closing# Fechamento de Lucros Acumulados" \
	--close-acct "Patrimonio Liquido:Lucros Acumulados" \
	--unmarked --explicit \
	-e "$YEAR_OPENING" \
  | sed 's/=.*//' \
  | tee -a "$STAGING_JOURNAL_CLOSING"


# Fechamento de Balanco
echo -e "\nFechando Balanco Ano Anterior"
hledger -f "$STAGING_JOURNAL_CLOSING" close \
	--close \
	--close-desc "#closing# Fechamento de Balanco" \
	--close-acct "Patrimonio Liquido:Abertura/Fechamento de Balanco" \
	--unmarked --explicit \
	-e "$YEAR_OPENING" \
  | sed 's/=.*//' \
  | tee -a "$TMP_JOURNAL_CLOSING"

echo -e "\nAbrindo Balanco Ano Atual"
hledger -f "$STAGING_JOURNAL_CLOSING" close \
	--open \
	--open-desc "#closing# Abertura de Balanco" \
	--open-acct "Patrimonio Liquido:Abertura/Fechamento de Balanco"  \
	--unmarked --explicit \
	-e "$YEAR_OPENING" \
  | sed 's/=.*//' \
  | tee -a "$TMP_JOURNAL_OPENING"


cat "$TMP_JOURNAL_CLOSING" >> "$STAGING_JOURNAL_CLOSING"
cat "$TMP_JOURNAL_OPENING" >> "$STAGING_JOURNAL_OPENING"
