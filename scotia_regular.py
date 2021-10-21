from helper import *


def open_close(transactions):
    """
    purpose: extract open and close balance
    transactions (df): transaction dataframe
    """
    open = transactions[transactions['Transaction'] == 'Opening Balance']
    close = transactions[transactions['Transaction'] == 'Closing Balance']
    print(open)
    print(close)

    open_amount = open['Amount'].values
    close_amount = close['Amount'].values
    diff = close_amount - open_amount
    print('Difference:', diff)


def transaction_summary(transactions):
    """
    purpose: create transaction summary
    transactions (df): transaction dataframe
    """
    # extract balance from transactions
    transactions = transactions[~transactions['Transaction'].str.contains('Balance')]

    # group transactions
    transactions['Type'] = 'Others'

    withdraw = [x.lower() for x in config['withdraw']]
    deposit = [x.lower() for x in config['deposit']]
    transactions.loc[transactions['Transaction'].str.lower().str.contains('|'.join(withdraw)), 'Type'] = 'Withdraw'
    transactions.loc[transactions['Transaction'].str.lower().str.contains('|'.join(deposit)), 'Type'] = 'Deposit'

    # add positive and negative for amounts
    transactions.loc[transactions['Type'] == 'Withdraw', 'Amount'] = transactions['Amount'] * -1

    consolidate = transactions.groupby(['Type', 'Transaction']).sum().stb.subtotal()

    # format amount
    consolidate['Amount'] = consolidate['Amount'].map('{:,.2f}'.format)
    print(consolidate)


if __name__ == '__main__':
    # set pdf statement path
    file = config['file']

    # extract pdf texts
    pdf = extract_text(file)

    # use regex to parse date, transactions and amount info
    date = "(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}"
    trans = ".+?"
    amount = "[$0-9,-]+\.{1}\d{2}"

    pattern = f"({date}) ({trans}) ({amount})"
    transactions = extract_transactions(pdf, pattern)

    # extract open close balance
    open_close(transactions)

    # create summary
    transaction_summary(transactions)
    print('Complete!')

