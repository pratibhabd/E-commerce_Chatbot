from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex
#from app.resources.router import router

encoder = HuggingFaceEncoder(
    name = "sentence-transformers/all-MiniLM-L6-v2"
)
#FAQ route
faq = Route(
    name = "faq",
    utterances = [
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "What is your return policy?",
        "How do I return a damaged item?",
        "Can I exchange a defective product?",
        "Do you offer refunds for faulty goods?",
        "Return and replacement process for defective items",
        # Payment methods
        "What payment methods are accepted?",
        "Can I pay with cash on delivery?",
        "Do you accept credit cards or GPay?",
        "Is EMI available?",
        "Can I use Paytm or UPI?",
        # Discounts
        "Do I get discount with the HDFC credit card?",
        "Are there any ongoing offers?",
        "Do you have any festival discounts?",
        "Is there a student discount?",
        "Do I get cashback on debit cards?"
    ]
)

#Product route
sql =  Route(
    name = "sql",
    utterances = [
        "I want to buy nike shoes that have 50% discount",
        "Are there any shoes under Rs 4000?",
        "Do you have formal shoes i size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of Puma running shoes?"
    ]
)

#Small-talk route
small_talk =  Route(
    name = "small_talk",
    utterances = [
    "How are you?",
    "What is your name?",
    "Are you a robot?",
    "What are you?",
    "What do you do?",
    "Are you fine?",
    "Whats up?",
    "Are you a Robot?"
    ]
)


index = LocalIndex(threshold=0.35)
router = SemanticRouter(encoder=encoder, index=index)
router.add([faq, sql, small_talk])

def inspect_query(query: str):
    print(f"\n🔍 Query: {query}")
    result = router(query)
    if result is None:
        print("⚠️ No matching route found — try lowering threshold or adding more utterances.")
    else:
        print(f"✅ Matched route: {result.name}")

if __name__ == '__main__':
    '''print(router("What is your return policy on defective product?").name)
    print(router("Pink puma shoes rate in range 5000 to 1000?").name)'''

    inspect_query("What is your return policy on defective product?")
    inspect_query("Pink puma shoes rate in range 5000 to 10000?")
    inspect_query("How are you?")


    '''USER QUERY → Semantic Router → (classifies intent)
                ↓
        ┌───────────────────────────┐
        │ If route == 'faq'         │
        │   → Search faq_data.csv   │
        │   → Find best matching Q  │
        │   → Return its answer     │
        └───────────────────────────┘
                ↓
        ┌───────────────────────────┐
        │ If route == 'sql'         │
        │   → Convert query to SQL  │
        │   → Run on SQLite DB      │
        │   → Return product data   │
        └───────────────────────────┘
'''