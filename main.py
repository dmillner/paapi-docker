from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import dataset
from datetime import datetime, date, timezone
import json

# connecting to a SQLite database
db = dataset.connect('sqlite:///sqlitefile.db')

# get a reference to the object tables
owner_info_table = db['owner_info']
account_table = db['account']
crypto_wallet_table = db['crypto_wallet']
contact_table = db['contact']
employee_table = db['employee']
item_table = db['item']
journal_entry_table = db['journal_entry']
sales_payment_table = db['sales_payment']
purchase_payment_table = db['purchase_payment']
sales_invoice_table = db['sales_invoice']
purchase_invoice_table = db['purchase_invoice']
sales_order_table = db['sales_order']
purchase_order_table = db['purchase_order']
credit_memo_table = db['credit_memo']
vendor_credit_memo_table = db['vendor_credit_memo']
quote_table = db['quote']
connection_table = db['connection']

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaxType(str, Enum):
    NONE = "NONE"
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    GSTONIMPORTS = "GSTONIMPORTS"


class JournalType(str, Enum):
    CASH_RECEIPTS = "CASH_RECEIPTS"
    CASH_DISBURSEMENTS = "CASH_DISBURSEMENTS"
    SALES = "SALES"
    PURCHASE = "PURCHASE"
    SALES_ORDER = "SALES_ORDER"
    PURCHASE_ORDER = "PURCHASE_ORDER"
    QUOTES = "QUOTES"
    PAYROLL = "PAYROLL"


class MetaData(BaseModel):
    create_time: Optional[str] = None
    last_updated_time: Optional[str] = None


class MetaDataResponse(BaseModel):
    create_time: Optional[str] = None
    last_updated_time: Optional[str] = None


class OwnerAddress(BaseModel):
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class OwnerInfo(BaseModel):
    display_name: str
    owner_name: Optional[str] = None
    owner_address: Optional[OwnerAddress] = None
    owner_telephone: Optional[str] = None
    owner_website: Optional[str] = None


class UpdateOwnerInfo(BaseModel):
    display_name: Optional[str] = None
    owner_name: Optional[str] = None
    owner_address: Optional[OwnerAddress] = None
    owner_telephone: Optional[str] = None
    owner_website: Optional[str] = None


class OwnerInfoResponse(BaseModel):
    display_name: Optional[str] = None
    owner_name: Optional[str] = None
    owner_address: Optional[OwnerAddress] = None
    owner_telephone: Optional[str] = None
    owner_website: Optional[str] = None


class Account(BaseModel):
    display_name: str = Query(...,
                              title="Display Name",
                              description="User recognizable display name for the Account.",
                              max_length=100
                              )
    account_code: str
    account_type: str
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaData] = None

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Personal Checking Account",
                "account_code": "101",
                "account_type": "Asset",
                "description": "Personal checking account for income and expenses",
                "tax_code": "NONE",
                "current_balance": 3500.45,
                "inactive": False,
            }
        }


class AccountResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    account_code: Optional[str] = None
    account_type: Optional[str] = None
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    current_balance: Optional[float] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaDataResponse] = None


class UpdateAccountResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    account_code: Optional[str] = None
    account_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    inactive: Optional[bool] = False
    time: Optional[str] = None


class UpdateAccount(BaseModel):
    display_name: Optional[str] = None
    account_code: Optional[str] = None
    account_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    inactive: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Personal Checking Account",
                "account_code": "101",
                "account_type": "Asset",
                "description": "Personal checking account for income and expenses",
                "tax_code": "NONE",
                "current_balance": 3500.45,
                "inactive": False,
            }
        }


class CryptoWallet(BaseModel):
    display_name: str = Query(..., title="Display Name",
                              description="User recognizable display name for the CryptoWallet.",
                              max_length=100)
    crypto_wallet_address: str
    crypto_wallet_type: str
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaData] = None

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Ethereum Crypto Wallet",
                "crypto_wallet_address": "00598756212",
                "crypto_wallet_type": "ETH",
                "description": "Used for Ethereum blockchain transactions",
                "tax_type": "NONE",
                "inactive": False,
            }
        }


class CryptoWalletResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    crypto_wallet_address: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    current_balance: Optional[float] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaDataResponse] = None


class UpdateCryptoWallet(BaseModel):
    display_name: Optional[str] = None
    crypto_wallet_address: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    inactive: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Ethereum Crypto Wallet",
                "crypto_wallet_address": "00598756212",
                "crypto_wallet_type": "ETH",
                "description": "Used for Ethereum blockchain transactions",
                "tax_type": "NONE",
                "inactive": False,
            }
        }


class UpdateCryptoWalletResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    crypto_wallet_address: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaDataResponse] = None


class JournalLineItems(BaseModel):
    account_code: str = None
    account_type: str = None
    amount: float = None
    posting_type: str = None


class JournalEntry(BaseModel):
    date: str = None
    journal_lines: List[JournalLineItems] = None
    description: Optional[str] = None
    posted: Optional[bool] = True
    journal_type: Optional[JournalType] = None
    validate_journal_type: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "date": "2022-06-22",
                "journal_lines": [
                    {
                        "account_code": "101",
                        "account_type": "Asset",
                        "amount": 1000.0,
                        "posting_type": "Debit",
                    },
                    {
                        "account_code": "400",
                        "account_type": "Revenue",
                        "amount": 1000.0,
                        "posting_type": "Credit",
                    }
                ],
                "description": "Revenue from garage sale",
                "posted": True,
                "journal_type": "CASH_RECEIPTS",
                "validate_journal_type": False
            }
        }


class JournalEntryResponse(BaseModel):
    id: str = None
    date: str = None
    journal_lines: List[JournalLineItems] = None
    description: Optional[str] = None
    posted: Optional[bool] = True
    journal_type: Optional[JournalType] = None
    validate_journal_type: Optional[bool] = False


class UpdateJournalEntry(BaseModel):
    id: str = None
    date: Optional[str] = None
    journal_lines: Optional[List[JournalLineItems]] = None
    description: Optional[str] = None
    posted: Optional[bool] = True
    journal_type: Optional[JournalType] = None
    validate_journal_type: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "date": "2022-06-22",
                "journal_lines": [
                    {
                        "account_code": "101",
                        "account_type": "Asset",
                        "amount": 1000.0,
                        "posting_type": "Debit",
                    },
                    {
                        "account_code": "400",
                        "account_type": "Revenue",
                        "amount": 1000.0,
                        "posting_type": "Credit",
                    }
                ],
                "description": "Revenue from garage sale",
                "posted": True,
                "journal_type": "CASH_RECEIPTS",
                "validate_journal_type": False
            }
        }


@app.get("/owner_info/", response_model=OwnerInfoResponse, tags=["Owner Info"])
async def read_owner_info():
    """
        Read owner_info:

    """
    owner_info = owner_info_table.find_one(id=1)
    if owner_info:
        return owner_info
    else:
        raise HTTPException(status_code=404, detail="OwnerInfo not found")


@app.get("/owner_info/query", tags=["Owner Info"])
async def query_owner_info(query: Optional[str] = None):
    """
        Query owner_info using a sql statement:

    """
    if query:
        final_results = []
        print(f"The query is {query}")
        # result = db.query('select * from owner_info')
        result = db.query(query)
        if result:
            for row in result:
                print(f"The row is {row}")
                final_results.append(row)
            print(f"final results are {final_results}")
            return final_results
        else:
            raise HTTPException(status_code=404, detail="OwnerInfo not found")


@app.put("/owner_info/", response_model=UpdateOwnerInfo, tags=["Owner Info"])
async def update_owner_info(owner_info: UpdateOwnerInfo):
    """
        Update owner_info with new information:

    """
    owner_info_to_update = owner_info_table.find_one(id=1)
    if owner_info_to_update:
        print(f"the owner_info to update is: {owner_info_to_update}")
        owner_info_dict = owner_info.dict()
        print(f"the owner_info_dict is: {owner_info_dict}")
        owner_info_dict['id'] = 1
        print(f"the updated owner_info_dict is: {owner_info_dict}")
        owner_info_table.update(owner_info_dict, ['id'])
        return owner_info_dict
    else:
        raise HTTPException(status_code=404, detail="OwnerInfo not found")


@app.post("/owner_info/", tags=["Owner Info"], include_in_schema=False)
async def create_owner_info(owner_info: OwnerInfo):
    """
        Create owner_info using required information:

    """
    owner_info_dict = owner_info.dict()

    db_insert = owner_info_table.insert(owner_info_dict)
    print(f"db_insert is {db_insert}")
    owner_info_dict['id'] = db_insert
    return owner_info_dict


@app.post("/account/", tags=["Account"])
async def create_account(account: Account):
    """
        Create a ledger account using required information:

    """
    account_dict = account.dict()

    db_insert = account_table.insert(account_dict)
    print(f"db_insert is {db_insert}")
    account_dict['id'] = db_insert
    return account_dict


@app.get("/account/query", tags=["Account"])
async def query_account(query: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
        Query a ledger account using a sql statement:

    """
    if query:
        final_results = []
        print(f"The query is {query}")
        # result = db.query('select * from account')
        result = db.query(query)
        if result:
            for row in result:
                print(f"The row is {row}")
                final_results.append(row)
            print(f"final results are {final_results}")
            return final_results[skip: skip + limit]
        else:
            raise HTTPException(status_code=404, detail="Account not found")


@app.get("/account/{account_id}", tags=["Account"])
async def read_account(account_id: int):
    """
        Read a ledger account using account_id:

    """
    account = account_table.find_one(id=account_id)
    if account:
        return account
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@app.put("/account/{account_id}", tags=["Account"])
async def update_account(account_id: int, account: UpdateAccount):
    """
        Update a ledger account with new information:

    """
    account_to_update = account_table.find_one(id=account_id)
    if account_to_update:
        print(f"the account to update is: {account_to_update}")
        account_dict = account.dict()
        print(f"the account_dict is: {account_dict}")
        account_dict['id'] = account_id
        print(f"the updated account_dict is: {account_dict}")
        account_table.update(account_dict, ['id'])
        return account_dict
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@app.delete("/account/{account_id}", tags=["Account"])
async def delete_account(account_id: int):
    """
        Delete a Ledger Account:

    """
    account_to_delete = account_table.find_one(id=account_id)
    if account_to_delete:
        print(f"the account to delete is: {account_to_delete}")
        account_table.delete(id=account_id)
        return {"message": f"Account with id {account_id} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@app.post("/crypto_wallet/", tags=["Crypto Wallet"])
async def create_crypto_wallet(crypto_wallet: CryptoWallet):
    """
        Create a ledger crypto_wallet using required information:

    """
    crypto_wallet_dict = crypto_wallet.dict()

    db_insert = crypto_wallet_table.insert(crypto_wallet_dict)
    print(f"db_insert is {db_insert}")
    crypto_wallet_dict['id'] = db_insert
    return crypto_wallet_dict


@app.get("/crypto_wallet/query", tags=["Crypto Wallet"])
async def query_crypto_wallet(query: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
        Query a ledger crypto_wallet using a sql statement:

    """
    if query:
        final_results = []
        print(f"The query is {query}")
        # result = db.query('select * from crypto_wallet')
        result = db.query(query)
        if result:
            for row in result:
                print(f"The row is {row}")
                final_results.append(row)
            print(f"final results are {final_results}")
            return final_results[skip: skip + limit]
        else:
            raise HTTPException(status_code=404, detail="Crypto Wallet not found")


@app.get("/crypto_wallet/{crypto_wallet_id}", tags=["Crypto Wallet"])
async def read_crypto_wallet(crypto_wallet_id: int):
    """
        Read a ledger crypto_wallet using crypto_wallet_id:

    """
    crypto_wallet = crypto_wallet_table.find_one(id=crypto_wallet_id)
    if crypto_wallet:
        return crypto_wallet
    else:
        raise HTTPException(status_code=404, detail="Crypto Wallet not found")


@app.put("/crypto_wallet/{crypto_wallet_id}", tags=["Crypto Wallet"])
async def update_crypto_wallet(crypto_wallet_id: int, crypto_wallet: UpdateCryptoWallet):
    """
        Update a ledger crypto_wallet with new information:

    """
    crypto_wallet_to_update = crypto_wallet_table.find_one(id=crypto_wallet_id)
    if crypto_wallet_to_update:
        print(f"the crypto_wallet to update is: {crypto_wallet_to_update}")
        crypto_wallet_dict = crypto_wallet.dict()
        print(f"the crypto_wallet_dict is: {crypto_wallet_dict}")
        crypto_wallet_dict['id'] = crypto_wallet_id
        print(f"the updated crypto_wallet_dict is: {crypto_wallet_dict}")
        crypto_wallet_table.update(crypto_wallet_dict, ['id'])
        return crypto_wallet_dict
    else:
        raise HTTPException(status_code=404, detail="Crypto Wallet not found")


@app.delete("/crypto_wallet/{crypto_wallet_id}", tags=["Crypto Wallet"])
async def delete_crypto_wallet(crypto_wallet_id: int):
    """
        Delete a Ledger Crypto Wallet:

    """
    crypto_wallet_to_delete = crypto_wallet_table.find_one(id=crypto_wallet_id)
    if crypto_wallet_to_delete:
        print(f"the crypto_wallet to delete is: {crypto_wallet_to_delete}")
        crypto_wallet_table.delete(id=crypto_wallet_id)
        return {"message": f"Crypto Wallet with id {crypto_wallet_id} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="Crypto Wallet not found")


@app.post("/journalentry/", tags=["Journal Entry"])
async def create_journal_entry(journal_entry: JournalEntry):
    """
        Create a journal entry using required information:

    """

    current_date = datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d')
    journal_entry_dict = journal_entry.dict()
    json_journal_entry_dict = journal_entry.dict()
    journal_lines = journal_entry_dict['journal_lines']
    journal_entry_date = journal_entry_dict['date']

    if not journal_entry_date:
        json_journal_entry_dict['date'] = current_date
        journal_entry_dict['date'] = current_date

    if not journal_lines:
        raise HTTPException(status_code=404, detail="Cannot Record An Empty Journal Entry")

    for line in journal_lines:
        print(f"line in journal_lines: is {line}")
        account_code = line['account_code']
        amount = line['amount']
        if not account_code:
            raise HTTPException(status_code=404, detail="All Journal Lines Must Contain account_code")
        if not amount:
            raise HTTPException(status_code=404, detail="All Journal Lines Must Contain amount")

        if line['posting_type'] == 'Credit' and line['amount'] > 0:
            line['amount'] = -line["amount"]

    print(f"Updated journal_lines are: {journal_lines}")

    code_amount = [[line['account_code'], line['amount']] for line in journal_lines]
    print(f"code_amount is: {code_amount}")

    if sum(line[1] for line in code_amount) != 0:
        raise HTTPException(status_code=404, detail="Unbalanced Journal Lines")

    print(f"journal_lines in journal_entry_dict is {journal_lines}")
    json_compatible_journal_lines = json.dumps(journal_lines)
    print(f"json_compatible_journal_lines in journal_entry_dict is {json_compatible_journal_lines}")
    json_journal_entry_dict["journal_lines"] = json_compatible_journal_lines
    db_insert = journal_entry_table.insert(json_journal_entry_dict)
    print(f"db_insert is {db_insert}")
    journal_entry_dict['id'] = db_insert
    return journal_entry_dict


@app.get("/journalentry/query", tags=["Journal Entry"])
async def query_journal_entry(query: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
           Query a journal entry using a sql statement:

    """
    if query:
        final_results = []
        print(f"The query is {query}")
        # result = db.query('select * from journal_entry')
        result = db.query(query)
        if result:
            for row in result:
                print(f"The row is {row['journal_lines']}")
                journal_lines = json.loads(row['journal_lines'])
                row['journal_lines'] = journal_lines
                final_results.append(row)
            print(f"final results are {final_results}")
            return final_results[skip: skip + limit]
        else:
            raise HTTPException(status_code=404, detail="Journal Entry not found")


@app.get("/journalentry/{journal_entry_id}", tags=["Journal Entry"])
async def read_journal_entry(journal_entry_id: str):
    """
        Read a journal_entry using journal_entry_id:

    """
    journal_entry = journal_entry_table.find_one(id=journal_entry_id)
    if journal_entry:
        journal_lines = journal_entry['journal_lines']
        json_compatible_line_items = json.loads(journal_lines)
        journal_entry['journal_lines'] = json_compatible_line_items
        return journal_entry
    else:
        raise HTTPException(status_code=404, detail="Journal Entry not found")


@app.put("/journalentry/{journal_entry_id}", tags=["Journal Entry"])
async def update_journal_entry(journal_entry_id: str, journal_entry: UpdateJournalEntry):
    """
        Update a journal_entry with new information:

    """
    journal_entry_to_update = journal_entry_table.find_one(id=journal_entry_id)
    if journal_entry_to_update:
        journal_entry_dict = journal_entry.dict()
        json_journal_entry_dict = journal_entry.dict()
        line_items = journal_entry_dict['journal_lines']
        print(f"line_items in journal_entry_dict is {line_items}")
        json_compatible_line_items = json.dumps(line_items)
        print(f"json_compatible_line_items in journal_entry_dict is {json_compatible_line_items}")
        json_journal_entry_dict["journal_lines"] = json_compatible_line_items
        journal_entry_dict['id'] = journal_entry_id
        json_journal_entry_dict['id'] = journal_entry_id
        print(f"the updated journal_entry_dict is: {journal_entry_dict}")
        journal_entry_table.update(json_journal_entry_dict, ['id'])

        return journal_entry_dict
    else:
        raise HTTPException(status_code=404, detail="Journal Entry not found")


@app.delete("/journalentry/{journal_entry_id}", tags=["Journal Entry"])
async def delete_journal_entry(journal_entry_id: str):
    """
        Delete a Journal Entry:

    """
    journal_entry_to_delete = journal_entry_table.find_one(id=journal_entry_id)
    if journal_entry_to_delete:
        print(f"the journal_entry to delete is: {journal_entry_to_delete}")
        journal_entry_table.delete(id=journal_entry_id)
        return {"message": f"Journal Entry with id {journal_entry_id} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="Journal Entry not found")


@app.get("/reports/profit_and_loss", tags=["Reports"])
async def get_profit_and_loss(start_date: Optional[date] = None, end_date: Optional[date] = None):
    """
        Query a journal entry using a sql statement:

    """

    result = journal_entry_table.find(date={'between': [start_date, end_date]})
    print(f"The result is {result}")
    accounts_by_type = {'revenue': {}, 'expense': {}}
    if result:
        for row in result:
            print(f"The row is {row['journal_lines']}")
            journal_lines = json.loads(row['journal_lines'])
            for each in journal_lines:
                print(f"each in journal_lines is {each}")

                if each['account_type'] in ["Revenue", "Expense"]:
                    key = str(each['account_type']).lower()
                    print(f"Key is {key}")
                    try:
                        accounts_by_type[f"{key}"][f"account_code_{each['account_code']}"].append(each['amount'])
                    except KeyError:
                        accounts_by_type[f"{key}"][f"account_code_{each['account_code']}"] = []
                        accounts_by_type[f"{key}"][
                            f"account_code_{each['account_code']}"].append(each['amount'])
    else:
        raise HTTPException(status_code=404, detail="Journal Entry not found")

    print(f"accounts by type are {accounts_by_type}")

    for account in accounts_by_type['revenue']:
        print(f"account in ACCOUNTS BY TYPE is {account}")
        accounts_by_type['revenue'][f'{account}'] = sum(accounts_by_type['revenue'][f'{account}'])

    for account in accounts_by_type['expense']:
        print(f"account in ACCOUNTS BY TYPE is {account}")
        accounts_by_type['expense'][f'{account}'] = sum(accounts_by_type['expense'][f'{account}'])

    print(f"UPDATED accounts by type are {accounts_by_type}")

    column_data_1 = [{"value": "Income"}, {"value": ""}]
    column_data_2 = [{"id": "45", "value": "Landscaping Services"}, {"value": ""}]
    column_data_3 = [{"id": "46", "value": "Job Materials"}, {"value": ""}]
    column_data_4 = [{"id": "48", "value": "Fountains and Garden Lighting"}, {"value": "275.00"}]
    column_data_5 = [{"id": "49", "value": "Plants and Soil"}, {"value": "150.00"}]
    column_data_6 = [{"value": "Total Job Materials"}, {"value": "425.00"}]
    column_data_7 = [{"value": "Total Landscaping Services"}, {"value": "425.00"}]
    column_data_8 = [{"id": "54", "value": "Pest Control Services"}, {"value": "-100.00"}]
    column_data_9 = [{"value": "Total Income"}, {"value": "325.00"}]
    column_data_10 = [{"value": "Gross Profit"}, {"value": "325.00"}]
    income_group = {
        "Header": {
            "ColData": column_data_1
        },
        "Rows": {
            "Row": [
                {
                    "Header": {
                        "ColData": column_data_2
                    },
                    "Rows": {
                        "Row": [
                            {
                                "Header": {
                                    "ColData": column_data_3
                                },
                                "Rows": {
                                    "Row": [
                                        {
                                            "ColData": column_data_4,
                                            "type": "Data"
                                        },
                                        {
                                            "ColData": column_data_5,
                                            "type": "Data"
                                        }

                                    ]
                                },
                                "type": "Section",
                                "Summary": {
                                    "ColData": column_data_6
                                }
                            }
                        ]
                    },
                    "type": "Section",
                    "Summary": {
                        "ColData": column_data_7
                    }
                },
                {
                    "ColData": column_data_8,
                    "type": "Data"
                }
            ]
        },
        "type": "Section",
        "group": "Income",
        "Summary": {
            "ColData": column_data_9
        }
    }
    gross_profit_group = {
        "type": "Section",
        "group": "Gross Profit",
        "Summary": {
            "ColData": column_data_10
        }
    }
    expense_group = {"Header": {}, "type": "Section", "group": "Expense", "Summary": {}}
    net_operating_income_group = {"type": "Section", "group": "Net Operating Income", "Summary": {}}
    net_income_group = {"type": "Section", "group": "Net Income", "Summary": {}}
    cogs_group = {"type": "Section", "group": "COGS", "Summary": {}}
    net_other_income_group = {"type": "Section", "group": "Net Other Income", "Summary": {}}
    other_expense_group = {"type": "Section", "group": "Other Expense", "Summary": {}}
    profit_and_loss = {
        "Header": {
            "Customer": "1",
            "ReportName": "ProfitAndLoss",
            "Option": [
                {
                    "Name": "AccountingStandard",
                    "Value": "GAAP"
                },
                {
                    "Name": "NoReportData",
                    "Value": "false"
                }
            ],
            "ReportBasis": "Accrual",
            "StartPeriod": f'{start_date}',
            "Currency": "USD",
            "EndPeriod": f'{end_date}',
            "Time": f'{datetime.now()}',
            "SummarizeColumnsBy": "Total"
        },
        "Rows": {
            "Row": [income_group, gross_profit_group, expense_group, net_operating_income_group,
                    net_income_group]
        },
        "Columns": {
            "Column": [
                {
                    "ColType": "Account",
                    "ColTitle": "",
                    "MetaData": [
                        {
                            "Name": "ColKey",
                            "Value": "account"
                        }
                    ]
                },
                {
                    "ColType": "Money",
                    "ColTitle": "Total",
                    "MetaData": [
                        {
                            "Name": "ColKey",
                            "Value": "total"
                        }
                    ]
                }
            ]
        }
    }

    p_n_l = {
        "Header": {
            "Customer": "1",
            "ReportName": "ProfitAndLoss",
            "Option": [
                {
                    "Name": "AccountingStandard",
                    "Value": "GAAP"
                },
                {
                    "Name": "NoReportData",
                    "Value": "false"
                }
            ],
            "ReportBasis": "Accrual",
            "StartPeriod": "2022-06-01",
            "Currency": "USD",
            "EndPeriod": "2022-06-30",
            "Time": "2022-03-03T13:00:18-08:00",
            "SummarizeColumnsBy": "Total"
        },
        "Rows": {
            "Row": [
                {
                    "Header": {
                        "ColData": [
                            {
                                "value": "Income"
                            },
                            {
                                "value": ""
                            }
                        ]
                    },
                    "Rows": {
                        "Row": [
                            {
                                "Header": {
                                    "ColData": [
                                        {
                                            "id": "45",
                                            "value": "Landscaping Services"
                                        },
                                        {
                                            "value": ""
                                        }
                                    ]
                                },
                                "Rows": {
                                    "Row": [
                                        {
                                            "Header": {
                                                "ColData": [
                                                    {
                                                        "id": "46",
                                                        "value": "Job Materials"
                                                    },
                                                    {
                                                        "value": ""
                                                    }
                                                ]
                                            },
                                            "Rows": {
                                                "Row": [
                                                    {
                                                        "ColData": [
                                                            {
                                                                "id": "48",
                                                                "value": "Fountains and Garden Lighting"
                                                            },
                                                            {
                                                                "value": "275.00"
                                                            }
                                                        ],
                                                        "type": "Data"
                                                    },
                                                    {
                                                        "ColData": [
                                                            {
                                                                "id": "49",
                                                                "value": "Plants and Soil"
                                                            },
                                                            {
                                                                "value": "150.00"
                                                            }
                                                        ],
                                                        "type": "Data"
                                                    }
                                                ]
                                            },
                                            "type": "Section",
                                            "Summary": {
                                                "ColData": [
                                                    {
                                                        "value": "Total Job Materials"
                                                    },
                                                    {
                                                        "value": "425.00"
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                },
                                "type": "Section",
                                "Summary": {
                                    "ColData": [
                                        {
                                            "value": "Total Landscaping Services"
                                        },
                                        {
                                            "value": "425.00"
                                        }
                                    ]
                                }
                            },
                            {
                                "ColData": [
                                    {
                                        "id": "54",
                                        "value": "Pest Control Services"
                                    },
                                    {
                                        "value": "-100.00"
                                    }
                                ],
                                "type": "Data"
                            }
                        ]
                    },
                    "type": "Section",
                    "group": "Income",
                    "Summary": {
                        "ColData": [
                            {
                                "value": "Total Income"
                            },
                            {
                                "value": "325.00"
                            }
                        ]
                    }
                },
                {
                    "group": "GrossProfit",
                    "type": "Section",
                    "Summary": {
                        "ColData": [
                            {
                                "value": "Gross Profit"
                            },
                            {
                                "value": "325.00"
                            }
                        ]
                    }
                },
                {
                    "Header": {
                        "ColData": [
                            {
                                "value": "Expenses"
                            },
                            {
                                "value": ""
                            }
                        ]
                    },
                    "type": "Section",
                    "group": "Expenses",
                    "Summary": {
                        "ColData": [
                            {
                                "value": "Total Expenses"
                            },
                            {
                                "value": ""
                            }
                        ]
                    }
                },
                {
                    "group": "NetOperatingIncome",
                    "type": "Section",
                    "Summary": {
                        "ColData": [
                            {
                                "value": "Net Operating Income"
                            },
                            {
                                "value": "325.00"
                            }
                        ]
                    }
                },
                {
                    "group": "NetIncome",
                    "type": "Section",
                    "Summary": {
                        "ColData": [
                            {
                                "value": "Net Income"
                            },
                            {
                                "value": "325.00"
                            }
                        ]
                    }
                }
            ]
        },
        "Columns": {
            "Column": [
                {
                    "ColType": "Account",
                    "ColTitle": "",
                    "MetaData": [
                        {
                            "Name": "ColKey",
                            "Value": "account"
                        }
                    ]
                },
                {
                    "ColType": "Money",
                    "ColTitle": "Total",
                    "MetaData": [
                        {
                            "Name": "ColKey",
                            "Value": "total"
                        }
                    ]
                }
            ]
        }
    }
    return profit_and_loss


@app.get("/reports/balance_sheet", tags=["Reports"])
async def get_balance_sheet(start_date: Optional[date] = None, end_date: Optional[date] = None):
    """
        Query a journal entry using a sql statement:

    """

    result = journal_entry_table.find(date={'between': [start_date, end_date]})
    print(f"The result is {result}")
    accounts_by_type = {'asset': {}, 'liability': {}, 'equity': {}}
    if result:
        for row in result:
            print(f"The row is {row['journal_lines']}")
            journal_lines = json.loads(row['journal_lines'])
            for each in journal_lines:
                print(f"each in journal_lines is {each}")

                if each['account_type'] in ["Asset", "Liability", "Equity"]:
                    key = str(each['account_type']).lower()
                    print(f"Key is {key}")
                    try:
                        accounts_by_type[f"{key}"][f"account_code_{each['account_code']}"].append(each['amount'])
                    except KeyError:
                        accounts_by_type[f"{key}"][f"account_code_{each['account_code']}"] = []
                        accounts_by_type[f"{key}"][
                            f"account_code_{each['account_code']}"].append(each['amount'])
    else:
        raise HTTPException(status_code=404, detail="Journal Entry not found")

    print(f"accounts by type are {accounts_by_type}")

    for account in accounts_by_type['asset']:
        print(f"account in ACCOUNTS BY TYPE is {account}")
        accounts_by_type['asset'][f'{account}'] = sum(accounts_by_type['asset'][f'{account}'])

    for account in accounts_by_type['liability']:
        print(f"account in ACCOUNTS BY TYPE is {account}")
        accounts_by_type['liability'][f'{account}'] = sum(accounts_by_type['liability'][f'{account}'])

    for account in accounts_by_type['equity']:
        print(f"account in ACCOUNTS BY TYPE is {account}")
        accounts_by_type['equity'][f'{account}'] = sum(accounts_by_type['equity'][f'{account}'])

    print(f"UPDATED accounts by type are {accounts_by_type}")
    balance_sheet = {}
    return balance_sheet
