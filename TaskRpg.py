class Player:
    def __init__(self, level, xp, coins, xp_mult, coin_mult):
        self.level = level
        self.xp = xp
        self.coins = coins
        self.xp_mult = xp_mult
        self.coin_mult = coin_mult
        self.max_xp = 10

    def gain_xp(self, xp, silent=False):
        gain = 0
        if silent:
            gain = xp
        else:
            gain = xp * self.xp_mult
            print(f'congrats, you gained {gain} xp!')
        self.xp += gain

        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp = self.level * 10
            print("level up!")

    def gain_coins(self, coins):
        self.coins += coins * self.coin_mult
        print(f"congrats, you gained {coins} coins\ncoin amount: {self.coins}")

    def show(self, task_list):
        print('==================================\n'
              f'xp - {self.xp} / {self.max_xp}\n'
              f'coins - {self.coins}\n'
              f'xp multiplier - {self.xp_mult}\n'
              f'coin multiplier - {self.coin_mult}\n'
              'pending tasks:\n')
        for item in task_list:
            print(f'task: {item.name} - id: {item.id}')


class Shop:
    def __init__(self, products):
        self.products = products

    def buy(self, id, player):
        total_xp = player.xp
        for i in range(1, player.level):
            total_xp += i * 10
        player.xp = 0
        player.level = 1
        player.max_xp = 10
        for product in self.products:
            if product.id == id:
                if product.value > player.coins or product.xp_value > total_xp:
                    print('you do not have enough money or xp to buy this product')
                elif product.kind == 'mult':
                    player.xp_mult += product.xp_mult
                    player.coin_mult += product.coin_mult
                total_xp -= product.xp_value
                player.coins -= product.value
                player.gain_xp(total_xp, True)
                break

    def show(self):
        for product in self.products:
            print('==================================\n'
                  f'product - {product.name}'
                  f'coin price - {product.value}'
                  f'xp price - {product.xp_value}'
                  f'description - {product.desc}'
                  f'id - {product.id}'
                  '==================================\n')
        while True:
            ask = input('what would you like to buy? (type the product id to buy or leave to exit the shop) ').lower()
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


task_list = []
player = Player(1, 0, 0, 1, 1)
shop = Shop([Product('xp multiplier', 30, 0, 'adds 0.5 to your xp multiplier', 1, 0.5, 0, 'mult'),
             Product('coin multiplier', 30, 10, 'adds 0.5 to your coin multiplier', 2, 0, 0.5, 'mult'),
             Product('general multiplier', 40, 30, 'adds 1 to both multipliers', 3, 1, 1, 'mult'),
             Product('30 free minutes', 30, 30, 'gives you 30 free minutes to do whatever you want', 4, 0, 0, 'mult')])


def add_task(task_list):
    id = 1
    task = input('What task would you like to add? ')
    dif = input('What is the difficulty? (easy, medium or hard) ')
    while dif.lower() not in ['easy', 'medium', 'hard']:
        dif = input('Enter a valid difficulty ')
    for item in task_list:
        id += 1
    task_list.append(Task(task, dif, id))
    return task_list


def remove_task(task_list, task_id, player=player):
    for item in task_list:
        if item.id == task_id:
            match item.dif:
                case 'easy':
                    player.gain_xp(2)
                case 'medium':
                    player.gain_xp(4)
                case 'hard':
                    player.gain_xp(6)
                case _:
                    print('how on earth did you set a difficulty that does not exist?')
                    player.gain_xp(-99999999)
                    print('penalty so you do not do that again!')
            task_list.remove(item)

    for i, task in enumerate(task_list, start=1):
        task.id = i
    if task_list == []:
        print('congrats! you completed all your tasks!')
        player.gain_xp(4)
    return task_list


while True:
    ask = input('What would you like to do? (type help or ? to see the commands): ')
    match ask:
        case "help":
            print('==================================\n'
                  '"add" - add a task\n'
                  '"rem" - remove a task\n'
                  '"shop" - open the shop\n'
                  '"leave" - end the program\n'
                  '"help" - show this message\n'
                  '"?" - show this message'
                  '==================================')
        case "?":
            print('==================================\n'
                  '"add" - add a task\n'
                  '"rem" - remove a task\n'
                  '"shop" - open the shop\n'
                  '"show" - show your data and task list'
                  '"leave" - end the program\n'
                  '"help" - show this message\n'
                  '"?" - show this message'
                  '==================================')
        case 'add':
            add_task(task_list)
        case 'rem':
            for item in task_list:
                print(f'task: {item.name} - id: {item.id}')
            which = input('enter the id of the task you want to remove: ')
            remove_task(task_list, int(which))
        case 'shop':
            shop.show()
        case 'show':
            player.show(task_list)
        case 'leave':
            break