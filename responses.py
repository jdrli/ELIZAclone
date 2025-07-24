import re
import time

response_patterns = {
    r'\b(hello|hi|hey)\b': lambda: "HELLO! HOW CAN I ASSIST YOU TODAY?",
    r'\b(how are you|how are you doing)\b': lambda: "I'M JUST A PROGRAM, BUT THANK YOU FOR ASKING.",
    r'\b(who are you|what is your name|your name)\b': lambda: "MY NAME IS ELIZA, YOUR VIRTUAL ASSISTANT.",
    r'\b(what|how)\b.*\b(time|date)\b': lambda: "RIGHT NOW, IT'S " + time.strftime("%Y-%m-%d %H:%M:%S") + ".",

    # Emotions
    r'\b(i feel|i am feeling|i’m feeling)\b.*\b(sad|down|unhappy|depressed|anxious)\b': lambda: "I'M SORRY TO HEAR THAT. WOULD YOU LIKE TO TALK ABOUT WHAT'S MAKING YOU FEEL THAT WAY?",
    r'\b(i feel|i am feeling|i’m feeling)\b.*\b(happy|joyful|good|great|excited)\b': lambda: "THAT'S WONDERFUL TO HEAR! WHAT'S BEEN GOING WELL LATELY?",
    r'\b(i feel|i am feeling|i’m feeling)\b.*\b(angry|mad|furious)\b': lambda: "ANGER CAN BE DIFFICULT TO PROCESS. WHAT DO YOU THINK IS CAUSING THESE FEELINGS?",
    r'\b(i am lonely|i feel lonely|i’m lonely)\b': lambda: "LONELINESS CAN BE HARD. WOULD YOU LIKE TO TALK ABOUT WHAT’S MAKING YOU FEEL THAT WAY?",

    # Self-doubt / fears
    r'\b(i can\'t|i cannot|i’m unable to)\b (.*)': lambda: "WHAT MAKES YOU THINK YOU CAN'T 5?",
    r'\b(i’m afraid|i am scared|i fear)\b': lambda: "FEAR IS A POWERFUL FEELING. WHAT IS IT THAT YOU FEAR?",
    r'\b(i don\'t know)\b': lambda: "IT'S OKAY NOT TO KNOW. CAN YOU TELL ME MORE ABOUT WHAT YOU'RE THINKING?",

    # Goals & dreams
    r'\b(i want to|i wish to|i would like to)\b (.*)': lambda: "WHAT WOULD IT MEAN FOR YOU TO 5?",
    r'\b(my dream is|i dream of|i hope to)\b': lambda: "TELL ME MORE ABOUT THIS DREAM.",
    r'\b(i have a goal|i\'m working on|i plan to)\b': lambda: "WHAT MOTIVATES YOU TOWARD THIS GOAL?",

    # Identity
    r'\b(i am|i’m)\b (.*)': lambda: "HOW LONG HAVE YOU BEEN 5?",
    r'\b(i feel like)\b (.*)': lambda: "WHAT MAKES YOU FEEL LIKE 5?",
    r'\b(i think i am)\b (.*)': lambda: "WHAT MAKES YOU THINK YOU ARE 5?",

    # Relationships
    r'\b(my (mother|father|mom|dad|parent))\b': lambda: "TELL ME MORE ABOUT YOUR RELATIONSHIP WITH YOUR 1.",
    r'\b(my (friend|partner|boyfriend|girlfriend|spouse|husband|wife))\b': lambda: "HOW DO YOU FEEL ABOUT YOUR 1?",
    r'\b(i miss|i lost|passed away|died)\b': lambda: "LOSS CAN BE VERY DIFFICULT. WOULD YOU LIKE TO TALK ABOUT IT?",

    # Questions about ELIZA
    r'\b(do you think)\b': lambda: "I'M MORE INTERESTED IN WHAT *YOU* THINK.",
    r'\b(can you help me)\b': lambda: "I'M HERE TO LISTEN. TELL ME MORE.",
    r'\b(are you real|you are not real|you’re not human)\b': lambda: "THAT'S TRUE. BUT I CAN STILL LISTEN AND RESPOND TO YOUR THOUGHTS.",
    r'\b(do you understand)\b': lambda: "I UNDERSTAND TO THE EXTENT I CAN, GIVEN MY PROGRAMMING. PLEASE, GO ON.",
    
    # Meta & Philosophical
    r'\b(what is the meaning of life)\b': lambda: "MANY PEOPLE STRUGGLE WITH THAT QUESTION. WHAT DOES LIFE MEAN TO YOU?",
    r'\b(why\b.*\bme)\b': lambda: "WHY DO YOU THINK IT'S ABOUT YOU?",
    r'\b(why\b.*\b(hurt|pain|suffer))\b': lambda: "LIFE CAN BE DIFFICULT AT TIMES. HOW HAVE YOU BEEN COPING WITH THESE CHALLENGES?",

    # Default goodbyes
    r'\b(bye|goodbye|see you|exit|quit)\b': lambda: "GOODBYE! TAKE CARE OF YOURSELF.",
}


doctor_rules = {
    "WHY": [
        ("(0 WHY DON'T I 0)", [
            "DO YOU BELIEVE I DON'T 5?",
            "PERHAPS I WILL 5 IN GOOD TIME.",
            "SHOULD YOU 5 YOURSELF?",
            "YOU WANT ME TO 5?",
        ]),
        ("(0 WHY CAN'T I 0)", [
            "DO YOU THINK YOU SHOULD BE ABLE TO 5?",
            "WHY CAN'T YOU 5?",
            "WHAT WOULD IT MEAN IF YOU COULD 5?",
            "HAVE YOU REALLY TRIED?",
        ]),
        ("(0 WHY 0)", [
            "WHY DO YOU THINK 5?",
            "WHAT MAKES YOU ASK THAT?",
            "DOES THAT QUESTION INTEREST YOU?",
        ]),
        ("=WHAT", [])  # fallback
    ],

    "WHAT": [
        ("(0 WHAT 0)", [
            "WHY DO YOU ASK?",
            "WHAT DO YOU THINK?",
            "WHAT COMES TO YOUR MIND WHEN YOU ASK THAT?",
            "DOES THAT QUESTION RELATE TO YOUR PROBLEMS?",
        ])
    ],

    "I": [
        ("(0 I AM 0)", [
            "HOW LONG HAVE YOU BEEN 5?",
            "DO YOU BELIEVE IT IS NORMAL TO BE 5?",
            "DO YOU ENJOY BEING 5?",
            "HOW DOES BEING 5 MAKE YOU FEEL?",
        ]),
        ("(0 I FEEL 0)", [
            "TELL ME MORE ABOUT SUCH FEELINGS.",
            "DO YOU OFTEN FEEL 5?",
            "WHEN DO YOU NORMALLY FEEL 5?",
            "WHAT DOES FEELING 5 MEAN TO YOU?",
        ]),
        ("(0 I WANT 0)", [
            "WHY DO YOU WANT 5?",
            "WHAT WOULD IT MEAN IF YOU GOT 5?",
            "SUPPOSE YOU GOT 5 — WHAT THEN?",
            "WHAT ELSE DO YOU WANT?",
        ]),
        ("(0 I CAN'T 0)", [
            "HOW DO YOU KNOW YOU CAN'T 5?",
            "HAVE YOU TRIED?",
            "PERHAPS YOU COULD IF YOU TRIED.",
            "WHAT WOULD IT TAKE FOR YOU TO BE ABLE TO 5?",
        ])
    ],

    "YOU": [
        ("(0 YOU ARE 0)", [
            "WHY DO YOU THINK I AM 5?",
            "DOES IT PLEASE YOU TO BELIEVE I AM 5?",
            "DO YOU SOMETIMES WISH I WERE 5?",
            "PERHAPS I AM 5 — WHAT DO YOU THINK?",
        ]),
        ("(0 YOU 0 ME 0)", [
            "WHY DO YOU THINK I 5 YOU?",
            "YOU THINK I 5 YOU — CAN YOU EXPLAIN?",
            "WHAT MAKES YOU THINK I 5 YOU?",
        ]),
        ("=I", [])
    ],

    "HELLO": [
        ("(0 HELLO 0)", [
            "HELLO. I AM GLAD YOU CAME.",
            "HI THERE. HOW ARE YOU FEELING TODAY?",
            "WELCOME. WHAT WOULD YOU LIKE TO DISCUSS?",
        ])
    ],

    "BYE": [
        ("(0 BYE 0)", [
            "GOODBYE. I HOPE TO TALK AGAIN SOON.",
            "FAREWELL. TAKE CARE OF YOURSELF.",
            "GOODBYE. REMEMBER, I'M ALWAYS HERE TO LISTEN.",
        ])
    ],

    "DEFAULT": [
        ("(0)", [
            "PLEASE TELL ME MORE.",
            "LET'S TALK MORE ABOUT THAT.",
            "CAN YOU EXPAND ON THAT?",
            "I SEE. AND WHAT DOES THAT MEAN TO YOU?",
            "IS THERE SOMETHING YOU'D LIKE TO DISCUSS FURTHER?",
        ])
    ]
}
