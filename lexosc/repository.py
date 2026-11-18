"""Consultas SQL parametrizadas. Não interpreta vigência por inferência."""
from .db import connection

DISCLAIMER = 'Acervo inicial incompleto. Ausência de resultado não significa ausência de norma. Vigência deve ser conferida na fonte oficial.'

def buscar_normas(termo: str = '', esfera: str = '', uf: str = '', assunto: str = '', limite: int = 20):
    limite = max(1, min(limite, 50))
    filtros, parametros = [], []
    if termo:
        filtros.append('(n.title ILIKE %s OR n.number ILIKE %s OR n.authority ILIKE %s)')
        parametros.extend([f'%{termo}%'] * 3)
    if esfera:
        filtros.append('n.sphere = %s'); parametros.append(esfera)
    if uf:
        filtros.append('n.uf = %s'); parametros.append(uf.upper())
    if assunto:
        filtros.append('EXISTS (SELECT 1 FROM unnest(n.topics) t WHERE t ILIKE %s)'); parametros.append(f'%{assunto}%')
    where = ('WHERE ' + ' AND '.join(filtros)) if filtros else ''
    sql = f'''SELECT n.id,n.title,n.sphere,n.uf,n.authority,n.norm_type,n.number,n.year,
        n.editorial_status,n.validity_status,n.verification_date,n.topics,
        (SELECT s.official_url FROM sources s WHERE s.norm_id=n.id ORDER BY s.id LIMIT 1) AS fonte_oficial
        FROM norms n {where} ORDER BY n.year DESC,n.id LIMIT %s'''
    with connection() as db:
        rows = db.execute(sql, [*parametros, limite]).fetchall()
    return {'resultados': rows, 'total_retornado': len(rows), 'aviso': DISCLAIMER}

def consultar_norma(norm_id: str):
    with connection() as db:
        n = db.execute('SELECT * FROM norms WHERE id=%s', (norm_id,)).fetchone()
        if not n:
            return {'erro': 'Norma não cadastrada', 'aviso': DISCLAIMER}
        fontes = db.execute('SELECT official_url,source_verified,accessed_at,sha256 FROM sources WHERE norm_id=%s', (norm_id,)).fetchall()
        versoes = db.execute('SELECT id,valid_from,valid_to,review_status,body_text IS NOT NULL AS possui_texto FROM norm_versions WHERE norm_id=%s ORDER BY captured_at DESC', (norm_id,)).fetchall()
    return {'norma': n, 'fontes': fontes, 'versoes': versoes, 'aviso': DISCLAIMER}

def consultar_dispositivo(norm_id: str, localizador: str):
    with connection() as db:
        rows = db.execute('''SELECT p.locator,p.content,v.valid_from,v.valid_to,v.review_status,s.official_url
        FROM provisions p JOIN norm_versions v ON v.id=p.version_id
        LEFT JOIN LATERAL (SELECT official_url FROM sources WHERE norm_id=v.norm_id ORDER BY id LIMIT 1) s ON TRUE
        WHERE v.norm_id=%s AND p.locator=%s ORDER BY v.captured_at DESC LIMIT 10''', (norm_id,localizador)).fetchall()
    return {'dispositivos':rows,'aviso': DISCLAIMER if not rows else 'Confira a versão e vigência antes de aplicar o dispositivo.'}

def listar_relacoes(norm_id: str):
    with connection() as db:
        rows = db.execute('''SELECT from_norm_id,to_norm_id,relation_type,official_evidence_url,review_status
        FROM norm_relations WHERE from_norm_id=%s OR to_norm_id=%s ORDER BY relation_type''', (norm_id,norm_id)).fetchall()
    return {'relacoes':rows,'aviso':DISCLAIMER}

def verificar_vigencia(norm_id: str, data_referencia: str = ''):
    with connection() as db:
        n = db.execute('SELECT id,title,validity_status,editorial_status,verification_date FROM norms WHERE id=%s', (norm_id,)).fetchone()
        vs = db.execute('SELECT valid_from,valid_to,review_status FROM norm_versions WHERE norm_id=%s', (norm_id,)).fetchall()
    if not n: return {'erro':'Norma não cadastrada','aviso':DISCLAIMER}
    return {'norma': n,'versoes_documentadas':vs,'data_solicitada':data_referencia or None,
            'conclusao':'Não é possível atestar vigência com base apenas no catálogo inicial. Exige revisão documental da norma e alterações.',
            'aviso':DISCLAIMER}
