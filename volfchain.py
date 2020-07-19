import hashlib as hasher
import json
from datetime import datetime


class Block:
    def __init__(self, idx: int, tsmp: datetime, data: any, prevhash: str):
        self.idx = idx
        self.timestamp = tsmp
        self.data = data
        self.previous_hash = prevhash
        self.hash = self.hash_block()

    def hash_block(self) -> str:
        sha = hasher.sha256()
        hashInput = (
            str(self.idx)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
        ).encode()
        sha.update(hashInput)

        return sha.hexdigest()

    def __str__(self):
        return f"#{self.idx}  Hash: {self.hash}"

    def json(self):
        return {
            "index": self.idx,
            "timestamp": self.timestamp,
            "data": self.data,
            "prevHash": self.previous_hash,
            "hash": self.hash,
        }


class BlockChain:
    def __init__(self):
        self.currIdx = 1
        self.blocks = [self.create_genesis_block()]
        self.transactions = []

    @property
    def lastBlock(self):
        if self.currIdx == 0:
            return None
        else:
            return self.blocks[-1]

    def create_genesis_block(self):
        return Block(0, datetime.now(), {"POW": 11, "transactions": []}, "0x0")

    def addTransaction(self, transJson: str):
        transaction = json.loads(transJson)
        self.transactions.append(transaction)

    def __str__(self):
        return "\n".join([str(x) for x in self.blocks])

    def json(self):
        return [x.json() for x in self.blocks]

    def proof_of_work(self, lastProof: int):
        inc = lastProof + 1

        while not (inc % 8 == 0 and inc % lastProof == 0):
            inc += 1

        return inc

    def create_block(self, minerAddr: str):
        last_block = self.blocks[-1]
        this_idx = last_block.idx + 1
        thisPow = self.proof_of_work(last_block.data["POW"])
        self.transactions.append(
            {"frm": "network", "to": minerAddr, "amount": 1}
        )
        this_data = {"POW": thisPow, "transactions": self.transactions[:]}
        this_hash = last_block.hash

        this_timestmp = datetime.now()

        newB = Block(this_idx, this_timestmp, this_data, this_hash)
        self.blocks.append(newB)
        self.transactions.clear()

        return newB

