import pickle

example_dict = {1: "6", 2: "2", 3: "f"}

pickle_out = open("dict.pickle", "wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()

pickle_in = open("dict.pickle", "rb")
example_dict = pickle.load(pickle_in)


print(example_dict)
print(example_dict[3])


example_dict2 = {1: 100, 2: 10, 3: 570, 4: 10}

pickle_out2 = open("dict.pickle", "wb")
pickle.dump(example_dict2, pickle_out2)
pickle_out2.close()


GRADIANT_SIZE = 100
MAX_ERROR = 10
TEAR_DEPTH = 570
MOVING_AVRAGE = 10
