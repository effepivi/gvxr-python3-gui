#!/usr/bin/env python3


#from PIL import Image

import random
import matplotlib
import sys, argparse

import numpy as np

import gvxrPython3 as gvxr
import App

x_ray_image = 0;

def main(argv):
    global x_ray_image;

    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, help="Input file (see http://assimp.sourceforge.net/main_features_formats.html for a list of supported file formats)")
    parser.add_argument("-unit",  type=str, help="Unit of length corresponding to the input", choices=["um", "mm", "cm", "dm", "m", "dam", "hm", "km"]);

    args = parser.parse_args()
    if args.input and args.unit:
        # Create an OpenGL context
        print("Create an OpenGL context")
        gvxr.createWindow();
        gvxr.setWindowSize(512, 512);


        # Set up the beam
        print("Set up the beam")
        gvxr.setSourcePosition(100.0, 0.0, 0.0, "cm");
        gvxr.usePointSource();
        #gvxr.useParallelBeam();
        gvxr.setMonoChromatic(0.08, "MeV", 1);

        # Set up the detector
        print("Set up the detector");
        gvxr.setDetectorPosition(-40.0, 0.0, 0.0, "cm");
        gvxr.setDetectorUpVector(0, 0, -1);
        gvxr.setDetectorNumberOfPixels(1024, 1024);
        gvxr.setDetectorPixelSize(0.5, 0.5, "mm");

        # Load the data
        print("Load the data");

        gvxr.loadSceneGraph(args.input, args.unit);

        gvxr.disableArtefactFiltering();

        #gvxr.loadMeshFile("chest", "./HVPTest/chest2.obj", "mm");
        #gvxr.invertNormalVectors("armR");
        #gvxr.invertNormalVectors("chest");

        node_label_set = [];
        node_label_set.append('root');

        # The list is not empty
        while (len(node_label_set)):

            # Get the last node
            last_node = node_label_set[-1];

            # Initialise the material properties
            #print("Set ", label, "'s Hounsfield unit");
            #gvxr.setHU(label, 1000)
            Z = gvxr.getElementAtomicNumber("H");
            gvxr.setElement(last_node, gvxr.getElementName(Z));

            # Change the node colour to a random colour
            gvxr.setColour(last_node, random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1.0);

            # Remove it from the list
            node_label_set.pop();

            # Add its Children
            for i in range(gvxr.getNumberOfChildren(last_node)):
                node_label_set.append(gvxr.getChildLabel(last_node, i));

            '''
        for label in gvxr.getMeshLabelSet():
            print("Move ", label, " to the centre");
            #gvxr.moveToCentre(label);

            #print("Move the mesh to the center");
            #gvxr.moveToCenter(label);

            #gvxr.invertNormalVectors(label);
        '''
        #gvxr.moveToCentre();
        gvxr.moveToCentre('root');

        # Compute an X-ray image
        #print("Compute an X-ray image");
        gvxr.disableArtefactFiltering();
        #gvxr.enableArtefactFilteringOnGPU();
        # Not working anymore gvxr.enableArtefactFilteringOnGPU();
        # Not working anymore gvxr.enableArtefactFilteringOnCPU();
        x_ray_image = np.array(gvxr.computeXRayImage());
        '''x_ray_image -= 0.0799;
        x_ray_image /= 0.08 - 0.0799;
        plt.ioff();
        plt.imshow(x_ray_image, cmap="gray");
        plt.show()
        '''
        #gvxr.setShiftFilter(-0.0786232874);
        #gvxr.setScaleFilter(726.368958);



        gvxr.displayScene()

        app = App.App(0.08);
        app.mainLoop();

if __name__ == "__main__":
   main(sys.argv[1:])

   exit()
