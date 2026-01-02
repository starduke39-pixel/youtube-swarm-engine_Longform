import os
import datetime
import config

# --- HARDCODED VIRAL SCRIPTS ---
# These are pre-written to guarantee the pipeline works without API errors.

SCRIPTS = {
    "Trivia_Core": """TITLE: 50 Question General Knowledge Marathon
Q: What is the capital city of Australia? | A: Canberra
Q: Which element has the chemical symbol 'O'? | A: Oxygen
Q: Who painted the Mona Lisa? | A: Leonardo da Vinci
Q: What is the largest planet in our solar system? | A: Jupiter
Q: In which year did the Titanic sink? | A: 1912
Q: What is the hardest natural substance on Earth? | A: Diamond
Q: Which country gifted the Statue of Liberty to the USA? | A: France
Q: How many hearts does an octopus have? | A: Three
Q: What is the main ingredient in guacamole? | A: Avocado
Q: Who wrote 'Romeo and Juliet'? | A: William Shakespeare
Q: What is the speed of light? | A: 299,792,458 meters per second
Q: Which planet is known as the Red Planet? | A: Mars
Q: What is the currency of Japan? | A: Yen
Q: How many bones are in the adult human body? | A: 206
Q: Which ocean is the largest? | A: Pacific Ocean
Q: Who was the first person to walk on the moon? | A: Neil Armstrong
Q: What is the chemical symbol for Gold? | A: Au
Q: Which animal is known as the King of the Jungle? | A: Lion
Q: What is the freezing point of water in Celsius? | A: 0 degrees
Q: How many continents are there? | A: Seven
Q: What is the tallest mountain in the world? | A: Mount Everest
Q: Who discovered penicillin? | A: Alexander Fleming
Q: What is the national bird of the United States? | A: Bald Eagle
Q: Which planet is closest to the sun? | A: Mercury
Q: What is the largest mammal in the world? | A: Blue Whale
Q: Who painted 'The Starry Night'? | A: Vincent van Gogh
Q: What is the square root of 64? | A: 8
Q: Which country has the most population? | A: India
Q: What is the capital of Italy? | A: Rome
Q: How many legs does a spider have? | A: Eight
""",

    "Ancient_Echoes": """TITLE: The Punishment of Prometheus
[Music: Sad, orchestral, slow building]
In the beginning, before men walked the earth, there were the Titans. And among them stood Prometheus, the one who thought before he acted. He looked upon the newly created humans, shivering in the cold, dark nights of the early world, and he felt something the other gods did not. He felt pity.

Zeus, the King of the Gods, sat high on Mount Olympus. He had forbidden the gift of fire to mankind. "Let them shiver," Zeus thundered. "If they have fire, they might think themselves equal to us." But Prometheus could not stand the suffering.

One dark night, while the Olympian gods slept, Prometheus climbed the sacred mountain. He took a hollow fennel stalk and touched it to the wheels of the Sun Chariot, stealing a single spark of divine fire. He carried it down to the mortal world.

For the first time, humans cooked their food. They warmed their caves. They forged tools. Civilization began, all because of that one spark.

But Zeus saw the smoke rising from the earth. His rage was absolute. He did not just want to kill Prometheus; he wanted him to suffer for eternity. He ordered Hephaestus, the smith god, to forge unbreakable chains. They dragged Prometheus to the highest peak of the Caucasus Mountains and bound him to the rock.

Every day, a giant eagle was sent by Zeus. It would tear open Prometheus's flesh and eat his liver. And because he was immortal, every night the flesh would heal, and the liver would grow back. Only for the eagle to return the next morning.

For thousands of years, Prometheus endured. He did not scream. He did not beg. He looked out over the world of men, seeing the fires burning in their cities, and he knew his sacrifice was worth it. This is the price of progress. This is the weight of defiance.
""",

    "Abyss_Archives": """TITLE: The Dyatlov Pass Incident
[Sound: Cold wind, static, eerie drone]
February 2nd, 1959. Nine experienced hikers pitch their tent on the slopes of Kholat Syakhl in the Ural Mountains. The local Mansi people call this place "The Dead Mountain." They would never be seen alive again.

When the rescue team found the campsite weeks later, they froze in horror. The tent had been cut open from the *inside*. Whatever happened that night, it made nine hardened survivalists panic so badly that they slashed their way out of their shelter and ran into the minus-30-degree blizzard without their boots.

Footprints showed them running down the slope, separating into groups. Two were found under a cedar tree, dressed only in underwear, next to the remains of a small fire. They had frozen to death. But it gets worse.

Further into the woods, three more bodies were found. They seemed to be trying to crawl back to the tent. But the final four hikers were found months later, buried under four meters of snow in a ravine. These bodies tell a darker story.

Dubinina and Zolotaryov had crushed chests, injuries that doctors compared to the force of a car crash. Yet, there were no external bruises. It was as if they had been crushed by high pressure. Dubinina was missing her tongue. Zolotaryov was missing his eyes.

And then, the radiation. Clothing found on the bodies tested positive for high levels of radioactive contamination.

What happened on the Dead Mountain? Was it an avalanche? But the tent was still standing. Was it a military test? Hikers miles away reported seeing strange orange orbs in the sky that night. Or was it something else? Something that the Soviet government kept classified for decades. To this day, the Dyatlov Pass incident remains the most disturbing unsolved mystery in exploration history.
""",

    "Apex_Lists": """TITLE: Top 5 Most Expensive Watches in the World
[Sound: Luxurious hip hop beat, cash register sounds]
Welcome to the upper echelon. Today we are counting down the Top 5 most expensive watches ever sold. These aren't just timepieces; they are history on a wrist.

Number 5: The Jacob & Co. Billionaire Watch. Price tag: 18 Million Dollars. Made famous by Floyd Mayweather, this watch is essentially a skeleton case completely invisible beneath 260 carats of emerald-cut diamonds.

Number 4: The Patek Philippe Henry Graves Supercomplication. Price tag: 24 Million Dollars. This is the most complicated watch ever made by human hands without computer assistance. It took 8 years to build and features a celestial chart based on the night sky above New York City.

Number 3: The Jaeger-LeCoultre Joaillerie 101 Manchette. Price tag: 26 Million Dollars. This looks more like a bracelet than a watch. It was gifted to Queen Elizabeth II for her Diamond Jubilee. It features 576 diamonds and a sapphire dial so small you need a magnifying glass to read it.

Number 2: The Graff Diamonds The Fascination. Price tag: 40 Million Dollars. This watch contains 152 carats of white diamonds. But the centerpiece is a 38-carat pear-shaped diamond that can actually be popped out and worn as a ring.

Number 1: The Graff Diamonds Hallucination. Price tag: 55 Million Dollars. This is it. The most expensive watch in the world. It is a kaleidoscope of 110 carats of extremely rare colored diamonds—pink, blue, green, and orange—set into a platinum bracelet. It is a masterpiece of gemology.
""",

    "Mind_Architect": """TITLE: The Dichotomy of Control
[Sound: Deep ambient drone, slow pacing]
There is only one way to happiness, and it is to cease worrying about things which are beyond the power of our will. This is the core teaching of Epictetus, the slave who became a philosopher.

It is called the Dichotomy of Control.

Imagine you are an archer. You have trained for years. You check your bow. You select the perfect arrow. You aim. You release. Up until the moment the arrow leaves your string, everything is in your control. Your preparation, your focus, your form.

But the moment that arrow is in the air, it is gone. A sudden gust of wind might blow it off course. The target might move. These things are *not* up to you.

Most people suffer because they attach their happiness to hitting the target. If they miss, they are crushed. They feel like failures.

The Stoic attaches their happiness to *shooting well*. If you aimed perfectly and released perfectly, you have succeeded. Whether the arrow hits or misses is irrelevant to your character.

Apply this to your life. You can control how hard you work, but you cannot control if you get the promotion. You can control how kind you are, but you cannot control if people like you.

When you focus only on your own actions, you become invincible. No one can stop you from doing your best. But if you focus on the outcome, you are a slave to fortune. Focus on the arrow, not the target.
"""
}

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    # We maintain the LongForm directory structure
    production_dir = os.path.join(config.BASE_DIR, f"Run_LongForm_{timestamp}")
    
    if not os.path.exists(production_dir):
        os.makedirs(production_dir)

    print(f"🚀 Starting Hardcoded Production Run: {timestamp}")

    for channel_name, script_content in SCRIPTS.items():
        print(f"\n📺 Processing Channel: {channel_name}...")
        
        channel_path = os.path.join(production_dir, channel_name)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)

        # We save it as '1_Hardcoded_Script.txt' so the other scripts pick it up
        filename = "1_Hardcoded_Script.txt"
        
        print(f"   ✍️ Writing Hardcoded Script...")
        with open(os.path.join(channel_path, filename), "w", encoding='utf-8') as f:
            f.write(script_content)

    print(f"\n✅ Scripts generated in '{production_dir}'")

if __name__ == "__main__":
    main()
