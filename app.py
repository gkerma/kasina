import streamlit as st
import pandas as pd
import io
import datetime

st.set_page_config(page_title="Kasina KBS Generator", layout="wide")

st.title("🎧 Kasina KBS Session Generator")
st.caption("Génération automatique de fichiers .KBS conformes au format officiel MindPlace.")
st.markdown("Format basé sur : _Kasina Basic Session Format_ :contentReference[oaicite:1]{index=1}")

st.subheader("Paramètres globaux")

color_control_mode = st.selectbox(
    "Color Control Mode",
    [0, 1, 2, 3],
    index=3,
    help="""0: device ColorSet • 1: global ColorSet • 2: ColorSet par segment • 3: RGB personnalisé"""
)

global_colorset = st.number_input("Global ColorSet (si Mode = 1)", min_value=1, max_value=16, value=1)

st.markdown("---")
st.subheader("Segments de la session")

default_segment = {
    "Time": 60.0,
    "Beat": 8.0,
    "L_Pitch": 110.0,
    "R_Pitch": 118.0,
    "L_Phase": 50,
    "S_Phase": 50,
    "L_AMDepth": 80,
    "S_AMDepth": 20,
    "Bright": 60,
    "Vol": 50,
    "SndWF": "Sine",
    "SndModWF": "Sine",
    "LgtModWF": "Sine",
    "LgtModPW": 0,
    "SndPW": 0,
    "SndModPW": 0,
    "SegCS": 1,
    "Red": 50,
    "Green": 50,
    "Blue": 50
}

waveforms = ["Sine", "Square", "Triangle", "Saw_Up", "Saw_Down", "Pink_Noise"]

num_segments = st.number_input("Nombre de segments", 1, 50, 3)

segments = []

for i in range(num_segments):
    st.markdown(f"### Segment {i+1}")
    with st.expander(f"Configurer le Segment {i+1}", expanded=False):

        seg = {}
        for key in default_segment:
            if key in ["SndWF", "SndModWF", "LgtModWF"]:
                seg[key] = st.selectbox(f"{key}", waveforms, key=f"{key}_{i}")
            elif key == "SegCS":
                seg[key] = st.number_input(f"{key}", 1, 16, 1, key=f"{key}_{i}")
            elif key in ["Red", "Green", "Blue"]:
                seg[key] = st.slider(f"{key} (%)", 0, 100, 50, key=f"{key}_{i}")
            else:
                seg[key] = st.number_input(f"{key}", value=float(default_segment[key]), key=f"{key}_{i}")

        segments.append(seg)

st.markdown("---")
st.subheader("📦 Export du fichier .KBS")

if st.button("Générer le fichier KBS"):
    output = io.StringIO()

    output.write(f"# Generated with Streamlit | {datetime.datetime.now()}\n")
    output.write(f"ColorControlMode: {color_control_mode}\n")
    output.write(f"GlobalColorSet: {global_colorset}\n\n")

    for i, seg in enumerate(segments):
        output.write(f"# Segment {i+1}\n")
        for k, v in seg.items():
            output.write(f"{k}: {v}\n")
        output.write("\n")

    kbs_data = output.getvalue().encode("utf-8")
    st.download_button(
        label="💾 Télécharger le fichier KBS",
        data=kbs_data,
        file_name="session.kbs",
        mime="text/plain"
    )

    st.success("Fichier .kbs généré avec succès ! 🎉")
