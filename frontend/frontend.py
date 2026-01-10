import os
from datetime import datetime

users = {}
current_user = None

STOCKS = {
    'APPL': {'name': 'Apple Inc.', 'price': 150.0},
    'GGL': {'name': 'Alphabet Inc.', 'price': 2800.0},
    'MSFT': {'name': 'Microsoft Corp.', 'price': 350.0},
    'AMZN': {'name': 'Amazon.com', 'price': 3200.0},
    'TSLA': {'name': 'Tesla Inc.', 'price': 700.0},
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_user(username, password, balance=10000):
    if username in users:
        return False
    users[username] = {'password': password, 'balance': balance, 'portfolio': {}, 'transactions': []}
    return True


def login(username, password):
    global current_user
    if username not in users or users[username]['password'] != password:
        return False
    current_user = username
    return True


def buy_stock(symbol, qty):
    user = users[current_user]
    price = STOCKS[symbol]['price']
    cost = price * qty
    if user['balance'] < cost:
        return False
    user['balance'] -= cost
    user['portfolio'][symbol] = user['portfolio'].get(symbol, 0) + qty
    user['transactions'].append({
        'date': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'type': 'ACHAT',
        'symbol': symbol,
        'qty': qty,
        'price': price,
        'total': cost
    })
    return True


def login_menu():
    clear()
    print("=== SIMULATEUR DE BOURSE ===\n")
    print("1. Connexion")
    print("2. Inscription")
    print("3. Quitter\n")

    choice = input("Choix: ")

    if choice == '1':
        clear()
        print("=== CONNEXION ===\n")
        u = input("Username: ")
        p = input("Password: ")
        if login(u, p):
            main_menu()
        else:
            print("\nErreur de connexion")
            input("Entree pour continuer...")
            login_menu()

    elif choice == '2':
        clear()
        print("=== INSCRIPTION ===\n")
        u = input("Username: ")
        p = input("Password: ")
        if len(u) < 3 or len(p) < 4:
            print("\nUsername min 3 char, password min 4 char")
            input("Entree...")
            login_menu()
        if create_user(u, p):
            print("\nCompte cree!")
            input("Entree...")
        login_menu()

    elif choice == '3':
        exit()
    else:
        login_menu()


def main_menu():
    global current_user
    clear()
    user = users[current_user]
    print(f"=== BIENVENUE {current_user} ===")
    print(f"Solde: {user['balance']:.2f} EUR\n")
    print("1. Acheter")
    print("2. Portfolio")
    print("3. Historique")
    print("4. Deconnexion\n")

    choice = input("Choix: ")

    if choice == '1':
        buy_menu()
    elif choice == '2':
        portfolio()
    elif choice == '3':
        history()
    elif choice == '4':
        current_user = None
        login_menu()
    else:
        main_menu()


def buy_menu():
    clear()
    print("=== ACTIONS DISPONIBLES ===\n")
    stocks = list(STOCKS.items())
    for i, (sym, info) in enumerate(stocks, 1):
        print(f"{i}. {sym} - {info['name']} - {info['price']:.2f} EUR")
    print(f"{len(stocks) + 1}. Retour\n")

    try:
        choice = int(input("Choix: "))
        if choice == len(stocks) + 1:
            main_menu()
        elif 1 <= choice <= len(stocks):
            sym = stocks[choice - 1][0]
            clear()
            print(f"=== ACHETER {sym} ===\n")
            print(f"Prix: {STOCKS[sym]['price']:.2f} EUR")
            qty = int(input("Quantite: "))
            total = qty * STOCKS[sym]['price']
            print(f"Total: {total:.2f} EUR")
            if input("Confirmer? (o/n): ") == 'o':
                if buy_stock(sym, qty):
                    print("Achat reussi!")
                else:
                    print("Fonds insuffisants")
            input("\nEntree...")
            buy_menu()
    except:
        buy_menu()


def portfolio():
    clear()
    user = users[current_user]
    print("=== MON PORTFOLIO ===\n")
    if not user['portfolio']:
        print("Portfolio vide")
    else:
        total = 0
        for sym, qty in user['portfolio'].items():
            val = qty * STOCKS[sym]['price']
            total += val
            print(f"{sym}: {qty} actions - {val:.2f} EUR")
        print(f"\nTotal: {total:.2f} EUR")
        print(f"Solde: {user['balance']:.2f} EUR")
        print(f"Patrimoine: {total + user['balance']:.2f} EUR")
    input("\nEntree...")
    main_menu()


def history():
    clear()
    user = users[current_user]
    print("=== HISTORIQUE ===\n")
    if not user['transactions']:
        print("Aucune transaction")
    else:
        for t in reversed(user['transactions']):
            print(f"{t['date']} - {t['type']} - {t['qty']} {t['symbol']} - {t['total']:.2f} EUR")
    input("\nEntree...")
    main_menu()


if __name__ == "__main__":
    login_menu()