from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime



class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class pessoa_fisica(cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = historico()

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
            print("\nOperação inválida! Saldo insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("Operação inválida! Valor informado é inválido!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDeposito realizado com sucesso!")

        else:
            print("\nOperação inválida! Valor informado é inválido!")
            return False
        
        return True
    
class conta_corrente(conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente) 
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nOperação recusada! Número máximo de saques díarios excedido!")

        elif excedeu_saques:
            print("\nOperação recusada! Número máximo de saques diário excedido!")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """

class historico: 

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
                    "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
                }
            )

class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)




   #FIXME: sistema não está operando corretamente (necessita de atualização mais avançada no método, para funcionar com as classes modeladas)


def novo_cliente(clientes):
     cpf= input("Informe o CPF (apenas números): ")
     cliente = filtro_de_cliente(cpf, clientes)

     if cliente:
          print("Cliente já possui conta")
          return
     nome = input("Digite o nome completo: ")
     nascimento = input("Informe a data de nascimento (dia/mês/ano): ")
     endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ")
     clientes.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})
     print("Novo cliente criado com sucesso!")


def filtro_de_cliente(cpf, cliente):
     cliente_filtrados = [cliente for cliente in clientes if cliente["cpf"] == cpf]
     return clientes_filtrados[0] if clientes_filtrados else None


def nova_conta(agencia, numero_conta, clientes):
     cpf = input("Informe o CPF: ")
     cliente = filtro_de_cliente(cpf, clientes)
     if cliente:
          print("\nConta criada com sucesso!")
          return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
     print ("cliente não encontrado! Criação de conta encerrada!")


def depositar(saldo, valor, extrato, /):
    if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                Print("\nDeposito realizado!")

    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def extrato_em_conta(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")






menu = """
      ~~~~ MENU INICIAL ~~~~
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Cliente
[5] Nova Conta
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"
clientes = []
contas = []

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = sacar(
             saldo=saldo,
             valor=valor,
             extrato=extrato,
             limite=limite,
             numero_saques=numero_saques,
             limite_saques=LIMITE_SAQUES,
        )

    elif opcao == "3":
        extrato_em_conta(saldo, extrato=extrato)

    elif opcao == "4":
        novo_cliente(clientes)

    elif opcao == "5":
        numero_conta = len(contas) + 1
        conta = nova_conta(AGENCIA, numero_conta, clientes)
        if conta:
             contas.append(conta)
                      
    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")