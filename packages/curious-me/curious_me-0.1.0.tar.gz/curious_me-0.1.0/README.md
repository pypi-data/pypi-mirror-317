# curious-me

# Installation
1. Clone the repository
```bash
git clone 
```
2. Create virtual environment and activate it
```bash
python -m venv venv
```
In Windows
```bash
venv\Scripts\activate
```
In Linux
```bash
source venv/bin/activate
```

3. Install package
```bash
cd curious_me/curious_me
pip install .
```
4. Run the application, first open python then run the following commands
```python
from curious_me import Curious
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
            model_name="grok-2-1212",
            temperature=0.1,
            base_url="https://api.x.ai/v1",
            api_key=<your api key>,
        )

topics = ['GPT', 'LLM', 'Decoder', 'Artificial generative Intelligence']
curious = Curious(topics=topics, llm=llm)
curious.ask("What are recent advances in GPT?")
curious.get_review("RAG")
curious.get_citation(claim="Leaky ReLU is better than ReLU")
```

![Demo](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ252MjM2MXl0NzY3eTF4NjRzNWthNHNkdHhwdHM3OGU0NzB6NzNzNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/E10XlPvYkO3aXNYoEl/giphy.gif)