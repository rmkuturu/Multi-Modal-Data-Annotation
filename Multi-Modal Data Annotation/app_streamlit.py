import csv
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
TEXT_CSV = DATA_DIR / "text" / "texts.csv"
IM_DIR = DATA_DIR / "images"
AU_DIR = DATA_DIR / "audio"
ANN_DIR = BASE / "annotations"
ANN_DIR.mkdir(exist_ok=True)

TEXT_LABELS = [
    "sample_id",
    "sentence",
    "sentiment_label",
    "prompt_adherence",
    "confidence",
    "needs_review",
    "notes",
    "annotator",
    "project_tag",
    "timestamp_utc",
]
IMAGE_LABELS = [
    "sample_id",
    "filename",
    "label",
    "xmin",
    "ymin",
    "xmax",
    "ymax",
    "confidence",
    "needs_review",
    "notes",
    "annotator",
    "project_tag",
    "timestamp_utc",
]
AUDIO_LABELS = [
    "sample_id",
    "filename",
    "label",
    "confidence",
    "needs_review",
    "notes",
    "annotator",
    "project_tag",
    "timestamp_utc",
]

st.set_page_config(page_title="Hedgehog Multi-Modal Evaluation Toolkit", layout="wide")
st.title("Hedgehog Multi-Modal Evaluation Toolkit")
st.caption("Independent derivative project built from the original work by armaanshk.")

menu = st.sidebar.selectbox(
    "Select mode",
    ["Text Review", "Image Review", "Audio Review", "Quality Dashboard", "Guidelines"],
)
st.sidebar.markdown("---")
annotator = st.sidebar.text_input("Annotator name", value="annotator_1")
project_tag = st.sidebar.text_input("Project tag", value="hedgehog_eval")


def append_csv_row(path: Path, columns: list[str], row: list):
    file_exists = path.exists()
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if not file_exists:
            writer.writerow(columns)
        writer.writerow(row)


def load_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)


def save_text_annotation(sample_id: str, sentence: str, sentiment: str, adherence: str, confidence: int, needs_review: bool, notes: str):
    append_csv_row(
        ANN_DIR / "text_labels.csv",
        TEXT_LABELS,
        [sample_id, sentence, sentiment, adherence, confidence, needs_review, notes, annotator, project_tag, datetime.utcnow().isoformat()],
    )


def save_image_annotation(sample_id: str, filename: str, label: str, xmin: int, ymin: int, xmax: int, ymax: int, confidence: int, needs_review: bool, notes: str):
    append_csv_row(
        ANN_DIR / "image_labels.csv",
        IMAGE_LABELS,
        [sample_id, filename, label, xmin, ymin, xmax, ymax, confidence, needs_review, notes, annotator, project_tag, datetime.utcnow().isoformat()],
    )


def save_audio_annotation(sample_id: str, filename: str, label: str, confidence: int, needs_review: bool, notes: str):
    append_csv_row(
        ANN_DIR / "audio_labels.csv",
        AUDIO_LABELS,
        [sample_id, filename, label, confidence, needs_review, notes, annotator, project_tag, datetime.utcnow().isoformat()],
    )


if menu == "Guidelines":
    st.header("Evaluation Guidelines")
    st.markdown(
        """
        Use this tool as a lightweight evaluator workflow, not just a simple labeler.

        ### Text Review
        - Assign a sentiment label.
        - Check whether the content is clear and consistent.
        - Use prompt adherence to note whether the item fits its intended task.

        ### Image Review
        - Label the dominant category.
        - Add bounding box coordinates when useful.
        - Flag unclear or low-confidence samples for second-pass review.

        ### Audio Review
        - Categorize the clip as Speech, Music, Noise, or Other.
        - Use notes for ambiguity, clipping, overlap, or quality concerns.

        ### Review Quality
        - Use confidence scores consistently.
        - Mark uncertain items with needs_review.
        - Add short notes when a future reviewer would benefit from context.
        """
    )
    st.info("This fork is tuned toward Project Hedgehog-style review workflows with confidence, notes, and follow-up flags.")

elif menu == "Text Review":
    st.header("Text Review")
    if not TEXT_CSV.exists():
        st.warning("Text dataset not found.")
    else:
        df = pd.read_csv(TEXT_CSV)
        if df.empty:
            st.warning("No text samples available.")
        else:
            idx = st.number_input("Text index", min_value=0, max_value=len(df) - 1, value=0)
            row = df.iloc[int(idx)]
            st.subheader("Sentence")
            st.write(row["sentence"])
            sentiment = st.radio("Sentiment label", ["Positive", "Negative", "Neutral"], horizontal=True)
            adherence = st.selectbox("Prompt adherence", ["Strong", "Partial", "Weak", "Unclear"])
            confidence = st.slider("Confidence", min_value=1, max_value=5, value=4)
            needs_review = st.checkbox("Flag for second-pass review")
            notes = st.text_area("Reviewer notes", placeholder="Add ambiguity notes, failure reasons, or edge cases.")
            if st.button("Save Text Review"):
                save_text_annotation(str(row["id"]), row["sentence"], sentiment, adherence, confidence, needs_review, notes)
                st.success("Text review saved.")

elif menu == "Image Review":
    st.header("Image Review")
    images = sorted(p.name for p in IM_DIR.glob("*.jpg"))
    if not images:
        st.warning("No image files found.")
    else:
        selected = st.selectbox("Select image", images)
        st.image(str(IM_DIR / selected), use_container_width=True)
        label = st.selectbox("Image label", ["Dog", "Cat", "Car", "Person", "Other"])
        st.caption("Optional: add bounding box coordinates in pixels.")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            xmin = st.number_input("xmin", min_value=0, value=0)
        with col2:
            ymin = st.number_input("ymin", min_value=0, value=0)
        with col3:
            xmax = st.number_input("xmax", min_value=0, value=0)
        with col4:
            ymax = st.number_input("ymax", min_value=0, value=0)
        confidence = st.slider("Confidence", min_value=1, max_value=5, value=4, key="image_confidence")
        needs_review = st.checkbox("Flag image for review")
        notes = st.text_area("Image review notes", placeholder="Missing object, weak composition, unclear sample, etc.")
        if st.button("Save Image Review"):
            save_image_annotation(Path(selected).stem, selected, label, xmin, ymin, xmax, ymax, confidence, needs_review, notes)
            st.success("Image review saved.")

elif menu == "Audio Review":
    st.header("Audio Review")
    audios = sorted(p.name for p in AU_DIR.glob("*.wav"))
    if not audios:
        st.warning("No audio files found.")
    else:
        selected = st.selectbox("Select audio", audios)
        st.audio(str(AU_DIR / selected))
        label = st.selectbox("Audio label", ["Speech", "Music", "Noise", "Other"])
        confidence = st.slider("Confidence", min_value=1, max_value=5, value=4, key="audio_confidence")
        needs_review = st.checkbox("Flag audio for review")
        notes = st.text_area("Audio review notes", placeholder="Overlapping speech, clipping, low quality, uncertain label, etc.")
        if st.button("Save Audio Review"):
            save_audio_annotation(Path(selected).stem, selected, label, confidence, needs_review, notes)
            st.success("Audio review saved.")

elif menu == "Quality Dashboard":
    st.header("Quality Dashboard")
    text_df = load_csv_or_empty(ANN_DIR / "text_labels.csv", TEXT_LABELS)
    image_df = load_csv_or_empty(ANN_DIR / "image_labels.csv", IMAGE_LABELS)
    audio_df = load_csv_or_empty(ANN_DIR / "audio_labels.csv", AUDIO_LABELS)

    total_reviews = len(text_df) + len(image_df) + len(audio_df)
    flagged_reviews = sum(df["needs_review"].fillna(False).astype(str).str.lower().eq("true").sum() for df in [text_df, image_df, audio_df] if not df.empty and "needs_review" in df.columns)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total reviews", total_reviews)
    c2.metric("Text reviews", len(text_df))
    c3.metric("Image reviews", len(image_df))
    c4.metric("Audio reviews", len(audio_df))
    st.metric("Flagged for follow-up", int(flagged_reviews))

    if not text_df.empty:
        st.subheader("Text Review Summary")
        if "sentiment_label" in text_df.columns:
            st.write(text_df["sentiment_label"].value_counts())
        st.dataframe(text_df, use_container_width=True)

    if not image_df.empty:
        st.subheader("Image Review Summary")
        if "label" in image_df.columns:
            st.write(image_df["label"].value_counts())
        st.dataframe(image_df, use_container_width=True)

    if not audio_df.empty:
        st.subheader("Audio Review Summary")
        if "label" in audio_df.columns:
            st.write(audio_df["label"].value_counts())
        st.dataframe(audio_df, use_container_width=True)

    if text_df.empty and image_df.empty and audio_df.empty:
        st.info("No saved reviews yet. Start by reviewing text, image, or audio samples.")
