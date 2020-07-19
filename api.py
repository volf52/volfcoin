from volfchain import Block, BlockChain

from fastapi import FastAPI, Request
from pydantic import BaseModel

node = FastAPI()

chain = BlockChain()


class Transaction(BaseModel):
    frm: str
    to: str
    amount: int


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
