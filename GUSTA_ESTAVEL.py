import asyncio
from playwright.async_api import async_playwright
import time


lista_erros = []
checkbox_selector = None

async def iniciar_browser():
    try:
        print("Iniciando o navegador Playwright...")
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)  # `headless=False` para ver o navegador
        context = await browser.new_context() #nova guia
        page = await context.new_page()#nova guia
        print("Navegador iniciado com sucesso.")
        return playwright, browser, page
    except Exception as e:
        print(f"Erro ao iniciar o navegador Playwright: {e}")
        return None, None, None

async def login_bling(page):
    try:

        await page.locator("#username").fill("financeiro@goiaspet.com.br")

        await page.locator("#login > div > div.login-content.u-flex.u-flex-col.u-items-center > div > div.password-container.u-self-stretch > div > input").fill("gp-matriz_s2-BLg")

        await page.locator("role=button[name='Entrar']").click()
        
        
        print('login com sucesso')

    except:
        print('erro de login')

async def filtrar_notas(page):
     
    #time.sleep(5)
    print(await page.locator("#open-filter").is_visible())  # Retorna True ou False - log

    #page.wait_for_selector("#open-filter", state="attached")  # Verifica se está no DOM
    await page.locator("#open-filter").wait_for(state="visible")  # Verifica visibilidade
    await page.locator("#open-filter").click(force=True)
    print('o botao está visivel')

    #page.locator(".InputDropdown-select[tabinex='0']").click(force=True)
    await page.locator("#select_situacao_nota").get_by_text("Selecione uma opção").click()
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    #await page.locator("span.InputDropdown-text", has_text = "Selecione uma opção").click(force=True)
    await page.locator("#filter-button-area").get_by_text("Filtrar").click()
    time.sleep(10)

print(checkbox_selector)

async def selecionar_checkbox_e_campo(page, index):
    try:
        print(f"Tentando acessar checkbox e campo da nota fiscal {index}...")
        campo_situacao_selector = f'tr:nth-child({index}) td:nth-child(5) span:nth-child(2) span'#seletor por elemento.tipo
        
        print(f'status nota:{campo_situacao_selector}')
        status_campo_situacao = await page.inner_text(campo_situacao_selector)
        print(f"Status da nota fiscal {index}: {status_campo_situacao}")

        if status_campo_situacao == "Pendente":
            print("status pendente - abrir e editar nota")
            checkbox_selector = f"tr:nth-child({index}) > td.checkbox-item > div > label"  
            if await page.is_visible(checkbox_selector):
                print('elemento existe')
                await page.locator(checkbox_selector).click()
            print(f"Checkbox da nota fiscal {index} selecionada com sucesso.")
        
            #campo_selector = f'tr:nth-child({index}) > td.span.visible-xs > span' 
            campo_selector = f'tr:nth-child({index}) td:nth-child(5) span:nth-child(2) span' 
            await page.locator(campo_selector).click(force=True)
            print(f"Campo da nota fiscal {index} selecionado com sucesso.")
            
            return True, index, checkbox_selector
            
        elif status_campo_situacao != "Pendente":
            print("nota pulada, não editada - status dif pendente")
            return False, index + 1, None
            
    except Exception as e:
        print(f"Erro ao selecionar checkbox ou campo da nota fiscal {index}: {e}")
        print(f"Returning: (False, {index + 1})")
        return False, index + 1, None

async def processar_itens_nota(page, cfop, index):
    try:
        print("Iniciando o processamento dos itens da nota fiscal...")

        item_selector_base = "#item{} > td:nth-child(1)"#SELETOR PARCIALMENTE VÁLIDO - COMPLETAR COM ITENS DINAMIGOS
        #item_selector_base = "#item0"
        print(f'{item_selector_base}:')

        for i in range(0, 11):  # Processar até 10 itens
            item_selector = item_selector_base.format(i)
            #await item_selector
            if await page.is_visible(item_selector):
                print(f"Item {i} encontrado.")
                await page.click(item_selector)
                await processar_item(page, cfop, index,  item_selector, checkbox_selector)
            else:
                print(f"Item {i} não encontrado. Finalizando processamento.")
                break
    except Exception as e:
        print(f"Erro ao processar os itens da nota fiscal: {e}")
        

async def processar_item(page, cfop, item_selector, index, checkbox_selector):
    try:
        print(f"Processando item com selector: {item_selector}")
        
        # Limpar campo de desconto
        try:
            desconto_selector = "#edValorDescontoItem"#criação variavel
            if await page.is_visible(desconto_selector):#condição de espera para elemento ser visivel
                await page.fill(desconto_selector, "")#espera e comando de ação
                print("Desconto removido com sucesso.")#retorno explicito
        except Exception as e:
            print(f"Erro ao apagar o desconto do item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False

        try:
        #copiar codigo
            codigo_prod = "#edCodigo"#declaração de variável
            if await page.is_visible(codigo_prod):#condição de espera para elemento visivel
                texto = await page.locator(codigo_prod).input_value()
                print(f"codigo produto: {texto}")
            else:
                print('Elemento nao visivel')
        except Exception as e:
            print(f"Erro ao copiar codigo do item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False

        #colar codigo
        try:
            colar_cod= '#edDescricao'
            if await page.locator(colar_cod).is_enabled():
                await page.fill(colar_cod, str(texto))
                print(f"codigo produto: {colar_cod}")
                time.sleep(2)
                await page.locator(colar_cod).press('Enter')
        except Exception as e:
            print(f"Erro ao processar o item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False
        

        # Preencher CFOP
        try:
            cfop_selector = "#edCfop"
            if await page.is_visible(cfop_selector):
                await page.fill(cfop_selector, str(cfop))
                print(f"CFOP preenchido: {cfop}")
        except Exception as e:
            print(f"Erro ao processar o item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False
        
     # Salvar alteraçõesTimeoutError
        await salvar_alteracoes_item(page)
        return True

    except Exception as e:
        print(f"Erro ao processar o item: {e}")
        await erro_editar_item(page, index, checkbox_selector)
        return False

async def erro_editar_item(page, index, checkbox_selector):
    print("bloco de erro de edição de nota fiscal")
    cancelar_editar_item_nota = "body > div.ui-dialog.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.fixed.slideIn.ui-dialog-newest.open > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button"
    await page.click(cancelar_editar_item_nota)
    #await cancelar_nota(page, index, checkbox_selector)    

async def salvar_alteracoes_item(page):
    try:
        #salvar_button_selector = page.get_by_role("button", name="Salvar").filter(has_text="Salvar", has_attribute="id", value="botaoSalvar")

        salvar_button_selector = page.locator("body > div.ui-dialog.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.fixed.slideIn.ui-dialog-newest.open > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button")
        await salvar_button_selector.click()
        print("Alterações do item salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar alterações do item: {e}")

async def salvar_alteracoes_nota(page):
    try:
        salvar_nota_selector = "#botaoSalvar"
        await page.click(salvar_nota_selector)
        time.sleep(4) 
        print("Alterações da nota fiscal salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar alterações da nota: {e}")
        botao_cancelar = "#botaoCancelar"
        await page.click(botao_cancelar)
        return False
        
async def verificar_erro_salvamento(page, index, checkbox_selector):
    try:
        mensagem_erro_selector = "#mensagem p"
        mensagem_erro = await page.inner_text(mensagem_erro_selector)

        if "Não foi possível salvar a Nota Fiscal" in mensagem_erro:
            print("Erro no salvamento")
            #mensagem_erro = await page.inner_text(mensagem_erro_selector)
            #await cancelar_nota(page, checkbox_selector, index)
            print(f"Mensagem de erro detectada: {mensagem_erro}")
            return True
        else: 
            print("Nenhum erro detectado após salvar a nota.")
            return False
                
    except Exception as e:
        print(f"Erro ao verificar mensagem de erro: {e}")
        return False
        
async def emitir_nota_fiscal(page, index):
    try:
        enviar_nota_selector = "#container > div.side.new-box-side > div.new-side-bar-full > div > div.main-actions > button:nth-child(1) > span.action-text.hide-on-minimize"
        imprimir_nota_selector = "#notaAcao"
        #texto_verificar = "#feedback_response_1 > div > div.AccordionPanel-header > div.AccordionPanel-label > div > span"

        if await page.is_visible(enviar_nota_selector):
            await page.click(enviar_nota_selector)
            print("Nota fiscal enviada com sucesso.")

        time.sleep(2)
        print("clicking prin#2 RN")
        await page.wait_for_selector(imprimir_nota_selector, state = "visible", timeout = 30000)
        #if await page.is_visible(imprimir_nota_selector):
        await page.click(imprimir_nota_selector)
             #issue: selector updated incorrectly
        print("clicked")
        #await asyncio.sleep(10)
        '''else:
            print("failed click")'''        

    except Exception as e:
        print(f"Erro ao emitir a nota fiscal {index}: {e}")

async def avaliar_impressao(page,index, checkbox_selector):
    
    mensagem_impressao = "#feedback_response_1 > div > div.AccordionPanel-header > div.AccordionPanel-label > div > span"
    x_final = "body > div.ui-dialog.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.fixed.slideIn.ui-dialog-newest.open > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button"

    try:
        await page.wait_for_selector(mensagem_impressao, state="visible", timeout=30000)
        mensagem = (await page.inner_text(mensagem_impressao)).strip()
        print(mensagem)
        time.sleep(1)

        if  "Notas fiscais eletrônicas não foram validadas!" in mensagem:
            await page.wait_for_selector(x_final, state="visible")
            await page.locator(x_final).click()
            print("erro na impressão da nota - possível consulta de situação")
            if await page.locator(checkbox_selector).is_checked():
                await page.click(checkbox_selector)
                return True, index + 1 
            #await page.wait_for_selector(x_final, state = "visible", timeout = 100000)
        else:
            await page.wait_for_selector(x_final, state="visible")
            await page.locator(x_final).click()
            print("impressao nota concluida com sucess")
            time.sleep(1.8)
            return False, index
        
    except Exception as e:
        print(f"erro ao avaliar a impressão: {e}")
        return False, index

'''async def cancelar_nota(page, checkbox_selector, index):
    try:
        botao_cancelar = "#botaoCancelar"
        await page.click(botao_cancelar)
        print("emissão de nota nota cancelada")
        await page.click(checkbox_selector)
        return True, index + 1
    except Exception as e:
        print('erro ao clicar no botao de cancelamento')
print(checkbox_selector)'''

async def processar_nota_fiscal(page, index, checkbox_selector):
    try:
        
        nota_selecionada, novo_index, checkbox_selector = await selecionar_checkbox_e_campo(page, index)
        print(f"Returned values - nota_selecionada: {nota_selecionada}, novo_index: {novo_index}, checkbox_selector: {checkbox_selector}")

        if nota_selecionada:
            cep_selector = "input#etiqueta_cep"
            print(cep_selector)
            time.sleep(2)
            cep_text = await page.input_value(cep_selector)
            cfop = determinar_cfop(cep_text)
            await processar_itens_nota(page, cfop, index)
            await salvar_alteracoes_nota(page)
            
            if await verificar_erro_salvamento(page, checkbox_selector, index):
                print(f"Erro ao salvar a nota fiscal {index}.")
                lista_erros.append(f"Erro ao salvar a nota fiscal {index}.")
                botao_cancelar = "#botaoCancelar"
                await page.click(botao_cancelar)
                print("emissão de nota nota cancelada")
                await page.click(checkbox_selector)
                return False, index + 1
                
            else:
                await emitir_nota_fiscal(page, index)
                await avaliar_impressao(page, index, checkbox_selector)
        return False, novo_index
    except Exception as e:
        print(f"Erro ao processar a nota fiscal {index}: {e}")
        return True, index + 1

def determinar_cfop(cep_text):
    #capturando o texto de um lugar vazio
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix)
    print(f"CEP numérico: {cep_num}")
    if (72800 <= cep_num <= 72999) or (73700 <= cep_num <= 76799):
        return 5102
    else:
        return 6108

async def main():
    playwright, browser, page = await iniciar_browser()
    if browser is None or page is None:
        print("Falha ao iniciar o navegador. Finalizando...")
        return

    await page.goto("https://www.bling.com.br/notas.fiscais.php#list")

    await login_bling(page)
    await filtrar_notas(page)

    success_count = 0
    error_count = 0
    index = 1
    notas_inexistentes_consecutivas = 0

    while True:
        try:
            nota_existe = await page.is_visible(f"tr:nth-child({index}) td:nth-child(1) div input")
            if not nota_existe:
                notas_inexistentes_consecutivas += 1
                print(f"Nota fiscal {index} não encontrada. Consecutivas: {notas_inexistentes_consecutivas}")
                if notas_inexistentes_consecutivas >= 2:
                    print("Encerrando script: Não há mais notas fiscais para processar.")
                    break
                index += 1
                continue

            notas_inexistentes_consecutivas = 0
            erro, novo_index = await processar_nota_fiscal(page, index, checkbox_selector)
            if erro:
                error_count += 1
            else:
                success_count += 1
            index = novo_index

        except Exception as e:
            print(f"Erro no processamento da nota fiscal {index}: {e}")
            error_count += 1
            index += 1

    print(f"Notas fiscais processadas com sucesso: {success_count}")
    print(f"Notas fiscais com erro: {error_count}")

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())