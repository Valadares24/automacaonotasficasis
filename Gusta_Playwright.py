import asyncio
from playwright.async_api import async_playwright
import time

lista_erros = []

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

        await page.locator("input#username").fill("financeiro@goiaspet.com.br")

        await page.locator("input.InputText-input[placeholder='Insira sua senha']").fill("gp-matriz_s2-BLg")

        #clicar_login_buttn
        await page.locator("role=button[name='Entrar']").click()
        
        
        print('login com sucesso')

    except:
        print('erro de login')
    

async def filtrar_notas(page):
     
    time.sleep(5)
    print(await page.locator("#open-filter").is_visible())  # Retorna True ou False - log

    #page.wait_for_selector("#open-filter", state="attached")  # Verifica se está no DOM
    await page.locator("#open-filter").wait_for(state="visible")  # Verifica visibilidade
    await page.locator("#open-filter").click(force=True)
    print('o botao está visivel')

    #page.locator(".InputDropdown-select[tabinex='0']").click(force=True)
    page.locator("span.InputDropdown-arrow").click()


    #time.sleep(10)


async def selecionar_checkbox_e_campo(page, index):
    try:
        print(f"Tentando acessar checkbox e campo da nota fiscal {index}...")
        campo_situacao_selector = f'tr:nth-child({index}) td:nth-child(5) span:nth-child(2) span'#seletor por elemento.tipo
        print(f'status nota:{campo_situacao_selector}')
        status_campo_situacao = await page.inner_text(campo_situacao_selector)
        print(f"Status da nota fiscal {index}: {status_campo_situacao}")

        if status_campo_situacao != "Pendente":
            return False, index + 1

        #checkbox_selector = f'tr:nth-child({index}) td:nth-child(1) div input'
        checkbox_selector = f"tr:nth-child({index}) td.checkbox-item input[type='checkbox']"
        campo_selector = f'tr:nth-child({index}) td:nth-child(4)'
        
        await page.click(checkbox_selector)
        print(f"Checkbox da nota fiscal {index} selecionada com sucesso.")

        await page.click(campo_selector)
        print(f"Campo da nota fiscal {index} selecionado com sucesso.")
        return True, index
    except Exception as e:
        print(f"Erro ao selecionar checkbox ou campo da nota fiscal {index}: {e}")
        return False, index + 1

async def processar_itens_nota(page, cfop):
    try:
        print("Iniciando o processamento dos itens da nota fiscal...")
        item_selector_base = "table > tbody > tr:nth-child({}) > td:nth-child(1)"
        for i in range(1, 11):  # Processar até 10 itens
            item_selector = item_selector_base.format(i)
            if await page.is_visible(item_selector):
                print(f"Item {i} encontrado.")
                await page.click(item_selector)
                await processar_item(page, cfop, item_selector)
            else:
                print(f"Item {i} não encontrado. Finalizando processamento.")
                break
    except Exception as e:
        print(f"Erro ao processar os itens da nota fiscal: {e}")

async def processar_item(page, cfop, item_selector):
    try:
        print(f"Processando item com selector: {item_selector}")
        
        # Limpar campo de desconto
        desconto_selector = "#edValorDescontoItem"
        if await page.is_visible(desconto_selector):
            await page.fill(desconto_selector, "")
            print("Desconto removido com sucesso.")

        # Preencher CFOP
        cfop_selector = "#edCfop"
        if await page.is_visible(cfop_selector):
            await page.fill(cfop_selector, str(cfop))
            print(f"CFOP preenchido: {cfop}")

        # Salvar alterações
        await salvar_alteracoes_item(page)
    except Exception as e:
        print(f"Erro ao processar o item: {e}")

async def salvar_alteracoes_item(page):
    try:
        salvar_button_selector = "button#salvar-item"
        await page.click(salvar_button_selector)
        print("Alterações do item salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar alterações do item: {e}")

async def salvar_alteracoes_nota(page):
    try:
        salvar_nota_selector = "button#salvar-nota"
        await page.click(salvar_nota_selector)
        print("Alterações da nota fiscal salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar alterações da nota: {e}")

async def verificar_erro_salvamento(page):
    try:
        mensagem_erro_selector = "#mensagem p"
        if await page.is_visible(mensagem_erro_selector):
            mensagem_erro = await page.inner_text(mensagem_erro_selector)
            print(f"Mensagem de erro detectada: {mensagem_erro}")
            return True
        print("Nenhum erro detectado após salvar a nota.")
        return False
    except Exception as e:
        print(f"Erro ao verificar mensagem de erro: {e}")
        return False

async def emitir_nota_fiscal(page, index):
    try:
        enviar_nota_selector = "button#enviar-nota"
        imprimir_nota_selector = "button#imprimir-nota"

        await page.click(enviar_nota_selector)
        print("Nota fiscal enviada com sucesso.")

        await page.click(imprimir_nota_selector)
        print("Nota fiscal enviada para impressão.")
    except Exception as e:
        print(f"Erro ao emitir a nota fiscal {index}: {e}")

async def processar_nota_fiscal(page, index):
    try:
        nota_selecionada, novo_index = await selecionar_checkbox_e_campo(page, index)
        if nota_selecionada:
            cep_selector = "input#cep"
            cep_text = await page.input_value(cep_selector)
            cfop = determinar_cfop(cep_text)
            await processar_itens_nota(page, cfop)
            await salvar_alteracoes_nota(page)
            if await verificar_erro_salvamento(page):
                print(f"Erro ao salvar a nota fiscal {index}.")
                lista_erros.append(f"Erro ao salvar a nota fiscal {index}.")
            else:
                await emitir_nota_fiscal(page, index)
        return False, novo_index
    except Exception as e:
        print(f"Erro ao processar a nota fiscal {index}: {e}")
        return True, index + 1

def determinar_cfop(cep_text):
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix.replace("-", ""))
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
            erro, novo_index = await processar_nota_fiscal(page, index)
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
