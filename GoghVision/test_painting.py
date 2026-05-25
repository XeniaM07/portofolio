from collections import defaultdict
import random

QUESTIONS = [
    {
        "question": "You wake up on a rainy day. What’s your first thought?",
        "answers": [
            "I’ll stay in and relax. Rain is calming.",
            "Let’s go somewhere cozy and get coffee.",
            "Rain matches my mood – I feel reflective.",
            "Rain or not, I’ll find a way to enjoy today."
        ]
    },
    {
        "question": "What kind of place makes you feel most at home?",
        "answers": [
            "A quiet, familiar room where I can recharge.",
            "Somewhere full of life, music, and movement.",
            "Anywhere close to nature or open skies.",
            "A place where I can express myself freely."
        ]
    },
    {
        "question": "When I'm overwhelmed, I usually...",
        "answers": [
            "Take a moment to reflect alone.",
            "Talk it out with someone I trust.",
            "Try to stay busy and keep moving.",
            "Distract myself with something beautiful."
        ]
    },
    {
        "question": "Which feeling do I relate to the most?",
        "answers": [
            "Soft sadness I can't explain.",
            "Gentle joy in everyday things.",
            "A desire to explore and connect.",
            "Deep, intense emotion I often hide."
        ]
    },
    {
        "question": "At a gathering, you’ll usually find me...",
        "answers": [
            "In a quiet corner observing.",
            "Chatting with people I know well.",
            "Roaming and meeting new faces.",
            "Thinking about when I’ll go home."
        ]
    },
    {
        "question": "What kind of beauty speaks to me most?",
        "answers": [
            "Night skies, stars, and silence.",
            "Sunlight, laughter, and movement.",
            "Delicate flowers and peaceful colors.",
            "Realness — even if it's raw or rough."
        ]
    },
    {
        "question": "Which statement feels closest to who I am?",
        "answers": [
            "I feel deeply and don't always show it.",
            "I’m passionate and full of energy.",
            "I seek safety and comfort in the familiar.",
            "I love new experiences and spaces."
        ]
    },
    {
        "question": "If I could live in a painting, it would be one with...",
        "answers": [
            "Blossoms, trees, and spring light.",
            "Warm colors and lively scenes.",
            "Fields, wind, and vast space.",
            "Deep blues, stars, and movement."
        ]
    },
    {
        "question": "People often say I...",
        "answers": [
            "Am thoughtful and quiet.",
            "Have a calm and steady energy.",
            "Am creative and full of ideas.",
            "Feel things more than I let on."
        ]
    },
    {
        "question": "Which day sounds most like you?",
        "answers": [
            "Reading indoors, curled in a blanket.",
            "Walking under open skies with wind in my face.",
            "People-watching from a busy café.",
            "Painting, journaling, or creating something new."
        ]
    },
    {
        "question": "When life gets hard, I...",
        "answers": [
            "Withdraw and think deeply.",
            "Push through and keep going.",
            "Focus on what still blooms.",
            "Let emotions flow until they ease."
        ]
    },
    {
        "question": "My ideal pace in life is...",
        "answers": [
            "Reflective and intentional.",
            "Slow and comforting.",
            "Fast and full of inspiration.",
            "Adaptable — I flow with what’s needed."
        ]
    },
    {
        "question": "How do I tend to express myself?",
        "answers": [
            "With poetry, music, or art.",
            "Through conversations and laughter.",
            "By caring for people around me.",
            "With honesty, even if it’s messy."
        ]
    },
    {
        "question": "What drives me more than anything?",
        "answers": [
            "A desire to understand myself.",
            "The need to feel safe and settled.",
            "Curiosity and connection.",
            "Hope, no matter how small."
        ]
    },
    {
        "question": "If someone truly knew me, they’d see that I...",
        "answers": [
            "Have strong emotions under the surface.",
            "Always try to bring light to others.",
            "See the world in soft, unique ways.",
            "Have grown a lot from pain and change."
        ]
    }
]

ANSWER_MAP = {
    1: {'a': ['wheat_field', 'irises'], 'b': ['cafe_terrace'], 'c': ['self_portrait', 'starry_night'], 'd': ['almond_blossom', 'sunflowers']},
    2: {'a': ['bedroom', 'self_portrait'], 'b': ['almond_blossom', 'irises'], 'c': ['wheat_field'], 'd': ['cafe_terrace']},
    3: {'a': ['starry_night'], 'b': ['sunflowers'], 'c': ['cafe_terrace'], 'd': ['bedroom']},
    4: {'a': ['irises', 'bedroom'], 'b': ['sunflowers', 'almond_blossom'], 'c': ['cafe_terrace'], 'd': ['starry_night', 'wheat_field']},
    5: {'a': ['bedroom'], 'b': ['wheat_field', 'starry_night'], 'c': ['cafe_terrace'], 'd': ['almond_blossom']},
    6: {'a': ['starry_night', 'self_portrait'], 'b': ['sunflowers'], 'c': ['almond_blossom', 'irises'], 'd': ['cafe_terrace']},
    7: {'a': ['self_portrait', 'irises'], 'b': ['wheat_field'], 'c': ['bedroom', 'sunflowers'], 'd': ['cafe_terrace']},
    8: {'a': ['almond_blossom', 'irises'], 'b': ['sunflowers', 'cafe_terrace'], 'c': ['wheat_field', 'bedroom'], 'd': ['starry_night', 'self_portrait']},
    9: {'a': ['irises', 'self_portrait'], 'b': ['bedroom', 'sunflowers'], 'c': ['cafe_terrace'], 'd': ['starry_night', 'wheat_field']},
    10: {'a': ['bedroom'], 'b': ['starry_night', 'wheat_field'], 'c': ['cafe_terrace'], 'd': ['sunflowers', 'almond_blossom']},
    11: {'a': ['starry_night', 'self_portrait'], 'b': ['sunflowers'], 'c': ['almond_blossom'], 'd': ['irises']},
    12: {'a': ['self_portrait', 'wheat_field'], 'b': ['bedroom'], 'c': ['sunflowers', 'cafe_terrace'], 'd': ['almond_blossom']},
    13: {'a': ['starry_night', 'irises'], 'b': ['sunflowers', 'cafe_terrace'], 'c': ['wheat_field', 'bedroom'], 'd': ['almond_blossom']},
    14: {'a': ['self_portrait', 'starry_night'], 'b': ['bedroom'], 'c': ['cafe_terrace'], 'd': ['irises', 'almond_blossom']},
    15: {'a': ['wheat_field', 'self_portrait'], 'b': ['sunflowers'], 'c': ['cafe_terrace', 'irises'], 'd': ['almond_blossom']}
}

DESCRIPTIONS = {
    "starry_night": "You are a dreamer with a vivid inner world, often caught between awe and anxiety. Your thoughts travel far — into stars, stories, and silent moments. Even when chaos swirls around you, you find meaning in the unseen and hope in the dark. There’s mystery in your calm and strength in your sensitivity.",
    "sunflowers": "You radiate warmth, positivity, and joy. Like sunflowers turning toward the light, you naturally seek out beauty and share it with others. Your energy is uplifting and your heart generous. People feel brighter around you — not because you try, but because you simply are.",
    "bedroom": "You value stability, comfort, and emotional safety. Quiet spaces recharge you, and you feel most alive when you're grounded and surrounded by the familiar. Simplicity isn’t boring to you — it’s beautiful. You're someone who creates peace for others just by being fully present.",
    "cafe_terrace": "You're curious, alive, and socially intuitive. You love to observe people, exchange ideas, and dive into meaningful conversations. Whether in a crowded café or a cozy corner, you feel most at home where minds meet. You're the kind of person who sparks energy wherever you go.",
    "irises": "You are gentle, introspective, and deeply connected to the emotional world. You notice the soft details, the quiet moments, and the unspoken feelings. Though you may move quietly through life, your presence is full of depth and empathy. There’s elegance in your emotions and beauty in your restraint.",
    "self_portrait": "You carry your story with honesty. Life hasn't always been kind, but you've turned pain into reflection and growth. You value authenticity and emotional truth. Though you may struggle to open up, your vulnerability is a quiet kind of courage. People trust you because you’ve walked through the dark and stayed kind.",
    "wheat_field": "You live with intensity. There's something raw, real, and beautifully unpredictable in you. You feel deeply and express freely — even if the world doesn’t always understand. Your passion often comes with storms, but within them lies clarity, strength, and a love for truth that cuts through the noise.",
    "almond_blossom": "You represent hope, healing, and quiet resilience. You’ve been through change, maybe loss, and still — you bloom. Your softness is your power, and your growth inspires others. Like a blossom in spring, your presence is gentle but full of life and light. You are a reminder that beauty begins again."
}

def calculate_result(answers):
    score = defaultdict(int)

    for i, ans in enumerate(answers, start=1):
        if ans.lower() in ANSWER_MAP.get(i, {}):
            for painting in ANSWER_MAP[i][ans.lower()]:
                score[painting] += 1

    max_score = max(score.values())
    top_paintings = [p for p, s in score.items() if s == max_score]

    result = random.choice(top_paintings)
    return {
        "painting": result,
        "description": DESCRIPTIONS[result],
        "score_table": dict(score)
    }
