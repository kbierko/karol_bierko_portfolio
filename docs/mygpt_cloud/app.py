import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
from supabase import create_client
import os


model_pricings = {
    "gpt-4o": {
        "input_tokens": 5.00 / 1_000_000,     # per token
        "output_tokens": 15.00 / 1_000_000,   # per token
    },
    "gpt-4o-mini": {
        "input_tokens": 0.150 / 1_000_000,    # per token
        "output_tokens": 0.600 / 1_000_000,   # per token
    },
}
MODEL = "gpt-4o"   # lub "gpt-4o-mini"
USD_TO_PLN = 3.73  # na dzień 2026-03-19
PRICING = model_pricings[MODEL]


openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


# ========
# CHATBOT
# ========
def get_chatbot_reply(user_prompt, memory):
    # dodaj system message
    messages=[
        {
            "role": "system",
            "content": st.session_state["chatbot_personality"],
         },
    ]

    # dodaj wszystkie wiadomości z pamięci
    for message in memory:
        messages.append({"role": message["role"], "content": message["content"]})

    # dodaj wiadomość użytkownika
    messages.append({"role": "user", "content": user_prompt})
    
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    usage = {}
    if response.usage:
        usage = {
            # INPUT TOKENS
            "prompt_tokens": response.usage.prompt_tokens,
            # OUTPUT TOKENS
            "completion_tokens": response.usage.completion_tokens,
            # INPUT + OUTPUT TOKENS
            "total_tokens": response.usage.total_tokens,
        }
    
    return {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "usage": usage,
    }

# ==================================
# CONVERSATION HISTORY AND DATABASE
# ==================================
DEFAULT_PERSONALITY = """
Jesteś pomocnikiem, który odpowiada na wszystkie pytania użytkownika.
Odpowiadaj na pytania w sposób zwięzły i zrozumiały
""".strip()


def load_conversation_to_state(conversation):
    st.session_state["id"] = conversation["id"]
    st.session_state["name"] = conversation["name"]
    st.session_state["messages"] = conversation.get("messages") or []
    st.session_state["chatbot_personality"] = conversation["chatbot_personality"]

def load_conversation(conversation_id):
    response = supabase.table("conversations") \
        .select("*") \
        .eq("id", conversation_id) \
        .single() \
        .execute()

    conversation = response.data

    load_conversation_to_state(conversation)
    return conversation


def save_current_conversation_messages():
    supabase.table("conversations").update({
        "messages": st.session_state["messages"]
    }).eq("id", st.session_state["id"]).execute()


def save_current_conversation_name():
    supabase.table("conversations").update({
        "name": st.session_state["new_conversation_name"]
    }).eq("id", st.session_state["id"]).execute()


def save_current_conversation_personality():
    supabase.table("conversations").update({
        "chatbot_personality": st.session_state["chatbot_personality"]
    }).eq("id", st.session_state["id"]).execute()


def create_new_conversation():
    response = supabase.table("conversations").insert({
        "name": "Nowa konwersacja",
        "chatbot_personality": DEFAULT_PERSONALITY,
        "messages": [],
    }).execute()

    conversation = response.data[0]

    load_conversation_to_state(conversation)

    st.rerun()


def switch_conversation(conversation_id):
    conversation = load_conversation(conversation_id)

    load_conversation_to_state(conversation)

    st.rerun()


def list_conversations():
    response = supabase.table("conversations") \
        .select("id, name") \
        .order("id", desc=True) \
        .execute()

    return response.data


# ==============
# MAIN PROGRAM
# ==============
conversations = list_conversations()

if conversations:
    load_conversation(conversations[0]["id"])
else:
    create_new_conversation()

st.title(":classical_building: MyGPT")

for message in st.session_state["messages"]:    
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("O co chcesz zapytać?")
if prompt:
    # wyświetlenie promptu użytkownika
    user_message = {"role": "user", "content": prompt}
    with st.chat_message("user"):
        st.markdown(user_message["content"])
    
    st.session_state["messages"].append(user_message)

    # wyświetlenie odpowiedzi AI
    with st.chat_message("assistant"):
        chatbot_message = get_chatbot_reply(
            prompt,
            memory=st.session_state["messages"][-10:], # przekazujemy ostatnie 10 wiadomości jako pamięć
        )
        st.markdown(chatbot_message["content"])

    st.session_state["messages"].append(chatbot_message)
    save_current_conversation_messages()


with st.sidebar:
    st.write("Aktualny model:", MODEL)
    total_cost = 0.0
    for message in st.session_state["messages"]:
        if "usage" in message:
            total_cost += message["usage"]["prompt_tokens"] * PRICING["input_tokens"]
            total_cost += message["usage"]["completion_tokens"] * PRICING["output_tokens"]
    
    c0, c1 = st.columns(2)
    with c0:
        st.metric("Koszt rozmowy (USD)", f"${total_cost:.4f}")
    with c1:
        st.metric("Koszt rozmowy (PLN)", f"{total_cost * USD_TO_PLN:.4f} zł")
    
    st.session_state["name"] = st.text_input(
        "Nazwa konwersacji",
        value=st.session_state["name"],
        key="new_conversation_name",
        on_change=save_current_conversation_name,
    )

    st.session_state["chatbot_personality"] = st.text_area(
        "Osobowość chatbota",
        max_chars=1000,
        height=200,
        value=st.session_state["chatbot_personality"],
        key="new_chatbot_personality",
        on_change=save_current_conversation_personality,
    )

    st.subheader("Konwersacje")
    if st.button("Nowa konwersacja"):
        create_new_conversation()
    
    # pokazujemy listę top5 konwersacji
    conversations = list_conversations()
    sorted_conversations = sorted(conversations, key=lambda x: x["id"], reverse=True)
    for conversation in sorted_conversations[:5]:
        c0, c1 = st.columns([10, 4])
        with c0:
            st.write(conversation["name"])
        with c1:
            if st.button("Załaduj", key=conversation["id"], disabled=conversation["id"] == st.session_state["id"]):
                switch_conversation(conversation["id"])