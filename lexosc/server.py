"""Servidor MCP de leitura: não afirma conclusões jurídicas sem fontes."""
from mcp.server.fastmcp import FastMCP
from . import repository as repo

mcp = FastMCP('LexOSC — Normas do Terceiro Setor', host='0.0.0.0', port=8000,
              stateless_http=True, json_response=True)

@mcp.tool()
def buscar_normas(termo: str = '', esfera: str = '', uf: str = '', assunto: str = '', limite: int = 20) -> dict:
    """Busca normas por identificação, esfera, UF e assunto. Acervo parcial, nunca presume inexistência."""
    return repo.buscar_normas(termo, esfera, uf, assunto, limite)

@mcp.tool()
def consultar_norma(norm_id: str) -> dict:
    """Retorna metadados, fonte oficial e disponibilidade de textos/versões de uma norma."""
    return repo.consultar_norma(norm_id)

@mcp.tool()
def consultar_dispositivo(norm_id: str, localizador: str) -> dict:
    """Consulta texto literal previamente importado e revisado, ex.: 'art. 1º'. Não inventa artigos."""
    return repo.consultar_dispositivo(norm_id, localizador)

@mcp.tool()
def listar_regulamentacoes(norm_id: str) -> dict:
    """Lista relações normativas cadastradas com link de evidência e estado de revisão."""
    return repo.listar_relacoes(norm_id)

@mcp.tool()
def consultar_normas_tce(uf: str = 'PR', termo: str = '', limite: int = 20) -> dict:
    """Pesquisa normas de controle externo de um estado (UF) no acervo disponível."""
    return repo.buscar_normas(termo=termo, esfera='controle_externo', uf=uf, limite=limite)

@mcp.tool()
def verificar_vigencia(norm_id: str, data_referencia: str = '') -> dict:
    """Apresenta os dados conhecidos sobre vigência, sem certificar períodos não revisados."""
    return repo.verificar_vigencia(norm_id, data_referencia)

if __name__ == '__main__':
    mcp.run(transport='streamable-http')
