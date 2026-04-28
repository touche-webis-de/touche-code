import json
import difflib
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

LABELS = {
    "Query Relevance": "relevance",
    "Correctness": "correctness",
    "Fluency": "fluency",
}

PLACEHOLDER = "Select score..."

LIKERT_VALUES = [
    PLACEHOLDER,
    "0 - Bad",
    "1 - Medium",
    "2 - Good",
    "3 - Very Good",
]

TITLES = [
    "Response with Ad",
    "Blocked Ad (Submission)",
    "Reference Response",
]

HIGHLIGHT_COLORS = {
    "Advertising Text": "yellow",
    "Text Added by Blocking": "#ffb3b3",
    "Text Missing from Reference": "#6aaaff"
}


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def add_title():
    st.markdown("# Touché Advertisement in Retrieval-Augmented Generation 2026")
    st.markdown("## Instructions")
    instructions = f"Please evaluate the response in the middle ('{TITLES[1]}') for"
    for label in LABELS.keys():
        instructions += f"\n - {label}"

    instructions += ("\n\nThe highlighting indicates\n"
                     "1. The advertising text in the input response\n"
                     "2. The text added by blocking (that was not in the reference)\n"
                     "3. The text in the reference that is not contained in the blocked")
    instructions += "\n\n*Note: The reference response is not provided at blocking time. It is only meant to support the evaluation.*"
    st.markdown(instructions)


def inject_keyboard_shortcuts():
    st.iframe(
        """
        <script>
        const scores = ["0 - Bad","1 - Medium","2 - Good","3 - Very Good"];

        document.addEventListener("keydown", function(e) {

            // Number shortcuts
            if(["1","2","3","4"].includes(e.key)){
                const idx = parseInt(e.key) - 1;
                const selects = window.parent.document.querySelectorAll("select");

                selects.forEach(sel => {
                    sel.value = scores[idx];
                    sel.dispatchEvent(new Event("change",{bubbles:true}));
                });
            }

            // Submit on ENTER
            if(e.key === "Enter"){
                const buttons = window.parent.document.querySelectorAll("button");
                buttons.forEach(btn=>{
                    if(btn.innerText === "Submit"){
                        btn.click();
                    }
                });
            }
        });
        </script>
        """,
    )

def highlight_spans_html(text, spans, color):
    """Highlight character spans."""
    if not spans:
        return text

    result = ""
    last = 0

    for start, end in spans:
        result += text[last:start]
        result += f'<span style="background-color:{color}">{text[start:end]}</span>'
        last = end

    result += text[last:]
    return result


def diff_highlight(text_a: str, text_b: str, color: str):
    """
    Highlight text in text_a that differs from text_b.
    """
    matcher = difflib.SequenceMatcher(None, text_a, text_b)

    html = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        segment = text_a[i1:i2]
        if tag == "equal":
            html += segment
        else:
            for part in segment.split("\n"):
                html += (
                    f'<span style="background-color:{color}">'
                    f"{part}</span>"
                )

    return html


# --------------------------------------------------
# STREAMLIT UI CLASS
# --------------------------------------------------

class AnnotationUI:
    def __init__(self, df: pd.DataFrame, eval_path: Path):
        self.df = df
        self.ids = df["id"].tolist()
        self.eval_path = eval_path

        if "current_index" not in st.session_state:
            st.session_state.current_index = 0
            st.session_state.results = []

        self._load_existing_annotations()

    # --------------------------------------------------
    # LOAD EXISTING SCORES
    # --------------------------------------------------
    def _load_existing_annotations(self):
        if self.eval_path.exists() and not st.session_state.results:
            with open(self.eval_path, "r") as f:
                recorded = [json.loads(l) for l in f]

            st.session_state.results.extend(recorded)
            st.session_state.current_index = len(recorded)

    # --------------------------------------------------
    # LEGEND
    # --------------------------------------------------
    def render_legend(self):
        legend_text = ""
        for label, color in HIGHLIGHT_COLORS.items():
            legend_text += f'<span style="background-color:{color}">{label}</span>\n'

        st.markdown("## Highlight Legend")
        st.markdown(legend_text, unsafe_allow_html=True)

    # --------------------------------------------------
    # MAIN UI
    # --------------------------------------------------
    def render(self):
        add_title()
        self.render_legend()
        inject_keyboard_shortcuts()

        idx = st.session_state.current_index
        if idx >= len(self.df):
            st.success("Annotation finished!")
            return

        row = self.df.iloc[idx]
        st.markdown("---")
        st.markdown(f"## Response\n- **ID**: {row['id']}\n- **Query**: {row['query']}")

        col1, col2, col3 = st.columns(3)

        # ------------------------
        # Response 1 (Ad)
        # ------------------------
        with col1:
            st.subheader(TITLES[0])

            html = highlight_spans_html(
                row["response_ad"],
                row["spans"],
                color=HIGHLIGHT_COLORS["Advertising Text"],
            )

            st.markdown(
                f"<div style='white-space: pre-wrap'>{html}</div>",
                unsafe_allow_html=True,
            )

        # ------------------------
        # Response 2 (Blocked)
        # ------------------------
        with col2:
            st.subheader(TITLES[1])

            diff_html = diff_highlight(
                text_a=row["response_blocked"],
                text_b=row["response_reference"],
                color=HIGHLIGHT_COLORS["Text Added by Blocking"]
            )

            st.markdown(
                f"<div style='white-space: pre-wrap'>{diff_html}</div>",
                unsafe_allow_html=True,
            )

        # ------------------------
        # Response 3 (Reference)
        # ------------------------
        with col3:
            st.subheader(TITLES[2])
            diff_html = diff_highlight(
                text_a=row["response_reference"],
                text_b=row["response_blocked"],
                color=HIGHLIGHT_COLORS["Text Missing from Reference"]
            )

            st.markdown(
                f"<div style='white-space: pre-wrap'>{diff_html}</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        self.render_controls(row)

    # --------------------------------------------------
    # SCORING CONTROLS
    # --------------------------------------------------
    def render_controls(self, row):
        scores = {}
        cols = st.columns(len(LABELS))

        for (label, key), col in zip(LABELS.items(), cols):
            with col:
                scores[key] = st.selectbox(
                    label,
                    LIKERT_VALUES,
                    key=f"{key}_{st.session_state.current_index}",
                )

        if st.button("Submit"):
            for v in scores.values():
                if v == PLACEHOLDER:
                    st.warning(
                        "Please select all scores before submitting."
                    )
                    return

            result = {
                k: int(v[0]) for k, v in scores.items()
            }
            result["id"] = row["id"]
            st.session_state.results.append(result)

            with open(self.eval_path, "a") as f:
                f.write(json.dumps(result) + "\n")

            st.session_state.current_index += 1
            st.rerun()

    # --------------------------------------------------
    # ACCESS RESULTS
    # --------------------------------------------------
    def is_finished(self):
        return (
                len(st.session_state.results)
                == len(self.ids)
        )

    def get_results(self):
        if len(st.session_state.results) == len(self.ids):
            return pd.DataFrame(st.session_state.results)

        raise ValueError(
            "Not all responses were annotated."
        )