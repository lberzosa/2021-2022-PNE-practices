class Seq:
    """A class for representing sequences"""

    #OTRA OPCION
    BASES_ALLOWED = ['A', 'C', 'G', 'T'] #es una cosntante dentro de la clase, es una propiedad / atributo de clase
    def are_bases_valid(strbases): #para for, el break se usa para salir, pero no lo solemos usar
        valid = True
        i = 0 #representa el indice / posicion
        while valid and i < len(strbases):
            if strbases[i] in Seq.BASES_ALLOWED: #una constante que le pertenece a toda la clase seq
                i += 1
            else:
                valid = False
        return valid

    def __init__(self, strbases):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        if Seq.are_bases_valid(strbases):
            self.strbases = strbases #atributo de objeto
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("incorrect sequence detected!!")

    def __str__(self):
        """Method called when the object is being printed"""

        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)


# --- Main program
s1 = Seq("AGTACACTGGT")
s2 = Seq("CGTAAC")

# -- Printing the objects
print(f"Sequence 1: {s1}")
print(f"Length: {s1.len()}")
print(f"Sequence 2: {s2}")
print(f"Length: {s2.len()}")

class Gene(Seq):
    """This class is derived from the Seq Class
       All the objects of class Gene will inheritate
       the methods from the Seq class
    """
    def __init__(self, strbases, name=""):
        # -- Call first the Seq initilizer and then the
        # -- Gene init method
        super().__init__(strbases) #el super hace alusion a la clase padre (en este caso es seq, clase que se hereda)
        self.name = name
        print("New gene created")

    def __str__(self):
        return self.name + "-" + self.strbases #especifico del gen, no lo tiene la clase secuencia

# --- Main program
s1 = Seq("AGTACACTGGT")
g = Gene("CGTAAC", "FRAT1")

# -- Printing the objects
print(f"Sequence 1: {s1}")
print(f"Gene: {g}")