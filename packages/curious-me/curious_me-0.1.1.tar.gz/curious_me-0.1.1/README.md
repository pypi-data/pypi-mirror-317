# curious-me
Small library to ask questions, get reviews and citations of papers.
Currently papers are fetched from arxiv but it can be possible to use other sources as well.


# Installation

1. Create virtual environment and activate it
```bash
python -m venv venv
```
In Windows
```bash
venv\Scripts\activate
```
In GNU/Linux
```bash
source venv/bin/activate
```

2. Install package
If using pip
```bash
pip install curious-me
```

If cloned the repo
```bash
cd curious-me/curious_me
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
curious = Curious(topics=topics, llm=llm) # or Curious(topics=topics, llm=llm, skip_search=True) if you # want to search papers and build vector store again
curious.ask("What are recent advances in GPT?")
curious.get_review("RAG")
curious.get_citation(claim="Leaky ReLU is better than ReLU")
```

![Demo](https://github.com/itsankitkp/gifstore/blob/main/curious_demo.gif)

# Note:
Steps for using own pdfs
1. Clone the repo.
2. Add your pdfs in the folder `curious-me/curious_me/research_papers`
3. Run the following commands
```python
from curious_me import Curious
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
            model_name="grok-2-1212",
            temperature=0.1,
            base_url="https://api.x.ai/v1",
            api_key=<your api key>,
        )
topics = [] # your topics
curious = Curious(topics=topics, llm=llm, skip_search=True, rebuild_vec_store=True)
curious.ask("Questions?")
```