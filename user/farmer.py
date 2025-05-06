import datasets
from langchain.docstore.document import Document

# Load the dataset
guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

# Convert dataset entries into Document objects
docs = [
    Document(
        page_content="\n".join([
            f"Name: {guest['name']}",
            f"Relation: {guest['relation']}",
            f"Description: {guest['description']}",
            f"Email: {guest['email']}"
        ]),
        metadata={"name": guest["name"]}
    )
    for guest in guest_dataset
]



def get_user_info(name: str) -> str:
    """_summary_

    Args:
        name (str): _description_
        age (int): _description_
        location (str): _description_
        crop_type (str): _description_
        total_land (int): _description_
    """
    pass


def get_user_chat_info():
    """
    Search Query _> HI paddy!  >>> suvo sokal {get_user_info().name}
     abar jomi barishal e, ekhon amar ki fosol cash kora uchit?    >> M: soil condition ?
     past history : ha ashole goto bochor uriya use korsilam 5 kg amar jomi te 
     present time : amar ki ekhon kono shar dewa uchit?
    
    
    insert db : year | presticide | quantity 
                2024    uriya         5
    
    
    read db : is their any shar in past years? 
    
    
    """
    pass

