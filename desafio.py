from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# Constantes
LIMITE_TRANSACOES = 10
AGENCIA = "0001"

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            conta.realizar_transacao(transacao)
        else:
            print("\n@@@ Operação falhou! A conta não pertence a este cliente. @@@")

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()
        self.numero_transacoes = 0

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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

    def realizar_transacao(self, transacao):
        if self.numero_transacoes >= LIMITE_TRANSACOES:
            print("\n@@@ Operação falhou! Limite de transações diárias atingido. @@@")
            return False
        sucesso = transacao.registrar(self)
        if sucesso:
            self.numero_transacoes += 1
        return sucesso

    def sacar_conta(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            print(f"Saldo atual: R$ {self._saldo:.2f}")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar_conta(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            print(f"Saldo atual: R$ {self._saldo:.2f}")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500):
        super().__init__(numero, cliente)
        self._limite = limite

    def sacar(self, valor):
        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
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
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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
        sucesso = conta.sacar_conta(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar_conta(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


# Funções do Menu
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

def depositar(usuarios, contas):
    cpf = input("Informe o CPF do titular: ")
    conta = buscar_conta_por_cpf(cpf, contas)
    if conta:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        conta.realizar_transacao(transacao)

def sacar(usuarios, contas):
    cpf = input("Informe o CPF do titular: ")
    conta = buscar_conta_por_cpf(cpf, contas)
    if conta:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        conta.realizar_transacao(transacao)

def exibir_extrato(usuarios, contas):
    cpf = input("Informe o CPF do titular: ")
    conta = buscar_conta_por_cpf(cpf, contas)
    if conta:
        print("\n=== Extrato ===")
        for transacao in conta.historico.transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")
        print(f"\nSaldo atual: R$ {conta.saldo:.2f}")

def criar_usuario(usuarios, contas):
    cpf = input("Informe o CPF (somente números): ")
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("\n@@@ Usuário já cadastrado! @@@")
            return

    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
    usuarios.append(usuario)
    print("\n=== Usuário criado com sucesso! ===")

def listar_usuarios(usuarios):
    if not usuarios:
        print("\n@@@ Nenhum cliente cadastrado! @@@")
        return

    print("\n=== Lista de Clientes ===")
    for usuario in usuarios:
        print("=" * 50)
        print(f"Nome: {usuario.nome}")
        print(f"CPF: {usuario.cpf}")
        print(f"Endereço: {usuario.endereco}")
        print("=" * 50)

def criar_conta(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(numero_conta, usuario)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(conta)

def buscar_conta_por_cpf(cpf, contas):
    for conta in contas:
        if conta.cliente.cpf == cpf:
            return conta
    print("\n@@@ Conta não encontrada! @@@")
    return None

def executar_menu():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(usuarios, contas)
        elif opcao == "s":
            sacar(usuarios, contas)
        elif opcao == "e":
            exibir_extrato(usuarios, contas)
        elif opcao == "nu":
            criar_usuario(usuarios, contas)
        elif opcao == "nc":
            criar_conta(usuarios, contas)
        elif opcao == "lc":
            listar_usuarios(usuarios)
        elif opcao == "cc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nSaindo do sistema...")
            break
        else:
            print("\n@@@ Opção inválida! Tente novamente. @@@")


# Executar o sistema
executar_menu()