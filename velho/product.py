# import psycopg2 as db

# print('grande menu')
# print('1. Inserir')
# print('0. Exit')

menu=input('escolha uma opcao para o menu')

match menu:
    case 0: 
        print('exit')
    case 1:
        print('Inserir')
    case 2:
        print('update')

# con = db.connect(
#     host="127.0.0.1",
#     database="produtos",
#     user="postgres",
#     password="71101959Aa"
# )

# cur=con.cursor()

# cur.execute("insert into produto (id,name) values (2,'bomdia')")

# cur.execute("select id, name from produto")
# rows=cur.fetchall()
# for r in rows:
#     print(f"id {r[0]} name {r[1]}")

# con.commit()

# cur.close()
# con.close()