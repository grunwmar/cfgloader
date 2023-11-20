from deserializer import DeserializerDict
import deserializer

deserializer.TO_STRING_INDENT = 2


FILE_LST = ["test_files/test.json", "test_files/test.yaml", "test_files/test.toml", "test_files/test.ini"]

for fn in FILE_LST:
    config = DeserializerDict.from_file(fn)
    print(fn, "-->", config.attrs().users)

