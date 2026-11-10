from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Floats, Boolean
from sqlalchemy import select, update, delete


# Создание
engine = create_engine('sqlite:///database.db;')
engine.connect()
metadata = MetaData()
studrnts_table = Table(
		'students', 
		'metadata', 
		Column('id', Integer, primary_key = True),
		Column('name', String(100), nullable = False), 
		Column('group', String(20)), 
		Column('gpa', Float, default = 0.0), 
		Column('is_active', Boolean, default = True),
		)

metadata create_all(engine)
with engine.connect() as connection:
	something = insert(students_table).values(
			name = 'Иванов И И',
			group = 'ИУ10-33',
			gpa = 4.5,
			)
	result = connection.execute(something)
	connection.commit()
	print(f"Добавлена строка с id={result.inserted_primary_key[0]}")

# Чтение
with engine.connect() as connection:
    statement = select(students_table)
    result = connection.execute(statement)

    for row in result:
        print(row.id, row.name, row.is_active)

    statement2 = select(students_table.c.name, students_table.c.gpa)
    result2 = connection.execute(statement2)

    for row in result2:
        print(row.name, row.gpa)

# Обновление
with engine.connect() as connection:
    statement(
        udate(students_table)
        .where(students_table.c.name == 'Петров П. П')
        .values(gpa = 4.6)
        )
result = connection.execute(statement)
connection.commit()
print(f"Обновлено строк {result.rowcount}")

statement2= delete(students_table).where(students_table.c.gpa < 3.5)
result = connection.execute(statement2)
connection.commit()
print(f"Удалено строк {result.rowcount}")
















        
    
