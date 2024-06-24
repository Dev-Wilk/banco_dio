from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass  
class Cliente:
    endereco: str
    contas: list = None  

    def __post_init__(self):  
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


@dataclass
class PessoaFisica(Cliente):
    nome: str
    data_nascimento: datetime.date
    cpf: str


@dataclass
class Conta:
    numero: str
    cliente: Cliente
    _saldo: float = 0.0
    _agencia: str = "0001"
    _historico: list = None

    def __post_init__(self):
        self._historico = []

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        if valor > self._saldo or valor <= 0:
            raise ValueError("Valor de saque inválido ou saldo insuficiente")
        self._saldo -= valor
        self._historico.append(("Saque", valor, datetime.now()))

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de depósito inválido")
        self._saldo += valor
        self._historico.append(("Depósito", valor, datetime.now()))


@dataclass
class ContaCorrente(Conta):
    limite: float = 500.0
    limite_saques: int = 3
    _saques_hoje: int = 0

    def sacar(self, valor):
        if self._saques_hoje >= self.limite_saques:
            raise ValueError("Limite de saques diários atingido")
        if valor > self.limite:
            raise ValueError("Valor do saque excede o limite")
        super().sacar(valor)
        self._saques_hoje += 1

    def __str__(self):
        return f"""
            Agência:\t{self._agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)
