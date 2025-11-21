import io
import re
import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="EthicsBot – Floridi", page_icon="🧠")

st.title(" EthicsBot — Floridi’s *The Ethics of Information*")
st.caption("Answers grounded ONLY in  indexed notes from the book (with page refs).")

# ----------------------------
# Data loading
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "floridi_dataset_final.csv",
        encoding="latin1",
        on_bad_lines="skip",
        engine="python"
    )

    # Clean invisible whitespace + fix bad cells
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Ensure required columns exist
    for col in ["chapter", "theme", "claim", "quote", "page_ref", "design_guideline"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")

    # Build retrieval text
    df["__text__"] = (df["theme"] + " " + df["claim"] + " " + df["quote"]).astype(str)
    df = df[df["__text__"].str.strip() != ""]

    #  Remove rows with empty text (prevents empty vocabulary)
    df = df[df["__text__"].str.len() > 3].reset_index(drop=True)

    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(df["__text__"])
    return df, vec, X


# ----------------------------
# PDF helpers
# ----------------------------
PDF_PATH = "INFORMATION ETHICS.pdf"  

def _extract_first_page_from_ref(page_ref: str):
    """Parse the first page number from strings like 'p.231–232' -> 231."""
    if not isinstance(page_ref, str):
        return None
    nums = re.findall(r"\d+", page_ref)
    if not nums:
        return None
    return int(nums[0])

@st.cache_data(show_spinner=False)
def render_pdf_page_image(page_num: int):
    """Return a PNG bytes snapshot of a PDF page (1-indexed)."""
    try:
        doc = fitz.open(PDF_PATH)
    except Exception as e:
        return None, f"Could not open PDF: {e}"
    idx = max(0, page_num - 1)  # PyMuPDF pages are 0-indexed
    if idx >= len(doc):
        return None, f"PDF has only {len(doc)} pages; requested p.{page_num}"
    page = doc.load_page(idx)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for readability
    img_bytes = pix.tobytes("png")
    return img_bytes, None

# ----------------------------
# Retrieval
# ----------------------------
def retrieve(query: str, k: int = 3):
    qv = vec.transform([query])
    sims = cosine_similarity(qv, X).ravel()
    order = sims.argsort()[::-1][:k]
    return df.iloc[order].assign(score=sims[order])

# Keep session history for download
if "answers" not in st.session_state:
    st.session_state.answers = []

# ----------------------------
# UI
# ----------------------------
q = st.text_input("Ask an ethical question about AI/data/systems:")

if q:
    if X.shape[0] == 0:
        st.error("Dataset contains no usable text. Please verify CSV formatting.")
        st.stop()
    results = retrieve(q, k=3)
    top = results.iloc[0]

    st.markdown(f"### Theme: **{top['theme']}**")
    st.caption(f"Chapter: {top['chapter']}")
    st.write(top["claim"])
    st.markdown(f"> “{top['quote']}” — *Floridi*, {top['page_ref']}")
    st.markdown(f"**Design Guideline:** {top['design_guideline']}")
    st.caption(f"Grounding: Floridi, *The Ethics of Information*, {top['page_ref']}")

    # PDF page preview (no weird indent here)
    with st.expander("🔎 Show page snapshot (from the book)"):
        page_num = _extract_first_page_from_ref(top["page_ref"])
        if page_num:
            img_bytes, err = render_pdf_page_image(page_num)
            if img_bytes:
                st.image(img_bytes, caption=f"Floridi, The Ethics of Information — page {page_num}")
            else:
                st.info(err or "Could not render the requested page.")
        else:
            st.info("No page number could be parsed from this reference.")

    # Other relevant angles
    with st.expander("See other relevant angles"):
        for i in range(1, len(results)):
            r = results.iloc[i]
            st.markdown(f"- **{r['theme']}** — {r['claim']} (see {r['page_ref']})")

    # Append to download history
    st.session_state.answers.append({
        "question": q,
        "theme": top["theme"],
        "claim": top["claim"],
        "quote": top["quote"],
        "page_ref": top["page_ref"],
        "design_guideline": top["design_guideline"]
    })

st.divider()
st.subheader("How this works")
st.write(
    "This chatbot does **retrieval** over a CSV built from Floridi's book. "
    "Each answer shows a short quote and **page reference** and can preview the book page. "
    
)

# Download CSV of Q&A for evidence
if st.session_state.answers:
    import csv
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["question", "theme", "claim", "quote", "page_ref", "design_guideline"])
    writer.writeheader()
    for row in st.session_state.answers:
        writer.writerow(row)
    st.download_button("Download today’s Q&A (CSV)", buf.getvalue(), file_name="ethicsbot_answers.csv", mime="text/csv")
