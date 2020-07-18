from datetime import datetime
import hashlib as hasher


class Block:
    def __init__(self, idx: int, tsmp: datetime, data: str, prevhash: str):
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
        return Block(0, datetime.now(), "Genesis Block", "0x0")

    def __str__(self):
        return "\n".join([str(x) for x in self.blocks])

    def create_block(self):
        last_block = self.blocks[-1]
        this_idx = last_block.idx + 1
        this_timestmp = datetime.now()
        this_data = f"Hey! I'm block {this_idx}"
        this_hash = last_block.hash

        newB = Block(this_idx, this_timestmp, this_data, this_hash)
        self.blocks.append(newB)

        return newB


if __name__ == "__main__":
    blockchain = BlockChain()
    for _ in range(19):
        blockchain.create_block()

    print(blockchain)
