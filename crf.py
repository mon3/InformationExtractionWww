import training_set_preparation
import argparse
import pycrfsuite
import numpy as np
from sklearn.metrics import classification_report
import pickle
import os

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs_path", dest="docs_path", type=str,
                        default="conferences-data/pagestorage-annotated")
    parser.add_argument("--model_name", dest="model_name", type=str, \
                        default="crf.model")
    parser.add_argument("--max_iterations", dest="max_iterations", type=int, default=1000)
    parser.add_argument("--train", dest="train", type=str2bool, default="true")
    parser.add_argument("--test", dest="test", type=str2bool, default="true")

    parser.add_argument("--serialized_data_path", dest="serialized_data_path", type=str,
                        default="serialized_data")
    return parser.parse_args()

def get_data(args):
    paths = [ os.path.join(args.serialized_data_path, 'X_train'),
              os.path.join(args.serialized_data_path, 'X_test'),
              os.path.join(args.serialized_data_path, 'Y_train'),
              os.path.join(args.serialized_data_path, 'Y_test') ]

    def pickle_data_save(data, file):
        n_bytes = 2 ** 31
        max_bytes = 2 ** 31 - 1
        bytes_out = pickle.dumps(data)
        with open(file, 'wb') as fp:
            for idx in range(0, n_bytes, max_bytes):
                fp.write(bytes_out[idx:idx + max_bytes])


    def pickle_data_load(file_path):
        max_bytes = 2 ** 31 - 1
        bytes_in = bytearray(0)
        input_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        return pickle.loads(bytes_in)

    for name in paths:
        if not os.path.isfile(name):

            print("Preparing data")
            X_train, X_test, Y_train, Y_test = \
                training_set_preparation.prepare_training_data(args.docs_path)

            print("X_train saving...")
            pickle_data_save(X_train, paths[0])
            print("Done")

            print("X_test saving...")
            pickle_data_save(X_test, paths[1])
            print("Done")

            print("Y_train saving...")
            pickle_data_save(Y_train, paths[2])
            print("Done")

            print("Y_test saving...")
            pickle_data_save(Y_test, paths[3])
            print("Done")

    print("X_train loading...")
    X_train = pickle_data_load(paths[0])
    print("Done")

    print("X_test loading...")
    X_test = pickle_data_load(paths[1])
    print("Done")

    print("Y_train loading...")
    Y_train = pickle_data_load(paths[2])
    print("Done")

    print("Y_test loading...")
    Y_test = pickle_data_load(paths[3])
    print("Done")

    print("Y_train labelling: ")
    truths = np.array([tag for row in Y_train for tag in row])
    unique, counts = np.unique(truths, return_counts=True)
    print(dict(zip(unique, counts)))

    print("Y_test: ")
    truths = np.array([tag for row in Y_test for tag in row])
    unique, counts = np.unique(truths, return_counts=True)
    print(dict(zip(unique, counts)))

    return X_train, X_test, Y_train, Y_test


def report_metrics(X_test, Y_test, args):
    print("\n\nReporting metrics...")
    labels = {'NAME': 0, 'TIME': 1, 'PLACE': 2, 'SHORT': 3, "DIFF": 4}

    tagger = pycrfsuite.Tagger()
    tagger.open(args.model_name)

    y_pred = [tagger.tag(xseq) for xseq in X_test]

    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in Y_test for tag in row])

    unique, counts = np.unique(truths, return_counts=True)
    print("TRUTHS:", dict(zip(unique, counts)))

    unique, counts = np.unique(predictions, return_counts=True)
    print("PREDICTIONS:", dict(zip(unique, counts)))

    print(classification_report(
        truths, predictions,
        target_names=["NAME", "TIME", 'PLACE', 'SHORT', "DIFF"]))


def prepare_crf_trainer(X_train, Y_train):
    trainer = pycrfsuite.Trainer(verbose=True)  # verbose = TRue wypisze
    # progres trenowania

    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    # Set the parameters of the model
    trainer.set_params({
        # coefficient for L1 penalty
        'c1': 0.1,

        # coefficient for L2 penalty
        'c2': 0.01,

        # maximum number of iterations
        'max_iterations': 100000,

        # whether to include transitions that
        # are possible, but not observed
        'feature.possible_transitions': True
    })

    # Provide a file name as a parameter to the train function, such that
    # the model will be saved to the file when training is finished
    return trainer


def main():

    args = parse_arguments()
    X_train, X_test, Y_train, Y_test = get_data(args)

    if args.train:
        trainer = prepare_crf_trainer(X_train, Y_train)
        trainer.train(args.model_name)

    if args.test:
        report_metrics(X_test, Y_test, args)

if __name__== "__main__":
    main()
