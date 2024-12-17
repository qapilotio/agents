from langchain_openai import ChatOpenAI

def initialize_llm(OPENAI_API_KEY):

    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=OPENAI_API_KEY,
    )