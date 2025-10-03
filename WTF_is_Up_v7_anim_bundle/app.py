import streamlit as st
import json, os

st.set_page_config(page_title="WTF is Up?", page_icon=None, layout="centered")

DATA_DIR = os.path.dirname(__file__)
with open(os.path.join(DATA_DIR, "content.json"), "r", encoding="utf-8") as f:
    CONTENT = json.load(f)

def init_state():
    ss = st.session_state
    ss.setdefault("phase", "welcome")
    ss.setdefault("handle", "")
    ss.setdefault("age_bracket", "13-15")
    ss.setdefault("adjective", "")
    ss.setdefault("animal", "")
    ss.setdefault("selected_moods", set())
    ss.setdefault("selected_scenarios", set())
    ss.setdefault("technique", None)
    ss.setdefault("time_choice", None)
    ss.setdefault("theme_color", "#AAB7F8")
    ss.setdefault("bg_anim", "Off")  # Off, Airplane, Penguin

init_state()

PRIMARY = "#AAB7F8"
TEXT = "#1f2937"

TECH_COLORS = {
    "Breath Work": "#CFE8FF",
    "Mindfulness": "#FFFACD",
    "Thinking Techniques": "#F8CFE3",
    "Other": "#E6E6FA"
}

def apply_css(bg_color=None, radial=False):
    theme = st.session_state.get("theme_color", PRIMARY)
    accent = bg_color or theme
    gradient_css = ""
    if radial:
        gradient_css = (
            f"background: radial-gradient(circle at 50% 35%, #FFFFFF 0%, #FFFFFF 22%, {accent} 75%, {accent} 100%) !important;"
        )
    st.markdown(
        f"""
        <style>
          .stApp {{
            background: {accent};
            {gradient_css}
          }}
          h1,h2,h3,p, label, div, span {{ color: {TEXT}; }}
          .header-bar {{
            text-align:center;
            margin: 8px 0 12px 0;
          }}
          .header-title {{
            font-weight: 900; font-size: 22px;
            padding: 4px 10px;
            border-radius: 10px;
            background: rgba(255,255,255,0.65);
            border: 1px solid rgba(0,0,0,0.06);
            display:inline-block;
          }}
          .center-card {{
            background: white;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
            border: 1px solid rgba(0,0,0,0.05);
          }}
          .question-title {{
            text-align:center; font-weight: 900; font-size: 34px; margin: 8px 0 22px 0;
          }}
          .chip-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            max-width: 860px; margin: 0 auto;
          }}
          @media (max-width: 640px) {{
            .chip-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
          }}
          .stButton>button {{
            width: 100%;
            background: #FFF9EF;
            border: 2px solid rgba(0,0,0,0.06);
            border-radius: 14px;
            padding: 12px 14px;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(0,0,0,0.08);
            transition: background .12s ease, transform .08s ease;
          }}
          .stButton>button:hover {{
            background: #FFF3C4;
            transform: translateY(-1px);
          }}
          .pill {{
            display:inline-block; padding:8px 14px; border-radius:999px;
            background: rgba(255,255,255,0.9); border:1px solid rgba(0,0,0,0.06); margin:6px 6px 0 0; font-weight:700;
          }}
          .footer-note {{
            position:fixed; bottom:8px; left:50%; transform:translateX(-50%);
            background: rgba(255,255,255,0.85); padding:6px 12px; border-radius:999px;
            font-size:12px; border:1px solid rgba(0,0,0,0.06); z-index:1000;
          }}
          .bg-anim {{
            position: fixed; inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
          }}
          .bg-anim svg, .bg-anim .sprite {{ position: absolute; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_bg_animation():
    choice = st.session_state.get("bg_anim", "Off")
    if choice == "Off":
        return

    if choice == "Airplane":
        html = """
        <style>
          @keyframes fly {
            0%   { transform: translateX(-15vw) translateY(var(--y)) rotate(0deg); opacity:.0; }
            5%   { opacity:.9; }
            50%  { transform: translateX(50vw) translateY(calc(var(--y) + 8px)) rotate(2deg); }
            100% { transform: translateX(115vw) translateY(var(--y)) rotate(-1deg); opacity:.0; }
          }
          .plane {
            width: 64px; height: 64px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,.12));
            animation: fly var(--dur) linear infinite;
            animation-delay: var(--delay);
          }
          .trail {
            stroke: rgba(255,255,255,.55);
            stroke-width: 4; fill: none;
            filter: drop-shadow(0 2px 6px rgba(0,0,0,.08));
          }
        </style>
        <div class="bg-anim">
          <svg class="plane" style="--y: -60px; --dur: 20s; --delay: 0s; left:-10vw; top:12%;" viewBox="0 0 64 64">
            <path d="M2 36 L26 36 L40 20 L44 20 L38 36 L62 36 L62 40 L38 40 L44 56 L40 56 L26 40 L2 40 Z" fill="white"/>
          </svg>
          <svg width="320" height="80" style="left:-10vw; top:12%; animation: fly 20s linear infinite;">
            <path class="trail" d="M0,60 C40,50 80,55 120,45 S240,35 320,40"/>
          </svg>
          <svg class="plane" style="--y: 40px; --dur: 28s; --delay: 5s; left:-10vw; top:37%;" viewBox="0 0 64 64">
            <path d="M2 36 L26 36 L40 20 L44 20 L38 36 L62 36 L62 40 L38 40 L44 56 L40 56 L26 40 L2 40 Z" fill="white"/>
          </svg>
          <svg width="320" height="80" style="left:-10vw; top:37%; animation: fly 28s linear infinite 5s;">
            <path class="trail" d="M0,60 C60,52 120,58 180,46 S260,38 320,44"/>
          </svg>
          <svg class="plane" style="--y: -20px; --dur: 24s; --delay: 10s; left:-10vw; top:62%;" viewBox="0 0 64 64">
            <path d="M2 36 L26 36 L40 20 L44 20 L38 36 L62 36 L62 40 L38 40 L44 56 L40 56 L26 40 L2 40 Z" fill="white"/>
          </svg>
          <svg width="320" height="80" style="left:-10vw; top:62%; animation: fly 24s linear infinite 10s;">
            <path class="trail" d="M0,60 C50,55 100,53 150,48 S230,40 320,42"/>
          </svg>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    elif choice == "Penguin":
        html = """
        <style>
          @keyframes waddle {
            0%   { transform: translateX(-10vw); opacity: .0; }
            5%   { opacity: .95; }
            50%  { transform: translateX(50vw) translateY(-2px); }
            100% { transform: translateX(115vw); opacity: .0; }
          }
          @keyframes prints {
            0%   { opacity: 0; }
            10%  { opacity: .7; }
            80%  { opacity: .3; }
            100% { opacity: 0; }
          }
          .penguin {
            font-size: 42px; line-height: 1;
            position:absolute; bottom: 12%;
            animation: waddle var(--dur) linear infinite;
            animation-delay: var(--delay);
            filter: drop-shadow(0 6px 10px rgba(0,0,0,.12));
          }
          .track {
            position: absolute; bottom: calc(12% - 6px);
            width: 12px; height: 8px; border-radius: 50%;
            background: rgba(255,255,255,.8);
            box-shadow: 2px 1px 0 rgba(0,0,0,.06);
            animation: prints var(--dur) linear infinite;
            animation-delay: var(--delay);
          }
        </style>
        <div class="bg-anim">
          <div class="penguin" style="--dur: 26s; --delay: 0s; left:-10vw;">🐧</div>
          """ + "".join([f"<div class='track' style='--dur:26s; --delay:0s; left:{x}vw;'></div>" for x in range(-8,112,6)]) + """
          <div class="penguin" style="--dur: 32s; --delay: 6s; left:-10vw; bottom: 18%;">🐧</div>
          """ + "".join([f"<div class='track' style='--dur:32s; --delay:6s; left:{x}vw; bottom: 18%;'></div>" for x in range(-8,112,7)]) + """
          <div class="penguin" style="--dur: 28s; --delay: 12s; left:-10vw; bottom: 25%;">🐧</div>
          """ + "".join([f"<div class='track' style='--dur:28s; --delay:12s; left:{x}vw; bottom: 25%;'></div>" for x in range(-8,112,8)]) + """
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

def header():
    st.markdown("<div class='header-bar'><span class='header-title'>WTF is Up</span></div>", unsafe_allow_html=True)

def footer():
    st.markdown("<div class='footer-note'>Educational support only • Not a diagnosis or treatment • In the U.S., call or text <b>988</b></div>", unsafe_allow_html=True)

def recommend(tags, minutes, age_bracket, technique=None):
    items = CONTENT["items"]
    def ok_age(item_age):
        if age_bracket == "13-15" and item_age.startswith("16"):
            return False
        return True
    def score(it):
        if technique and it.get("technique") != technique: 
            return -1e9
        if not ok_age(it.get("age_range","13-18")): 
            return -1e9
        if minutes is not None and it.get("minutes", 10) > minutes: 
            return -1e9
        overlap = len(set(it.get("tags", [])) & set(tags))
        time_fit = 1.0 if it.get("minutes", 10) <= minutes else 0.0
        return overlap*2 + time_fit
    ranked = sorted(items, key=lambda x: score(x), reverse=True)
    out = [x for x in ranked if score(x) > -1e5]
    return out[:4] if out else ranked[:2]

def chip_page(question_text, options, state_set_name):
    apply_css(bg_color="#AAB7F8", radial=True)
    render_bg_animation()
    st.markdown(f"<div class='question-title'>{question_text}</div>", unsafe_allow_html=True)
    chosen = st.session_state.get(state_set_name, set())
    st.markdown("<div class='chip-grid'>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, opt in enumerate(options):
        with cols[idx % 3]:
            if st.button(opt, key=f"{state_set_name}_{idx}"):
                if opt in chosen: chosen.remove(opt)
                else: chosen.add(opt)
                st.session_state[state_set_name] = chosen
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if chosen:
        st.markdown("".join([f"<span class='pill'>{x}</span>" for x in chosen]), unsafe_allow_html=True)

# ---------- FLOW ----------
apply_css()
header()
with st.sidebar:
    st.selectbox("Background animation", ["Off", "Airplane", "Penguin"], key="bg_anim")
render_bg_animation()

if st.session_state.phase == "welcome":
    st.markdown(
        "<div class='center-card'><h2>Welcome</h2>"
        "<p>This app shares supportive, clinician-approved self-help resources for teens. "
        "It is educational and not a diagnosis or a substitute for professional care. "
        "If you are in crisis in the U.S., call or text <b>988</b>.</p></div>",
        unsafe_allow_html=True,
    )
    adjs = ["Ferocious","Curious","Gentle","Bold","Radiant","Calm","Brave","Witty","Kind","Steady","Swift","Bright"]
    animals = ["Penguin","Otter","Hawk","Dolphin","Panda","Tiger","Koala","Falcon","Fox","Seal","Heron","Lynx"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.adjective = st.selectbox("Pick an adjective", adjs, index=0)
    with c2:
        st.session_state.animal = st.selectbox("Pick an animal", animals, index=0)
    with c3:
        st.session_state.age_bracket = st.selectbox("Age range", ["13-15","16-18"], index=0)

    if st.button("Continue"):
        st.session_state.handle = f"{st.session_state.adjective} {st.session_state.animal}"
        st.session_state.phase = "feelings"
        st.rerun()

elif st.session_state.phase == "feelings":
    moods = ["Anxious","Sad","Angry","Stressed","Panic","Overwhelmed","Lonely","Sleep problems",
             "School pressure","Family conflict","Bullying","Sports pressure","Focus","Motivation",
             "Breakup","Friend drama","Body image","Social media","Rumination","Worry"]
    chip_page("How Do You Feel Today?", moods, "selected_moods")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅ Back"): st.session_state.phase = "welcome"; st.rerun()
    with c2:
        if st.button("Clear feelings"): st.session_state.selected_moods = set(); st.rerun()
    with c3:
        if st.button("Next ➜", disabled=not bool(st.session_state.selected_moods)): st.session_state.phase = "scenarios"; st.rerun()

elif st.session_state.phase == "scenarios":
    scenarios = ["Argument with a friend","Got a bad grade","Sports pressure","Family conflict","Online drama","Felt left out"]
    chip_page("Did Something Happen Today?", scenarios, "selected_scenarios")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅ Back"): st.session_state.phase = "feelings"; st.rerun()
    with c2:
        if st.button("Clear scenarios"): st.session_state.selected_scenarios = set(); st.rerun()
    with c3:
        if st.button("Next ➜"): st.session_state.phase = "techniques"; st.rerun()

elif st.session_state.phase == "techniques":
    apply_css(bg_color="#AAB7F8", radial=False)
    render_bg_animation()
    st.markdown("### How Should We Fix This?")
    opts = ["Breath Work","Mindfulness","Thinking Techniques","Other"]
    cols = st.columns(4)
    for i,opt in enumerate(opts):
        with cols[i]:
            if st.button(opt, key=f"tech_{i}", use_container_width=True):
                st.session_state.technique = opt
                st.session_state.theme_color = TECH_COLORS[opt]
                st.session_state.phase = "time"
                st.rerun()
    if st.button("⬅ Back"): st.session_state.phase = "scenarios"; st.rerun()

elif st.session_state.phase == "time":
    apply_css(bg_color=st.session_state.get("theme_color", PRIMARY), radial=False)
    render_bg_animation()
    st.markdown("### How much time do you have?")
    times = [2,5,10,15,20]
    cols = st.columns(5)
    for i,t in enumerate(times):
        with cols[i]:
            if st.button(f"{t} min", key=f"time_{t}", use_container_width=True):
                st.session_state.time_choice = t
                st.session_state.phase = "plan"; st.rerun()
    if st.button("⬅ Back"): st.session_state.phase = "techniques"; st.rerun()

elif st.session_state.phase == "plan":
    apply_css(bg_color=st.session_state.get("theme_color", PRIMARY), radial=False)
    render_bg_animation()
    st.markdown("### Your plan")
    tags = [m.lower() for m in st.session_state.selected_moods]
    recs = recommend(tags, st.session_state.time_choice or 10, st.session_state.age_bracket, st.session_state.technique)
    if not recs:
        st.info("Here are a few safe starters.")
        recs = [x for x in CONTENT["items"] if x.get("technique")==st.session_state.technique][:3]
        if not recs:
            recs = CONTENT["items"][:2]
    for it in recs:
        with st.container(border=True):
            st.markdown(f"**{it['title']}**")
            st.caption(it["summary"])
            st.write("Technique:", it.get("technique",""), " • Minutes:", it.get("minutes",5))
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Start over"):
            for k in ["phase","selected_moods","selected_scenarios","technique","time_choice"]:
                if k=="phase": st.session_state[k] = "welcome"
                elif isinstance(st.session_state.get(k), set): st.session_state[k] = set()
                else: st.session_state[k] = None
            st.session_state.theme_color = PRIMARY
            st.rerun()
    with c2:
        if st.button("Pick different moods"): st.session_state.phase = "feelings"; st.rerun()
    with c3:
        if st.button("Back to time"): st.session_state.phase = "time"; st.rerun()

footer()
