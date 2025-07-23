import re
import time

exit_commands = ["exit", "quit", "bye", "goodbye"]

response_patterns = {
    r'\b(hello|hi)\b': lambda: "HELLO! HOW CAN I ASSIST YOU TODAY?",
    r'\b(what|how)\b.*\b(name|your name)\b': lambda: "MY NAME IS ELIZA, YOUR VIRTUAL ASSISTANT.",
    r'\b(what|how)\b.*\b(feeling|feel|doinghi)\b': lambda: "I'M JUST A PROGRAM, BUT I'M HERE TO HELP YOU WITH YOUR FEELINGS.",
    r'\b(sad|unhappy|depressed)\b': lambda: "I'M SORRY TO HEAR THAT YOU'RE FEELING THIS WAY. IT'S IMPORTANT TO TALK ABOUT IT.",
    r'\b(happy|joyful|excited)\b': lambda: "THAT'S GREAT TO HEAR! WHAT IS MAKING YOU FEEL THIS WAY?",
    r'\b(what|how)\b.*\b(time|date)\b': lambda: "RIGHT NOW, IT'S " + time.strftime("%Y-%m-%d %H:%M:%S") + ".",
}

def run_eliza():
    user_input = ""

    while user_input.lower() not in exit_commands:
        user_input = input("")
        
        if user_input.lower() in exit_commands:
            print("GOODBYE! TAKE CARE!")
            break
        else:
            response_found = False
            for pattern, response_fn in response_patterns.items():
                if re.search(pattern, user_input, re.IGNORECASE):
                    print("\n")
                    print(response_fn())
                    response_found = True
                    break
            
            if not response_found:
                print("I'M NOT SURE HOW TO RESPOND TO THAT. CAN YOU TELL ME MORE?")

run_eliza()
