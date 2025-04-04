from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)

  def adicionar_conta(self, conta):
    self.contas.append(conta)


class PessoaFisica(Cliente):
  def __init__(self, nome, cpf, data_nascimento, endereco):
    super().__init__(endereco)
    self.cpf = cpf
    self.nome = nome
    self.data_nascimento = data_nascimento


class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()

  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(cliente, numero)

  @property
  def saldo(self):
    return self._saldo
  
  @property
  def numero(self):
    return self._numero
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico
  
  def sacar(self, valor):
    saldo = self.saldo
    excedeu_limite = valor > saldo
    
    if excedeu_limite:
      print("Saldo insuficiente")
    elif valor > 0:
      self._saldo -= valor
      print(f"Saque de {valor} realizado com sucesso. Saldo atual: {self.saldo}")
      return True
    else:
      print("Valor de saque inválido")
    return False

    

  def depositar(self, valor):
    if valor > 0:
      self._saldo += valor
      print(f"Depósito de {valor} realizado com sucesso. Saldo atual: {self.saldo}")
    else:
      print("Valor de depósito inválido")
      return False
    
    return True
  

class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques

  def sacar(self, valor):
    numero_saques = len(
      [Transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
    )

    excedeu_limite = valor > self.limite
    excedeu_saques = numero_saques >= self.limite_saques

    if excedeu_limite:
      print("O valor do saque excede o limite da conta")

    elif excedeu_saques:
        print("Número de saques excedido")

    else:
        return super().sacar(valor)
      
  def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
  

class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

  def adicionar_transacao(self, transacao):
    self.transacoes.append(
      {
        "tipo": transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
      }
    )


class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass

  @abstractmethod
  def registrar(self, conta):
    pass


class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)


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

def filtrar_cliente(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    print("\n@@@ Usuário não encontrado! @@@")
    return None

def filtrar_conta(cpf, contas):
    for conta in contas:
        if conta.cliente.cpf == cpf:
            return conta
    print("\n@@@ Conta não encontrada! @@@")
    return None

def depositar(contas):
    cpf = input("Informe o CPF do cliente: ")
    conta = filtrar_conta(cpf, contas)

    if conta:
        valor = float(input("Informe o valor a ser depositado: "))
        transacao = Deposito(valor)
        transacao.registrar(conta)

def sacar(contas):
    cpf = input("Informe o CPF do cliente: ")
    conta = filtrar_conta(cpf, contas)

    if conta:
        valor = float(input("Informe o valor a ser sacado: "))
        transacao = Saque(valor)
        transacao.registrar(conta)

def exibir_extrato(contas):
    cpf = input("Informe o CPF do cliente: ")
    conta = filtrar_conta(cpf, contas)
    transacoes = conta.historico.transacoes

    if conta:
      if transacoes:
        print("\n=== Extrato ===")
        for transacao in conta.historico.transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: {transacao['valor']:.2f}")
        print(f"Saldo atual: {conta.saldo:.2f}")
        print("=" * 30)

    if not transacoes:
        print("Nenhuma transação encontrada.")
        return

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Usuário já cadastrado.")
            return
        
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
    usuarios.append(usuario)
    print("Usuário criado com sucesso.")

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print("\n=== Lista de Usuários ===")
    for usuario in usuarios:
        print("=" * 30)
        print(f"Nome: {usuario.nome}")
        print(f"CPF: {usuario.cpf}")
        print(f"Endereço: {usuario.endereco}")
        print("=" * 30)

def criar_conta(usuarios, contas):
   cpf = input("Informe o CPF do cliente: ")
   usuario = filtrar_cliente(cpf, usuarios)

   if not usuario:
       print("Usuário não encontrado.")
       return
   
   numero_conta = len(contas) + 1
   conta = ContaCorrente(numero_conta, usuario)
   contas.append(conta)
   print("Conta criada com sucesso.")

def listar_contas(contas):
    if not contas:
       print("Nenhuma conta cadastrada.")
       return
    
    print("\n=== Listagem de Contas ===")
    for conta in contas:
        print("=" * 30)
        print(f"Nome: {conta.cliente.nome}")
        print(f"CPF: {conta.cliente.cpf}")
        print(f"Conta: {conta.numero}")
        print(f"Saldo: {conta.saldo:.2f}")
        print("=" * 30)

def main():
   usuarios = []
   contas = []

   while True:
       opcao = menu()

       if opcao == "d":
           depositar(contas)
       elif opcao == "s":
           sacar(contas)
       elif opcao == "e":
           exibir_extrato(contas)
       elif opcao == "nu":
           criar_usuario(usuarios)
       elif opcao == "nc":
           criar_conta(usuarios, contas)
       elif opcao == "lc":
           listar_usuarios(usuarios)
       elif opcao == "cc":
           listar_contas(contas)
       elif opcao == "q":
           print("Saindo...")
           break
       else:
           print("Opção inválida. Tente novamente.")
       print("=" * 30)


main()
