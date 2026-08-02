import urllib.parse
import flet as ft

WHATSAPP_NUMERO = "5522992356039"

PRECO_POR_M2 = {
    "Mato Baixo": 1.50,
    "Mato Médio": 2.00,
    "Mato Alto": 3.00,
}

AREA_MINIMA_M2 = 50
VALOR_MINIMO_SERVICO = 150.00


def calcular_orcamento(area_m2: float, tipo_mato: str) -> dict:
    preco_unitario = PRECO_POR_M2.get(tipo_mato, 0.0)
    area_cobravel = max(area_m2, AREA_MINIMA_M2)
    valor_calculado = area_cobravel * preco_unitario
    valor_final = max(valor_calculado, VALOR_MINIMO_SERVICO)

    return {
        "preco_unitario": preco_unitario,
        "area_cobravel": area_cobravel,
        "valor_final": valor_final,
    }


def main(page: ft.Page):
    # Configurações da página e Metatags para preview do WhatsApp
    page.title = "MTS-ROÇAGEM - Serviços de Roçagem e Limpeza"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 10
    page.spacing = 15
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.meta_tags = {
        "og:title": "MTS-ROÇAGEM | Serviços Profissionais de Roçagem",
        "og:description": "Orçamento rápido de roçagem e limpeza de terrenos em Saquarema e região.",
        "og:image": "https://mts-ro-agem.onrender.com/banner1.jpg",
        "description": "Calculadora e orçamento de serviços de roçagem em Saquarema.",
    }

    # ==================== CABEÇALHO ====================
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(src="/logo.jpeg", width=80, height=50),
                ft.Text("ONLINE", size=18, margin=10, color="#00FFD5")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor="#f5f5f5",
        border_radius=8,
    )

    banner_img = ft.Container(
        content=ft.Image(src="/banner1.jpg"),
        border_radius=10,
    )

    text_secundario = ft.Container(
        content=ft.Text(
            "Ajudamos você a manter seu quintal limpo, seguro e bem cuidado com transparência, preço justo e atendimento rápido.",
            size=15,
            weight=ft.FontWeight.BOLD,
            color="green",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        padding=10,
    )

    # ==================== GALERIA ====================
    galeria = ft.Row(
        spacing=20,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(src="/img_card2.jpg", height=250),
                            ft.Text(
                                "Seu Terreno Limpo",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                            ft.Text("Trabalho e respeito", color="grey"),
                        ]
                    ),
                    padding=15,
                )
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(src="/img_card3.jpg", height=250),
                            ft.Text(
                                "Seu quintal sempre lindo",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                            ft.Text(
                                "Quintal limpo e organizado.", color="grey"
                            ),
                        ]
                    ),
                    padding=15,
                )
            ),
        ],
    )
    text_secundario2 = ft.Container(
      content=ft.Text(
            "ATENDIMENTO: Bacaxa; Araruama e São Vicente de Paula",
            size=15,
            weight=ft.FontWeight.BOLD,
            #color="#A5FF00AD",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        padding=10,
    )

    # ==================== FORMULÁRIO DE ORÇAMENTO ====================
    titulo_orcamento = ft.Text(
        "Solicite seu Orçamento",
        size=22,
        weight=ft.FontWeight.BOLD,
        color="green",
    )

    campo_nome = ft.TextField(
        label="Nome do Cliente", border_color="green", width=350
    )
    campo_endereco = ft.TextField(
        label="Endereço", border_color="green", width=350
    )
    campo_referencia = ft.TextField(
        label="Ponto de Referência", border_color="green", width=350
    )
    campo_area = ft.TextField(
        label="Área do terreno (m²)",
        border_color="green",
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_tipo_mato = ft.Dropdown(
        label="Situação do mato",
        width=350,
        border_color="green",
        options=[
            ft.dropdown.Option("Mato Baixo"),
            ft.dropdown.Option("Mato Médio"),
            ft.dropdown.Option("Mato Alto"),
        ],
        value="Mato Médio",
    )

    texto_resultado = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    texto_erro = ft.Text(color="red", size=13)

    def validar_campos() -> bool:
        texto_erro.value = ""
        if not campo_nome.value or not campo_endereco.value:
            texto_erro.value = "Preencha nome e endereço para continuar."
            return False
        try:
            area = float(campo_area.value.replace(",", "."))
            if area <= 0:
                raise ValueError
        except (ValueError, AttributeError):
            texto_erro.value = "Informe uma área válida em m² (ex: 120)."
            return False
        return True

    def obter_link_whatsapp() -> str:
        """Gera o link de envio com o texto formatado caso os dados sejam válidos"""
        if not validar_campos():
            return f"https://wa.me/{WHATSAPP_NUMERO}"

        area = float(campo_area.value.replace(",", "."))
        resultado = calcular_orcamento(area, campo_tipo_mato.value)

        mensagem = (
            "Olá! Gostaria de solicitar um orçamento de roçada:\n\n"
            f"Nome: {campo_nome.value}\n"
            f"Endereço: {campo_endereco.value}\n"
            f"Ponto de referência: {campo_referencia.value or 'não informado'}\n"
            f"Área: {area:.0f} m²\n"
            f"Situação do mato: {campo_tipo_mato.value}\n"
            f"Valor estimado: R$ {resultado['valor_final']:.2f}"
        )
        return f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(mensagem)}"

    def on_calcular(e):
        if not validar_campos():
            texto_resultado.value = ""
            page.update()
            return

        area = float(campo_area.value.replace(",", "."))
        resultado = calcular_orcamento(area, campo_tipo_mato.value)

        texto_resultado.value = (
            f"Área considerada: {resultado['area_cobravel']:.0f} m²\n"
            f"Preço por m²: R$ {resultado['preco_unitario']:.2f}\n"
            f"Valor estimado do serviço: R$ {resultado['valor_final']:.2f}"
        )

        botao_whatsapp.url = obter_link_whatsapp()
        page.update()

    def on_atualizar_whatsapp(e):
        if validar_campos():
            botao_whatsapp.url = obter_link_whatsapp()
            page.update()

    botao_calcular = ft.ElevatedButton(
        "Calcular Orçamento",
        icon=ft.Icons.CALCULATE,
        bgcolor="green",
        color="white",
        on_click=on_calcular,
    )

    botao_whatsapp = ft.ElevatedButton(
        "Enviar pelo WhatsApp",
        icon=ft.Icons.CHAT,
        bgcolor="#25D366",
        color="white",
        url=f"https://wa.me/{WHATSAPP_NUMERO}",
        on_click=on_atualizar_whatsapp,
    )

    formulario_orcamento = ft.Container(
        content=ft.Column(
            controls=[
                titulo_orcamento,
                campo_nome,
                campo_endereco,
                campo_referencia,
                campo_area,
                campo_tipo_mato,
                ft.Row(
                    controls=[botao_calcular, botao_whatsapp],
                    wrap=True,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                texto_erro,
                texto_resultado,
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        margin=ft.Margin(0, 20, 0, 20),
        bgcolor="black",
        border_radius=10,
        alignment=ft.Alignment.CENTER,
    )

    # ==================== RODAPÉ ====================
    rodape = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "MTS-ROÇAGEM",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="green",
                ),
                ft.Text(
                    "Serviços Profissionais de Roçagem e Manutenção de Terrenos",
                    size=12,
                    color="grey",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=1, color="#333333"),
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.EMAIL, color="green", size=16),
                                ft.Text(
                                    "mtsrocagem@gmail.com",
                                    size=13,
                                    color="white",
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PHONE, color="green", size=16),
                                ft.Text(
                                    "(22) 99235-6039", size=13, color="white"
                                ),
                            ],
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    spacing=20,
                ),
                ft.Text(
                    "© 2026 MTS-ROÇAGEM - Todos os direitos reservados.",
                    size=11,
                    color="grey",
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        bgcolor="#111111",
        border_radius=8,
        margin=ft.Margin(0, 20, 0, 0),
    )

    page.add(
        header,
        banner_img,
        text_secundario,
        galeria,
        text_secundario2,
        formulario_orcamento,
        rodape,
    )


ft.app(
    target=main,
    assets_dir="assets",
)

