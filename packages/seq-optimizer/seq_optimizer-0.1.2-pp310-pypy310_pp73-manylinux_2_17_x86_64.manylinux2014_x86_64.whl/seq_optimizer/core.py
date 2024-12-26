from seq_optimizer import _seq_optimizer
from typing import List

def find_longest_common_sequence(seq: List[List[int]]) -> List[int]:
    return _seq_optimizer.find_longest_common_sequence(seq)

def filter_special_tokens(seq: List[int], special_tokens: List[int]) -> List[int]:
    return _seq_optimizer.filter_special_tokens(seq, special_tokens)