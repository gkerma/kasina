# ============================================================
# CYBERM00D — Kasina Studio PRO (Cloud-compatible)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

st.set_page_config(page_title="CYBERM00D • Kasina Studio PRO", layout="wide")

# ============================================================
# HEADER / BRANDING
# ============================================================

st.markdown("""
# **CYBERM00D — Kasina Studio PRO**
### Générateur professionnel de sessions AVS (.KBS)
- Prévisualisation DreamMachine  
- Mode Haute Fidélité Kasina G/D  
- Timeline complète (Beat / RGB / Intensité)  
- IA avancée pour composer des sessions complètes  
- Générateur de Covers pro  
---
""")

# ============================================================
# HIGH-FIDELITY KASINA SIMULATION (G/D)
# ============================================================

def generate_hifi_frame(beat, rgb_left, rgb_right, frame_idx):
    img = Image.new("RGB", (800, 400), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    pulse = 0.5 + 0.5 * np.sin(frame_idx * beat * 0.18)

    # Left
    lx, ly = 200, 200
    pr = int(40 + pulse * 30)
    draw.ellipse((lx-pr, ly-pr, lx+pr, ly+pr), fill=rgb_left)

    # Right
    rx, ry = 600, 200
    draw.ellipse((rx-pr, ry-pr, rx+pr, ry+pr), fill=rgb_right)

    return img

# ============================================================
# DREAMMACHINE + KASINA STYLE PREVIEW
# ============================================================

def generate_visual_frame(beat, rgb, waveform, frame_idx):
    img = Image.new("RGB", (600, 600), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    r,g,b = rgb
    pulse = 0.5 + 0.5 * np.sin(frame_idx * beat * 0.2)

    cx, cy = 300, 300
    for radius in range(40, 300, 25):
        color = (int(r*(radius/300)), int(g*(radius/300)), int(b*(radius/300)))
        width = int(4 + pulse * 3)
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius),
                     outline=color, width=width)

    pr = int(30 + 20 * pulse)
    draw.ellipse((cx-pr, cy-pr, cx+pr, cy+pr), fill=(r, g, b))

    return img

# ============================================================
# COVER GENERATOR
# ============================================================

def generate_cover(title, duration, rgb):
    img = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    r,g,b = rgb

    cx, cy = 512, 512
    for radius in range(50, 500, 50):
        color = (
            int(r*(radius/500)),
            int(g*(radius/500)),
            int(b*(radius/500))
        )
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius),
                     outline=color, width=10)

    draw.text((60, 60), "CYBERM00D", fill=(r, g, b))
    draw.text((60, 200), title, fill=(255, 255, 255))
    draw.text((60, 300), f"Durée : {duration} min", fill=(200, 200, 200))

    return img

# ============================================================
# IA AVANCÉE — COMPOSITION AUTOMATIQUE
# ============================================================

def ai_generate_advanced(style, duration_min, intensity, chroma, progression):

    num_segments = max(4, int(duration_min / 6))
    segments = []

    profiles = {
        "energisant":  {"range": (10, 20), "pitch": (130, 220)},
        "psychedelique": {"range": (4, 10), "pitch": (110, 160)},
        "sommeil": {"range": (2, 7), "pitch": (80, 120)},
        "voyage": {"range": (3, 9), "pitch": (90, 150)}
    }

    chroma_profiles = {
        "cold":   (20, 60, 120),
        "warm":   (120, 60, 20),
        "neutral":(80, 80, 80),
        "rainbow":(np.random.randint(0,100),
                   np.random.randint(0,100),
                   np.random.randint(0,100)),
        "deep":   (50, 10, 80)
    }

    base_r, base_g, base_b = chroma_profiles[chroma]
    prof = profiles[style]

    for i in range(num_segments):
        p = i / (num_segments - 1)

        if progression == "rise":
            beat = np.interp(p, [0,1], prof["range"])
        elif progression == "fall":
            beat = np.interp(p, [0,1], prof["range"][::-1])
        elif progression == "wave":
            beat = np.interp(np.sin(p*np.pi*2)*0.5+0.5, [0,1], prof["range"])
        else:
            beat = sum(prof["range"])/2

        pitch_l = np.random.uniform(*prof["pitch"])
        pitch_r = pitch_l + beat

        if intensity == "soft":
            Ld, Sd = 40, 20
        elif intensity == "medium":
            Ld, Sd = 70, 40
        else:
            Ld, Sd = 100, 60

        r = min(100, base_r + p*40)
        g = min(100, base_g + p*40)
        b = min(100, base_b + p*40)

        segments.append({
            "Time": (duration_min*60)/num_segments,
            "Beat": round(beat,2),
            "L_Pitch": round(pitch_l,2),
            "R_Pitch": round(pitch_r,2),
            "L_AMDepth": Ld,
            "S_AMDepth": Sd,
            "Bright": int(np.interp(p,[0,1],[40,100])),
            "Vol": int(np.interp(p,[0,1],[30,80])),
            "Red": int(r),
            "Green": int(g),
            "Blue": int(b),
            "SndWF": np.random.choice(["Sine","Triangle","Saw_Up","Saw_Down"]),
            "SndModWF": np.random.choice(["Sine","Triangle","Square"]),
            "LgtModWF": np.random.choice(["Sine","Triangle","Saw_Up","Saw_Down"])
        })

    return segments

# ============================================================
# KBS FILE EXPORT
# ============================================================

def generate_kbs_file(global_cfg, segments):
    buf = io.StringIO()
    buf.write(f"# CYBERM00D Kasina Studio PRO — {datetime.datetime.now()}\n")
    buf.write(f"ColorControlMode: {global_cfg['color_control_mode']}\n")
    buf.write(f"GlobalColorSet: {global_cfg['global_colorset']}\n\n")

    for i, seg in enumerate(segments):
        buf.write(f"# Segment {i+1}\n")
        for k, v in seg.items():
            buf.write(f"{k}: {v}\n")
        buf.write("\n")

    return buf.getvalue().encode("utf-8")

# ============================================================
# SIDEBAR — GLOBAL SETTINGS
# ============================================================

st.sidebar.title("⚙️ Paramètres")

color_control_mode = st.sidebar.selectbox("Color Control Mode", [0,1,2,3], index=3)
global_colorset = st.sidebar.number_input("Global ColorSet", 1, 16, 1)

# ============================================================
# IA AVANCÉE — SIDEBAR
# ============================================================

st.sidebar.markdown("### 🤖 IA Avancée")

ai_enabled = st.sidebar.checkbox("Activer IA avancée", value=False)

if ai_enabled:
    style = st.sidebar.selectbox("Style",["energisant","psychedelique","sommeil","voyage"])
    duration = st.sidebar.select_slider("Durée (min)", [10,20,30,45,60,90,120])
    intensity = st.sidebar.selectbox("Intensité",["soft","medium","intense"])
    chroma = st.sidebar.selectbox("Palette chromatique",["cold","warm","neutral","rainbow","deep"])
    progression = st.sidebar.selectbox("Progression",["rise","plateau","fall","wave"])

    if st.sidebar.button("🎼 Composer session IA"):
        st.session_state.segments = ai_generate_advanced(style,duration,intensity,chroma,progression)
        st.success("Session IA générée !")

# ============================================================
# SEGMENTS MANUELS
# ============================================================

st.subheader("🧩 Segments")

if "segments" not in st.session_state:
    st.session_state.segments = []

if st.button("Ajouter un segment"):
    st.session_state.segments.append({
        "Time": 60, "Beat": 8,
        "L_Pitch": 110, "R_Pitch": 118,
        "L_AMDepth": 80, "S_AMDepth": 20,
        "Bright": 60, "Vol": 50,
        "Red": 50, "Green": 50, "Blue": 50,
        "SndWF": "Sine", "SndModWF": "Sine","LgtModWF": "Sine"
    })

df = pd.DataFrame(st.session_state.segments)
edited_df = st.data_editor(df)
segments = edited_df.to_dict("records")
st.session_state.segments = segments

# ============================================================
# HIGH-FIDELITY PREVIEW
# ============================================================

st.subheader("👁️ Haute Fidélité (G/D)")

if segments:
    seg = segments[0]
    rgb_left = (seg["Red"], 0, seg["Blue"])
    rgb_right = (0, seg["Green"], seg["Blue"])
    frame = generate_hifi_frame(seg["Beat"],rgb_left,rgb_right,1)
    st.image(frame)

# ============================================================
# DREAMMACHINE PREVIEW
# ============================================================

st.subheader("🌈 DreamMachine Mix")

if segments:
    seg = segments[0]
    f = generate_visual_frame(seg["Beat"],(seg["Red"],seg["Green"],seg["Blue"]),
                              seg["LgtModWF"],2)
    st.image(f)

# ============================================================
# TIMELINE
# ============================================================

st.subheader("📈 Timeline")

def plot_timeline(segments):
    times=[]
    beat=[]; bright=[]
    red=[]; green=[]; blue=[]
    t=0

    for seg in segments:
        duration = seg["Time"]
        for i in np.linspace(0,1,20):
            times.append(t + i*duration)
            beat.append(seg["Beat"])
            bright.append(seg["Bright"])
            red.append(seg["Red"])
            green.append(seg["Green"])
            blue.append(seg["Blue"])
        t+=duration

    fig,ax=plt.subplots(4,1,figsize=(10,12),sharex=True)
    ax[0].plot(times,beat,color="white"); ax[0].set_ylabel("Beat")
    ax[1].plot(times,bright,color="yellow"); ax[1].set_ylabel("Bright")
    ax[2].plot(times,red,color="red"); ax[2].plot(times,green,color="green")
    ax[2].plot(times,blue,color="blue"); ax[2].set_ylabel("RGB")
    ax[3].set_xlabel("Temps (s)")

    fig.patch.set_facecolor("#000")
    for a in ax:
        a.set_facecolor("#101010")
        a.grid(color="gray",linestyle="--",alpha=0.3)

    return fig

if st.button("Générer timeline"):
    fig = plot_timeline(segments)
    st.pyplot(fig)

# ============================================================
# COVER GENERATOR
# ============================================================

st.subheader("🎨 Cover CYBERM00D")

title = st.text_input("Titre de la session","Session personnalisée")
duration_input = st.number_input("Durée (min)",1,300,20)

if st.button("Générer Cover"):
    rgb = (segments[0]["Red"],segments[0]["Green"],segments[0]["Blue"]) if segments else (80,40,120)
    cover = generate_cover(title,duration_input,rgb)

    buf = io.BytesIO()
    cover.save(buf,format="PNG")
    buf.seek(0)

    st.image(buf,caption="Cover générée")

    st.download_button("Télécharger la Cover",data=buf,file_name="cover.png",
                       mime="image/png")

# ============================================================
# EXPORT KBS
# ============================================================

st.subheader("📦 Export KBS")

if st.button("Exporter KBS"):
    global_cfg = {
        "color_control_mode": color_control_mode,
        "global_colorset": global_colorset
    }

    kbs_data = generate_kbs_file(global_cfg,segments)

    st.download_button(
        "💾 Télécharger session.kbs",
        data=kbs_data,
        file_name="session.kbs"
    )

    st.success("Fichier KBS généré avec succès !")
