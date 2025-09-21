import mysql.connector

def coneccao(Host:str,User:str,Password:str,Database:str):
    '''Set para a conexão com o banco de dados 

    ----- Sintaxe ----- 

    coneccao ( Host , User , Password , Database )

    Host = IP ou nome de onde esta localizado o host(Normalmente localhost)
    
    User = Nome de usuário para logar no banco de dados

    password = A senha para entrar no banco de dados

    database = nome do banco de dados com o qual irá trabalhar'''
    
    global mydb
    #variavel global para ser utilizado nas outras funções

    mydb = mysql.connector.connect(
            host=Host,
            user = User,
            password=Password,
            database=Database,
            )
    
def select(tabela:str,parametros:list):
    '''Função para listar valores de uma tabela no banco de dados

    ----- Sintaxe -----
    
    MySQL : SELECT parametros FROM tabela 
    
    select( tabela , parametros ):
    
    tabela = nome da tabela que será realizada a pesquisa

    parametros = lista de parametros que deseja incluir na lista podendo deixar somente ['*'] para procurar tudo

    ----- exemplo -----

    select ( "cliente" , [ "*" ] )

    ou
    
    select ( "cliente" , [ "nome" , "e-mail" ] )    '''

    banco = mydb.cursor()
    try:       
        banco.execute("SELECT "+', '.join(parametros)+" FROM "+tabela+";")
        select_result = banco.fetchall()
        for c in select_result:
            print(c)

    except mysql.connector.Error as err:
        # Erros expecificos do MySQL Connector
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            select_result=("Erro ao tentar selecionar dados: Usuário ou senha estão incorretos")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            select_result=("Erro ao tentar selecionar dados: Banco de dados não existente")
        else:
            select_result=(f"Erro ao tentar selecionar dados: {err}")

    except Exception as e:
        # Outras exceções inexperadas do python
        select_result=(f"Erro ao tentar selecionar dados: um erro inesperado com Python ocorreu: {e}")
    
    print(select_result)
    #Mostra o resultado, seja bem sucedido ou mostra o erro

def delete(tabela:str,parametro:str,valor:str):
    '''Função para deletar dados em uma tabela no banco de dados

    ----- onde -----
    
    MySQL :  DELETE FROM tabela WHERE parametro = valor
    
    delete( tabela , parametros , valor):

    tabela = nome da tabela que será realizada a exclusão

    parametro = parametro que será usado para a exclusão ( Normalmente ID da tabela)

    valor = valor do parametro para a exclusão

    ----- exemplo -----

    delete ( "cliente" , "id_cliente" , "25" )     '''

    try:
        banco = mydb.cursor()
        sql=("DELETE FROM "+tabela+" WHERE "+parametro+" = "+valor)
        banco.execute(sql)
        mydb.commit()
        delete_result=("Linha deletada")

    except mysql.connector.Error as err:
        # Erros expecificos do MySQL Connector
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            delete_result=("Erro ao tentar excluir dados: Usuário ou senha estão incorretos")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            delete_result=("Erro ao tentar excluir dados: Banco de dados não existente")
        else:
            delete_result=(f"Erro ao tentar excluir dados: {err}")

    except Exception as e:
        # Outras exceções inexperadas do python
        delete_result=(f"Erro ao tentar excluir dados: um erro inesperado com Python ocorreu: {e}")
    print(delete_result)
    #Mostra o resultado, seja bem sucedido ou mostra o erro

def insert(tabela:str,colunas:list,valores:list):
    '''Função para inserir dados em uma tabela no banco de dados

    ----- onde -----
    
    MySql =  INSERT INTO tabela ( colunas ) VALUES ( valores )

    insert ( tabela , colunas , valores )

    tabela = nome da tabela que será realizada a adição

    colunas = lista dos nomes das colunas da tabela onde os valores serão introduzidos

    valor = lista de valores que será inserido nas colunas

    ----- exemplo -----

    insert ( "cliente" , [ "nome" , "cidade" ] , [ "João" , "Belém" ] )

    '''
    
    if len(colunas)!=len(valores):
            print("Erro de Parametros!")
    # garantia de que o número de colunas selecionadas e o número de dados a ser inseridos sejam iguais e um erro não ocorra 
    
    else:
        try:
            banco = mydb.cursor()
            sql = ("INSERT INTO "+tabela+" ("+', '.join(colunas)+") VALUES ('"+"', '".join(valores)+"')")
            banco.execute(sql)
            mydb.commit()
            insert_result=("Dados inseridos com sucesso")
        
        except mysql.connector.Error as err:
                # Erros expecificos do MySQL Connector
                if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    insert_result=("Erro ao tentar inserir dados: Usuário ou senha estão incorretos")
                elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                    insert_result=("Erro ao tentar inserir dados: Banco de dados não existente")
                else:
                    insert_result=(f"Erro ao tentar inserir dados: {err}")

        except Exception as e:
            # Outras exceções inexperadas do python
            insert_result(f"Erro ao tentar inserir dados: um erro inesperado com Python ocorreu: {e}")
    
    print(insert_result)
    #Mostra o resultado, seja bem sucedido ou mostra o erro

def update(tabela:str,colunas:list,valores:list,condicao:list,valor_condicao:list):
    '''Função para atualizar dados em uma tabela no banco de dados

    ----- onde -----
    
    MySQL =  UPDATE tabela SET ( colunas = valores ) WHERE condicao = valor_condicao

    update ( tabela , colunas , valores , condicao , valor_condicao)

    tabela = nome da tabela que será realizada a atualização

    colunas = lista das colunas onde os valores serão atualizados

    valor = lista de valores que será atualizada nas colunas

    condicao = nome da coluna que será usada como parametro para substituição (Normalmente ID)
        
    valor_condicao = valor da coluna usada como parametro

    ----- exemplo -----

    update ( "cliente" , [ "nome" , "cidade" ] , [ "Fernando" , "Rio de Janeiro" ] , [ "id_cliente" ] , [ "26" ])

    '''
    
    try:
        # garantia de que o número de colunas selecionadas e o número de dados a ser inseridos sejam iguais e um erro não ocorra 
        if len(colunas)!=len(valores):
            update_result=("Erro de Parametros!")
        # garantia de que o número de condições selecionadas e o número de dados a condicionados sejam iguais para não ocorrer outro erro
        elif len(condicao)!=len(valor_condicao):
            update_result=("Erro de condições!")
        
        else:
            sets_parametros=[]
            sets_condicao=[]
            # sets_X existem para formatar a união das colunas com os dados garantindo que seja usado no SQL
            for c in range(len(colunas)):
                # sets_parametros ficará :  colunas = 'valores' 
                sets_parametros.append(colunas[c]+"='"+valores[c]+"'")
            for c in range(len(condicao)):
                # sets_condicao ficará :  condicao = 'valor_condicao' 
                sets_condicao.append(condicao[c]+"='"+valor_condicao[c]+"'")
            try:
                banco = mydb.cursor()
                sql=("UPDATE "+tabela+" SET "+', '.join(sets_parametros)+" WHERE "+','.join(sets_condicao)+";")
                banco.execute(sql)
                mydb.commit()
                update_result=("Dados atualizados com sucesso")
            
            except mysql.connector.Error as err:
                # Erros expecificos do MySQL Connector
                if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    update_result=("Erro ao tentar atualizar dados: Usuário ou senha estão incorretos")
                elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                    update_result=("Erro ao tentar atualizar dados: Banco de dados não existente")
                else:
                    update_result=(f"Erro ao tentar atualizar dados: {err}")

            except Exception as e:
                # Outras exceções inexperadas do python
                update_result=(f"Erro ao tentar atualizar dados: um erro inesperado com Python ocorreu: {e}")
    except:
        update_result=("Um erro inesperado ocorreu ")

    print(update_result)
    #Mostra o resultado, seja bem sucedido ou mostra o erro