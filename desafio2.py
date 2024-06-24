import textwrap
from abc import ABC
from datetime import datetime
from datetime import date
import re

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def validar_data_nascimento(data_nascimento):
        """Valida uma data de nascimento."""
        try:
            datetime.strptime(data_nascimento, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def calcular_idade(self):
        """Calcula a idade da pessoa física."""
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
    
    def validar_cpf(cpf):
        """Valida um CPF brasileiro."""
        cpf = str(cpf)
        cpf = re.sub('[^0-9]', '', cpf)

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

    # Calcula o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = 11 - (soma % 11)
        if resto == 10 or resto == 11:
            resto = 0
        if resto != int(cpf[9]):
            return False

    # Calcula o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = 11 - (soma % 11)
        if resto == 10 or resto == 11:
            resto = 0
        if resto != int(cpf[10]):
            return False

        return True

    def __str__(self):
        return f"Cliente Pessoa Física: {self.nome}, CPF: {self.cpf}, Idade: {self.calcular_idade()}"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()  

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

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            self.historico.registrar(f"Saque de R$ {valor:.2f} realizado em {datetime.now()}")
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self.historico.registrar(f"Depósito de R$ {valor:.2f} realizado em {datetime.now()}")
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def transferir(self, destino, valor):
        if self.sacar(valor):
            destino.depositar(valor)
            self.historico.registrar(f"Transferência de R$ {valor:.2f} para a conta {destino.numero} em {datetime.now()}")
            print("\n=== Transferência realizada com sucesso! ===")
            return True
        else:
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite_saques = limite_saques
        self._numero_saques = 0  

    def get_limite(self):
        return 500  # Exemplo com limite fixo de 500

    def set_limite(self, novo_limite):
        pass

    def sacar(self, valor):
        limite_atual = self.get_limite()
        saques_restantes = self._limite_saques - self._numero_saques

        if valor > limite_atual:
            print(f"\n@@@ Operação falhou! O valor do saque (R$ {valor:.2f}) excede o limite atual (R$ {limite_atual:.2f}). @@@")
        elif self._numero_saques >= self._limite_saques:
            print(f"\n@@@ Operação falhou! Você já atingiu o limite de {self._limite_saques} saques diários. @@@")
        elif not super().sacar(valor):
            return False  # Falha no saque da classe base (saldo insuficiente, etc.)
        else:
            self._numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
            return True

        return False

    def resetar_saques(self):
        self._numero_saques = 0

    def __str__(self):
        titular = self.cliente.nome if isinstance(self.cliente, PessoaFisica) else "Não disponível"
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{titular}
        """



class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar(self, transacao):
        self._transacoes.append(transacao)

    def extrato(self):
        print("\n###### Extrato da Conta ######")
        if not self._transacoes:
            print("Nenhuma transação realizada.")
        else:
            for transacao in self._transacoes:
                tipo = transacao.split()[0]  # Extrai o tipo da transação
                if tipo == "Saque":
                    print(f"- {transacao} (Saldo atual: R$ {self._calcular_saldo_apos_transacao(transacao):.2f})")
                else:  # Depósito ou Transferência
                    print(f"+ {transacao} (Saldo atual: R$ {self._calcular_saldo_apos_transacao(transacao):.2f})")

    def _calcular_saldo_apos_transacao(self, transacao):
        valor = float(transacao.split()[2][3:])  # Extrai o valor da transação
        tipo = transacao.split()[0]
        if tipo == "Saque":
            return self._saldo_atual - valor
        else:  # Depósito ou Transferência
            return self._saldo_atual + valor

    @property
    def _saldo_atual(self):
        saldo = 0
        for transacao in self._transacoes:
            valor = float(transacao.split()[2][3:])
            tipo = transacao.split()[0]
            if tipo == "Saque":
                saldo -= valor
            else:
                saldo += valor
        return saldo


class Transacao(ABC):
    def __init__(self):
        self.data_hora = datetime.now()
        self.tipo = self.__class__.__name__

    @abstractproperty
    def valor(self):
        pass

    def __str__(self):
        return f"{self.tipo} de R$ {self.valor:.2f} em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"

@dataclass
class Saque(Transacao):
    valor: float
    conta: Conta

    def registrar(self):
        if not self.conta.sacar(self.valor):
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self.conta.historico.registrar(self) 

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
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    if len(cliente.contas) > 1:
        print("\n==== Contas do Cliente ====")
        for i, conta in enumerate(cliente.contas):
            print(f"{i+1}. Conta {conta.numero}")
        escolha = int(input("Selecione a conta desejada: ")) - 1
        if 0 <= escolha < len(cliente.contas):
            return cliente.contas[escolha]
        else:
            print("\n@@@ Opção inválida! @@@")
            return
    else:
        return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao.tipo}: R$ {transacao.valor:.2f} em {transacao.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()