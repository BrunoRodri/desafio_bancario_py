menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(saldo, valor_deposito, extrato):
  if valor_deposito > 0:
    saldo += valor_deposito
    extrato += f"Deposito: R$ {valor_deposito:.2f}\n"
    print(f"Deposito efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
  else:
    print("Valor de deposito inválido!")
  return saldo, extrato
def sacar(saldo, valor_saque, extrato, numero_saques, limite):
    if valor_saque > saldo:
        print("Saldo insuficiente!")
    elif valor_saque > limite:
        print("O valor do saque excede o limite!")
    elif numero_saques >= LIMITE_SAQUES:
        print("Número máximo de saques diários atingido!")
    elif valor_saque > 0:
        saldo -= valor_saque
        numero_saques += 1
        extrato += f"Saque: R$ {valor_saque:.2f}\n"
        print(f"Saque efetuado com sucesso! Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor de saque inválido!")
    return saldo, extrato, numero_saques

while True:

  opcao = input(menu)

  if opcao == "d":
    valor_deposito = float(input("Informe o valor do deposito: "))
    saldo, extrato = depositar(saldo, valor_deposito, extrato)
  elif opcao == "s":
    valor_saque = float(input("Informe o valor do saque: "))
    saldo, extrato, numero_saques = sacar(saldo, valor_saque, extrato, numero_saques, limite)
  elif opcao == "e":
    print("\nExtrato:")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
  elif opcao == "q":
    print("Saindo do sistema...")
    break
  else:
    print("Opção inválida! Tente Novamente")
