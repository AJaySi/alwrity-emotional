import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

def sidebar():
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for Emotional Triggers Copywriting")
    with st.expander("What is **Emotional Triggers Copywriting** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's Emotional Triggers Copywriting, and How to use this AI generator 🗣️
            ---
            #### Emotional Triggers Copywriting

            Emotional Triggers Copywriting focuses on tapping into the emotions of the audience to evoke specific feelings or reactions. It involves:

            1. **Identifying Emotions**: Understanding the emotional triggers that resonate with the target audience.
            2. **Creating Emotional Connections**: Crafting copy that connects with the audience on an emotional level.
            3. **Eliciting Desired Emotions**: Using words, phrases, and storytelling techniques to evoke the desired emotional response.

            Emotional Triggers Copywriting is effective in creating impactful and memorable content that resonates with the audience's emotions.

            #### Emotional Triggers Copywriting: Simple Example

            - **Fear**: "Don't miss out on this limited-time offer before it's too late!"
            - **Joy**: "Experience the pure joy of achieving your fitness goals with our revolutionary workout program."
            - **Trust**: "Join thousands of satisfied customers who have trusted us to deliver quality products and services."

            ---
        ''')


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling Emotional Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('**Enter Brand/Company Name**', help="Enter the name of your brand or company.")
        with col2:
            description = st.text_input('**Describe What your Brand/Company Does ?** (In 5-6 words)', help="Describe your product or service briefly.")

        trust = st.text_input('Build Trust or Reliability',
                      help="Build trust and credibility by showcasing testimonials, guarantees, or endorsements.",
                      placeholder="Testimonials from satisfied customers..., Our guarantee that...")

        if st.button('**Get Emotional Triggers Copy**'):
            if trust.strip():
                with st.spinner("Generating Emotional Triggers Copy..."):
                    emotional_copy = generate_emotional_copy(brand_name, description, trust)
                    if emotional_copy:
                        st.subheader('**👩🔬👩🔬 Your Emotional Triggers Copy**')
                        st.markdown(emotional_copy)
                    else:
                        st.error("💥 **Failed to generate Emotional Triggers copy. Please try again!**")
            else:
                st.error("All fields are required!")

    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_emotional_copy(brand_name, description, trust):
    prompt = f"""As an expert copywriter, I need your help in creating 3 marketing campaigns for {brand_name},
        which is a {description}. Your task is to use Emotional Triggers Copywriting formula, to craft compelling copy.
        Use language that triggers fear or urgency to prompt action.
        Create a sense of joy or happiness by highlighting the benefits or outcomes.
        Build trust and credibility by showcasing, Trust: {trust}
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """ """
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using Emotional Triggers Copywriting - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Fear:
    Don't miss out on this limited-time offer before it's too late!

    ### Joy:
    Experience the pure joy of achieving your fitness goals with our revolutionary workout program.

    ### Trust:
    Join thousands of satisfied customers who have trusted us to deliver quality products and services.
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=3):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()
