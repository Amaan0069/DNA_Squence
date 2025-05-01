def compare_sequences(seq1: str, seq2: str) -> float:
    length = min(len(seq1), len(seq2))
    match_count = sum(1 for i in range(length) if seq1[i] == seq2[i])
    return round((match_count / length) * 100, 2)
