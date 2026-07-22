

class Player:
    def __init__(self, level, xp, coins, xpmult, coinmult):
        self.level = level
        self.xp = xp
        self.coins = coins
        self.xp_mult = xpmult
        self.coin_mult = coinmult
        self.max_xp = 10
        
    def gainxp(self, xp, silent = False):
        gain = 0
        if silent:
            gain = xp
        else:
            gain = xp * self.xp_mult
            print(f'parabens, vc ganhou {gain} de xp!')
        self.xp += gain
        
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp = self.level * 10
            print("level up!")

        
    def gaincoins (self, coins):
        self.coins += coins * self.coin_mult
        print(f"parabens, voce ganhou {coins} moedas\nquantidade de moedas: {self.coins}")
    
    def show(self, tasklist):
        print('==================================\n'
        f'xp - {self.xp} / {self.max_xp}\n'
        f'moedas - {self.coins}\n'
        f'multiplicador de xp - {self.xp_mult}\n'
        f'multiplicador de moedas - {self.coin_mult}\n'
        'tarefas pendentes:\n')
        for item in tasklist:
            print(f'tarefa: {item.name} - id: {item.id}')

class Shop:
    def __init__(self, products):
        self.products = products
    def buy(self, id, player):
        total_xp = player.xp
        for i in range(1, player.level):
            total_xp += i *10
        player.xp = 0
        player.level = 1
        player.max_xp = 10
        for i in self.products:
            if i.id == id:
                if i.value > player.coins or i.xp_value > total_xp:
                    print('voce não tem dinheiro ou xp o suficiente para comprar esse produto')
                elif i.kind == 'mult':
                    player.xp_mult += i.xp_mult
                    player.coin_mult += i.coin_mult
                total_xp -= i.xp_value
                player.coins -= i.value
                player.gainxp(total_xp, True)
                break
        
    def show(self):
        for product in self.products:
            print('==================================\n' \
                f'produto - {product.name}' \
                f'preço em moedas - {product.value}' \
                f'preço em xp - {product.xp_value}' \
                f'descrição - {product.desc}' \
                f'id - {product.id}' \
                '==================================\n')
        while True:
            ask = input('o que gostaria de comprar? (digite o id do produto para comprar e leave para sair da loja) ').lower()
            if ask == 'leave':
                break
            else:
                self.buy(int(ask), player)


class Product:
    def __init__(self, name, value, xp_value, description, id, xp_mult, coin_mult, kind):
        self.name = name
        self.value = value
        self.xp_value = xp_value
        self.desc = description
        self.id = id
        self.xp_mult = xp_mult
        self.coin_mult = coin_mult
        self.kind = kind
class Task:
    def __init__(self, name, dif, id):
        self.name = name
        self.dif = dif
        self.id = id
tasklist = []
player = Player(1, 0, 0, 1, 1)
shop = Shop([Product('multiplicador de xp', 30, 0, 'adiciona 0.5 ao seu multiplicador de xp', 1, 0.5, 0, 'mult'),
             Product('multiplicador de moedas', 30, 10, 'adiciona 0.5 ao seu multiplicador de moedas', 2, 0, 0.5, 'mult'),
             Product('multiplicador geral', 40, 30, 'adiciona 1 a ambos os multiplicadores', 3, 1, 1, 'mult'),
             Product('30 minutos livres', 30, 30, 'te dá 30 minutos livres para fazer o que quiser', 4, 0, 0, 'mult')])

def Add_task(tasklist,):
    id = 1
    task = input('Que tarefa deseja adicionar? ')
    dif = input('Qual a dificuldade? (facil, medio ou dificil) ')
    while dif.lower() not in ['facil', 'medio', 'dificil']:
        dif = input('Digite uma dificuldade valida')
    for iten in tasklist:
        id += 1
    tasklist.append(Task(task, dif, id))
    return tasklist

def Rem_task(tasklist, taskid, player = player):
    for i in tasklist:
        if i.id == taskid:
            match i.dif:
                case 'facil':
                    player.gainxp(2)
                case 'medio':
                    player.gainxp(4)
                case 'dificil':
                    player.gainxp(6)
                case _:
                    print('como diabos vc colocou uma dificuldade que não existe?')
                    player.gainxp(-99999999)
                    print('penalidade para vc n fazer isso de novo!')
            tasklist.remove(i)
            
    
    for i, task in enumerate(tasklist, start=1):
        task.id = i
    if tasklist == []:
        print ('parabens! voce completou todas as tarefas!')
        player.gainxp(4)
    return tasklist

while True:
    ask = input('O que deseja fazer? (digite help ou ? para ver os comandos): ')
    match ask:
        case "help":
            print('==================================\n' \
                '"add" - adicionar tarefa\n' \
                '"rem" - remover tarefa\n' \
                '"shop" - abrir a loja\n' \
                '"leave" - encerrar o programa\n' \
                '"help" - mostrar essa mensagem\n' \
                '"?" - mostrar essa mensagem' \
                '==================================')
        case "?":
            print('==================================\n' \
                '"add" - adicionar tarefa\n' \
                '"rem" - remover tarefa\n' \
                '"shop" - abrir a loja\n' \
                '"show" - mostrar seus dados e lista de tarefas'
                '"leave" - encerrar o programa\n' \
                '"help" - mostrar essa mensagem\n' \
                '"?" - mostrar essa mensagem' \
                '==================================')
        case 'add':
            Add_task(tasklist)
        case 'rem':
            for item in tasklist:
                print(f'tarefa: {item.name} - id: {item.id}')
            which = input('digite o id da tarefa que deseja remover: ')
            Rem_task(tasklist, int(which))
        case 'shop':
            shop.show()
        case 'show':
            player.show(tasklist)
        case 'leave':
            break