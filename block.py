from time import time

from utility.printable import Printable


class Block(Printable):
    """A single block of our blockchain.
    
    Attributes:
        :index: The index of this block.
        :previous_hash: The hash of the previous block in the blockchain.
        :timestamp: The timestamp of the block (automatically generated by default).
        :transactions: A list of transaction which are included in the block.
        :proof: The proof of work number that yielded this block.
    """

    def __init__(self, index, previous_hash, transactions, proof, timestamp=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
