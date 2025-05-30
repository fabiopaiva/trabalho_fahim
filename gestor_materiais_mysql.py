import mysql.connector

# Conectar ao banco MySQL com tratamento de erro
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="500195",  # altere aqui sua senha
        database="escola_materiais"
    )
    cursor = conn.cursor()
    print("✅ Conectado ao banco de dados com sucesso.")
except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar ao MySQL: {err}")
    exit()

# Função: Adicionar material
def adicionar_material(nome, tipo, quantidade, localizacao="", observacao=""):
    cursor.execute('''
        INSERT INTO materiais (nome, tipo, quantidade, localizacao, observacao)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nome, tipo, quantidade, localizacao, observacao))
    conn.commit()
    print("✅ Material adicionado!")

# Função: Listar materiais
def listar_materiais():
    cursor.execute('SELECT * FROM materiais')
    resultados = cursor.fetchall()
    if resultados:
        for row in resultados:
            print(row)
    else:
        print("📭 Nenhum material encontrado.")

# Função: Atualizar material
def atualizar_material(id, nome=None, tipo=None, quantidade=None, localizacao=None, observacao=None):
    cursor.execute('SELECT * FROM materiais WHERE id = %s', (id,))
    material = cursor.fetchone()
    if material is None:
        print("❌ Material não encontrado.")
        return

    nome = nome or material[1]
    tipo = tipo or material[2]
    quantidade = quantidade if quantidade is not None else material[3]
    localizacao = localizacao or material[4]
    observacao = observacao or material[5]

    cursor.execute('''
        UPDATE materiais
        SET nome = %s, tipo = %s, quantidade = %s, localizacao = %s, observacao = %s
        WHERE id = %s
    ''', (nome, tipo, quantidade, localizacao, observacao, id))
    conn.commit()
    print("✅ Material atualizado!")

# Função: Deletar material
def deletar_material(id):
    cursor.execute('DELETE FROM materiais WHERE id = %s', (id,))
    conn.commit()
    print("✅ Material deletado!")

# Menu principal
if __name__ == '__main__':
    print("\n📦 Sistema de Gestão de Materiais Escolares\n")

    while True:
        print("\n1 - Adicionar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Deletar")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            tipo = input("Tipo (Cadeira, Mesa, Computador, etc): ")
            quantidade = int(input("Quantidade: "))
            localizacao = input("Localização (sala, bloco, etc): ")
            observacao = input("Observação: ")
            adicionar_material(nome, tipo, quantidade, localizacao, observacao)

        elif opcao == '2':
            listar_materiais()

        elif opcao == '3':
            try:
                id = int(input("ID do material: "))
                nome = input("Novo nome (ou Enter para manter): ")
                tipo = input("Novo tipo (ou Enter para manter): ")
                quantidade = input("Nova quantidade (ou Enter para manter): ")
                localizacao = input("Nova localização (ou Enter para manter): ")
                observacao = input("Nova observação (ou Enter para manter): ")

                atualizar_material(
                    id,
                    nome if nome else None,
                    tipo if tipo else None,
                    int(quantidade) if quantidade else None,
                    localizacao if localizacao else None,
                    observacao if observacao else None
                )
            except ValueError:
                print("❌ ID ou quantidade inválidos.")

        elif opcao == '4':
            try:
                id = int(input("ID do material: "))
                deletar_material(id)
            except ValueError:
                print("❌ ID inválido.")

        elif opcao == '5':
            print("👋 Encerrando o sistema.")
            break
        else:
            print("❌ Opção inválida.")

    cursor.close()
    conn.close()

