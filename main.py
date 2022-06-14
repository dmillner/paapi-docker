from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from enum import Enum
import dataset

# connecting to a SQLite database
db = dataset.connect('sqlite:///private_api.db')

crypto_wallet_table = db['crypto_wallet']

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


class MetaData(BaseModel):
    create_time: Optional[str] = None
    last_updated_time: Optional[str] = None


class MetaDataResponse(BaseModel):
    create_time: Optional[str] = None
    last_updated_time: Optional[str] = None


class CryptoWallet(BaseModel):
    display_name: str = Query(..., title="Display Name",
                              description="User recognizable display name for the CryptoWallet.",
                              max_length=100)
    crypto_wallet_number: str
    crypto_wallet_type: str
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    current_balance: Optional[float] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaData] = None

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Ethereum Crypto Wallet",
                "crypto_wallet_number": "00598756212",
                "crypto_wallet_type": "ETH",
                "description": "Used for business income and expenses",
                "tax_type": "NONE",
                "current_balance": 3500.45,
                "active": True,
            }
        }


class CryptoWalletResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    crypto_wallet_number: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_code: Optional[TaxType] = None
    current_balance: Optional[float] = None
    inactive: Optional[bool] = False
    meta_data: Optional[MetaDataResponse] = None


class UpdateCryptoWalletResponse(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None
    crypto_wallet_number: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    current_balance: Optional[float] = None
    active: Optional[bool] = True
    time: Optional[str] = None


class UpdateCryptoWallet(BaseModel):
    display_name: Optional[str] = None
    crypto_wallet_number: Optional[str] = None
    crypto_wallet_type: Optional[str] = None
    description: Optional[str] = None
    tax_type: Optional[TaxType] = None
    current_balance: Optional[float] = None
    active: Optional[bool] = True

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Ethereum Crypto Wallet",
                "crypto_wallet_number": "00598756212",
                "crypto_wallet_type": "ETH",
                "description": "Used for business income and expenses",
                "tax_type": "NONE",
                "current_balance": 3500.45,
                "active": True,
            }
        }


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
