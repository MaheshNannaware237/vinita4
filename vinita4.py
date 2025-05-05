import streamlit as st
import hashlib
import time

# Function to generate a unique hash for each block
def generate_hash(block):
    block_string = (
        f"{block['index']}{block['transaction']['holder_name']}"
        f"{block['transaction']['account_number']}{block['transaction']['ifsc_code']}"
        f"{block['transaction']['type']}{block['transaction']['amount']}"
        f"{block['timestamp']}{block['previous_hash']}"
    )
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to create a new block
def create_block(index, transaction, previous_hash):
    return {
        "index": index,
        "transaction": transaction,
        "timestamp": time.time(),
        "previous_hash": previous_hash
    }

# Initialize blockchain with genesis block
def init_blockchain():
    genesis_transaction = {
        "holder_name": "Genesis Account",
        "account_number": "0000000000",
        "ifsc_code": "BANK0000000",
        "type": "Initialization",
        "amount": 0.0
    }

    genesis_block = {
        "index": 0,
        "transaction": genesis_transaction,
        "timestamp": time.time(),
        "previous_hash": "0"
    }
    return [genesis_block]

# Add a new transaction block
def add_transaction(holder_name, account_number, ifsc_code, txn_type, amount):
    previous_block = st.session_state.blockchain[-1]
    new_index = previous_block["index"] + 1
    previous_hash = generate_hash(previous_block)

    transaction = {
        "holder_name": holder_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "type": txn_type,
        "amount": amount
    }

    new_block = create_block(new_index, transaction, previous_hash)
    st.session_state.blockchain.append(new_block)

# Initialize session state
if "blockchain" not in st.session_state:
    st.session_state.blockchain = init_blockchain()

# Streamlit UI
st.title("🏦 Bank Ledger Blockchain")

st.sidebar.header("➕ Add New Transaction")
with st.sidebar.form("transaction_form"):
    name = st.text_input("Account Holder Name")
    acc_no = st.text_input("Account Number")
    ifsc = st.text_input("IFSC Code")
    txn_type = st.selectbox("Transaction Type", ["Deposit", "Withdrawal", "Transfer"])
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if name and acc_no and ifsc and amount > 0:
            add_transaction(name, acc_no, ifsc, txn_type, amount)
            st.success("Transaction added to the blockchain!")
        else:
            st.error("Please fill all fields correctly.")

st.subheader("📄 Blockchain Ledger")
for block in st.session_state.blockchain:
    txn = block["transaction"]
    with st.expander(f"Block {block['index']} - {txn['holder_name']}"):
        st.write(f"**Account Number:** {txn['account_number']}")
        st.write(f"**IFSC Code:** {txn['ifsc_code']}")
        st.write(f"**Transaction Type:** {txn['type']}")
        st.write(f"**Amount:** ${txn['amount']}")
        st.write(f"**Timestamp:** {time.ctime(block['timestamp'])}")
        st.code(f"{block['previous_hash']}", language="text")
