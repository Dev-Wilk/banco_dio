menu = """


[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair


=>"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


while True:
    opcao= input(menu) 

    if opcao == "d":
        valor = float(input("Informe o valor do deposito: "))

        if valor > 0:
            saldo+= valor
            extrato += f"Depósito: R$ {valor:.2f}\n " 
            

        else:
            print("Operação invalida! O valor informado não valido")  

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        exedeu_saldo =valor > saldo
        exedeu_limite = valor > limite
        exedeu_saques = numero_saques >= LIMITE_SAQUES

        if exedeu_saldo:
            print("Falha no saque, valor do saldo insufiente ")

        elif exedeu_limite:
            print("Erro!! O valor do saque exedeu o limite.")

        elif exedeu_saques:
            print("Exedeu o limites de saques possiveis.")

        elif valor>0:
            saldo-= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é invalido.")

    elif opcao =="e" :
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
   

    elif opcao == "q":
        break

    else: 
        print("Operação invalida, selecione operação desejada: ")