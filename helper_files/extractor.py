import argparse
import pycrfsuite

from actors.utils import training_set_preparation
from actors.utils.htmlparser import get_filtered_text


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs_path", dest="docs_path", type=str,
                        default="conferences-data/real-data")
    parser.add_argument("--model_name", dest="model_name", type=str, \
                        default="crf.model")
    return parser.parse_args()

def get_labelling(X_test, args):

    tagger = pycrfsuite.Tagger()
    tagger.open(args.model_name)
    y_pred = [tagger.tag(xseq) for xseq in X_test]
    i = 0
    for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
        if x != 'DIFF' :
            print("%s (%s)" % (y, x))


def main():
    args = parse_arguments()
    X_train, X_test, Y_train, Y_test = training_set_preparation.prepare_training_data(args.docs_path)
    print(len(X_test))
    get_labelling(X_test, args)



if __name__== "__main__":
    main()
