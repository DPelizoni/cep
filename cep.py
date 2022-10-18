import requests
import PySimpleGUI as sg


def cep(numero):
    """Busca CEP de uma API"""
    try:
        url = f'https://viacep.com.br/ws/{numero}/json/'
        request = requests.get(url)
        response = request.json()

        cep_validado = response['cep']
        logradouro = response['logradouro']
        bairro = response['bairro']
        localidade = response['localidade']
        uf = response['uf']
        ddd = response['ddd']
        return cep_validado, logradouro, bairro, localidade, uf, ddd
    except Exception:
        return


def name(text):
    """Padronização do espacamento onde fica o texto"""
    NAME_SIZE = 12
    espacamento = NAME_SIZE - len(text)
    return sg.T(f'{text} {" " * espacamento}', s=(NAME_SIZE, 1), pad=(4, 0))


def buscar(window, logradouro, bairro, localidade, uf, ddd):
    window['-LOGRADOURO-'].update(logradouro)
    window['-BAIRRO-'].update(bairro)
    window['-LOCALIDADE-'].update(localidade)
    window['-UF-'].update(uf)
    window['-DDD-'].update(ddd)
    window['-STATUS-'].update('')
    window['Salvar'].update(disabled=False)


def salvar(window):
    window['-STATUS-'].update('Endereço salvo com sucesso!', text_color='#00FF00')
    window['-CEP-'].update('')
    window['-CEP-'].set_focus()
    window['Salvar'].update(disabled=True)


def layout_main():
    layout = [
        [sg.T('CEP'), sg.I(k='-CEP-', justification='c', s=(10, 1)), sg.B('Buscar')],
        [name('Logradouro'), sg.I(k='-LOGRADOURO-', do_not_clear=False)],
        [name('Número'), sg.I(k='-NUMERO-', s=(15, 1), do_not_clear=False)],
        [name('Complemento'), sg.I(k='-COMPLEMENTO-', do_not_clear=False)],
        [name('Bairro'), sg.I(k='-BAIRRO-', do_not_clear=False)],
        [name('Localidade'), sg.I(k='-LOCALIDADE-', do_not_clear=False)],
        [name('UF'), sg.I(k='-UF-', s=(3, 1), do_not_clear=False)],
        [name('DDD'), sg.I(k='-DDD-', s=(3, 1), do_not_clear=False)],
        [sg.B('Salvar', disabled=True, expand_x=True), sg.B('Exit', expand_x=True)],
    ]
    return layout


def layout_frame():
    frame = [
        [sg.Frame('Endereço', layout_main())],
        [sg.StatusBar(' ' * 100, auto_size_text=True, k='-STATUS-')],
    ]
    return frame


def main():
    sg.set_options(font='_ 10')

    # Cria a janela com os componentes
    window = sg.Window('Buscar CEP', layout_frame(), finalize=True)

    while True:
        # Eventos e Valores disponíveis para acesso
        event, values = window.read()

        try:
            cep_validado, logradouro, bairro, localidade, uf, ddd = cep(values['-CEP-'])

            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break
            elif event == 'Buscar':
                buscar(window, logradouro, bairro, localidade, uf, ddd)
            elif event == 'Salvar':
                salvar(window)
        except TypeError:
            window['-STATUS-'].update('Informe um CEP válido', text_color='red')
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break

    window.close()


if __name__ == '__main__':
    main()
