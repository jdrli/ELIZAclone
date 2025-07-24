import re
import responses


exit_commands = ["exit", "quit", "bye", "goodbye"]

def run_eliza():
    user_input = ""

    while user_input.lower() not in exit_commands:
        user_input = input("")
        
        if user_input.lower() in exit_commands:
            print("GOODBYE! TAKE CARE!")
            break
        else:
            response_found = False
            for pattern, response_fn in responses.response_patterns.items():
                if re.search(pattern, user_input, re.IGNORECASE):
                    print("\n")
                    print(response_fn())
                    response_found = True
                    break
            
            if not response_found:
                print("I SEE. CAN YOU TELL ME MORE ABOUT THAT?")

run_eliza()
