from pathlib import Path
from typing import Sequence

import streamlit as st
from PyPDF2 import PdfReader

from zotero_assist.billing import query_billing_info
from zotero_assist.result import Result
from zotero_assist.widgets.content import Content
from zotero_assist.widgets.interaction import Interaction
from zotero_assist.zot.retrieve_all_local_pdfs import retrieve_all_local_pdfs


@st.cache_data
def get_all_zotero_pdfs() -> Sequence[Path]:
    return retrieve_all_local_pdfs()


@st.cache_data
def get_available_summary_for(pdf_file: Path) -> str:
    return (zotero_info_subject(pdf_file) or
            pdf_first_page_abstract(pdf_file) or
            Result.ok("No summary found.")).unwrap()


def zotero_info_subject(pdf_file: Path) -> Result[str]:
    zt_info_file = pdf_file.parent / ".zotero-ft-info"
    if zt_info_file.exists():
        zt_infos = zt_info_file.read_text().splitlines()
        for line in zt_infos:
            line_split = line.split(':')
            if line_split[0].strip() == 'Subject':
                return Result.ok(line_split[1].strip())
    return Result.error("No Zotero info subject found")


def pdf_first_page_abstract(pdf_file: Path) -> Result[str]:
    first_page_lines = PdfReader(pdf_file).pages[0].extract_text()
    for line in first_page_lines:
        if line.lower().startswith('abstract'):
            return Result.ok(line)
    return Result.error("No abstract found in pdf")


def add_zotero_pdfs(filenames: Sequence[Path]) -> None:
    for file in filenames:
        with st.expander(file.stem):
            st.write(get_available_summary_for(file))
            st.code(file.as_posix(), 'bash')
            st.button('select', key=file.stem, on_click=select_pdf, kwargs=dict(pdf=file))


def select_pdf(pdf: Path) -> None:
    if 'chat_history' in st.session_state:
        st.session_state['chat_history'].clear()
    if 'message_to_send' in st.session_state:
        st.session_state.message_to_send = ''

    st.session_state['selected_pdf'] = pdf


@st.cache_resource
def make_interaction():
    return Interaction(st.session_state)


@st.cache_resource
def make_content():
    return Content(st.session_state)


def has_pfd_selected():
    return 'selected_pdf' in st.session_state


def get_message() -> str:
    if 'message_to_send' not in st.session_state:
        st.session_state.message_to_send = ''
    st.text_input("You: ", "", key="input", on_change=clear_input)
    return st.session_state.message_to_send


def clear_input():
    st.session_state.message_to_send = st.session_state.input
    st.session_state.input = ''


st.set_page_config(page_title='zotero-assist', layout="wide")

billing = query_billing_info()
st.subheader("Billing:")
st.write(f"Usage: {billing.total_usage_usd:.2f}USD / {billing.limit_usd:.2f}USD")
st.write(f"Today's usage: {billing.today_usage_usd:.2f}USD")

st.title('Zotero Assist')

pdf_filenames = get_all_zotero_pdfs()

with st.sidebar:
    with st.expander("settings"):
        st.session_state['index_type'] = st.selectbox("Index type:", ['vector', 'tree'])
        st.session_state['index_model'] = st.selectbox("Index model:", ['text-ada-001', 'text-babbage-001', 'text-curie-001', 'gpt-3.5-turbo', 'text-davinci-003'])
        st.session_state['chat_model'] = st.selectbox("Chat model:", ['text-ada-001', 'text-babbage-001', 'text-curie-001', 'gpt-3.5-turbo'])
        st.session_state['max_history'] = st.number_input("Length of chat history:", min_value=1, value=100)

    st.markdown('---')
    st.subheader("Papers:")
    add_zotero_pdfs(pdf_filenames[:2])

interaction, content = st.columns([1, 1])

with interaction:
    chat_container = st.container()
    input_container = st.container()
    chat_widget = make_interaction()

    if has_pfd_selected():
        chat_widget.load_selected_history(chat_container)

    with input_container:
        message = get_message()
        if message and has_pfd_selected():
            chat_widget.send_to_selected(message, chat_container, mode='default')
            st.session_state.message_to_send = ''

with content:
    content_widget = make_content()
    if has_pfd_selected():
        st.subheader("Key concepts:")
        content_widget.show_summary()
        with st.container():
            st.write("""<div class='YScrollMarker'/>""", unsafe_allow_html=True)
            content_widget.show_pdf()

st.markdown("""
<style>
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    height: 700px;
    max-height: 700px;
    overflow-y: auto;
    overflow-x: hidden;
} 
</style>
""", unsafe_allow_html=True)
