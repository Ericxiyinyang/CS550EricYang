from art import tprint
import tqdm

class AlgebraHoudini:
    def __init__(self, input_number):
        self.og_number = input_number

    def magic_calc(self):
        tranformed_number = self.og_number
        print("✨Are you ready to be impressed???✨")
        input("First, add 10 to your number\n(press enter to continue)")
        tranformed_number += 10
        print(f"You should now have: {tranformed_number}")
        input("Next, multiply your number by 2\n(press enter to continue)")
        tranformed_number *= 2
        print(f"You should now have: {tranformed_number}")
        input("Next, subtract 20 from your number\n(press enter to continue)")
        tranformed_number -= 20
        print(f"You should now have: {tranformed_number}")
        input("Finally, divide by your original number\n(press enter to continue)")
        tranformed_number /= self.og_number
        print(f"You should now have: {tranformed_number}")


