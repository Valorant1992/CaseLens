import json

errors = []
warnings = []

with open('customers.json') as f: customers = json.load(f)
with open('accounts.json') as f: accounts = json.load(f)
with open('counterparties.json') as f: counterparties = json.load(f)
with open('transactions.json') as f: transactions = json.load(f)
with open('alerts.json') as f: alerts = json.load(f)
with open('alert_transactions.json') as f: alert_txns = json.load(f)
with open('cases.json') as f: cases = json.load(f)
with open('case_alerts.json') as f: case_alerts = json.load(f)
with open('case_events.json') as f: case_events = json.load(f)
with open('case_notes.json') as f: case_notes = json.load(f)
with open('screening_hits.json') as f: hits = json.load(f)
with open('customer_risk_profiles.json') as f: profiles = json.load(f)

cust_ids = {c['customer_id'] for c in customers}
acct_ids = {a['account_id'] for a in accounts}
cp_ids = {c['counterparty_id'] for c in counterparties}
txn_ids = {t['transaction_id'] for t in transactions}
alert_ids = {a['alert_id'] for a in alerts}
case_ids = {c['case_id'] for c in cases}

allowed_statuses = {'OPEN', 'AUTO_CLEARED', 'ESCALATED', 'ESCALATED_TO_L2'}

# Alerts
for a in alerts:
    aid = a['alert_id']
    if a['customer_id'] not in cust_ids:
        errors.append(f'Alert {aid}: bad customer_id {a["customer_id"]}')
    if a['account_id'] not in acct_ids:
        errors.append(f'Alert {aid}: bad account_id {a["account_id"]}')
    if a['primary_txn_id'] not in txn_ids:
        errors.append(f'Alert {aid}: bad primary_txn_id {a["primary_txn_id"]}')
    if a['status'] not in allowed_statuses:
        errors.append(f'Alert {aid}: invalid status "{a["status"]}"')
    if a['severity'] in ('HIGH', 'CRITICAL') and a['status'] == 'AUTO_CLEARED':
        warnings.append(f'Alert {aid}: severity={a["severity"]} with status=AUTO_CLEARED (check justification)')

# Transactions
for t in transactions:
    tid = t['transaction_id']
    if t['customer_id'] not in cust_ids:
        errors.append(f'TXN {tid}: bad customer_id')
    if t['account_id'] not in acct_ids:
        errors.append(f'TXN {tid}: bad account_id')
    cp = t.get('counterparty_id')
    if cp and cp not in cp_ids:
        errors.append(f'TXN {tid}: bad counterparty_id {cp}')

# Alert transactions
for at in alert_txns:
    if at['alert_id'] not in alert_ids:
        errors.append(f'alert_transactions: bad alert_id {at["alert_id"]}')
    if at['transaction_id'] not in txn_ids:
        errors.append(f'alert_transactions: bad txn_id {at["transaction_id"]}')

# Cases
for c in cases:
    cid = c['case_id']
    if c['primary_alert_id'] not in alert_ids:
        errors.append(f'Case {cid}: bad primary_alert_id {c["primary_alert_id"]}')
    if c['customer_id'] not in cust_ids:
        errors.append(f'Case {cid}: bad customer_id {c["customer_id"]}')

# Case alerts
for ca in case_alerts:
    if ca['case_id'] not in case_ids:
        errors.append(f'case_alerts: bad case_id {ca["case_id"]}')
    if ca['alert_id'] not in alert_ids:
        errors.append(f'case_alerts: bad alert_id {ca["alert_id"]}')

# Case events
for ev in case_events:
    if ev['case_id'] not in case_ids:
        errors.append(f'case_events {ev["event_id"]}: bad case_id {ev["case_id"]}')

# Case notes
for n in case_notes:
    if n['case_id'] not in case_ids:
        errors.append(f'case_notes {n["note_id"]}: bad case_id {n["case_id"]}')

# Screening hits
for h in hits:
    if h['customer_id'] not in cust_ids:
        errors.append(f'Hit {h["hit_id"]}: bad customer_id {h["customer_id"]}')

# Counts
print(f'Customers:       {len(customers):>4}')
print(f'Accounts:        {len(accounts):>4}')
print(f'Counterparties:  {len(counterparties):>4}')
print(f'Transactions:    {len(transactions):>4}')
print(f'Alerts:          {len(alerts):>4}')
print(f'Cases:           {len(cases):>4}')
print(f'Case events:     {len(case_events):>4}')
print(f'Case notes:      {len(case_notes):>4}')
print(f'Screening hits:  {len(hits):>4}')
print()

if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  [ERR] {e}')
else:
    print('No errors found.')

if warnings:
    print('WARNINGS:')
    for w in warnings:
        print(f'  [WRN] {w}')
else:
    print('No warnings.')
