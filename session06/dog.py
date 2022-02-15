class dog:
    def __init__(self, the_name, the_age):
        self.name = the_name
        self.age = the_age

    def say_your_name(self):
        print("I'm {}, and I'm sitting down here".format(self.name))

    def show_your_age(self):
        print("I'm {} years old!".format(self.age))

    def say_what_you_like(self):
        print("I like aritmetic")

    def multiply(self, first_operand, second_operand):
        print(f'easy! the result is {first_operand * second_operand}')

ares = dog('ares', 10)  #def __init__(self, the_name, the_age):, the_name = ares, the_age = 10
ares.say_your_name()
ares.show_your_age()
ares.say_what_you_like()
ares.multiply(3,5)