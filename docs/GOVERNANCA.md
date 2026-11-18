# Governança do acervo LexOSC

1. **Fonte primária**: o catálogo só aceita URLs oficiais de órgãos emissores; referências secundárias podem servir à descoberta, nunca à transcrição normativa certificada.
2. **Sem confirmação automática de vigência**: metadados iniciais usam `nao_verificada`; a marcação `vigente` exige análise de publicação, alterações, revogações e regras transitórias.
3. **Histórico imutável**: versões antigas e seus hashes devem ser preservados; nunca sobrescrever silenciosamente texto já publicado.
4. **Dispositivos**: importar apenas texto efetivamente recuperado da fonte; registrar versão, localizador e estado de revisão. Ausência de dispositivo não significa inexistência jurídica.
5. **Cobertura transparente**: registrar órgãos e períodos monitorados, última inspeção e eventuais falhas de coleta; catalogar não equivale a importar o texto integral.
6. **Licenças**: código sob MIT; direitos sobre textos, layout de portais, documentos e bases externas precisam de avaliação própria antes da republicação em massa.
7. **Segurança**: servidor demonstrativo sem autenticação não deve ser exposto diretamente à internet. Para API pública, aplicar gateway HTTPS, limitação de tráfego, controle de abuso, logs mínimos e revisão contra injeção de prompt nos documentos.
8. **Mudanças**: registrar quem validou e quando, com evidência de fonte, e estabelecer fila de revisão humana para conflito entre versões.
9. **Regime aplicável**: determinar natureza da entidade, instrumento, ente concedente, origem dos recursos e data relevante. Não inferir competência fiscalizatória apenas pela UF.
