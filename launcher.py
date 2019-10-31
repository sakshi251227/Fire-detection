import argparse

from test_model import graphically_test_model, evaluate_model
from train_inception_based_model import train_and_save_Inception_based_model
from video_fire_detection import detect_fire_on_the_fly
from keras.applications.inception_v3 import preprocess_input as inception_preprocess_input


if __name__ == '__main__':

    classes = ['fire', 'no_fire', 'start_fire']

    parser = argparse.ArgumentParser(description='Convolutional neural network for forest fire detection',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(title='Mode selection',
                                       description='Network can be trained on a provided dataset or predictions can be'
                                                   'made using a pre-trained model',
                                       help='', dest='mode')

    subparsers.required = True

    parser_train = subparsers.add_parser('train',
                                         help='Create and train the InceptionV3-based model.',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_train.add_argument('-data',
                              type=str,
                              action='store',
                              dest='dataset',
                              help='Path to the dataset on which to train.',
                              default=argparse.SUPPRESS,
                              required=True)

    parser_train.add_argument('-prop',
                              type=float,
                              action='store',
                              dest='proportion',
                              help='Proportion of the dataset to be used for training (the rest is for validation).',
                              default=argparse.SUPPRESS,
                              required=True)

    parser_train.add_argument('-epochs',
                              type=int,
                              action='store',
                              dest='epochs',
                              help='Number of epochs.',
                              default=10,
                              required=False)

    parser_train.add_argument('-batch',
                              type=int,
                              action='store',
                              dest='batch_size',
                              help='Size of a batch.',
                              default=32,
                              required=False)

    parser_tune = subparsers.add_parser('tune', help='Fine-tune an pre-trained Inception-V3-based model.',
                                        formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser_tune.add_argument('-model',
                             type=str,
                             action='store',
                             dest='model_path',
                             help='Path to the pre-trained model.',
                             default=argparse.SUPPRESS,
                             required=True)

    parser_tune.add_argument('-lr',
                             type=float,
                             action='store',
                             dest='learning_rate',
                             help='Learning rate to be used for fine-tuning.',
                             default=0.001,
                             required=False)

    parser_tune.add_argument('-data',
                              type=str,
                              action='store',
                              dest='dataset',
                              help='Path to the dataset on which to train.',
                              default=argparse.SUPPRESS,
                              required=True)

    parser_tune.add_argument('-prop',
                              type=float,
                              action='store',
                              dest='proportion',
                              help='Proportion of the dataset to be used for training (the rest is for validation).',
                              default=argparse.SUPPRESS,
                              required=True)

    parser_tune.add_argument('-epochs',
                              type=int,
                              action='store',
                              dest='epochs',
                              help='Number of epochs.',
                              default=10,
                              required=False)

    parser_tune.add_argument('-batch',
                              type=int,
                              action='store',
                              dest='batch_size',
                              help='Size of a batch.',
                              default=32,
                              required=False)

    parser_predict = subparsers.add_parser('predict',
                                           help='Perform prediction on a provided picture.')

    parser_predict.add_argument('-path',
                                type=str,
                                action='store',
                                dest='image_path',
                                help='Path to an image.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_predict.add_argument('-model',
                                type=str,
                                action='store',
                                dest='model_path',
                                help='Path to a trained model.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_video = subparsers.add_parser('video',
                                           help='Perform prediction on a video.',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_video.add_argument('-in',
                                type=str,
                                action='store',
                                dest='input_video_path',
                                help='Path to an mp4 video.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_video.add_argument('-out',
                                type=str,
                                action='store',
                                dest='output_video_path',
                                help='Path to output annotated mp4 video.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_video.add_argument('-model',
                                type=str,
                                action='store',
                                dest='model_path',
                                help='Path to a trained model.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_video.add_argument('-freq',
                                type=str,
                                action='store',
                                dest='freq',
                                help='Prediction is to be made every freq frames.',
                                default=12,
                                required=False)

    parser_test = subparsers.add_parser('test',
                                           help='Test a model on a test set of images.')

    parser_test.add_argument('-data',
                                type=str,
                                action='store',
                                dest='dataset',
                                help='Path to a test set.',
                                default=argparse.SUPPRESS,
                                required=True)

    parser_test.add_argument('-model',
                                type=str,
                                action='store',
                                dest='model_path',
                                help='Path to a trained model.',
                                default=argparse.SUPPRESS,
                                required=True)

    parsed = parser.parse_args()

    if parsed.mode == "train":

        train_and_save_Inception_based_model(parsed.dataset,
                                             fine_tune_existing=None,
                                             learning_rate=0.001,
                                             percentage=parsed.proportion,
                                             nbr_epochs=parsed.epochs,
                                             batch_size=parsed.batch_size)

    elif parsed.mode == "tune":

        train_and_save_Inception_based_model(parsed.dataset,
                                             fine_tune_existing=parsed.model_path,
                                             learning_rate=parsed.learning_rate,
                                             percentage=parsed.proportion,
                                             nbr_epochs=parsed.epochs,
                                             batch_size=parsed.batch_size)
    elif parsed.mode == "predict":
        print('image path: ', parsed.image_path)
        print('model path: ', parsed.model_path)

    elif parsed.mode == "video":

        detect_fire_on_the_fly(parsed.input_video_path,
                               parsed.output_video_path,
                               parsed.model_path,
                               inception_preprocess_input,
                               (224,224),
                               parsed.freq)

    elif parsed.mode == "test":
        print(evaluate_model(parsed.model_path, classes, inception_preprocess_input, parsed.dataset))