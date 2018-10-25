import tkinter as tk
from tkinter import ttk
import MaterialSelection
import gvxrPython3 as gvxr

class App:
    def __init__(self, anEnergy):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=480, height=800, background="blue")

        self.rotation_var           = tk.DoubleVar()
        self.artefact_filtering_var = tk.IntVar()
        self.energy_var             = tk.DoubleVar();
        self.energy_var.set(anEnergy);
        self.source_shape = tk.IntVar()
        self.energy_var.set(0);

        MODES = [
                ("None", 0),
                ("CPU",  1),
                ("GPU",  2),
        ]

        self.artefact_filtering_var.set(2)
        self.artefactFilteringSelection();


        for text, mode in MODES:
            self.b = tk.Radiobutton(self.canvas, text=text,
                    variable=self.artefact_filtering_var, value=mode,  command=self.artefactFilteringSelection)
            self.b.pack(anchor=tk.W)

        self.scale = tk.Scale(self.canvas ,from_=0, to=359, variable = self.rotation_var,  command=self.rotationScene, orient=tk.HORIZONTAL )
        self.scale.pack(anchor=tk.CENTER)

        self.last_angle = 0

        self.angle_label = tk.Label(self.canvas)
        self.angle_label.pack()
        self.rotationScene(0);


        self.energy = tk.Scale(self.canvas ,from_=0.001, to=100000, resolution=0.001, variable = self.energy_var,  command=self.setEnergy, orient=tk.HORIZONTAL )
        self.energy.pack(anchor=tk.CENTER)

        self.energy_label = tk.Label(self.canvas)
        self.energy_label.pack()
        self.setEnergy(0)

        MODES = [
                ("Point source", 0),
                ("Parallel beam",  1),
        ]

        for text, mode in MODES:
            temp = tk.Radiobutton(self.canvas, text=text, variable=self.source_shape, value=mode, command=self.setSourceShape)
            temp.pack(anchor=tk.W)

        print ("Set the source shape");
        self.setSourceShape();

        self.button = tk.Button(self.canvas, text="Save images", command=self.saveImage)
        self.button.pack(anchor=tk.CENTER)


        self.tree = ttk.Treeview(self.canvas, columns=("Children", "Material", "Density"))
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        self.tree.heading("Children", text="Children");
        self.tree.heading("Material",       text="Material");
        self.tree.heading("Density",       text="Density");

        self.tree.pack(padx=10, pady=10)

        node_label='root';
        children=gvxr.getNumberOfChildren(node_label);
        node_id = self.tree.insert('', 'end', text=node_label,values=(children, "N/A", "N/A"))

        list_of_parents = [];

        if children:
            list_of_parents.append((node_label, node_id));

        while len(list_of_parents):
            (parent_label, parent_id) = list_of_parents[-1];
            list_of_parents.pop();

            for i in range(gvxr.getNumberOfChildren(parent_label)):
                child_label = gvxr.getChildLabel(parent_label, i);
                child_children = gvxr.getNumberOfChildren(child_label);

                node_id = self.tree.insert(parent_id, 'end', text=child_label, values=(str(0), gvxr.getMaterialLabel(child_label), str(gvxr.getDensity(child_label))))

                if child_children:
                    list_of_parents.append((child_label, node_id));



        self.canvas.pack();

        self.root.after(10, self.idle)

        self.root.mainloop()

    def setSourceShape(self):
        if self.source_shape.get() == 0:
            print ("Use point source");
            gvxr.usePointSource();

        elif self.source_shape.get() == 1:
            print ("Use parallel beam");
            gvxr.useParallelBeam();

        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()

    def setEnergy(self, event):
        global x_ray_image
        gvxr.setMonoChromatic(self.energy_var.get(), "MeV", 1);
        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()

        selection = "Energy = " + str((self.energy_var.get())) + ' MeV'
        self.energy_label.config(text = selection)


    def OnDoubleClick(self, event):
        item = self.tree.identify('item', event.x, event.y)

        text = self.tree.item(item,"text")
        if text == "root":
            print ("Ignore root")
        elif text == "":
            print ("Ignore empty name")
        else:
            print("you clicked on", text)

            material_selection = MaterialSelection.MaterialSelection(self.root, text, gvxr.getMaterialLabel(text), gvxr.getDensity(text));
            child_children = gvxr.getNumberOfChildren(text);

            if material_selection.cancel == False:
                global x_ray_image;

                # Element
                if material_selection.materialType.get() == 0:
                    gvxr.setElement(text, material_selection.element_name.get());
                    gvxr.setDensity(text, float(material_selection.density.get()), "g/cm3");
                # Mixture
                elif material_selection.materialType.get() == 1:
                    gvxr.setMixture(text, material_selection.mixture.get());
                    gvxr.setDensity(text, float(material_selection.density.get()), "g/cm3");
                # Compound
                elif material_selection.materialType.get() == 2:
                    gvxr.setCompound(text, material_selection.compound.get());
                    gvxr.setDensity(text, float(material_selection.density.get()), "g/cm3");
                # Hounsfield unit
                elif material_selection.materialType.get() == 3:
                    gvxr.setHU(text, material_selection.hounsfield_value.get());
                # Mass attenuation coefficient
                elif material_selection.materialType.get() == 4:
                    gvxr.setDensity(text, float(material_selection.density.get()), "g/cm3");
                    print("?");
                # Linear attenuation coefficient
                elif material_selection.materialType.get() == 5:
                    gvxr.setDensity(text, float(material_selection.density.get()), "g/cm3");
                    print("?");

                self.tree.item(item, values=(str(child_children), gvxr.getMaterialLabel(text), str(gvxr.getDensity(text))))

                x_ray_image = gvxr.computeXRayImage();
                gvxr.displayScene()

                #node_id = self.tree.insert(parent_id, 'end', text=child_label, values=(str(0), gvxr.getMaterialLabel(child_label)))


    def artefactFilteringSelection(self):
        global x_ray_image;

        value = self.artefact_filtering_var.get();
        if value is 0:
            gvxr.disableArtefactFiltering();
        elif value is 1:
            gvxr.enableArtefactFilteringOnCPU();
        elif value is 2:
            gvxr.enableArtefactFilteringOnGPU();

        x_ray_image = gvxr.computeXRayImage();


    def rotationScene(self, widget):
        global x_ray_image;
        selection = "Angle = " + str(int(self.rotation_var.get())) + ' deg'
        self.angle_label.config(text = selection)

        gvxr.rotateScene(self.rotation_var.get() - self.last_angle, 0, -1, 0);
        self.last_angle = self.rotation_var.get();

        x_ray_image = gvxr.computeXRayImage();
        gvxr.displayScene()


    def saveImage(self):
        gvxr.saveLastLBuffer();
        gvxr.saveLastXRayImage();

    def idle(self):
        gvxr.displayScene()
        '''w=random.randint(1,100)
        h=random.randint(1,100)
        canvas.create_rectangle(w,h,w+150,h+150)
        def callback(event):
            if True:
                print("clicked2")
                tk.after_cancel(task)
        canvas.bind("<Button-1>",callback)
        tk.after(1000,task) '''
        self.root.after(10, self.idle)