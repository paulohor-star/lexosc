"""Carga idempotente de catálogo: metadados não equivalem a texto integral validado."""
import json
from pathlib import Path
from .db import connection

def main():
    arquivo = Path(__file__).resolve().parents[1] / 'data' / 'catalogo_inicial.json'
    normas = json.loads(arquivo.read_text(encoding='utf-8'))
    with connection() as conn:
        with conn.cursor() as c:
            for n in normas:
                c.execute('''INSERT INTO norms (id,sphere,uf,authority,norm_type,number,year,title,topics)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET
                title=EXCLUDED.title,topics=EXCLUDED.topics''',
                (n['id'],n['sphere'],n.get('uf'),n['authority'],n['norm_type'],n['number'],n['year'],n['title'],n['topics']))
                c.execute('''INSERT INTO sources (norm_id,official_url) VALUES (%s,%s)
                ON CONFLICT (norm_id,official_url) DO NOTHING''',(n['id'],n['official_url']))
            # Relações documentadas por páginas oficiais; revisão jurídica continua pendente.
            relations = [
              ('BR-DEC-8726-2016','BR-LEI-13019-2014','regulamenta','https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8726.htm'),
              ('BR-DEC-11948-2024','BR-DEC-8726-2016','altera','https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/decreto/d11948.htm'),
              ('TCEPR-IN-61-2011','TCEPR-RES-28-2011','regulamenta','https://www.tce.pr.gov.br/conteudo/instrucao-normativa-n-61-de-1-de-dezembro-de-2011/237412/area/249/'),
              ('TCEPR-RES-140-2026','TCEPR-RES-28-2011','revoga','https://www.tce.pr.gov.br/noticias/tce-pr-inicia-por-foz-ciclo-de-capacitacao-sobre-nova-norma-relativa-a-transferencias.htm')]
            for r in relations:
                c.execute('''INSERT INTO norm_relations (from_norm_id,to_norm_id,relation_type,official_evidence_url)
                   VALUES (%s,%s,%s,%s) ON CONFLICT (from_norm_id,to_norm_id,relation_type) DO NOTHING''',r)
    print(f'Catálogo inicial: {len(normas)} normas referenciadas. Textos integrais não importados.')

if __name__ == '__main__': main()
