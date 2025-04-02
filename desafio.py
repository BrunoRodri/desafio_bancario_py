from datetime import datetime
# Desafio Banco

menu = """
################################################################
                           MENU

                        [d] Depositar
                        [s] Sacar
                        [e] Extrato
                        [q] Sair

################################################################

=> """

saldo = 0
limite = 500
extrato = ""
numero_transacoes = 0
LIMITE_TRANSACOES =10
mascara_ptbr = "%d/%m/%Y %H:%M"

def depositar(saldo, valor_deposito, extrato, numero_transacoes):
  if numero_transacoes == LIMITE_TRANSACOES:
    print("Número máximo de transações diárias atingido!")
  elif valor_deposito > 0:
    saldo += valor_deposito
    numero_transacoes += 1
    data_hora_atual = datetime.now()
    extrato += f"Deposito: R$ {valor_deposito:.2f} {data_hora_atual.strftime(mascara_ptbr)}\n"
    print(f"Deposito efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
  else:
    print("Valor de deposito inválido!")
  return saldo, extrato, numero_transacoes

def sacar(saldo, valor_saque, extrato, numero_transacoes, limite):
    if valor_saque > saldo:
        print("Saldo insuficiente!")
    elif valor_saque > limite:
        print("O valor do saque excede o limite!")
    elif numero_transacoes >= LIMITE_TRANSACOES:
        print("Número máximo de saques diários atingido!")
    elif valor_saque > 0:
        saldo -= valor_saque
        numero_transacoes += 1
        data_hora_atual = datetime.now()
        extrato += f"Saque: R$ {valor_saque:.2f} {data_hora_atual.strftime(mascara_ptbr)}\n"
        print(f"Saque efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor de saque inválido!")
    return saldo, extrato, numero_transacoes

while True:

  opcao = input(menu)

  if opcao == "d":
    valor_deposito = float(input("Informe o valor do deposito: "))
    saldo, extrato, numero_transacoes = depositar(saldo, valor_deposito, extrato, numero_transacoes)
  elif opcao == "s":
    valor_saque = float(input("Informe o valor do saque: "))
    saldo, extrato, numero_transacoes = sacar(saldo, valor_saque, extrato, numero_transacoes, limite)
  elif opcao == "e":
    print("\nExtrato:")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
  elif opcao == "q":
    print("Saindo do sistema...")
    break
  else:
    print("Opção inválida! Tente Novamente")
