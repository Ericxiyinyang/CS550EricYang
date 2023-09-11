from art import tprint

print("Hello world!")
first_name = input("What is your name? \n>>>")
print(f"Hello! {first_name}. Nice to meet you!")
# print("Hello!")
# tprint(first_name)
location = input("Where are you from? (town) \n>>>")
location.lower().strip()

if location == "vancouver" or "van":
    print("No way! I'm from Vancouver too!")
else:
    print("Nice to know!")