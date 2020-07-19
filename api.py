from fastapi import FastAPI, Request
from pydantic import BaseModel

from volfchain import Block, BlockChain

node = FastAPI()

chain = BlockChain()

minerAddress = "0x00123456789"


class Transaction(BaseModel):
    frm: str
    to: str
    amount: float


@node.get("/")
async def root():
    return {"message": "hello there"}


@node.post("/txion")
def transaction(trans: Transaction):
    chain.addTransaction(trans.json())

    print("New Transaction")
    print(f"FROM:\t{trans.frm}")
    print(f"TO:\t{trans.to}")
    print(f"AMOUNT:\t{trans.amount}")

    return {"msg": "Transaction submission successfull"}


@node.get("/mine")
def mine():
    newBlock = chain.create_block(minerAddress)

    return newBlock.json()


@node.get("/chain")
def seeChain():
    return chain.json()


@node.get("/pending")
def pending_transactions():
    return {"pending": chain.transactions}
