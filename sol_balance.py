import psycopg2
from solana.rpc.api import Client
from datetime import datetime
from spl.token.constants import TOKEN_PROGRAM_ID

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="4321",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Establish connection to the Solana RPC endpoint
solana_endpoint = "https://solana-api.projectserum.com"
solana_conn = Client(solana_endpoint)

# Function to get and store SOL balance for each user account
def get_and_store_sol_balances():

    print("Getting and storing SOL balances for all non-zero accounts...")

    # Get current timestamp
    timestamp = datetime.now().isoformat()

    # Get all program accounts using token program id
    program_accounts = solana_conn.get_program_accounts(TOKEN_PROGRAM_ID)

    for account in program_accounts:
        public_key = account["pubkey"]
        balance = solana_conn.get_balance(public_key)
        insert_query = "INSERT INTO solana_balances (public_key, balance, last_update) VALUES (%s, %s, %s)"
        data = (public_key, balance, timestamp)
        cur.execute(insert_query, data)

    conn.commit()

# Call the function to get and store SOL balances for non-zero accounts
get_and_store_sol_balances()

# Close the PostgreSQL connection
cur.close()
conn.close()
