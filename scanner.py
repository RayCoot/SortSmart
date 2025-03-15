import base64
import os
from functools import wraps

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from LoggingUtil import get_logger

load_dotenv()

logger=get_logger("scaner")

class LLMInstance:
    _instance = None

    @staticmethod
    def get_instance():
        if LLMInstance._instance is None:
            LLMInstance._instance = ChatOpenAI(
                model="gpt-4o-2024-08-06",
                temperature=0.5,
            )
        return LLMInstance._instance


# query openai gpt llm with both image and text input
def query_recycle_method_from_image(image_bytes:bytes, city:str, region:str)->str:
    logger.info(f"query_recycle_method_from_image enter: city {city} region {region}")
    llm=LLMInstance.get_instance()
    # use york as default
    summary_file_name = "./data/york-summary.txt"
    if os.path.exists(f"./data/{city}-summary.txt"):
        summary_file_name=f"./data/{city}-summary.txt"
    elif os.path.exists(f"./data/{region}-summary.txt"):
        summary_file_name=f"./data/{region}-summary.txt"

    with open(f"{summary_file_name}", "r", encoding="utf-8") as file:
        instruction = file.read()
    image_b64 = base64.b64encode(image_bytes).decode()
    prompt = (f"identify one major object in this image, then use the dispose/collection instruction: {instruction}."
              "suggest best way to dispose major object as garbage, example: green bin, blue box, regular garbage bag, paper yark bag, drop off at depot."
              "if required to drop off of at Recycling Depots & Drop Off Centres, give address, contact and hours."
              "Use MarkDown format, prefer list"
              )
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
            },
        ],
    )
    llm2 = ChatOpenAI(
        model="gpt-4o-2024-08-06",
        temperature=0.5,
    )

    response = llm.invoke([message])
    logger.info(f"query_recycle_method_from_image exit: {response}")
    return response.content

# with open("./data/test1.jpg", "rb") as file:
#     image_bytes = file.read()
# print(query_recycle_method_from_image(image_bytes, city="toronto", region=""))


