import tkinter as tk
import gvxrPython3 as gvxr

class GeometricalTransformation:
    def __init__(self, root, aText, XRayVis):

        self.root = root;

        self.xray_vis = XRayVis;

        self.selected_node = aText;

        self.rotation_dictionary = dict();
        self.transformation_dictionary = dict();

        self.x_rotation_value = tk.IntVar()
        self.y_rotation_value = tk.IntVar()
        self.z_rotation_value = tk.IntVar()

        self.x_rotation_value.set(0)
        self.y_rotation_value.set(0)
        self.z_rotation_value.set(0)

        self.createWindow();
        self.updateWindowTitle(self.selected_node);
        #root.wait_window(self.window)

    def createWindow(self):
        self.window = tk.Toplevel(self.root);

        self.x_rotation_slider = tk.Scale(self.window, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.x_rotation_value, command=self.setXRotation)
        self.x_rotation_label = tk.Label(self.window)

        self.y_rotation_slider = tk.Scale(self.window, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.y_rotation_value, command=self.setYRotation)
        self.y_rotation_label = tk.Label(self.window)

        self.z_rotation_slider = tk.Scale(self.window, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.z_rotation_value, command=self.setZRotation)
        self.z_rotation_label = tk.Label(self.window)

        self.button = tk.Button(self.window, text="Reset", command=self.setReset)

        self.x_rotation_slider.pack()
        self.x_rotation_label.pack()

        self.y_rotation_slider.pack()
        self.y_rotation_label.pack()

        self.z_rotation_slider.pack()
        self.z_rotation_label.pack()

        self.button.pack(anchor=tk.CENTER)


        #self.updateWidgetStatus();

    def setXRotation(self, event):
        selection = "Rotation in X = " + str((self.x_rotation_value.get())) + ' degrees'
        self.x_rotation_label.config(text = selection)
        gvxr.rotateNode(self.selected_node, self.x_rotation_value.get() - self.rotation_dictionary[self.selected_node][0], 1, 0 ,0);
        self.rotation_dictionary[self.selected_node][0] = self.x_rotation_value.get();
        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()
        self.xray_vis.draw(x_ray_image);

    def setYRotation(self, event):
        selection = "Rotation in Y = " + str((self.y_rotation_value.get())) + ' degrees'
        self.y_rotation_label.config(text = selection)
        gvxr.rotateNode(self.selected_node, self.y_rotation_value.get() - self.rotation_dictionary[self.selected_node][1], 0, 1 ,0);
        self.rotation_dictionary[self.selected_node][0] = self.y_rotation_value.get();
        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()
        self.xray_vis.draw(x_ray_image);

    def setZRotation(self, event):
        selection = "Rotation in Z = " + str((self.z_rotation_value.get())) + ' degrees'
        self.z_rotation_label.config(text = selection)
        gvxr.rotateNode(self.selected_node, self.z_rotation_value.get() - self.rotation_dictionary[self.selected_node][2], 0, 0 ,1);
        self.rotation_dictionary[self.selected_node][0] = self.z_rotation_value.get();
        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()
        self.xray_vis.draw(x_ray_image);

    def setReset(self):
        print ("Reset roation of ", self.selected_node);
        self.x_rotation_value.set(0);
        self.y_rotation_value.set(0);
        self.z_rotation_value.set(0);

        self.setZRotation(0);
        self.setYRotation(0);
        self.setXRotation(0);

        gvxr.setNodeTransformationMatrix(self.selected_node, self.transformation_dictionary[self.selected_node]);
        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()
        self.xray_vis.draw(x_ray_image);


    def updateWindowTitle(self, aSelectedNode):
        self.selected_node = aSelectedNode;
        self.window.title("Set geometrical transformation of Node " + self.selected_node);

        # The node is not in the dictionary
        if self.selected_node not in self.rotation_dictionary:
            print (self.selected_node, " is not in the dictionary");
            # Add the node to the dictionary
            self.rotation_dictionary[self.selected_node] = [0, 0, 0];
        # The node is in the dictionary
        else:
            print (self.selected_node, " is in the dictionary");
            print ("Its rotation angles are ", self.rotation_dictionary[self.selected_node])

        # The node is not in the dictionary
        if self.selected_node not in self.transformation_dictionary:
            print (self.selected_node, " is not in the dictionary");
            # Add the node to the dictionary
            self.transformation_dictionary[self.selected_node] = gvxr.getNodeTransformationMatrix(self.selected_node);

        self.x_rotation_value.set(self.rotation_dictionary[self.selected_node][0]);
        self.y_rotation_value.set(self.rotation_dictionary[self.selected_node][1]);
        self.z_rotation_value.set(self.rotation_dictionary[self.selected_node][2]);

        self.setXRotation(self.x_rotation_value.get());
        self.setYRotation(self.y_rotation_value.get());
        self.setZRotation(self.z_rotation_value.get());

    def updateElementDensity(self, event):
        self.density.set(gvxr.getElementDensity(event));

        selection = str(self.density.get())
        self.density_text.delete(0, len(self.density_text["text"]));

        self.density_text.insert(0, selection)
        self.density_text.pack()

        self.density_text["text"] = selection;
        self.density_text.pack()

        self.density_text["text"] = selection;
        self.density_text.pack()

        self.density_text.config(text = selection)
        self.density_text.pack()

        self.density_text.config(text = selection)
        self.density_text.pack()


    def clicOK(self):
        self.cancel = False;
        self.window.destroy()

    def clicCancel(self):
        self.cancel = True;
        self.window.destroy()

    def updateWidgetStatus(self):
        self.hounsfield_slider.configure(state = tk.DISABLED);
        self.element_menu.configure(state = tk.DISABLED);
        self.mixture_text.configure(state = tk.DISABLED);
        self.compound_text.configure(state = tk.DISABLED);
        self.density_text.configure(state = tk.DISABLED);

        # Element
        if self.materialType.get() == 0:
            self.element_menu.configure(state = 'normal');
            self.density_text.configure(state = 'normal');
        # Mixture
        elif self.materialType.get() == 1:
            self.mixture_text.configure(state = 'normal');
            self.density_text.configure(state = 'normal');
        # Compound
        elif self.materialType.get() == 2:
            self.compound_text.configure(state = 'normal');
            self.density_text.configure(state = 'normal');
        # Hounsfield unit
        elif self.materialType.get() == 3:
            self.hounsfield_slider.configure(state = 'normal');
        # Mass attenuation coefficient
        elif self.materialType.get() == 4:
            print("?");
            self.density_text.configure(state = 'normal');
        # Linear attenuation coefficient
        elif self.materialType.get() == 5:
            print("?");
            self.density_text.configure(state = 'normal');
