import unittest, time

from uninformed_search import find_path

WORD_LIST_SMALL = ["AIM", "ARM", "ART", "RIM", "RAM", "RAT",
                    "ROT", "RUM", "RUN", "BOT", "JAM", "JOB",
                    "JAB", "LAB", "LOB", "LOG", "SUN"]

WORD_LIST_LARGE = []
with open("Dictionary.txt") as f:
    for line in f:
        WORD_LIST_LARGE.append(line.strip())

class TestMazeAgent(unittest.TestCase):

    def doTest(self, word_list, start_word, end_word, expected_path_length):
        print("\nRunning test {} ('{}' to '{}')".format(self._testMethodName, start_word, end_word))
        word_list_orig = set(word_list)

        start_time = time.time()
        path = find_path(start_word, end_word, word_list)
        duration = time.time() - start_time
        print("    time taken: {:<05}s".format(round(duration,3)))
        print("    path={}".format(path))

        if expected_path_length == 0:
            self.assertIsNone(path, "there is no path, so you should return None")
            return
        
        self.assertIsNotNone(path, "there is a path, so you should return a list of strings")
        self.assertGreater(len(path), 0, "path is empty")

        path = [word.upper() for word in path]

        self.assertEqual(path[0],  start_word, "incorrect start word")
        self.assertEqual(path[-1], end_word,   "incorrect end word")

        prev_word = path[0]
        for word in path[1:]:
            self.assertTrue(word in word_list_orig,
                            "word '{}' is not in word_list".format(word))
            self.assertEqual(len(word), len(start_word),
                              "word '{}' has incorrect length".format(word))
            differences = 0
            for i in range(len(word)):
                if word[i] != prev_word[i]:
                    differences += 1
            self.assertEqual(differences, 1,
                             "'{}' cannot come after '{}' in path".format(word, prev_word))
            prev_word = word

        self.assertEqual(len(path), expected_path_length, "shortest path is length {}, your path is length {}".format(expected_path_length, len(path)))

    def test01(self):
        self.doTest(WORD_LIST_SMALL, "AIM", "BOT", 6)

    def test02(self):
        self.doTest(WORD_LIST_SMALL, "LOG", "JAM", 5)

    def test03(self):
        self.doTest(WORD_LIST_SMALL, "LOG", "SUN", 9)

    def test04(self):
        self.doTest(WORD_LIST_LARGE, "IVY", "EYE", 4)

    def test05(self):
        self.doTest(WORD_LIST_LARGE, "IF", "GO", 6)
    
    def test06(self):
        self.doTest(WORD_LIST_LARGE, "LYRE", "MAKE", 5)
    
    def test07(self):
        self.doTest(WORD_LIST_LARGE, "BEGIN", "FOUND", 0)
    
    def test08(self):
        self.doTest(WORD_LIST_LARGE, "GRACED", "CEASES", 8)

    def test09(self):
        self.doTest(WORD_LIST_LARGE, "AFFLICT", "POTTERY", 0)

    def test10(self):
        self.doTest(WORD_LIST_LARGE, "CLEARING", "WRAPPING", 22)

    def test11(self):
        self.doTest(WORD_LIST_LARGE, "MINTS", "ROUGE", 9)

    def test12(self):
        self.doTest(WORD_LIST_LARGE, "THYME", "LAPSE", 0)
    
    def test13(self):
        self.doTest(WORD_LIST_LARGE, "ELUDE", "SEWED", 15)

    def test14(self):
        self.doTest(WORD_LIST_LARGE, "MANGLED", "CRACKED", 0)

if __name__ == "__main__":
    result = unittest.main(failfast=True)
