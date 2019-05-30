import os
import tensorflow as tf
import numpy as np
from PIL import Image
import time

class Classifier():
    
# start constructor
    def __init__(self):

        #Loading graph and labels
        self.RETRAINED_LABELS_TXT_FILE_LOC = os.getcwd() + "/" + "retrained_labels.txt"
        self.RETRAINED_GRAPH_PB_FILE_LOC = os.getcwd() + "/" + "retrained_graph.pb"

        if not self.checkIfNecessaryPathsAndFilesExist():
            print("Graph or label not detected")
        else:
            print("Graph and label found")
        # end if

        # get a list of classifications from the labels file
        self.classifications = []
        # for each line in the label file . . .
        for currentLine in tf.gfile.GFile(self.RETRAINED_LABELS_TXT_FILE_LOC):
            # remove the carriage return
            self.classification = currentLine.rstrip()
            # and append to the list
            self.classifications.append(self.classification)
        # end for

        # show the classifications to prove out that we were able to read the label file successfully
        print("classifications = " + str(self.classifications))

        # load the graph from file
        with tf.gfile.FastGFile(self.RETRAINED_GRAPH_PB_FILE_LOC, 'rb') as retrainedGraphFile:
            # instantiate a GraphDef object
            graphDef = tf.GraphDef()
            # read in retrained graph into the GraphDef object
            graphDef.ParseFromString(retrainedGraphFile.read())
            # import the graph into the current default Graph, note that we don't need to be concerned with the return value
            _ = tf.import_graph_def(graphDef, name='')
        # end with

        with tf.Session() as sess:
            # get the final tensor from the graph
            self.finalTensor = sess.graph.get_tensor_by_name('final_result:0')

        # getting image path
        self.imageFileWithPath = os.path.join(os.getcwd(), "image.jpg")

# end constructor

# start function
    def classify(self):

        with tf.Session() as sess:
            

            # checking if image is saved
            while not os.path.isfile(self.imageFileWithPath):
                print("waiting")
                time.sleep(1)
            

            # loading image
            image = Image.open(self.imageFileWithPath)# will automatically show error if file is not found

            # convert the PIL image (numpy array) to a TensorFlow image
            tfImage = np.array(image)[:, :, 0:3]

            # run the network to get the predictions
            predictions = sess.run(self.finalTensor, {'DecodeJpeg:0': tfImage})

            # sort predictions from most confidence to least confidence
            sortedPredictions = predictions[0].argsort()[-len(predictions[0]):][::-1]

            # getting the prediction
            strClassification = self.classifications[sortedPredictions[0]]

            # if the classification (obtained from the directory name) ends with the letter "s", remove the "s" to change from plural to singular
            if strClassification.endswith("s"):
                strClassification = strClassification[:-1]
            # end if

            # get confidence, then get confidence rounded to 2 places after the decimal
            confidence = predictions[0][sortedPredictions[0]]

            # get the score as a %
            scoreAsAPercent = confidence * 100.0

            #deleting the image
            os.remove(self.imageFileWithPath)

            # return result
            return strClassification.title() + ", " + "{0:.2f}".format(scoreAsAPercent) + "% confidence".title()

# start function
    def checkIfNecessaryPathsAndFilesExist(self):

        if not os.path.exists(self.RETRAINED_LABELS_TXT_FILE_LOC):
            print('ERROR: RETRAINED_LABELS_TXT_FILE_LOC "' + self.RETRAINED_LABELS_TXT_FILE_LOC + '" does not seem to exist')
            return False
        # end if

        if not os.path.exists(self.RETRAINED_GRAPH_PB_FILE_LOC):
            print('ERROR: RETRAINED_GRAPH_PB_FILE_LOC "' + self.RETRAINED_GRAPH_PB_FILE_LOC + '" does not seem to exist')
            return False
        # end if

        return True
# end function
