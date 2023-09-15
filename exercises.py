import random


def create_random_meditation(category) -> str:
    meditations = {
        "hopes_and_dreams": [
            "Using the client info, Ask the client to visualize a specific hope or dream listed in their 'hopes and dreams' section. Encourage them to imagine themselves successfully achieving it, and feeling a sense of accomplishment and joy.",
            "Using the client info, Guide the client to imagine themselves in the future, having successfully achieved all the hopes and dreams listed in their 'hopes and dreams' section. Encourage them to visualize the details of this success, how it feels, and what they are doing.",
            "Using the client info, Guide the client to visualize a ball of positive energy in their hands. Encourage them to imagine this energy ball filling with all the positive emotions, thoughts, and experiences they need to achieve the hopes and dreams listed in their 'hopes and dreams' section. Then guide them to imagine absorbing this energy into their body, filling them with positivity and strength.",
            "Using the client info, Ask the client to visualize a cord of energy extending from their root chakra (base of their spine) down into the earth. Guide them to imagine this cord grounding them and providing them with the stability and strength to achieve the hopes and dreams listed in their 'hopes and dreams' section.",
            "Using the client info, Guide the client to recall a time when they successfully achieved a similar hope or dream listed in their 'hopes and dreams' section. Encourage them to immerse themselves in that memory, and then visualize transferring that state to the current hopes and dreams they are working towards.",
            "Using the client info, Guide the client to focus on things that they are grateful for, despite the hopes and dreams that are yet to be achieved listed in their 'hopes and dreams' section. Encourage them to feel the gratitude deeply, and then visualize this positive energy helping them in achieving their hopes and dreams.",
            "Using the client info, Ask the client to visualize a healing light enveloping their body, healing any physical, emotional, or mental blocks related to the hopes and dreams listed in their 'hopes and dreams' section.",
            "Using the client info, Guide the client to visualize themselves working towards their hopes and dreams creatively and efficiently. Encourage them to imagine the process of achieving their hopes and dreams as a creative and enjoyable journey.",
            "Using the client info, Ask the client to recall a time when they felt extremely confident and successful in achieving a hope or dream, perhaps similar to those listed in their 'hopes and dreams' section. Guide them to anchor that feeling by touching their thumb and forefinger together. Then, whenever they work towards a hope or dream, remind them to touch their thumb and forefinger together to trigger that anchored feeling.",
            "Using the client info, Guide the client to imagine a golden bridge in front of them that represents their path to achieving the hopes and dreams listed in their 'hopes and dreams' section. Encourage them to visualize themselves walking across this bridge with confidence and ease, and achieving any hopes and dreams that arise along the way.",
        ],
        "skills_and_achievements": [
            "Using the client info, Ask the client to visualize a specific skill or achievement. Encourage them to imagine themselves using that skill or achievement in a positive way, and feeling a sense of pride and accomplishment.",
            "Using the client info, Guide the client to imagine themselves in the future, having further developed the skills and achievements. Encourage them to visualize the details of this future, how it feels, and what they are doing.",
            "Using the client info, Guide the client to visualize a trophy or award that represents the skills and achievements. Encourage them to imagine receiving this trophy or award, and feeling a sense of pride and recognition.",
            "Using the client info, Ask the client to visualize a tree with branches and leaves, each representing a skill or achievement. Guide them to imagine this tree growing strong and tall, symbolizing their growth and development.",
            "Using the client info, Guide the client to recall a time when they successfully used a skill or achieved something significant. Encourage them to immerse themselves in that memory, and then visualize themselves using that experience to achieve even greater success in the future.",
            "Using the client info, Guide the client to focus on the positive emotions associated with their skills and achievements. Encourage them to feel these emotions deeply, and then visualize these positive emotions empowering them to achieve even greater success.",
            "Using the client info, Ask the client to visualize a light inside them that represents the essence of their skills and achievements. Guide them to imagine this light expanding and filling their entire being with positive energy and self-confidence.",
            "Using the client info, Guide the client to visualize themselves sharing their skills and achievements with others, and making a positive impact on the world.",
            "Using the client info, Ask the client to recall a time when they felt extremely confident and successful, perhaps related to a moment. Guide them to anchor that feeling by touching their thumb and forefinger together. Then, whenever they need a boost of self-confidence, remind them to touch their thumb and forefinger together to trigger that anchored feeling.",
            "Using the client info, Guide the client to imagine a celebration in their honor, recognizing the skills and achievements. Encourage them to visualize the details of this celebration, the people there, the setting, the atmosphere, and the sense of pride and accomplishment they feel.",
        ],
        "gratitude": [
            "Using the client info, Guide the client to reflect on a skill they have developed, and then lead them to express gratitude for the opportunities and experiences that allowed them to develop that skill.",
            "Using the client info, Ask the client to reflect on an achievement they are proud of, and then guide them to express gratitude for the skills and abilities that enabled them to reach that achievement.",
            "Using the client info, Guide the client to visualize a situation where they successfully used a skill or achieved something significant. Then, encourage them to express gratitude for this success and for the abilities that enabled it.",
            "Using the client info, Ask the client to visualize a celebration in their honor, recognizing both their skills and achievements, and the things they are grateful for. Encourage them to feel a sense of pride and gratitude.",
            "Using the client info, Encourage the client to reflect on how their skills and achievements have contributed to their personal growth. Then guide them to express gratitude for this growth and for the abilities that enabled it.",
            "Using the client info, Guide the client to visualize themselves using their skills and achievements to overcome a challenge. Then, encourage them to express gratitude for their strength and resilience.",
            "Using the client info, Ask the client to list their skills and achievements, and then guide them to express gratitude for each one, while also acknowledging the self-confidence that comes from recognizing their own abilities.",
            "Using the client info, Guide the client to create positive affirmations that combine acknowledgment of their skills and achievements with expressions of gratitude. For example, 'I am grateful for my ability to [skill] which has led me to [achievement]'",
            "Using the client info, Ask the client to visualize the positive impact their skills and achievements have had on others, and then guide them to express gratitude for the opportunity to make a difference.",
            "Using the client info, Encourage the client to reflect on the opportunities they have had to use their skills and achieve their goals, and then guide them to express gratitude for these opportunities.",
        ],
        "empowerment": [
            "Using the client info,  Guide the client to visualize themselves successfully completing each task from their 'current tasks' list. Then, encourage them to imagine how completing each task brings them one step closer to their long-term hopes and dreams.",
            "Using the client info,  Ask the client to create positive affirmations that link their current tasks to their long-term hopes and dreams. For example, 'Completing [current task] is bringing me closer to [long-term dream]'.",
            "Using the client info,  Guide the client to visualize the sense of accomplishment they will feel upon completing all the tasks on their 'current tasks' list, and how this will contribute to achieving their long-term hopes and dreams.",
            "Using the client info,  Ask the client to reflect on how each task on their 'current tasks' list is connected to their long-term hopes and dreams. Encourage them to see the bigger picture and the purpose behind each task.",
            "Using the client info,  Guide the client to visualize themselves empowered and confident, successfully completing their 'current tasks' and moving towards their long-term hopes and dreams.",
            "Using the client info, Ask the client to reflect on their past achievements and the strengths they used to achieve them. Encourage them to see how these strengths can empower them to complete their 'current tasks' and achieve their hopes and dreams.",
            "Using the client info,  Ask the client to visualize any potential obstacles that may arise while completing their 'current tasks', and then guide them to visualize themselves overcoming these obstacles with confidence and determination.",
            "Using the client info,  Encourage the client to reflect on the reasons behind their long-term hopes and dreams, and how these reasons can motivate them to complete their 'current tasks'.",
            "Using the client info,  Guide the client to visualize their future, having completed all their 'current tasks' and achieved their long-term hopes and dreams. Encourage them to feel the sense of accomplishment and fulfillment.",
        ],
        "current_tasks": [
            "Using the client info,  Instruction: Guide the client to imagine themselves in the future, having already completed all their current tasks. For each one, encourage them to visualize the details of their success, how it feels, and what they are doing.",
            "Using the client info,  Instruction: Ask the client to visualize the obstacles and challenges they are currently facing in completing their current tasks. Encourage them to imagine themselves successfully overcoming each one, and feeling a sense of accomplishment and relief.",
            "Using the client info, Instruction: Guide the client to visualize a ball of positive energy in their hands. Encourage them to imagine this energy ball filling with all the positive emotions, thoughts, and experiences they need to complete their current tasks . Then guide them to imagine absorbing this energy into their body, filling them with positivity and strength.",
            "Using the client info,  Instruction: Ask the client to visualize a cord of energy extending from their root chakra (base of their spine) down into the earth. Guide them to imagine this cord grounding them and providing them with stability and strength to overcome their challenges and obstacles  in completing their current tasks.",
            "Using the client info, Instruction: Guide the client to recall a time when they felt really resourceful, confident, and successful. Encourage them to immerse themselves in that memory, and then visualize transferring that state to their current tasks .",
            "Using the client info, Instruction: Guide the client to focus on things that they are grateful for based on the provided user info. Encourage them to feel the gratitude deeply, and then visualize this positive energy helping them in manifesting their goals and overcoming challenges in completing their current tasks.",
            "Using the client info,  Instruction: Ask the client to visualize a healing light enveloping their body, healing any physical, emotional, or mental blocks that are preventing them from completing their current tasks .",
            "Using the client info,  Instruction: Guide the client to visualize themselves working on their current tasks  creatively and efficiently. Encourage them to imagine the process of completing their tasks as a creative and enjoyable journey.",
            "Using the client info, Instruction: Ask the client to recall a time when they felt extremely confident and successful – ask them to squeeze their thumb and forefinger together to anchor the feeling. Once in this state of mind, go through their current tasks as recorded in the user info. Explain how they can squeeze their thumb and forefinger together whenever they want to feel powerful and confident.",
            "Using the client info,  Instruction: Guide the client to imagine a golden bridge in front of them that represents their path to completing their current tasks . Encourage them to visualize themselves walking across this bridge with confidence and ease, overcoming any obstacles and challenges that arise along the way.",
        ],
        "misc": [
            "Using the client info, Guide the client to imagine themselves in the future, having already achieved all their hopes and dreams. For each one, encourage them to visualize the details of their success, how it feels, and what they are doing.",
            "Using the client info, Ask the client to visualize the obstacles and challenges they are currently facing. Encourage them to imagine themselves successfully overcoming each one, and feeling a sense of accomplishment and relief.",
            "Using the client info, Guide the client to visualize a ball of positive energy in their hands. Encourage them to imagine this energy ball filling with all the positive emotions, thoughts, and experiences they need to achieve their hopes and dreams . Then guide them to imagine absorbing this energy into their body, filling them with positivity and strength.",
            "Using the client info, Ask the client to visualize a cord of energy extending from their root chakra (base of their spine) down into the earth. Guide them to imagine this cord grounding them and providing them with stability and strength to overcome their challenges and obstacles .",
            "Using the client info, Guide the client to recall a time when they felt really resourceful, confident, and successful. Encourage them to immerse themselves in that memory, and then visualize transferring that state their current tasks (as recorded). Also mention their hopes and dreams as recorded.",
            "Using the client info, Guide the client to focus on things that they are grateful for based on the provided user info. Encourage them to feel the gratitude deeply, and then visualize this positive energy helping them in manifesting their goals and overcoming challenges.",
            "Using the client info, Ask the client to visualize a healing light enveloping their body, healing any physical, emotional, or mental blocks that are preventing them from achieving their hopes and dreams .",
            "Using the client info, Guide the client to visualize themselves working on their hopes and dreams  creatively and efficiently. Encourage them to imagine the process of achieving their goals as a creative and enjoyable journey.",
            "Using the client info, Ask the client to recall a time when they felt extremely confident and successful - ask them to squeeze their thumb and forefinger together to anchor the feeling. Once in this state of mind, go through their hopes and dreams as recorded in the client info. Explain how they can squeeze their thumb and forefinger together whenever they want to feel powerful and confident.",
            "Using the client info, Guide the client to imagine a golden bridge in front of them that represents their path to achieving their hopes and dreams . Encourage them to visualize themselves walking across this bridge with confidence and ease, overcoming any obstacles and challenges that arise along the way.",
            "Using the client info, Have the client breath in golden light representing each one of their hopes and dreams, and breathe out dark smoke representing each obstacle and challenge. Use the recorded client info.",
        ],
    }

    if category not in meditations:
        raise ValueError("Invalid category provided.")

    return random.choice(meditations[category])


print(create_random_meditation("hopes_and_dreams"))
