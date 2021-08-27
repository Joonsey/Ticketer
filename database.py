from datetime import datetime, time
import sqlite3, random, string

conn = sqlite3.connect('data.db')


c = conn.cursor()


def createDB():
    with conn:
        try:
            c.execute("""CREATE TABLE ticket (id integer, date text, context text, author text, solved text)""")
        except:
            print("Database already exists.")


def insertTicket(id, ctx, author, solved=True):
    with conn:
        if type(solved) == bool or solved.lower() == 'True' or 'False':
            try:
                c.execute("INSERT INTO ticket VALUES (:id, :date, :ctx, :author, :solved)", 
                {"id":id, "date":datetime.now().__str__()[0:-7], "ctx":ctx, "author":author, "solved":str(solved).capitalize()})
            except ValueError:
                print("Insertion of ticket failed, ticket either already exists or input is invalid.")
                raise
            return id
        else:
            print('Invalid value for "solved", variable of type bool expected.')


def fetchTicket(id):
    with conn:
        try:
            c.execute("SELECT * FROM ticket WHERE id=:id", {'id':id})
            return c.fetchall()
        except:
            print('entry does not exists or id is out of range.')


def fetchAllTickets(author=0, orderByTime=False):
    with conn:
        if author:
            try:
                c.execute("SELECT * FROM ticket WHERE author=:author", {"author":author})
            except ValueError:
                print('Invalid author name, not found in database')
        else:
            try:
                c.execute("SELECT * FROM ticket ORDER BY id")
            except:
                print('something went wrong.')
        return c.fetchall()


def wipeDB():
    """USE WITH CAUTION! WILL REMOVE ALL ENTRIES IN ticket TABLE!"""
    with conn:
        try:
            c.execute("DELETE FROM ticket")
            print('Database wiped successfuly!')
        except:
            print('Wipe unsuccessful.')


def changeSolved(id, newValue):
    with conn:
        if type(id) == int:
            try:
                old = fetchTicket(id)
                c.execute("""
                UPDATE ticket
                SET solved = replace(solved, :old, :new)
                WHERE id = :id
                """,
                {"old":old[0][-1], "new":str(newValue), "id":id})
            except:
                print('Change failed.')


def changeCtx(id, newCtx):
    with conn:
        if type(id) == int:
            try:
                old = fetchTicket(id)
                c.execute("""
                UPDATE ticket
                SET context = replace(context, :old, :new)
                WHERE id = :id
                """,
                {"old":old[0][-3], "new":str(newCtx), "id":id})
            except:
                print('Change failed.')
                

def changeAuthor(id, newAuthor):
    with conn:
        if type(id) == int:
            try:
                old = fetchTicket(id)
                c.execute("""
                UPDATE ticket
                SET author = replace(author, :old, :new)
                WHERE id = :id
                """,
                {"old":old[0][-2], "new":str(newAuthor), "id":id})
            except:
                print('Change failed.')


def removeTicketById(id):
    with conn:
        if type(id) == int:
            try:
                c.execute("""
                DELETE
                FROM ticket
                WHERE id = :id
                """,
                {"id":id})
            except:
                print('Removal failed.')


def removeTickets(arr):
    for i in arr:
        removeTicketById(i)


def montyCarloTest(x=0,y=100):
    for i in range(x,y):
        insertTicket(i+1, random.choice(string.ascii_letters), random.choice(string.ascii_letters), True)
    print(f'Test data created with id from range {x} to {y}')
        

conn.commit()


if __name__ == "__main__":
    d = fetchAllTickets()
    for i in d:
        print(i)