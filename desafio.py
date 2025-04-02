from datetime import datetime
import textwrap
# Desafio Banco

########## Variáveis e constantes###########
usuarios = []
contas = []
saldo = 0
limite = 500
extrato = ""
numero_transacoes = 0
AGENCIA = "0001"
LIMITE_TRANSACOES =10
mascara_ptbr = "%d/%m/%Y %H:%M"

############ Funções ############
def menu():
    menu = """
    ########################## MENU ###############################
                           

                        [d]\tDepositar
                        [s]\tSacar
                        [e]\tExtrato
                        [nu]\tNovo Usuário
                        [nc]\tCriar Conta
                        [lc]\tListar Clientes
                        [cc]\tListar Contas
                        [q]\tSair

    ###############################################################

=> """
    return input(textwrap.dedent(menu)).strip().lower()

def depositar(saldo, extrato, numero_transacoes):
    if numero_transacoes == LIMITE_TRANSACOES:
        print("Número máximo de transações diárias atingido!")
        return saldo, extrato, numero_transacoes

    valor_deposito = float(input("Informe o valor do depósito: "))
    if valor_deposito > 0:
        saldo += valor_deposito
        numero_transacoes += 1
        data_hora_atual = datetime.now()
        extrato += f"Depósito: R$ {valor_deposito:.2f} {data_hora_atual.strftime(mascara_ptbr)}\n"
        print(f"Depósito efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor de depósito inválido!")
    return saldo, extrato, numero_transacoes

def sacar(saldo, extrato, numero_transacoes, limite):
    if numero_transacoes >= LIMITE_TRANSACOES:
      print("Número máximo de transações diários atingido!")
      return saldo, extrato, numero_transacoes
    
    valor_saque = float(input("Informe o valor do saque: "))
    if valor_saque > saldo:
        print("Saldo insuficiente!")
    elif valor_saque > limite:
        print("O valor do saque excede o limite!")
    elif valor_saque > 0:
        saldo -= valor_saque
        numero_transacoes += 1
        data_hora_atual = datetime.now()
        extrato += f"Saque: R$ {valor_saque:.2f} {data_hora_atual.strftime(mascara_ptbr)}\n"
        print(f"Saque efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor de saque inválido!")
    return saldo, extrato, numero_transacoes

def exibir_extrato(saldo, extrato):
    print("\nExtrato:")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Usuário já cadastrado!")
            return
        
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento (ddmmyyyy): ")

    # Endereço
    logradouro = input("Informe o logradouro: ")
    numero = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    estado = input("Informe a sigla do estado (UF): ")
    endereco = f"{logradouro}, {numero} - {bairro}, {cidade}/{estado}"

    usuarios.append({
       "nome": nome,
        "data_nascimento": data_nascimento,
       "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")

def criar_conta(usuarios):

    cpf = input("Informe o CPF do usuário: ")
    usuario_encontrado = False
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = True
            break
    if not usuario_encontrado:
        print("Usuário não encontrado!")
        return
    
    numero_conta = len(contas) + 1
    contas.append({
        "numero_conta": numero_conta,
        "usuario": usuario["nome"],
        "cpf": cpf,
    })
    
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
      for usuario in usuarios:
        print(f"Nome: {usuario['nome']}, Data Nascimento: {usuario['data_nascimento']} CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agencia:{AGENCIA}, Conta: {conta['numero_conta']}, Nome: {conta['usuario']} CPF: {conta['cpf']}")
            
def sair():
    print("Saindo do sistema...")
    exit()

opcoes_menu = {
    "d": lambda: depositar(saldo, extrato, numero_transacoes),
    "s": lambda: sacar(saldo, extrato, numero_transacoes, limite),
    "e": lambda: exibir_extrato(saldo, extrato),
    "nu": lambda: criar_usuario(usuarios),
    "nc": lambda: criar_conta(usuarios),
    "lc": lambda: listar_usuarios(usuarios),
    "cc": lambda: listar_contas(contas),
    "q": sair
}

while True:
  opcao = menu()
  acao = opcoes_menu.get(opcao)

  if acao:
    resultado = acao()

    if resultado:
            if isinstance(resultado, tuple):  
                saldo, extrato, numero_transacoes = resultado
  else:
    print("Opção inválida! Tente Novamente")

