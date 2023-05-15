import colorama
from key import API_KEY
import requests
import json


def gpt_gerar(mm):
    id_model = 'gpt-3.5-turbo'  # Sua Chave API openAI
    header = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    body = {
        'model': id_model,
        'messages': [{'role': 'user', 'content': f'{mm}'}]
    }

    body = json.dumps(body)
    req = requests.post('https://api.openai.com/v1/chat/completions', headers=header, data=body)
    answer = req.json()

    try:
        return str(answer['choices'][0]['message']['content']).replace('.', '').lower()
    except KeyError:
        print('Erro servidor')


animal = gpt_gerar('Gere o nome de uma animal, se o nome tiver acento, por exemplo leão, remova o acento,'
                   'tambem nao pode ser nome composto, por exemplo "diabo da tasmania"'
                   'e se tiver "ç" mude para "c", de todo modo só pode ser respondido com uma única palavra')

dica_animal = gpt_gerar(f'Tenho um jogo de forca e preciso de uma dica sobre esse animaml: {animal}'
                        'com apenas uma frase simples me de uma dica, sem citar pontos chaves'
                        'exemplos: vaca e leite')

lista_correta = []
letras_digitadas = []
vidas = 5

if ' ' in animal:  # As vezes o chatGPT retorna uma frase, esse codigo faz a frase ser cortada
    animal = animal.split(' ')[0]

print(dica_animal)

while True:
    for letras in animal:
        if letras in letras_digitadas:
            print(letras, end='')
            lista_correta.append(letras)
        else:
            print('_', end='')
    if set(animal) == set(lista_correta):
        print(colorama.Fore.GREEN, '- era a palavra Voce ganhou!!!', colorama.Style.RESET_ALL)
        break
    escolha = str(input(' Digite uma letra- '))

    if escolha.lower() == animal.lower():
        print(colorama.Fore.MAGENTA, 'Voce ganhou, acertou toda a palavra!', colorama.Style.RESET_ALL)
        break

    elif 1 < len(escolha) < 3:
        print('Apenas uma letra por favor')

    elif len(escolha) > 3:
        print('Voce parece ter dado um chute, mas errou')

    inter = set(animal) & set(escolha)
    if len(inter) > 2:
        print('Voce quase acertou, esta perto')

    if not escolha in animal and len(escolha) == 1:
        print(colorama.Fore.RED, f'Letra "{escolha.upper()}" -  Nao esta na palavra secreta!')
        vidas -= 1

    if escolha.isdigit():
        print(colorama.Fore.RED, 'Digite uma letra Valida', colorama.Style.RESET_ALL)
    else:
        letras_digitadas.append(escolha)
    if vidas == 0:
        print('Suas vidas acabaram')
