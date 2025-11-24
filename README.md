# Pesquisa de Mestrado – Identidade PO 2.0

Este repositório contém os códigos e dados fictícios utilizados para replicar a metodologia da pesquisa de mestrado desenvolvida no Centro Paula Souza.

## Objetivo
Demonstrar a construção de dashboards analíticos para avaliação de competências do Product Owner (PO), incluindo gráficos (Radar, Termômetro), medidas DAX e configuração de segurança RLS.

## Estrutura do Repositório
```
/codigo-mestrado/
    ├── README.md                # Documentação do projeto
    ├── grafico_termometro.py    # Código Python para gráfico termômetro
    ├── medidas_dax.txt          # Medidas DAX utilizadas no Power BI
    ├── rls_configuracao.txt     # Lógica de segurança Row Level Security
    ├── dataset_replicavel.xlsx  # Base de dados fictícia para replicação
    ├── grafico_dispersao.py     # Código fonte do gráfico de dispersão
    
```

## Instruções para Replicação
1. Baixe o arquivo `dataset_ficticio.xlsx`.
2. Abra o Power BI e conecte-se ao arquivo.
3. Insira as medidas DAX do arquivo `medidas_dax.txt`.
4. Configure a segurança RLS conforme `rls_configuracao.txt`.
5. Execute o script Python `grafico_termometro.py` no visual Python do Power BI.

## Aviso de Compliance
Os dados originais foram anonimizados e substituídos por dados fictícios. Este repositório não contém informações sensíveis ou proprietárias da empresa Corpay.

## DOI
Será registrado no [Zenodo](https://zenodo.org/) para garantir referência acadêmica.
