import tkinter as tk
import gvxrPython3 as gvxr

class MaterialSelection:
    def __init__(self, root, aText, aMaterialLabel, aDensity):
        self.materialType = tk.IntVar()
        self.hounsfield_value = tk.IntVar()
        self.selected_element = "Hydrogen";
        self.cancel = True;
        self.mixture = tk.StringVar()
        self.compound = tk.StringVar()
        self.density = tk.StringVar()
        self.element_name = tk.StringVar()
        self.compound.set("e.g. H2O for water");
        self.mixture.set("e.g. Ti90Al6V4");
        self.density.set(str(aDensity));

        print(aMaterialLabel)
        if (aMaterialLabel[0 : len("HU: ")] == "HU: "):
            self.materialType.set(3)
            self.hounsfield_value.set(int(aMaterialLabel[len("HU: ") : len(aMaterialLabel)]));

        elif (aMaterialLabel[0 : len("Element: ")] == "Element: "):
            self.materialType.set(0)
            self.selected_element = aMaterialLabel[len("Element: ") : len(aMaterialLabel)];

        elif (aMaterialLabel[0 : len("Mixture: ")] == "Mixture: "):
            self.materialType.set(1)
            self.mixture.set(aMaterialLabel[len("Mixture: ") : len(aMaterialLabel)]);

        elif (aMaterialLabel[0 : len("Compound: ")] == "Compound: "):
            self.materialType.set(2)
            self.compound.set(aMaterialLabel[len("Compound: ") : len(aMaterialLabel)]);
        else:
            print ("It's ??")
            self.materialType.set(0)
            self.hounsfield_value.set(0);

        self.root = root;






        self.createWindow(aText);
        root.wait_window(self.window)

    def createWindow(self, aText):
        self.window = tk.Toplevel(self.root);
        self.window.title("Set material properties of Node " + aText);
        self.buttonOK     = tk.Button(self.window, text="OK", command=self.clicOK)
        self.buttonCancel = tk.Button(self.window, text="Cancel", command=self.clicCancel)
        #self.buttonOK.grid(row=0,column=0, sticky=tk.W)
        #self.buttonCancel.grid(row=0,column=0, sticky=tk.W)
        self.buttonOK.pack(anchor=tk.W)
        self.buttonCancel.pack(anchor=tk.W)

        MODES = [
                ("Element",                        0),
                ("Mixture",                        1),
                ("Compound",                       2),
                ("Hounsfield unit",                3),
                #("Mass attenuation coefficient",   4),
                #("Linear attenuation coefficient", 5),
        ]

        choices = [];
        for i in range(1, 100):
            choices.append(gvxr.getElementName(i));
        self.element_name.set(self.selected_element) # set the default option

        for text, mode in MODES:
            self.b = tk.Radiobutton(self.window, text=text,
                    variable=self.materialType, value=mode,  command=self.updateWidgetStatus)
            self.b.pack(anchor=tk.W)

            if text == "Element":
                self.element_menu = tk.OptionMenu(self.window, self.element_name, *choices, command=self.updateElementDensity);
                self.element_menu.pack(anchor=tk.W)
            elif text == "Mixture":
                self.mixture_text = tk.Entry(self.window, textvariable=self.mixture)
                self.mixture_text.pack()
            elif text == "Compound":
                self.compound_text = tk.Entry(self.window, textvariable=self.compound)
                self.compound_text.pack()
            elif text == "Hounsfield unit":
                self.hounsfield_slider = tk.Scale(self.window, from_=-1000, to=3000, orient=tk.HORIZONTAL, variable=self.hounsfield_value)
                self.hounsfield_slider.pack()

        self.density_text = tk.Entry(self.window, textvariable=self.density)
        self.density_text.pack()

        self.updateWidgetStatus();

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
