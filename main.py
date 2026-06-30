import streamlit as str_visual
import base64
import os
from datetime import datetime
from streamlit_option_menu import option_menu
# CORREÇÃO 1: Importando o cliente do Supabase que estava faltando
from supabase import create_client, Client

# Configuração da página - Usando "wide" para aproveitar melhor o espaço como um site real
str_visual.set_page_config(layout="wide", page_title="MTS Roçagem", page_icon="🌱")

# 1. FUNÇÃO PARA LINKAR O SEU CSS
def linkar_css(nome_do_arquivo):
    if os.path.exists(nome_do_arquivo):
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            str_visual.markdown(f"<style>{arquivo.read()}</style>", unsafe_allow_html=True)

# Aplica as regras de estilo personalizadas
linkar_css("static/estilo.css")

# ---- CONFIGURAÇÃO DO BACKGROUND (FUNDO) ----
caminho_da_imagem = "static/fundo.jpg"
def pegar_fundo_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as arquivo:
            dados = arquivo.read()
        return base64.b64encode(dados).decode()
    return ""

fundo_base64 = pegar_fundo_base64(caminho_da_imagem)

# Aplica o fundo limpo e suave na aplicação se a imagem existir
if fundo_base64:
    str_visual.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{fundo_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# 2. CABEÇALHO / NAVBAR (MENU SUPERIOR)
# ==============================================================================
with str_visual.container(key="nav-menu"):
    # Criamos 2 colunas: Logo e Links do Menu
    col_logo, col_links = str_visual.columns([1, 1], vertical_alignment="center")
    
    with col_logo:
        # Texto simulando a logo profissional verde da imagem
        str_visual.markdown('<div class="logo-texto"> MTS ROÇAGEM</div><div class="logo-sub">SERVIÇOS PROFISSIONAIS</div>', unsafe_allow_html=True)
        
    with col_links:
      tab1, tab2, tab3 = str_visual.tabs(["Home", "Sobre", "Lista"])

with tab2:
  # ========================================================# CONEXÃO COM O BANCO DEDADOS (SUPABASE)=======================================================# Suas credenciais oficiais do projeto "Portal_Rocagem"
  SUPABASE_URL = str_visual.secrets["SUPABASE_URL"]
  SUPABASE_KEY = str_visual.secrets["SUPABASE_KEY"]

  # Inicializa o cliente do banco de dados na nuvem
  supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================================================
# CONFIGURAÇÃO DA INTERFACE DO USUÁRIO (STREAMLIT)
# ========================================================
  str_visual.title("🌱 Portal Roçagem Saquarema")
  str_visual.subheader("Olá Claudio! Testando o banco de dados com Streamlit")

# Formulário para organizar os campos na tela
  with str_visual.form("formulario_orcamento"):
    txt_nome = str_visual.text_input("Nome do Cliente", placeholder="Ex: Danilo")
    txt_whatsapp = str_visual.text_input("WhatsApp", placeholder="Ex: 229098807")
    txt_terreno = str_visual.number_input("Tamanho do Terreno (m²)", min_value=0, step=1)
    chk_lixo = str_visual.checkbox("Com retirada de lixo?")

    # Botão para disparar o cálculo e o envio
    btn_enviar = str_visual.form_submit_button("Calcular e Salvar no Banco")

  # ========================================================
  # LÓGICA DE PROCESSAMENTO E SALVAMENTO (Identado dentro da Tab2)
  # ========================================================
  if btn_enviar:
      # CORREÇÃO 2: Alterado de st.warning para str_visual.warning devido ao seu apelido do Streamlit
      if not txt_nome or not txt_whatsapp or txt_terreno == 0:
          str_visual.warning("⚠️ Por favor, preencha todos os campos do formulário!")
      else:
          try:
              # 1. Realiza o cálculo do orçamento (Ex: R$ 1,50 por m² + R$ 100 do lixo)
              valor_base = txt_terreno * 1.50
              adicional_lixo = 100.0 if chk_lixo else 0.0
              total_supabase = valor_base + adicional_lixo

              # 2. Insere os dados diretamente na tabela "orcamentos" do Supabase
              supabase.table("orcamentos").insert({
                  "nome_cliente": txt_nome,
                  "whatsapp": txt_whatsapp,
                  "tamanho_terreno": txt_terreno,
                  "com_retirada_lixo": chk_lixo,
                  "valor_total": total_supabase
              }).execute()

              # 3. Exibe mensagem de sucesso na tela com o valor calculado
              str_visual.success(f"✅ Sucesso! Orçamento de R$ {total_supabase:.2f} salvo no Supabase!")

          except Exception as erro:
              # Se houver algum erro de conexão, ele avisa na tela
              str_visual.error(f"❌ Erro ao conectar ou salvar no banco: {erro}")

# ==============================================================================
# 3. SEÇÃO HERO / BANNER PRINCIPAL
# ==============================================================================
# Criando um layout de duas colunas para o Banner (Texto gigante na esquerda, Imagem na direita)
col_banner_texto, col_banner_img = str_visual.columns([2, 2], vertical_alignment="center")

with col_banner_texto:
    str_visual.markdown("""
        <div class="hero-sessao">
            <p class="hero-tagline">ROÇAGEM PROFISSIONAL EM</p>
            <h1 class="hero-titulo">Saquarema,<br>Araruama e<br>São Vicente</h1>
            <p class="hero-descricao">Terrenos limpos, rápido e sem complicação.<br>Orçamento na hora e preço justo!</p>
        </div>
    """, unsafe_allow_html=True)
with col_banner_img:
    str_visual.image("static/banner_roçadeira.jpg", width=800)
      
    
# Botões de ação rápida abaixo do texto do banner
col_btn1, col_btn2 = str_visual.columns([1, 1], vertical_alignment="center")
with col_btn1:
    str_visual.markdown('<a href="#sistema-de-orçamento-por-metro-m" class="btn-solicitar"> Solicitar Orçamento</a>', unsafe_allow_html=True)
with col_btn2:
    str_visual.markdown('<a href="tel:22992356039" class="btn-telefone">📞 (22) 99235-6039</a>', unsafe_allow_html=True)
        
# Selos/Badges de benefícios
str_visual.markdown("""
        <div class="badges-container">
            <span class="badge">Atendimento rápido</span>
            <span class="badge"> Equipamentos professionals</span>
            <span class="badge"> Preço justo</span>
        </div>
    """, unsafe_allow_html=True)
    
str_visual.markdown("""<h2 class="titulo_do_meio">Empresa de Roçagem e Conservação de Terrenos e Jardins!</h2>""", unsafe_allow_html=True)


# ==============================================================================
# 4. QUADRADOS DE DIFERENCIAIS (OS 4 CARDS VERDES)
# ==============================================================================
str_visual.markdown('<div class="espacador"></div>', unsafe_allow_html=True)

card1, card2, card3, card4 = str_visual.columns(4)

with card1:
    str_visual.markdown('<div class="card-diferencial"><h3> Corte rápido</h3><p>Limpeza de terrenos com agilidade e qualidade total.</p></div>', unsafe_allow_html=True)
    str_visual.markdown("")
with card2:
    str_visual.markdown('<div class="card-diferencial"><h3> Mato alto</h3><p>Trabalhamos brutos com todos os tipos de vegetação.</p></div>', unsafe_allow_html=True)
    str_visual.markdown("")
with card3:
    str_visual.markdown('<div class="card-diferencial"><h3> Atendimento Local</h3><p>Atendemos Saquarema, Araruama e São Vicente.</p></div>', unsafe_allow_html=True)
    str_visual.markdown("")
with card4:
    str_visual.markdown('<div class="card-diferencial"><h3>Garantido</h3><p>Compromisso com a limpeza e satisfação do cliente.</p></div>', unsafe_allow_html=True)


# ==============================================================================
# 5. SISTEMA DE ORÇAMENTO ATUALIZADO (MODERNO)
# ==============================================================================
str_visual.markdown('<div class="espacador"></div>', unsafe_allow_html=True)

str_visual.markdown("""
    <div class="titulo-secao-container">
        <h2 class="titulo-secao">Sistema de Orçamento por metro (m²)</h2>
        <p class="subtitulo-secao">Preencha os dados abaixo e receba uma estimativa de preço na hora!</p>
    </div>
""", unsafe_allow_html=True)

# Bloco do formulário
with str_visual.container(key="formulario-orcamento-pagina"):
    # Dividindo os campos em 4 colunas horizontais
    f_col1, f_col2, f_col3, f_col4 = str_visual.columns(4)
    
    with f_col1:
        nome_cliente = str_visual.text_input("Qual seu nome?", placeholder="Digite seu nome")
    with f_col2:
        area_terreno = str_visual.number_input("Tamanho do terreno (m²):", min_value=0, value=0, step=50)
    with f_col3:
        tipo_mato = str_visual.selectbox("Tipo de mato:", ["Baixo", "Médio", "Alto"])
    with f_col4:
        dificuldade = str_visual.selectbox("Dificuldade do terreno:", ["Baixa (Plano)", "Média (Aclive/Declive)", "Alta (Pedras/Lixo)"])

    # Lógica de cálculo matemática
    preco_base = 1.50
    if tipo_mato == "Médio":
        preco_base = 2.50
    elif tipo_mato == "Alto":
        preco_base = 3.50
        
    # Adicional por dificuldade do terreno
    if dificuldade == "Média (Aclive/Declive)":
        preco_base += 0.50
    elif dificuldade == "Alta (Pedras/Lixo)":
        preco_base += 1.00
        
    total = area_terreno * preco_base

    str_visual.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Criando as colunas para o botão ficar organizado
    col_btn_calcular, col_vazia = str_visual.columns([1, 3])
    
    with col_btn_calcular:
        gerar_orcamento = str_visual.button("Calcular Orçamento", key="butao", use_container_width=True)


# ==============================================================================
# 6. RESULTADO DO ORÇAMENTO (DESIGN DE TABELA DA SEGUNDA IMAGEM)
# ==============================================================================
if gerar_orcamento:
    str_visual.markdown(f"""
        <div class="resultado-box">
            <h3 style="text-align: center; color: #14532d; margin-bottom: 20px;">Resultado do Orçamento</h3>
            <div class="resultado-grid">
                <div class="res-item"><strong> Cliente:</strong><br>{nome_cliente if nome_cliente else "Não informado"}</div>
                <div class="res-item"><strong> Área:</strong><br>{area_terreno} m²</div>
                <div class="res-item"><strong> Tipo de Mato:</strong><br>{tipo_mato}</div>
                <div class="res-item valor-destaque"><strong> Valor Estimado:</strong><br>R$ {total:.2f}</div>
            </div>
            <p class="aviso-orcamento"> Este é um valor estimado. Para o orçamento final e agendamento, entre em contato conosco!</p>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 7. RODAPÉ (FOOTER PROFISSIONAL)
# ==============================================================================
str_visual.markdown('<div class="espacador"></div>', unsafe_allow_html=True)
str_visual.markdown("""
    <div class="footer-completo">
        <div class="footer-grid">
            <div class="footer-col">
                <h3> MTS ROÇAGEM</h3>
                <p>Serviços profissionais de roçagem e limpeza de terrenos em Saquarema, Araruama e São Vicente.</p>
            </div>
            <div class="footer-col">
                <h3> Contato</h3>
                <p>WhatsApp: (22) 99235-6039<br>Atendimento: Seg a Sáb - 07:00 às 18:00</p>
            </div>
        </div>
        <hr style="border-color: #2b8a3e; margin: 20px 0;">
        <p style="text-align: center; font-size: 12px; color: #a3e635;">© 2026 MTS Roçagem. Desenvolvido no Termux. Todos os direitos reservados.</p>
    </div>
""", unsafe_allow_html=True)
