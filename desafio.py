

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta , transacao):
        transacao.resgistrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero , cliente):
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
        saldo = self._saldo
        exedeu_saldo = valor > saldo

        if exedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self.saldo -= valor
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é invalido")

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito feito com sucesso!")
        else:
            print("Valor informado é invalido!")

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
         super().__init__(numero, cliente)
         self.limite = limite
         self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.
            transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque > self.limite_saque

        if excedeu_limite:
            print("Operação falhou! Excedeu o valor de saque.")
        elif excedeu_saque:
            print("Operação falhou! Numero maximo de saques exedido.")
        else:
            return super().sacar(valor)
    
        return False

    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/c: \t\t{self.numero}
            Titular: \t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            [
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            ]
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethood
    def registrar(self, conta):
        pass

class Saque(Transacao):
      