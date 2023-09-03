import random


def create_random_prompt() -> str:
    exercises = [
        "Guide the client to imagine themselves in the future, having already achieved all their goals and dreams (see client info). For each one, encourage them to visualize the details of their success, how it feels, and what they are doing.",
        "Ask the client to visualize the obstacles and challenges they are currently facing (as recorded in the client info). Encourage them to imagine themselves successfully overcoming each one, and feeling a sense of accomplishment and relief.",
        "Guide the client to visualize a ball of positive energy in their hands. Encourage them to imagine this energy ball filling with all the positive emotions, thoughts, and experiences they need to achieve their goals and dreams (the ones in the client info). Then guide them to imagine absorbing this energy into their body, filling them with positivity and strength.",
        "Ask the client to visualize a cord of energy extending from their root chakra (base of their spine) down into the earth. Guide them to imagine this cord grounding them and providing them with stability and strength to overcome their challenges and obstacles (as specified in the user info).",
        "Guide the client to recall a time when they felt really resourceful, confident, and successful. Encourage them to immerse themselves in that memory, and then visualize transferring that state their current tasks (as recorded). Also mention their hopes and dreams as recorded.",
        "Guide the client to focus on things that they are grateful for based on the provided user info. Encourage them to feel the gratitude deeply, and then visualize this positive energy helping them in manifesting their goals and overcoming challenges.",
        "Ask the client to visualize a healing light enveloping their body, healing any physical, emotional, or mental blocks that are preventing them from achieving their goals and dreams (the goals and dreams in the user info).",
        "Guide the client to visualize themselves working on their goals and dreams (as recorded in the client info) creatively and efficiently. Encourage them to imagine the process of achieving their goals as a creative and enjoyable journey.",
        "Ask the client to recall a time when they felt extremely confident and successful - ask them to squeeze their thumb and forefinger together to anchor the feeling. Once in this state of mind, go through their goals and dreams as recorded in the client info. Explain how they can squeeze their thumb and forefinger together whenever they want to feel powerful and confident.",
        "Guide the client to imagine a golden bridge in front of them that represents their path to achieving their goals and dreams (as recorded in the client info). Encourage them to visualize themselves walking across this bridge with confidence and ease, overcoming any obstacles and challenges that arise along the way.",
        "Have the client breath in golden light representing each one of their hopes and dreams, and breathe out dark smoke representing each obstacle and challenge. Use the recorded client info.",
    ]
    # elif type == "current_tasks":
    #     exercises = [
    #         "Future Self Visualization: Instruction: Guide the client to imagine themselves in the future, having already completed all their current tasks (as recorded in the user info). For each one, encourage them to visualize the details of their success, how it feels, and what they are doing.",
    #         "Obstacle Overcoming Visualization: Instruction: Ask the client to visualize the obstacles and challenges they are currently facing (as recorded in the user info) in completing their current tasks. Encourage them to imagine themselves successfully overcoming each one, and feeling a sense of accomplishment and relief.",
    #         "Positive Energy Ball Exercise: Instruction: Guide the client to visualize a ball of positive energy in their hands. Encourage them to imagine this energy ball filling with all the positive emotions, thoughts, and experiences they need to complete their current tasks (as recorded in the user info). Then guide them to imagine absorbing this energy into their body, filling them with positivity and strength.",
    #         "Root Chakra Grounding Exercise: Instruction: Ask the client to visualize a cord of energy extending from their root chakra (base of their spine) down into the earth. Guide them to imagine this cord grounding them and providing them with stability and strength to overcome their challenges and obstacles (as specified in the user info) in completing their current tasks.",
    #         "Resourceful State Visualization: Instruction: Guide the client to recall a time when they felt really resourceful, confident, and successful. Encourage them to immerse themselves in that memory, and then visualize transferring that state to their current tasks (as recorded in the user info).",
    #         "Gratitude Meditation: Instruction: Guide the client to focus on things that they are grateful for based on the provided user info. Encourage them to feel the gratitude deeply, and then visualize this positive energy helping them in manifesting their goals and overcoming challenges in completing their current tasks.",
    #         "Healing Light Visualization: Instruction: Ask the client to visualize a healing light enveloping their body, healing any physical, emotional, or mental blocks that are preventing them from completing their current tasks (as recorded in the user info).",
    #         "Creative Visualization: Instruction: Guide the client to visualize themselves working on their current tasks (as recorded in the user info) creatively and efficiently. Encourage them to imagine the process of completing their tasks as a creative and enjoyable journey.",
    #         "Anchor Visualization: Instruction: Ask the client to recall a time when they felt extremely confident and successful – ask them to squeeze their thumb and forefinger together to anchor the feeling. Once in this state of mind, go through their current tasks as recorded in the user info. Explain how they can squeeze their thumb and forefinger together whenever they want to feel powerful and confident.",
    #         "Golden Bridge Visualization: Instruction: Guide the client to imagine a golden bridge in front of them that represents their path to completing their current tasks (as recorded in the user info). Encourage them to visualize themselves walking across this bridge with confidence and ease, overcoming any obstacles and challenges that arise along the way.",
    #         "Breathing Meditation: Instruction: Have the client breath in golden light representing each one of their current tasks, and breathe out dark smoke representing each obstacle and challenge. Use the recorded client info.",
    #     ]

    # Pick a random exercise
    random_exercise = random.choice(exercises)
    return random_exercise
