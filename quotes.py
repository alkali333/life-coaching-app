import random


def get_random_quote() -> str:
    quotes = [
        "Alexander Graham Bell: 'Concentrate all your thoughts upon the work at hand. The sun's rays do not burn until brought to a focus.'",
        "Aristotle: 'We are what we repeatedly do. Excellence, then, is not an act, but a habit.'",
        "Bruce Lee: 'The successful warrior is the ordinary person with laser-like focus.'",
        'Sir Isaac Newton was asked how he discovered the law of gravity. He replied, "By thinking about it all the time."',
        "Tony Robbins: 'Where focus goes, energy flows.'",
        "Confucius: 'The nature of man is always the same; it is their habits that separate them.'",
        "Winston Churchill: 'You will never reach your destination if you stop and throw stones at every dog that barks.'",
        "Roy T. Bennett: 'Focus on your strengths, not your weaknesses. Focus on your character, not your reputation. Focus on your blessings, not your misfortunes.'",
        "Lao Tzu: 'To the mind that is still, the whole universe surrenders.'",
        "Seneca: 'It's not that we have a short time to live, but that we waste much of it.'",
        "Marcus Aurelius: 'Concentrate every minute like a Roman— like a man— on doing what’s in front of you with precise and genuine seriousness, tenderly, willingly, with justice.'",
    ]

    random_quote = random.choice(quotes)
    return random_quote
