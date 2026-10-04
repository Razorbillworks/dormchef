import re
import streamlit as st
import ollama

MODEL = "gemma2:2b"
FRIEND = "Abhishek"

# Theme set from inside the file. Must run before any st.* call.
for _k, _v in {
    "theme.base": "light",
    "theme.primaryColor": "#1F5C57",
    "theme.backgroundColor": "#F6F1E3",
    "theme.secondaryBackgroundColor": "#FBF8EE",
    "theme.textColor": "#1B241F",
}.items():
    try:
        st._config.set_option(_k, _v)
    except Exception:
        pass

st.set_page_config(
    page_title=f"DormChef: recipes for {FRIEND}",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap');

:root {
  color-scheme: light;
  --ink: #1B241F;
  --muted: #62695F;
  --ivory: #F6F1E3;
  --field: #FBF8EE;
  --line: #D8CFB8;
  --slip: #FFFDF6;
  --turmeric: #F2B705;
  --turmeric-dark: #D9A300;
  --teal: #1F5C57;
}

.stApp, [data-testid="stAppViewContainer"] { background: var(--ivory) !important; color: var(--ink) !important; }

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; height: 0; }

html { font-size: 14px !important; }
.block-container {
  padding-top: 2.8rem !important; padding-bottom: 3rem !important;
  max-width: 1500px !important;
  padding-left: 3rem !important; padding-right: 3rem !important;
}
.stApp h1 { padding: 0 !important; }
[data-testid="stHeaderActionElements"] { display: none !important; }

.stApp, .stApp label, .stApp p, .stApp input, .stApp textarea, .stApp button, .stApp li {
  font-family: 'Bricolage Grotesque', system-ui, sans-serif;
}
.stApp label p, .stApp [data-testid="stWidgetLabel"] p { font-weight: 700; font-size: 0.98rem; color: var(--ink) !important; }

.wordmark {
  font-weight: 800; font-size: 2.6rem; line-height: 1.05; letter-spacing: -0.03em;
  color: var(--ink); margin: 0; overflow-wrap: break-word;
}
.subtitle { font-weight: 700; font-size: 1.5rem; letter-spacing: -0.01em; color: var(--teal); margin: 0.6rem 0 0.4rem 0; }
.tagline { color: var(--muted); font-size: 1.08rem; max-width: 46rem; margin: 0 0 1.6rem 0; }

.friend-note {
  background: #F0E8CF; border-left: 5px solid var(--turmeric);
  padding: 0.85rem 1.1rem; margin: 0 0 1.4rem 0; border-radius: 0 6px 6px 0;
  color: var(--ink); font-size: 1rem; line-height: 1.5;
}
.friend-note b { font-weight: 800; }

/* inputs */
.stApp textarea, .stApp input[type="text"] {
  background: var(--field) !important;
  border: 1.5px solid var(--line) !important;
  border-radius: 6px !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
}
.stApp textarea:focus, .stApp input[type="text"]:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 3px rgba(31, 92, 87, 0.18) !important;
}
.stApp [data-testid="stTextInput"] > div > div,
.stApp [data-testid="stTextArea"] > div > div { background: transparent !important; border: none !important; }
.stApp ::placeholder { color: #8C8F80 !important; -webkit-text-fill-color: #8C8F80 !important; }

.stApp [data-baseweb="select"] > div { background: var(--field) !important; border: 1.5px solid var(--line) !important; border-radius: 6px !important; }
.stApp [data-baseweb="tag"] { background: var(--teal) !important; color: #fff !important; }
.stApp [data-baseweb="tag"] span { color: #fff !important; }

/* the one action button */
div.stButton > button {
  background: var(--turmeric) !important;
  color: var(--ink) !important;
  border: 2px solid var(--ink) !important;
  border-radius: 6px !important;
  font-weight: 800 !important;
  font-size: 1.05rem !important;
  padding: 0.7rem 1.4rem !important;
  box-shadow: 3px 3px 0 var(--ink);
  transition: transform 0.08s ease, box-shadow 0.08s ease;
}
div.stButton > button p { color: var(--ink) !important; font-weight: 800 !important; }
div.stButton > button:hover {
  background: var(--turmeric-dark) !important;
  transform: translate(1px, 1px);
  box-shadow: 2px 2px 0 var(--ink);
}
div.stButton > button:active { transform: translate(3px, 3px); box-shadow: 0 0 0 var(--ink); }
div.stButton > button:focus-visible { outline: 3px solid var(--teal) !important; outline-offset: 3px; }

/* the recipe slip */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--slip);
  border: 2px dashed #A39B85 !important;
  border-radius: 4px !important;
  padding: 1.1rem 1.4rem 1.4rem 1.4rem;
  box-shadow: 0 2px 0 var(--line);
  min-height: 24rem;
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li {
  font-family: 'Newsreader', Georgia, serif;
  font-size: 1.12rem; line-height: 1.6; color: var(--ink);
}
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
  font-family: 'Bricolage Grotesque', system-ui, sans-serif;
  font-weight: 800; letter-spacing: -0.02em; color: var(--ink);
}
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2 { font-size: 1.8rem; margin-top: 0; }
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 { font-size: 1.1rem; }

.slip-empty { font-family: 'Newsreader', Georgia, serif; color: var(--muted); font-size: 1.15rem; line-height: 1.6; }
.slip-empty b { font-family: 'Bricolage Grotesque', system-ui, sans-serif; color: var(--ink); font-size: 1.35rem; display: block; margin-bottom: 0.4rem; }
.avoid-note { font-size: 0.92rem; color: var(--muted); margin: 0.6rem 0 0 0; }

/* bottom strip */
hr { border: none; border-top: 1.5px solid var(--line); margin: 3rem 0 2rem 0; }
.why-heading { font-weight: 800; font-size: 1.6rem; color: var(--ink); margin: 0 0 1.4rem 0; }
.why-item { border-left: 4px solid var(--turmeric); padding-left: 1.1rem; }
.why-item b { display: block; font-weight: 800; font-size: 1.15rem; color: var(--teal); margin-bottom: 0.35rem; }
.why-item span { color: var(--ink); font-size: 1.05rem; line-height: 1.55; }
.built-with { color: var(--muted); font-size: 0.98rem; margin: 2.5rem 0 0 0; padding-top: 1.2rem; border-top: 1.5px solid var(--line); }

/* phones and small tablets */
@media (max-width: 760px) {
  .block-container {
    padding-top: 1rem !important; padding-bottom: 2rem !important;
    padding-left: 1.1rem !important; padding-right: 1.1rem !important;
  }
  .wordmark { font-size: 2rem; }
  .subtitle { font-size: 1.15rem; }
  .tagline { font-size: 1rem; margin-bottom: 1.2rem; }
  .friend-note { font-size: 0.95rem; }
  .stApp textarea, .stApp input[type="text"] { font-size: 16px !important; }
  div.stButton > button { width: 100% !important; padding: 0.9rem 1rem !important; font-size: 1.1rem !important; }
  [data-testid="stVerticalBlockBorderWrapper"] { padding: 0.9rem 1rem 1.1rem 1rem; min-height: 14rem; }
  [data-testid="stVerticalBlockBorderWrapper"] h1,
  [data-testid="stVerticalBlockBorderWrapper"] h2 { font-size: 1.5rem; }
  [data-testid="stVerticalBlockBorderWrapper"] p,
  [data-testid="stVerticalBlockBorderWrapper"] li { font-size: 1.05rem; }
  hr { margin: 2rem 0 1.4rem 0; }
  .why-heading { font-size: 1.3rem; margin-bottom: 1rem; }
  .why-item { margin-bottom: 1.1rem; }
  .built-with { margin-top: 1.2rem; font-size: 0.92rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<h1 class="wordmark">DormChef: Midnight Pantry Rescue</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="subtitle">Recipes for {FRIEND}\'s hostel room, made from whatever is in it</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="tagline">Tell it what\'s in the room and what you can cook on. '
    "It writes a short recipe that actually works with a kettle or a sandwich toaster.</p>",
    unsafe_allow_html=True,
)

GEAR_OPTIONS = ["Electric kettle", "Sandwich toaster", "Induction plate", "No cooking"]
PRIORITIES = ["High protein", "Ready in 5 minutes", "Comfort food", "Cheap"]
SPICE_LEVELS = ["Mild", "Medium", "Hot"]

left, right = st.columns([1, 1.1], gap="large")

# ---------------------------------------------------------------------------
# Left: the form
# ---------------------------------------------------------------------------
with left:
    st.markdown(
        f'<div class="friend-note"><b>Built for {FRIEND}.</b> He\'s a hostel roommate who tracks his '
        "protein every day and only has an electric kettle and a sandwich toaster. "
        "Everything below starts with his setup.</div>",
        unsafe_allow_html=True,
    )

    items = st.text_area(
        "What's in the room?",
        value="3 eggs, 2 slices brown bread, butter, black pepper, chili flakes",
        height=100,
        help="Separate things with commas. Include small stuff like salt or ketchup.",
    )

    gear = st.multiselect(
        "What can you cook on?",
        GEAR_OPTIONS,
        default=["Electric kettle", "Sandwich toaster"],
    )

    c1, c2 = st.columns(2)
    with c1:
        priority = st.selectbox("What matters most?", PRIORITIES)
    with c2:
        spice = st.select_slider("How spicy?", options=SPICE_LEVELS, value="Hot")

    avoid = st.text_input(
        "Allergies or foods to avoid",
        placeholder="e.g. peanuts, mushrooms, dairy",
    )

    go = st.button("Find me a recipe")

# ---------------------------------------------------------------------------
# Recipe logic
# ---------------------------------------------------------------------------
SYSTEM = (
    "You are a practical cook helping a college student in a hostel room with very limited equipment. "
    "Rules you must follow: "
    "1) Use ONLY the ingredients listed, plus water and salt. Do not invent extra ingredients. "
    "2) Never put eggs or any food directly into an electric kettle or onto its heating element. "
    "If the kettle is the only heat source, boil eggs in a heatproof mug or bowl of boiling water instead. "
    "3) With a sandwich toaster, wrap or contain messy fillings so nothing leaks onto the plates. "
    "4) Keep quantities realistic for one person and keep the steps short. "
    "5) Never use any ingredient on the avoid list, not even in small amounts."
)

DAIRY = ["milk", "butter", "cheese", "paneer", "curd", "yogurt", "yoghurt", "ghee", "cream",
         "whey", "khoya", "lassi", "buttermilk"]
NUTS = ["peanut", "peanuts", "groundnut", "almond", "almonds", "cashew", "cashews", "walnut",
        "walnuts", "pistachio", "hazelnut", "nutella", "peanut butter"]
GLUTEN = ["bread", "wheat", "maida", "atta", "roti", "chapati", "pasta", "noodles", "maggi",
          "semolina", "suji", "rusk"]

ALLERGEN_GROUPS = {
    "dairy": DAIRY, "milk": DAIRY, "lactose": DAIRY,
    "egg": ["egg", "eggs", "mayonnaise", "mayo", "omelette", "omelet"],
    "peanut": ["peanut", "peanuts", "groundnut", "peanut butter"],
    "nut": NUTS,
    "gluten": GLUTEN, "wheat": GLUTEN,
    "soy": ["soy", "soya", "tofu"],
    "fish": ["fish", "tuna", "salmon"],
    "shellfish": ["prawn", "prawns", "shrimp", "crab"],
}


def get_blocked_terms(avoid_text):
    blocked = set()
    for part in re.split(r"[,\n;/]| and ", avoid_text.lower()):
        part = part.strip()
        if not part:
            continue
        blocked.add(part)
        for key, words in ALLERGEN_GROUPS.items():
            if key in part:
                blocked.update(words)
    return blocked


def mentions(text, term):
    return re.search(r"\b" + re.escape(term), text.lower()) is not None


def split_ingredients(items_text, blocked):
    kept, removed = [], []
    for raw in re.split(r"[,\n]", items_text):
        item = raw.strip()
        if not item:
            continue
        if any(mentions(item, t) for t in blocked):
            removed.append(item)
        else:
            kept.append(item)
    return kept, removed


def build_prompt(kept, blocked) -> str:
    gear_text = ", ".join(gear) if gear else "no cooking equipment"
    avoid_text = ", ".join(sorted(blocked)) if blocked else "nothing"
    return f"""Cook: {FRIEND}
Ingredients available: {", ".join(kept)}
Equipment: {gear_text}
Main goal: {priority}
Spice level: {spice}
Never use any of these: {avoid_text}

Write the recipe in exactly this format:

## (recipe name)
**Time:** (minutes)  
**Protein (rough):** (grams)

### You'll use
(short list of the ingredients from above)

### Steps
(numbered steps, each one short)

**Heads-up:** (one plain sentence about cleanup or safety, not a heading)
"""


def stream_recipe(kept, blocked):
    stream = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": build_prompt(kept, blocked)},
        ],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]


# ---------------------------------------------------------------------------
# Right: the recipe slip
# ---------------------------------------------------------------------------
with right:
    slip = st.container(border=True)
    with slip:
        if not go:
            st.markdown(
                '<div class="slip-empty"><b>Your recipe shows up here.</b>'
                "Fill in the room, then press the yellow button. "
                "It takes a few seconds because the model is running on the laptop, not in the cloud.</div>",
                unsafe_allow_html=True,
            )
        elif not items.strip():
            st.warning("Add at least one ingredient first.")
        elif not gear:
            st.warning('Pick at least one thing to cook on, or choose "No cooking".')
        else:
            blocked = get_blocked_terms(avoid)
            kept, removed = split_ingredients(items, blocked)
            if not kept:
                st.warning("Everything on your list contains something you asked to avoid. Add other ingredients.")
            else:
                if removed:
                    st.info("Left out because you asked to avoid it: " + ", ".join(removed))
                try:
                    recipe = st.write_stream(stream_recipe(kept, blocked))
                    found = sorted(t for t in blocked if mentions(recipe, t))
                    if found:
                        st.warning(
                            "This recipe mentions " + ", ".join(found) +
                            ", which you asked to avoid. Don't use it. Press the button again for a new one."
                        )
                    if avoid.strip():
                        st.markdown(
                            f'<p class="avoid-note">Asked to avoid: {avoid.strip()}. '
                            "Small AI models can miss things, so read the ingredient list before cooking.</p>",
                            unsafe_allow_html=True,
                        )
                except Exception:
                    st.error(
                        "Couldn't reach the model. Make sure the Ollama app is running, "
                        f"and that you've pulled it with: ollama pull {MODEL}"
                    )

# ---------------------------------------------------------------------------
# Bottom: why open source
# ---------------------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p class="why-heading">Why it runs on open-source AI</p>', unsafe_allow_html=True)

w1, w2, w3 = st.columns(3, gap="large")
with w1:
    st.markdown(
        '<div class="why-item"><b>Works offline</b><span>The model runs on the laptop through Ollama, '
        "so it still works when the hostel Wi-Fi drops.</span></div>",
        unsafe_allow_html=True,
    )
with w2:
    st.markdown(
        '<div class="why-item"><b>Costs nothing</b><span>No API key, no subscription and no '
        "per-request fees.</span></div>",
        unsafe_allow_html=True,
    )
with w3:
    st.markdown(
        f'<div class="why-item"><b>Stays private</b><span>What {FRIEND} eats and what he\'s allergic to '
        "never leaves the machine.</span></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    '<p class="built-with">Built with Gemma 2 (2B) running locally through Ollama and Streamlit. '
    "Code written with GitHub Copilot.</p>",
    unsafe_allow_html=True,
)