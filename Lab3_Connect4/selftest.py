from connect4 import legal_moves, drop_piece

def test_legal_moves():
    b = [""]*7
    assert legal_moves(b) == list(range(7))

def test_drop_piece():
    b = [""]*7
    b2 = drop_piece(b, 0, "X")
    assert b2[0] == "X"

# Run all tests
if __name__ == "__main__":
    test_legal_moves()
    test_drop_piece()
    print("All tests passed ✅")
