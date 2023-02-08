# Student Name: Zeynep Baydemir
# Student Number: 
# Compile Status: Compiling
# Program Status: Working
# Notes:

from mpi4py import MPI
import argparse

comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

# parses arguments in command line to get the name of the input file, test file and merge method
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, required=True)
parser.add_argument('--merge_method', type=str, required=True)
parser.add_argument('--test_file', type=str, required=True)
args = parser.parse_args()


# distributes data line by line to workers almost evenly
# every worker is a key in the dictionary and the list of lines for each worker are the values of the dictionary
def input_distributor(sample_file):
    # list of lines of the input
    input_lines = sample_file.readlines()
    # checks end of the input lines
    while bool(input_lines):
        for k in range(1, world_size):
            # checks whether the end of the input file
            if bool(input_lines):
                # adds line to the value of the worker in the dictionary
                if k in input_dict.keys():
                    (input_dict[k].append(input_lines.pop(0)))
                else:
                    input_dict[k] = []
    # sends value of the worker in the dictionary which is list of lines
    for j in range(1, world_size):
        comm.send(input_dict[j], dest=j, tag=11)


# reads test file and calculates the probability of bigram by dividing number of bigram to number of first word
# writes the probability
def test_prob_calculator(test_file):
    # list of lines of the test file
    test_lines = test_file.readlines()
    for line in test_lines:
        # checks bigram exist
        if (line.split("\n"))[0] in dict_for_prob.keys():
            # number of the bigram
            numerator = dict_for_prob[(line.split("\n"))[0]]
            # number of the first word of the bigram
            denominator = dict_for_prob[(line.split())[0]]
            # number of the bigram / number of the first word
            probability = float(numerator) / float(denominator)
        else:
            probability = 0
        print("P(" + (line.split("\n"))[0] + ") = " + str(probability))


# adds bigrams and unigrams in the data that is sent from worker to dictionary of all unigrams and bigrams
def add_dict_elem(dict_from_workers, dict_for_probs):
    for key in dict_from_workers.keys():
        if key in dict_for_probs.keys():
            # increasing value of unigram or bigram by the value of it if unigram or bigram exist
            dict_for_probs[key] += dict_from_workers[key]
        else:
            # adding key to dictionary with value of the key
            dict_for_probs[key] = dict_from_workers[key]
    return dict_for_probs


#  splits data of workers to unigrams and bigrams and adds them to dictionary of worker
def data_to_dict(data_of_workers, workers_dict):
    for sentence in data_of_workers:
        index = 0
        # line without '\n' at the end of the line
        sentence_no_endline = sentence.split("\n")
        # list of words in the list
        word_list = sentence_no_endline[0].split()
        n_of_words = len(word_list)
        for word in word_list:
            # adds bigram to the dictionary
            if index < (n_of_words - 1):
                # creates bigram
                str_bi = word_list[index] + " " + word_list[index + 1]
                # adds bigram to dictionary
                if str_bi in workers_dict:
                    workers_dict[str_bi] += 1
                else:
                    workers_dict[str_bi] = 1
                index += 1
            # adds unigram to the dictionary
            if word in workers_dict.keys():
                workers_dict[word] += 1
            else:
                workers_dict[word] = 1
    return workers_dict


# checks requirement type
merge_method = args.merge_method
if merge_method == "MASTER":
    is_master = True
elif merge_method == "WORKERS":
    is_master = False

# master opens input and test files
# distributes data almost evenly by calling input_distributor function
# gets data from workers or the last worker according to argument and adds all unigrams and bigrams to dictionary
# calculates probability of bigram
if rank == 0:
    f_input = open(args.input_file, "r")
    # a dictionary to distribute data to workers
    input_dict = {}
    input_distributor(f_input)
    # a dictionary which will include all bigrams and unigrams to calculate the probabilty
    dict_for_prob = {}
    f_test = open(args.test_file, "r")
    # if argument is MASTER, receive data from all workers
    if is_master:
        for i in range(1, world_size):
            dict_from_worker = comm.recv(source=i, tag=11)
            # adds bigrams and unigrams that received from worker to dictionary of all unigrams and bigrams
            add_dict_elem(dict_from_worker, dict_for_prob)
    # if argument is WORKERS, receive data from the last worker
    else:
        dict_from_worker = comm.recv(source=world_size-1, tag=11)
        # adds bigrams and unigrams that received from worker to dictionary of all unigrams and bigrams
        add_dict_elem(dict_from_worker, dict_for_prob)
    # calculates probability of bigram
    test_prob_calculator(f_test)

else:
    if is_master:
        # worker receives data from master
        data = comm.recv(source=0, tag=11)
        # prints number of lines for each worker
        print("rank " + str(rank) + ": " + str(len(data)))
        worker_dict = {}
        # splits data of worker to unigrams and bigrams
        data_to_dict(data, worker_dict)
        # worker sends dictionary of bigrams and unigrams to the master
        comm.send(worker_dict, dest=0, tag=11)
    else:
        # worker receives data from master
        data = comm.recv(source=0, tag=11)
        print("rank " + str(rank) + ": " + str(len(data)))
        # if the worker is the first worker
        if rank == 1:
            worker_dict = {}
            # splits data of worker to unigrams and bigrams
            data_to_dict(data, worker_dict)
            # if there is only one worker, it sends dictionary of bigrams and unigrams to the master
            if world_size == 2:
                comm.send(worker_dict, dest=0, tag=11)
            # if there is more than one worker, it sends dictionary of bigrams and unigrams to the second worker
            else:
                comm.send(worker_dict, dest=2, tag=11)
        else:
            # receives dictionary of bigrams and unigrams from the previous worker
            previous_worker_dict = comm.recv(source=rank-1, tag=11)
            # if the previous worker sends data successfully
            if previous_worker_dict:
                worker_dict = {}
                # splits data of worker to unigrams and bigrams
                data_from_source = data_to_dict(data, worker_dict)
                # adds bigrams and unigrams from the previous worker to its dictionary
                cumulative_dict = add_dict_elem(previous_worker_dict, data_from_source)
                # the last worker sends dictionary that includes all bigrams and unigrams to master
                if rank == world_size-1:
                    comm.send(cumulative_dict, dest=0, tag=11)
                # the worker sends dictionary that includes bigrams and unigrams in its data to next worker
                else:
                    comm.send(cumulative_dict, dest=rank+1, tag=11)
