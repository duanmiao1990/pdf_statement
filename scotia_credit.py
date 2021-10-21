import matplotlib.pyplot as plt
from pandas.plotting import table

from helper import *


def credit_summary(transactions):
    """
    purpose: create transaction summary
    transactions (df): transaction dataframe
    """

    # group transactions
    transactions['Type'] = 'Others'
    groups = config['credit_categories']
    for group, value in groups.items():
        transactions.loc[transactions['Transaction'].str.lower().str.contains('|'.join([x.lower() for x in value])),
                         'Type'] = group
    # credit items
    credits = transactions[transactions['Type'] == 'Credit']
    print(credits)
    debits = transactions[transactions['Type'] != 'Credit']

    # format amount
    consolidate = debits.groupby(['Type', 'Transaction']).sum().stb.subtotal()
    consolidate['Amount'] = consolidate['Amount'].map('{:,.2f}'.format)
    print(consolidate)
    return debits


def pie_chart(transactions):
    df = transactions.groupby('Type').sum()
    grandtotal = df['Amount'].sum()
    df['%'] = df['Amount']/grandtotal*100
    df['%'] = df['%'].map('{:,.1f}'.format)
    df = df.sort_values(by=['Amount'])

    # plot chart
    plt.figure(figsize=(12, 8))

    ax1 = plt.subplot(121)
    df['Amount'].plot(kind='pie', subplots=True, ax=ax1, autopct='%1.1f%%', ylabel='', legend=False, fontsize=10)

    ax2 = plt.subplot(122)
    plt.axis('off')
    plt.ylabel('')
    df['Type'] = df.index
    df = df.append({'Amount': '{:,.2f}'.format(grandtotal), '%': 100}, ignore_index=True)
    tbl = table(ax2, df.fillna(''), loc='best')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    plt.savefig('credit_summary.png')


if __name__ == '__main__':
    # set pdf statement path
    file = config['file']

    # extract pdf texts
    pdf = extract_text(file)

    # use regex to parse date, transactions and amount info
    transaction_number = "\d{3}"
    transaction_date = "(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}"
    post_date = "(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}"
    trans = ".+?"
    amount = "[$0-9,-]+\.{1}\d{2}"
    pattern = f"{transaction_number} ({transaction_date}) {post_date} ({trans}) ({amount})"
    transactions = extract_transactions(pdf, pattern)

    # create summary
    debits = credit_summary(transactions)
    pie_chart(debits)
    print('Complete!')
