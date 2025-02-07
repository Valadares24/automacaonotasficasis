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
    time.sleep(6)

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

        valor_unitario = '#edValorUnitario'
        antigo_valor_unitario_selector = await page.input_value(valor_unitario)
        antigo_valor_unitario_selector_float = float(antigo_valor_unitario_selector.replace(",", ".").strip())
        #valor = await  page.input_value(valor_unitario)
        print(f'valor unitário antes da edição da nota: {antigo_valor_unitario_selector_float}')


        time.sleep(2)

        try:
        #copiar codigo
            codigo_prod = "#edCodigo"#declaração de variável
            if await page.is_visible(codigo_prod) and await page.locator(codigo_prod).is_enabled():#condição de espera para elemento visivel
                codigo_copiado = await page.locator(codigo_prod).input_value()

                if codigo_copiado.strip() == "": #make sure it is not empty/garantindo que nao ta vazio
                    raise ValueError("O valor nao foi copiado, está em branco")
                else:
                    print(f'o codigo do produto foi copiado com sucesso e é: {codigo_copiado}')    
                
                #print(f"codigo produto: {codigo_copiado}")
            else:
                print('Elemento nao visivel ou habilitado')
                await erro_editar_item(page, index, checkbox_selector)
                return False
        except Exception as e:
            print(f"Erro ao copiar codigo do item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False

        #colar codigo

        try:
            
            campo_colar_cod= '#edDescricao'                #VARIAVEL CRIADA
            nome_prod= await page.input_value(campo_colar_cod)         #VARIAVEL CRIADA
            print (nome_prod)
            if await page.locator(campo_colar_cod).is_visible() and await page.locator(campo_colar_cod).is_enabled():#visivel e habilitado
                await page.locator(campo_colar_cod).fill("")#ancorar condicional no estado em branco
                await page.fill(campo_colar_cod, str(codigo_copiado))
                print(f"codigo produto: {campo_colar_cod}")#codigo numerico
                codigo_colado = await page.input_value(campo_colar_cod)#codigo numerico colado para verificação de pasting  #VARIAVEL CRIADA
                print(f'o valor do campo apos o codigo ter sido colado é: {codigo_colado}')
                time.sleep(5)
                #await page.wait_for_function(f""" const field = document.querySelector('{codigo_colado}'); field && field.value === '{codigo_copiado}' """, timeout = 5000 )
                if codigo_colado == codigo_copiado:#verificacao de colagem - os codigos sao os mesmos ou n
                    print(f'codigo copiado e colado com sucesso: {codigo_copiado} é o mesmo {codigo_colado}')
                else:
                    print(f'os codigos sao diferentes: {codigo_copiado} != {codigo_colado}')
                    await erro_editar_item(page, index, checkbox_selector)
                    time.sleep(3)
                    return False
      #se os codigos colados sao os mesmos, agora o ponto é verificar a presença do nome do produto, e não o estado vazio - a colagem do codigo está respaldada de fato?
                
                await page.locator(campo_colar_cod).press('Enter')
                print('produto selecionado')
                time.sleep(3)
                novo_nome_produto = await page.input_value(campo_colar_cod)
                print(novo_nome_produto)

                

                if nome_prod == novo_nome_produto:
                    print(f'produto selecionado com sucesso: {nome_prod} = {novo_nome_produto}')
                else:
                    print("nome do produto  nao atualizado")
                    await erro_editar_item(page, index, checkbox_selector)
                    time.sleep(3)
                    return False
            
                print(f'o antigo valor unitario é:{antigo_valor_unitario_selector_float}')            
        except Exception as e:
            print(f"Erro ao processar o item: {e}")
            await erro_editar_item(page, index, checkbox_selector)
            return False
        

        # Preencher CFOP
        #time.sleep(2)   
        novo_valor_unitario = '#edValorUnitario'
        novo_valor_unitario_selector = await page.input_value(novo_valor_unitario)
        print(novo_valor_unitario_selector)
        novo_valor_unitario_selector_float = float(novo_valor_unitario_selector.replace(",", ".").strip())
        print(f' valor antigo é {antigo_valor_unitario_selector} e do tipo: {type(antigo_valor_unitario_selector_float)}')
        print(f' valor novo é {novo_valor_unitario_selector_float} e do tipo: {type(novo_valor_unitario_selector_float)}')


        print(f'o novo valor unitario é:{novo_valor_unitario_selector_float}')
        
        if  round(novo_valor_unitario_selector_float, 2) <  round(antigo_valor_unitario_selector_float, 2):
            print(f'a diferenca e de: {antigo_valor_unitario_selector_float} - {novo_valor_unitario_selector_float}')
            print(f"Valor atualizado com sucesso")    
        else:
            print("valor unitario nao atualizado")
            await erro_editar_item(page, index, checkbox_selector)
            time.sleep(4)
            return False  
        
        
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
        #time.sleep(3) 
        print("pressionado botao de salvamento da nota com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar alterações da nota: {e}")
        botao_cancelar = "#botaoCancelar"
        await page.click(botao_cancelar)
        return False
        
async def verificar_erro_salvamento(page):
    print('verificando erro de salvamento')
    await page.wait_for_timeout(3000)#tempo alterado

    try:


        await page.wait_for_load_state("load")

        mensagem_erro_locator =  page.locator("#mensagem > p:nth-child(2)")#seletor atualizado com  await page.locator

        await mensagem_erro_locator.wait_for(state = 'visible', timeout=9000)#testando visibilidade do elemento apontando diretamente para a variavel
        for _ in range(3):
            try:
                mensagem_erro = await mensagem_erro_locator.inner_text()#usando tecnicas mistas, cuidado
                if mensagem_erro.strip():
                    break
            except Exception as e:
                print(f'erro ao capturar mensagem de erro')
            await page.wait_for_timeout(1000)

        print(f'resultado verificação de erro: {mensagem_erro}')
        print(mensagem_erro)

        if "Não foi possível salvar a Nota Fiscal" in mensagem_erro:#NAO ESTA FUNCIONANDO CORRETAMENTE
            print("Erro no salvamento detectado corretamente")
            await verificar_tipo_erro(page)
            return True
        else: 
            print("Nenhum erro detectado após salvar a nota.")
            return False

                
    except Exception as e:
        print(f"Erro ao verificar mensagem de erro: {e}")
        return False
        
async def verificar_tipo_erro(page):
    await page.wait_for_load_state("load")

    seletor_mensagem_erro_salvamento_ampla = "#mensagem > ul > li"
    await page.wait_for_selector(seletor_mensagem_erro_salvamento_ampla, timeout = 1000)
    
    mensagens_erro_selector = await page.query_selector_all(seletor_mensagem_erro_salvamento_ampla)
    mensagens_erro = []
    
    for element in mensagens_erro_selector:
        texto_especifico_erro = await element.inner_text()
        print(f'mensagem de erro capturada: {texto_especifico_erro}')
        print(f'foram encontradas : {len(mensagens_erro)} mensagens de erro após tentativa de salvamento')
        mensagens_erro.append(texto_especifico_erro)
            
    
    #erro_especifico_capturado_texto = await page.inner_text(mensagens_erro)
    #lista_erros.append(mensagens_erro.strip())
    #print(f'os erros são: {erro_especifico_capturado_texto}')
    
    # if verificar_erro_salvamento:
    #     if"O valor do campo município não foi encontrado no sistema" in retorno_erro_especifico:
            #mensagem > ul > li:nth-child(1)

async def emitir_nota_fiscal(page, index):
    try:
        enviar_nota_selector = "#container > div.side.new-box-side > div.new-side-bar-full > div > div.main-actions > button:nth-child(1) > span.action-text.hide-on-minimize"
        imprimir_nota_selector = "#notaAcao"
        #codigo_copiado_verificar = "#feedback_response_1 > div > div.AccordionPanel-header > div.AccordionPanel-label > div > span"

        #await page.wait_for_function (""" const field = document.querySelector('#notaAcao); return field && field.value """)
        if await page.wait_for_selector(enviar_nota_selector, state = 'visible', timeout=40000):
            await page.click(enviar_nota_selector)
            print("Nota fiscal enviada com sucesso.")

        time.sleep(2)
        print("clicking prin#2 RN")
        await page.wait_for_selector(imprimir_nota_selector, state = "visible", timeout=4000)

        if page.locator(imprimir_nota_selector).is_enabled:
        #if await page.is_visible(imprimir_nota_selector):
            await page.click(imprimir_nota_selector)
             #issue: selector updated incorrectly
            print("clicked")
        #await asyncio.sleep(10)
        else:
            print("failed click")        

    except Exception as e:
        print(f"Erro ao emitir a nota fiscal {index}: {e}")

async def avaliar_impressao(page,index, checkbox_selector):
    
    mensagem_impressao = "#feedback_response_1 > div > div.AccordionPanel-header > div.AccordionPanel-label > div > span"
    x_final = "body > div.ui-dialog.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.fixed.slideIn.ui-dialog-newest.open > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button"

    try:
        await page.wait_for_selector(mensagem_impressao, state="visible", timeout=120000)
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

async def processar_nota_fiscal(page, index, checkbox_selector):
    try:
        
        nota_selecionada, novo_index, checkbox_selector = await selecionar_checkbox_e_campo(page, index)
        print(f"Returned values - nota_selecionada: {nota_selecionada}, novo_index: {novo_index}, checkbox_selector: {checkbox_selector}")

        if nota_selecionada:
            cep_selector = "#etiqueta_cep"
            print(cep_selector)
            time.sleep(2)
            cep_text = await page.input_value(cep_selector)
            cfop = determinar_cfop(cep_text)
            await processar_itens_nota(page, cfop, index)
            await salvar_alteracoes_nota(page)
            
            if await verificar_erro_salvamento(page):
                print(f"Erro ao salvar a nota fiscal {index}.")
                lista_erros.append(f"Erro ao salvar a nota fiscal {index}.")
                botao_cancelar = "#botaoCancelar"
                await page.click(botao_cancelar)
                print("emissão de nota nota cancelada")
                await page.click(checkbox_selector)
                print('seletor desmarcado')
                return False, index + 1
                
            else:
                await emitir_nota_fiscal(page, index)
                await avaliar_impressao(page, index, checkbox_selector)
                print('impressao concluida normalmente - item sem necessidade de uncheck')
        return False, novo_index
    except Exception as e:
        print(f"Erro ao processar a nota fiscal {index}: {e}")
        return True, index + 1

def determinar_cfop(cep_text):
    #capturando o codigo_copiado de um lugar vazio
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
                    print(lista_erros)
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
    print(lista_erros)
    print(mensagens_erro)

    await browser.close()   

if __name__ == "__main__":
    asyncio.run(main())