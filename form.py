import streamlit as st
from dotenv import load_dotenv
from services import GSPGameService
from typing import Optional

load_dotenv()

from configs import PROMPT_COLLECTION, GAMES, DOWNLOAD_GAME_URL

st.set_page_config(
    page_title='Crafta',
    page_icon='🎮'
)

if 'submit_disabled' not in st.session_state:
    st.session_state.submit_disabled = False

if 'success' not in st.session_state:
    st.session_state.success = None

if 'error' not in st.session_state:
    st.session_state.error = None

st.markdown('''
        <style>
            .stMain {
                overflow: hidden !important;
            }

            .stMainBlockContainer {
                padding: 1rem 1rem 10rem;
            }

            #MainMenu, .stStatusWidget {
                display: none !important;
            }

            textarea {
                resize: none !important;
            }

            a {
                font-weight: bold;
                color: rgb(255, 255, 255) !important;
                font-size: 15px;
            }
        </style>
    ''', 
    unsafe_allow_html=True
)

st.title(
    body='Crafta: game creator'
)

st.write('''
    Create your own game without programming. Artificial intelligence will do everything for you. All you need to do is turn on your imagination.
''')

with st.sidebar:
    st.title('Try those games:')
    for name, url in GAMES:
        st.markdown(f'- <a href="{url}" target="_blank">{name}</a>', unsafe_allow_html=True)

@st.dialog('Prompt collection')
def show_dialog():
    for prompt in PROMPT_COLLECTION:
        st.write(prompt)
        st.divider()

show_dialog_button = st.button(
   label='Show prompt collection',
   key='show_dialog_button',
   help='Look at the prompt examples',
   disabled=st.session_state.submit_disabled,
   on_click=show_dialog
)

prompt_field = st.text_area(
    label='Your prompt:',
    key='prompt_field',
    help='Write down a detailed prompt and send it to AI for generation and publishing game.',
    max_chars=1000,
    height=200,
    width=800
)

def on_submit():
    st.session_state.submit_disabled = True
    st.session_state.success = None
    st.session_state.error = None

submit_prompt = st.button(
    label='Let\'s GO',
    key='submit_prompt',
    help='Clicking button, you sending your idea to AI.',
    type='primary',
    disabled=st.session_state.submit_disabled,
    on_click=on_submit
)

def generate_save_publish() -> Optional[str]:
    if not prompt_field:
        return
    
    with GSPGameService() as service:
        status, err_description, output_text = service.generate(prompt=prompt_field)

        if not status:
            st.session_state.error = err_description
            return None
        
        status, err_description, file_name = service.save(output_text)
        if not status:
            st.session_state.error = err_description
            return None
        
        url = service.publish(file_name)

    styles = '''
        <style>
            .custom-bg {
                background-color: rgba(61, 213, 109, 0.2);
                color: rgb(92, 228, 136);
                padding: 10px;
                border-radius: 5px;
                margin: 0px 0px 5px 0px;
            }

            .custom-bg p {
                margin: 0px;
            }
        </style>
    '''

    return f'{styles}'\
        '<div class="custom-bg">' \
        '   Congratulations 🎉 ' \
        f'   <p>Your game by <a href="{url}" target="_blank">URL</a>' \
        f'   or <a href="{DOWNLOAD_GAME_URL}/{file_name}" target="_blank">SAVE IT</a></p>' \
        '</div>'

if isinstance(st.session_state.success, str):
    st.markdown(st.session_state.success, unsafe_allow_html=True)

if isinstance(st.session_state.error, str):
    st.error(st.session_state.error)

if submit_prompt:
    st.session_state.submit_disabled = True

    st.info('Waiting, please ...')
    st.session_state.success = generate_save_publish()
    st.session_state.submit_disabled = False
    st.rerun()

# python -m streamlit run form.py --server.address=0.0.0.0 --server.port=8001