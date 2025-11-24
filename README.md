# Identidade PO – Pesquisa de Mestrado (Centro Paula Souza)

Este repositório contém **códigos, medidas DAX, regras de segurança e dados fictícios** para replicar a metodologia da pesquisa de mestrado que avalia competências de Product Owners (PO) e constrói dashboards analíticos no **Microsoft Power BI**.

---

## **Objetivo**
Permitir que qualquer pesquisador ou profissional replique:
- A modelagem dimensional da base de dados.
- As medidas DAX para cálculo de indicadores.
- A configuração de segurança **Row Level Security (RLS)**.
- A integração de scripts Python para gráficos customizados (Radar e Termômetro).

---

## **Estrutura do Repositório**
```
/codigo-mestrado/
    ├── README.md                # Este tutorial completo
    ├── dataset_replicavel.xlsx  # Base fictícia com estrutura idêntica à original
    ├── grafico_dispersao.py     # Código Python para gráfico dispersao
    ├── grafico_termometro.py    # Código Python para gráfico termômetro
    ├── medidas_dax.txt          # Medidas DAX utilizadas no Power BI
    ├── figura1.jpeg             # Exemplo de grafico de dispersao
    ├── figura2.jpeg             # Modelagem de dados e relacionamentos
```

---

## **Pré-requisitos**
1. **Microsoft Power BI Desktop**
   - Baixe em: [https://powerbi.microsoft.com/desktop](https://powerbi.microsoft.com/desktop)
   - Instale seguindo as instruções do site oficial.

2. **Python (para scripts no Power BI)**
   - Baixe em: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Durante a instalação, marque a opção **“Add Python to PATH”**.
   - Instale as bibliotecas necessárias:
     ```bash
     pip install matplotlib numpy pandas
     ```

---

## **Passo 1 – Conectar ao Dataset**
- Abra o **Power BI Desktop**.
- Clique em **Obter Dados > Excel**.
- Selecione o arquivo `dataset_replicavel.xlsx`.
- Carregue todas as tabelas (Dim_Pessoa, Dim_Habilidade, Dim_Resposta, Dim_Tribo, Dim_PO2, Fato_Avaliacao_Resumida, Fato_Avaliacao_Detalhada).

---

## **Passo 2 – Configurar Relacionamentos**
No **Gerenciador de Relacionamentos**:
- **Fato_Avaliacao_Detalhada[Id_Pessoa] → Dim_Pessoa[Id_Pessoa]**
- **Fato_Avaliacao_Detalhada[Id_Habilidade] → Dim_Habilidade[Id_Habilidade]**
- **Fato_Avaliacao_Detalhada[Id_Resposta] → Dim_Resposta[Id_Resposta]**
- **Fato_Avaliacao_Detalhada[Id_Tipo_Resposta] → Dim_Tipo_Resposta[Id_Tipo_Resposta]**
- **Dim_Pessoa[Id_Tribo] → Dim_Tribo[Id_Tribo]**
- **Dim_PO2[Id_Tribo] → Dim_Tribo[Id_Tribo]**

**Dica:** Configure a cardinalidade como **1:N** e a direção do filtro como **Ambos**.

---

## **Passo 3 – Criar Medidas DAX**
Copie as medidas do arquivo `medidas_dax.txt` e insira no Power BI:
- Vá em **Modelagem > Nova Medida**.
- Cole cada medida (ex.: `Final_Score`, `Classificação`, `Qtd_Consistente_Destaque_Fixo`, etc.).

Essas medidas calculam:
- Percentuais de respostas positivas.
- Médias por empresa, tribo e profissional.
- Classificação por faixa (Critical Gap, Gap, Medium, Strong).

---

## **Passo 4 – Configurar Segurança (RLS)**
- Vá em **Modelagem > Gerenciar Funções**.
- Crie uma função chamada **RLS_PO**
  ```DAX
  [Email_Corpay] = USERPRINCIPALNAME() || [Email_Fleetcor] = USERPRINCIPALNAME()
  ```
- Crie funções adicionais para **PO²** e **Executivos**.
- Publique no **Power BI Service** e atribua os usuários às funções na aba **Segurança**.

---

## **Passo 5 – Executar Código Python (Gráfico Dispersao)**
- No Power BI, insira um **Visual Python**.
- Copie o conteúdo do arquivo `grafico_dispersao.py`.
- Certifique-se de que o Python está configurado em **Arquivo > Opções > Scripts Python**.
- Execute o script para gerar o gráfico dispersao.

---

## **Passo 6 – Executar Código Python (Gráfico Termômetro)**
- No Power BI, insira um **Visual Python**.
- Copie o conteúdo do arquivo `grafico_termometro.py`.
- Certifique-se de que o Python está configurado em **Arquivo > Opções > Scripts Python**.
- Execute o script para gerar o gráfico termômetro.

---

## **Passo 7 – Publicar e Compartilhar**
- Salve o arquivo `.pbix`.
- Publique no **Power BI Service**.
- Configure permissões conforme as regras RLS.

---

## **Mockups e Diagramas**

- **Figura 1:** Exemplo do dashboard com gráficos dispersao.
- **Figura 2:** Estrutura dimensional do modelo de dados.

---

```
Franca, Phelipe Gomes Correia de. (2025). Identidade PO – Pesquisa de Mestrado. DOI: [inserir DOI]
```

---

## **Aviso de Compliance**
Todos os dados foram anonimizados. Nenhuma informação sensível da empresa Corpay foi incluída.
