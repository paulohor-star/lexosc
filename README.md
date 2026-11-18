# LexOSC — Repositório Nacional de Normas do Terceiro Setor

Protótipo público e aberto de consulta a referências normativas federais e do TCE-PR via **Model Context Protocol (MCP)**, em Python + PostgreSQL.

> **Estado atual:** catálogo inicial com referências e relações normativas. **Não contém texto integral importado, consolidação jurídica, nem verificação automática de vigência.** Não use como atestado de situação legal. A ausência de resultados não significa ausência de norma.

## Estrutura

- `sql/001_init.sql`: banco relacional (normas, fontes, versões, dispositivos e relações).
- `data/catalogo_inicial.json`: nove referências iniciais de legislação federal e TCE-PR.
- `lexosc/seed.py`: importação idempotente dos metadados.
- `lexosc/repository.py`: consultas parametrizadas ao PostgreSQL.
- `lexosc/server.py`: seis ferramentas MCP de leitura.
- `docs/GOVERNANCA.md`: critérios editoriais, controles e limites.

## Executar (Docker Compose)

Requisitos: Docker com Compose.

```bash
cp .env.example .env
# Edite .env: troque a senha e use o mesmo valor em DATABASE_URL se executar fora do Docker.
docker compose up -d --build
docker compose exec mcp python -m lexosc.seed
```

Servidor MCP local: `http://127.0.0.1:8000/mcp` (Streamable HTTP).

Para visualizar os dados:
```bash
docker compose exec db psql -U lexosc -d lexosc -c 'SELECT id,title,validity_status FROM norms ORDER BY id;'
```

Para atualizar o esquema depois da primeira inicialização, use uma migração explícita. O SQL de `docker-entrypoint-initdb.d` só roda na criação inicial do volume.

## Consultas MCP

`buscar_normas`, `consultar_norma`, `consultar_dispositivo`, `listar_regulamentacoes`, `consultar_normas_tce`, `verificar_vigencia`.

Na versão 0.1, `consultar_dispositivo` não terá resultados: isso é **intencional** até que o processo de coleta + revisão importe versões e artigos completos.

Exemplos de parâmetros:
- `buscar_normas({"termo":"13.019"})` pode não encontrar a pontuação, pois os números são normalizados; use `{"termo":"13019"}`.
- `consultar_normas_tce({"uf":"PR","termo":"transferências"})`.
- `consultar_norma({"norm_id":"TCEPR-RES-140-2026"})`.

## Próximos marcos

1. Verificador automatizado de URL oficial (HTTP, SHA-256, snapshot e trilha de auditoria).
2. Importadores separados por fonte (Planalto, TCE-PR), com respeito às condições de acesso.
3. Extração e revisão humana de texto integral e artigos.
4. Busca textual de dispositivos, vigência temporal e testes jurídicos documentados.
5. Gateway público HTTPS com limites e observabilidade; então conectar ao ChatGPT.

## Publicar no GitHub

Crie um repositório público vazio `lexosc` e execute dentro desta pasta:

```bash
git init
git add .
git commit -m "feat: estrutura inicial LexOSC"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/lexosc.git
git push -u origin main
```

Não publique senhas reais, `.env`, dados pessoais ou extrações sem avaliar licença e condições dos sites.

## Licença

Código do projeto: MIT (`LICENSE`). Normas oficiais e materiais de terceiros não são automaticamente abrangidos pela licença do código.

## Testes estáticos

```bash
python -m unittest discover -s tests -v
python -m compileall -q lexosc
```

**Limite da validação atual:** testes de catálogo e compilação passaram durante a preparação; o servidor MCP e a conexão PostgreSQL dependem de execução em ambiente com Docker ou PostgreSQL.
