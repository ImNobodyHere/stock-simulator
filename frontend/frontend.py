import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Simulateur Bourse", page_icon="📈", layout="centered")

if 'users' not in st.session_state:
    st.session_state.users = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

STOCKS = {
    'APPL': {'name': 'Apple Inc.', 'price': 150.0},
    'GGL': {'name': 'Alphabet Inc.', 'price': 2800.0},
    'MSFT': {'name': 'Microsoft Corp.', 'price': 350.0},
    'AMZN': {'name': 'Amazon.com', 'price': 3200.0},
    'TSLA': {'name': 'Tesla Inc.', 'price': 700.0},
}

def create_user(username, password, initial_balance=10000):
    if username in st.session_state.users:
        return False, "Ce nom d'utilisateur existe déjà"

    st.session_state.users[username] = {
        'password': password,
        'balance': initial_balance,
        'portfolio': {},  # {symbol: quantity}
        'transactions': []
    }
    return True, "Compte créé avec succès"


def login_user(username, password):
    if username not in st.session_state.users:
        return False, "Utilisateur introuvable"

    if st.session_state.users[username]['password'] != password:
        return False, "Mot de passe incorrect"

    st.session_state.current_user = username
    return True, f"Bienvenue {username} !"


def logout_user():
    st.session_state.current_user = None


def get_user_data():
    if st.session_state.current_user:
        return st.session_state.users[st.session_state.current_user]
    return None


def buy_stock(symbol, quantity):
    user_data = get_user_data()
    if not user_data:
        return False, "Utilisateur non connecté"

    if symbol not in STOCKS:
        return False, "Action introuvable"

    price = STOCKS[symbol]['price']
    total_cost = price * quantity

    if user_data['balance'] < total_cost:
        return False, f"Fonds insuffisants (coût: {total_cost:.2f}€)"

    user_data['balance'] -= total_cost

    if symbol in user_data['portfolio']:
        user_data['portfolio'][symbol] += quantity
    else:
        user_data['portfolio'][symbol] = quantity

    user_data['transactions'].append({
        'date': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'type': 'ACHAT',
        'symbol': symbol,
        'quantity': quantity,
        'price': price,
        'total': total_cost
    })

    return True, f" Achat réussi : {quantity} {symbol} pour {total_cost:.2f}€"




def show_auth_page():

    st.markdown("<h1 style='text-align: center;'> Simulateur de Bourse</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Plateforme de trading virtuel pour étudiants</p>",
                unsafe_allow_html=True)

    st.markdown("---")


    tab1, tab2 = st.tabs([" Connexion", " Inscription"])

    with tab1:
        st.subheader("Se connecter")

        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error(" Veuillez remplir tous les champs")
                else:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(f" {message}")


    with tab2:
        st.subheader("Créer un compte")

        with st.form("signup_form"):
            new_username = st.text_input("Choisir un nom d'utilisateur")
            new_password = st.text_input("Choisir un mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            initial_balance = st.number_input("Solde initial (€)", min_value=1000, value=10000, step=1000)

            submit = st.form_submit_button("S'inscrire", use_container_width=True)

            if submit:
                if not new_username or not new_password:
                    st.error(" Veuillez remplir tous les champs")
                elif len(new_username) < 3:
                    st.error(" Le nom d'utilisateur doit contenir au moins 3 caractères")
                elif len(new_password) < 4:
                    st.error(" Le mot de passe doit contenir au moins 4 caractères")
                elif new_password != confirm_password:
                    st.error(" Les mots de passe ne correspondent pas")
                else:
                    success, message = create_user(new_username, new_password, initial_balance)
                    if success:
                        st.success(f" {message}")
                        st.info("Vous pouvez maintenant vous connecter")
                    else:
                        st.error(f" {message}")




def show_main_page():

    user_data = get_user_data()
    username = st.session_state.current_user

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f" Bienvenue {username}")
    with col2:
        if st.button(" Déconnexion"):
            logout_user()
            st.rerun()

    st.markdown(f"###  Solde : *{user_data['balance']:.2f} €*")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([" Acheter des actions", " Mon Portfolio", " Historique"])

    with tab1:
        st.subheader("Actions Disponibles")

        for symbol, info in STOCKS.items():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.markdown(f"*{symbol}*")
                    st.caption(info['name'])

                with col2:
                    st.markdown(f"Prix : *{info['price']:.2f} €*")

                with col3:
                    if st.button("Acheter", key=f"buy_{symbol}"):
                        st.session_state.selected_stock = symbol

                st.markdown("---")

        if 'selected_stock' in st.session_state and st.session_state.selected_stock:
            selected = st.session_state.selected_stock
            st.markdown(f"### Acheter {selected} - {STOCKS[selected]['name']}")

            with st.form("buy_form"):
                quantity = st.number_input(
                    "Quantité",
                    min_value=1,
                    max_value=1000,
                    value=1,
                    step=1
                )

                total_cost = quantity * STOCKS[selected]['price']
                st.info(f" Coût total : *{total_cost:.2f} €*")

                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button(" Confirmer l'achat", use_container_width=True)
                with col2:
                    cancel = st.form_submit_button(" Annuler", use_container_width=True)

                if submit:
                    success, message = buy_stock(selected, quantity)
                    if success:
                        st.success(message)
                        st.balloons()
                        del st.session_state.selected_stock
                        st.rerun()
                    else:
                        st.error(message)

                if cancel:
                    del st.session_state.selected_stock
                    st.rerun()

    with tab2:
        st.subheader("Mon Portefeuille")

        if not user_data['portfolio']:
            st.info(" Votre portfolio est vide. Achetez des actions pour commencer !")
        else:
            total_value = 0

            for symbol, quantity in user_data['portfolio'].items():
                price = STOCKS[symbol]['price']
                value = quantity * price
                total_value += value

                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 2, 2])

                    with col1:
                        st.markdown(f"*{symbol}*")
                        st.caption(STOCKS[symbol]['name'])

                    with col2:
                        st.metric("Quantité", quantity)

                    with col3:
                        st.metric("Prix", f"{price:.2f} €")

                    with col4:
                        st.metric("Valeur", f"{value:.2f} €")

                    st.markdown("---")

            st.markdown(f"###  Valeur totale du portfolio : *{total_value:.2f} €*")
            st.markdown(f"*Patrimoine total : {total_value + user_data['balance']:.2f} €*")

    with tab3:
        st.subheader("Historique des Transactions")

        if not user_data['transactions']:
            st.info(" Aucune transaction pour le moment")
        else:
            for trans in reversed(user_data['transactions']):
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

                    with col1:
                        st.markdown(f"*{trans['date']}*")

                    with col2:
                        emoji = "🟢" if trans['type'] == "ACHAT" else "🔴"
                        st.markdown(f"{emoji} {trans['type']}")

                    with col3:
                        st.markdown(f"{trans['quantity']} {trans['symbol']}")

                    with col4:
                        st.markdown(f"*{trans['total']:.2f} €*")
                        st.caption(f"Prix unitaire : {trans['price']:.2f} €")

                    st.markdown("---")



def main():
    if st.session_state.current_user is None:
        show_auth_page()
    else:
        show_main_page()


if __name__ == "_main_":
    main()