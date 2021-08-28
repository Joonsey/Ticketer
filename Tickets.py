from database import *


class Ticket:
    

    def __init__(self, id : int, author : str, ctx : str, solved: bool) -> None:
        self.id = id
        self.author = author
        self.context = ctx
        self.solved = bool(solved)
        self.exsist = True


        if not fetchTicket(id):
            insertTicket(id, ctx, author, solved)
            self.date = fetchTicket(id)[0][1]
        else:
            self.exsist = False
            raise Exception(f'Ticket of id ({id}) already exsists.')


    def changeAuthor(self, author):
        if changeAuth(self.id, author) == True:
            self.author = author
        else:
            print('Error changing author.')

    def changeContext(self, ctx):
        if changeCtx(self.id, ctx):
            self.context = ctx
        else:
            print('Error changing context')


    def changeSolvedState(self, solvedState : bool):
        if changeSolved(self.id, solvedState):
            self.solved = solvedState
        else:
            print('Error changing context')

            


    #def makeEntry(self, id, ctx, author, solved):
    #    """never call this method. It's excusively used to initiate the database entry"""
    #    insertTicket(id, ctx, author, solved)


    
    def removeTicket(self):
        try:
            removeTicketById(self.id)
            self.exsist = False

        except:
            print('Ticket already removed.')


    def __str__(self):
        return f"Ticket object with data:  id: {self.id}, author: {self.author}, date: {self.date}, context: {self.context}, solved: {self.solved}"



if __name__ == "__main__":
    wipeDB()

    tickets = [Ticket(i, 'jae', 'lmao', True) for i in range(20)]

    for y, x in enumerate(fetchAllTickets()):

        print(tickets[y])
        print(x)

        #tickets[y].changeContext()


    for y, x in enumerate(fetchAllTickets()):
        
        print(tickets[y])
        print(x)

        

