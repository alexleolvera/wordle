#!/usr/bin/env python3
import sys
import random
from datetime import date

WORDS = [
    "crane", "slate", "trace", "lemon", "tiger", "grape", "plant", "storm", "brush", "crisp",
    "flint", "gloom", "blaze", "frost", "grain", "pride", "scout", "shelf", "swift", "thump",
    "quirk", "plumb", "knack", "gusto", "fiend", "elder", "dwarf", "crest", "brawl", "anvil",
    "perch", "notch", "medal", "lusty", "kneel", "joust", "infer", "hutch", "groan", "found",
    "evoke", "drown", "champ", "bluff", "axiom", "wrath", "vouch", "trout", "snare", "rogue",
    "pixel", "oxide", "nymph", "mirth", "lunge", "knave", "joist", "inept", "haste", "graft",
    "flair", "exert", "debut", "crimp", "brunt", "atone", "zonal", "yield", "xenon", "waltz",
    "vapid", "untie", "tryst", "squat", "rivet", "quota", "pivot", "ovoid", "nudge", "myrrh",
    "lofty", "knelt", "joker", "inked", "havoc", "gauze", "froth", "envoy", "duchy", "cleft",
    "bleat", "askew", "zesty", "wordy", "visor", "upset", "trove", "swirl", "rumba", "query",
]

VALID_GUESSES = set(WORDS) | {
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
    "agent", "agree", "ahead", "aisle", "alarm", "album", "alert", "alike", "alive", "alley",
    "allow", "alone", "along", "altar", "angel", "anger", "angle", "angry", "anime", "ankle",
    "annex", "antic", "apart", "apple", "apply", "arena", "argue", "arise", "armor", "arrow",
    "aside", "asset", "atlas", "attic", "audio", "audit", "augur", "avail", "avert", "avoid",
    "awake", "award", "aware", "awful", "azure", "badge", "basic", "basis", "beach", "beard",
    "beast", "began", "begin", "being", "below", "bench", "berry", "birth", "black", "blade",
    "blank", "blast", "blaze", "bleed", "blend", "bless", "blind", "block", "blood", "bloom",
    "blown", "board", "bonus", "boost", "booth", "bound", "boxer", "brain", "brand", "brave",
    "bread", "break", "breed", "breve", "brick", "bride", "brief", "bring", "broad", "broke",
    "brook", "brown", "built", "bunch", "burst", "buyer", "cabin", "cache", "camel", "candy",
    "cargo", "carry", "catch", "cause", "cease", "chain", "chair", "chaos", "charm", "chart",
    "chase", "cheap", "check", "cheek", "chess", "chest", "chief", "child", "choir", "chuck",
    "civic", "civil", "claim", "clamp", "clash", "class", "clean", "clear", "clerk", "click",
    "cliff", "climb", "cling", "clock", "clone", "close", "cloud", "clown", "coach", "coast",
    "color", "comic", "comma", "court", "cover", "crack", "craft", "crash", "crawl", "crazy",
    "creek", "cross", "crowd", "crown", "crude", "cruel", "crush", "crust", "curve", "cycle",
    "daily", "dance", "dealt", "decay", "decoy", "defer", "delay", "dense", "depot", "depth",
    "derby", "devil", "digit", "dirty", "disco", "dizzy", "dodge", "doing", "donor", "doubt",
    "dough", "draft", "drain", "drama", "drape", "dread", "dream", "dress", "dried", "drift",
    "drill", "drink", "drive", "drone", "drove", "druid", "drunk", "dryer", "dunce", "dying",
    "eager", "eagle", "early", "earth", "ebony", "eight", "elite", "email", "emote", "empty",
    "enact", "enjoy", "enter", "entry", "equal", "error", "essay", "event", "every", "exact",
    "excel", "exist", "extra", "fable", "facet", "faith", "false", "fancy", "fatal", "fault",
    "feast", "fence", "fetch", "fever", "fewer", "fiber", "field", "fifth", "fifty", "fight",
    "final", "first", "fixed", "flame", "flash", "fleet", "flesh", "float", "flood", "floor",
    "flora", "flour", "flown", "fluid", "focus", "force", "forge", "forum", "frame", "frank",
    "fraud", "fresh", "front", "fugue", "fully", "funds", "funny", "genre", "ghost", "giant",
    "given", "gland", "glass", "gleam", "glide", "globe", "gloss", "glove", "going", "golem",
    "grace", "grand", "grant", "grasp", "grass", "grave", "great", "greed", "green", "greet",
    "grind", "gripe", "grips", "groan", "group", "grove", "grown", "guard", "guess", "guide",
    "guild", "guile", "guise", "gulch", "gummy", "guppy", "harsh", "haunt", "heads", "heart",
    "heavy", "hedge", "hence", "herbs", "hinge", "hippo", "holly", "honor", "horse", "hotel",
    "house", "human", "humor", "hundred", "hurry", "hyena", "hyper", "ideal", "image", "imply",
    "inbox", "index", "indie", "infer", "input", "inter", "intro", "ionic", "issue", "ivory",
    "japan", "jewel", "joint", "juice", "juicy", "jumbo", "jumpy", "knife", "knock", "known",
    "label", "lance", "large", "laser", "latch", "later", "laugh", "layer", "leafy", "learn",
    "lease", "least", "leave", "legal", "level", "light", "limit", "liner", "links", "lion",
    "liver", "local", "lodge", "logic", "loose", "lover", "lower", "lucky", "lunar", "lyric",
    "magic", "major", "maker", "manor", "maple", "march", "marsh", "match", "mayor", "media",
    "mercy", "merge", "merit", "metal", "might", "minor", "minus", "mixed", "model", "money",
    "month", "moral", "mossy", "motel", "motor", "mourn", "mouse", "mouth", "movie", "muddy",
    "mural", "music", "nasal", "never", "night", "ninja", "noise", "north", "novel", "nurse",
    "nymph", "oasis", "ocean", "offer", "often", "olive", "onset", "opera", "orbit", "order",
    "other", "ought", "outer", "outdo", "owned", "owner", "ozone", "paint", "panic", "paper",
    "party", "pasta", "patch", "pause", "peace", "peach", "pearl", "pedal", "penny", "phase",
    "phone", "photo", "piano", "piece", "pilot", "pinch", "pirate", "pitch", "pixel", "pizza",
    "place", "plain", "plane", "plank", "plate", "plaza", "plead", "pluck", "plume", "plush",
    "poach", "point", "polar", "polyp", "poppy", "porch", "posed", "power", "press", "price",
    "prime", "print", "prior", "prize", "probe", "prone", "proof", "prose", "proud", "prove",
    "prowl", "proxy", "psalm", "pulse", "punch", "pupil", "purge", "purse", "queen", "queue",
    "quick", "quiet", "quill", "quite", "quota", "quote", "racer", "radar", "radio", "raise",
    "rally", "ranch", "range", "rapid", "raven", "reach", "react", "realm", "rebel", "refer",
    "reign", "relax", "repay", "repel", "reset", "resin", "reuse", "ridge", "right", "risky",
    "rival", "river", "roast", "robin", "robot", "rocky", "roman", "rouge", "rough", "round",
    "route", "royal", "rugby", "ruler", "rural", "rusty", "safer", "saint", "salad", "sauce",
    "scale", "scene", "scone", "scope", "score", "sense", "serve", "seven", "shade", "shake",
    "shall", "shame", "shape", "share", "shark", "sharp", "shear", "shine", "shirt", "shook",
    "shoot", "shore", "short", "shout", "shove", "shown", "sight", "silly", "since", "sixth",
    "sixty", "skill", "skull", "skunk", "skype", "slash", "sleek", "sleep", "sleet", "slide",
    "sling", "slope", "sloth", "slump", "smile", "smite", "smock", "smoke", "snake", "solar",
    "solve", "sorry", "south", "space", "spare", "spark", "speak", "spear", "speed", "spend",
    "spice", "spine", "spoke", "spoon", "sport", "spray", "squad", "stack", "staff", "stage",
    "stake", "stale", "stall", "stand", "stark", "start", "state", "stays", "steal", "steel",
    "steer", "stern", "stick", "still", "sting", "stock", "stone", "stood", "store", "stomp",
    "story", "stout", "stove", "strap", "straw", "stray", "strip", "study", "style", "sugar",
    "suite", "sunny", "super", "surge", "swamp", "swear", "sweep", "sweet", "swept", "sword",
    "swore", "sworn", "syrup", "table", "taffy", "tango", "taste", "tawny", "teach", "teeth",
    "tempo", "tense", "tenth", "tepid", "terra", "terse", "their", "there", "these", "thing",
    "think", "third", "thorn", "those", "three", "threw", "throw", "thumb", "tidal", "tight",
    "timer", "tired", "title", "today", "token", "total", "touch", "tough", "toxic", "trace",
    "track", "trade", "trail", "train", "trait", "tramp", "trash", "treat", "trend", "trial",
    "trick", "tried", "troll", "troop", "truck", "truly", "trunk", "trust", "truth", "tulip",
    "tunic", "tuple", "tutor", "twice", "twist", "tying", "udder", "ultra", "uncle", "under",
    "unify", "union", "unity", "until", "upper", "usher", "usual", "utter", "valor", "value",
    "valve", "vault", "venom", "verse", "video", "vigil", "viral", "visit", "vista", "vital",
    "vivid", "vocal", "voice", "voter", "vow", "wager", "waist", "watch", "water", "weary",
    "weave", "weigh", "weird", "where", "which", "while", "white", "whole", "whose", "wield",
    "witch", "woman", "women", "world", "worry", "worst", "worth", "would", "wound", "wring",
    "wrote", "yacht", "yearn", "young", "yours", "youth", "zebra", "zonal",
}

GREEN  = "\033[42m\033[30m"
YELLOW = "\033[43m\033[30m"
GRAY   = "\033[100m\033[37m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

def pick_word():
    idx = date.today().toordinal() % len(WORDS)
    return WORDS[idx]

def score_guess(guess, answer):
    result = ["gray"] * 5
    answer_remaining = list(answer)
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "green"
            answer_remaining[i] = None
    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in answer_remaining:
            result[i] = "yellow"
            answer_remaining[answer_remaining.index(g)] = None
    return result

def render_tile(letter, color):
    bg = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}[color]
    return f"{bg} {letter.upper()} {RESET}"

def render_guess(guess, scores):
    return "  " + "".join(render_tile(g, s) for g, s in zip(guess, scores))

def render_board(guesses, scores_list):
    lines = []
    for i in range(6):
        if i < len(guesses):
            lines.append(render_guess(guesses[i], scores_list[i]))
        else:
            lines.append("  " + "".join(f"\033[90m[ ]\033[0m" for _ in range(5)))
    return "\n".join(lines)

def render_keyboard(used):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    out = []
    for row in rows:
        line = "  "
        for ch in row:
            state = used.get(ch, "unused")
            if state == "green":
                line += f"{GREEN} {ch.upper()} {RESET}"
            elif state == "yellow":
                line += f"{YELLOW} {ch.upper()} {RESET}"
            elif state == "gray":
                line += f"{GRAY} {ch.upper()} {RESET}"
            else:
                line += f" {ch.upper()} "
        out.append(line)
    return "\n".join(out)

def update_keyboard(used, guess, scores):
    priority = {"green": 3, "yellow": 2, "gray": 1, "unused": 0}
    for g, s in zip(guess, scores):
        if priority[s] > priority.get(g, 0):
            used[g] = s

def clear():
    print("\033[2J\033[H", end="")

def main():
    answer = pick_word()
    guesses = []
    scores_list = []
    used = {}
    message = ""

    while True:
        clear()
        print(f"\n{BOLD}  W O R D L E{RESET}  {DIM}(daily #{date.today().toordinal() % len(WORDS) + 1}){RESET}\n")
        print(render_board(guesses, scores_list))
        print()
        print(render_keyboard(used))
        print()

        if message:
            print(f"  {message}\n")
            message = ""

        if guesses and guesses[-1] == answer:
            attempts = len(guesses)
            print(f"  {BOLD}You got it in {attempts}!{RESET} The word was {GREEN} {answer.upper()} {RESET}\n")
            print(f"  Play again tomorrow, or run with --random for a fresh word.\n")
            break

        if len(guesses) == 6:
            print(f"  {BOLD}Out of guesses!{RESET} The word was {GREEN} {answer.upper()} {RESET}\n")
            break

        remaining = 6 - len(guesses)
        try:
            raw = input(f"  Guess ({remaining} left): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            sys.exit(0)

        if len(raw) != 5:
            message = "Please enter a 5-letter word."
            continue

        if not raw.isalpha():
            message = "Letters only, please."
            continue

        if raw not in VALID_GUESSES:
            message = f"'{raw}' is not in the word list."
            continue

        scores = score_guess(raw, answer)
        guesses.append(raw)
        scores_list.append(scores)
        update_keyboard(used, raw, scores)

if __name__ == "__main__":
    if "--random" in sys.argv:
        import random as _r
        # Override pick_word for random mode
        def pick_word(): return _r.choice(WORDS)  # noqa: F811
    main()
