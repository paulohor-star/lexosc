CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE TABLE IF NOT EXISTS norms (
 id TEXT PRIMARY KEY, sphere TEXT NOT NULL CHECK (sphere IN ('federal','estadual','municipal','controle_externo')),
 uf CHAR(2), municipality_ibge CHAR(7), authority TEXT NOT NULL,
 norm_type TEXT NOT NULL, number TEXT NOT NULL, year INTEGER NOT NULL,
 title TEXT NOT NULL, publication_date DATE, applicability_notes TEXT,
 editorial_status TEXT NOT NULL DEFAULT 'nao_verificado' CHECK (editorial_status IN ('nao_verificado','em_revisao','verificado')),
 validity_status TEXT NOT NULL DEFAULT 'nao_verificada' CHECK (validity_status IN ('nao_verificada','vigente','revogada','parcialmente_revogada')),
 verification_date TIMESTAMPTZ, topics TEXT[] NOT NULL DEFAULT '{}', created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 UNIQUE(authority,norm_type,number,year)
);
CREATE TABLE IF NOT EXISTS sources (
 id BIGSERIAL PRIMARY KEY, norm_id TEXT NOT NULL REFERENCES norms(id) ON DELETE CASCADE,
 official_url TEXT NOT NULL, source_kind TEXT NOT NULL DEFAULT 'pagina_oficial',
 accessed_at TIMESTAMPTZ, http_status INTEGER, sha256 TEXT, snapshot_path TEXT,
 source_verified BOOLEAN NOT NULL DEFAULT FALSE, UNIQUE(norm_id,official_url)
);
CREATE TABLE IF NOT EXISTS norm_versions (
 id BIGSERIAL PRIMARY KEY, norm_id TEXT NOT NULL REFERENCES norms(id) ON DELETE CASCADE,
 valid_from DATE, valid_to DATE, captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 body_text TEXT, checksum_sha256 TEXT, review_status TEXT NOT NULL DEFAULT 'pendente',
 CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);
CREATE TABLE IF NOT EXISTS provisions (
 id BIGSERIAL PRIMARY KEY, version_id BIGINT NOT NULL REFERENCES norm_versions(id) ON DELETE CASCADE,
 locator TEXT NOT NULL, provision_type TEXT NOT NULL, parent_id BIGINT REFERENCES provisions(id),
 content TEXT NOT NULL, UNIQUE(version_id,locator)
);
CREATE TABLE IF NOT EXISTS norm_relations (
 id BIGSERIAL PRIMARY KEY, from_norm_id TEXT NOT NULL REFERENCES norms(id),
 to_norm_id TEXT NOT NULL REFERENCES norms(id), relation_type TEXT NOT NULL
 CHECK(relation_type IN ('regulamenta','altera','revoga','correlata')),
 official_evidence_url TEXT NOT NULL, review_status TEXT NOT NULL DEFAULT 'pendente',
 UNIQUE(from_norm_id,to_norm_id,relation_type)
);
CREATE INDEX IF NOT EXISTS idx_norms_topics ON norms USING GIN(topics);
CREATE INDEX IF NOT EXISTS idx_norms_title_trgm ON norms USING GIN(title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_provisions_content ON provisions USING GIN(to_tsvector('portuguese',content));
CREATE INDEX IF NOT EXISTS idx_versions_norm ON norm_versions(norm_id);
