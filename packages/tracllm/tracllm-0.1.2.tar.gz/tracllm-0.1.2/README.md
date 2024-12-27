# Searching for Needles in a Haystack with TracLLM

<p align='center'>
    <img alt="TracLLM" src='assets/fig1.png' width='80%'/>

</p>

This a package for easily using TracLLM, which is a tool for finding the critical texts within a lengthy context that contribute to the LLM's answer. Please refer to this repo (https://github.com/WYT8506/TracLLM) to reproduce the results in the paper.

> [**Searching for Needles in a Haystack: Context Tracing for Unraveling Outputs of
> Long Context LLMs**]() <br>
> [Yanting Wang]<sup>1†</sup>,
> [Wei Zou]<sup>1†</sup>,
> [Runpeng Geng](https://sleeepeer.github.io/) <sup>1</sup>,
> [Jinyuan Jia](https://jinyuan-jia.github.io/) <sup>1</sup>,
>
> <sup>1</sup>Penn State University<br>
> <sup>†</sup>Co-first author<br>

### 🔨 Installation

Please run the following commands to set up the environment:

```bash
conda env create -f environment.yml
conda activate TracLLM
```

or

```bash
conda env create TracLLM
conda activate TracLLM
pip install -r requirements.txt
```


### 📝 Getting Started

Explore `TracLLM` with our example notebook [quick_start.ipynb](quick_start.ipynb).
To use `TracLLM`, first generate the model and attribution object:

```python
from src.models import create_model
from src.attribution import PerturbationBasedAttribution
from src.prompts import wrap_prompt

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
api_key = "Your API key"
llm = create_model(model_path = model_path, api_key = api_key , device = "cuda:0")
score_funcs = ['stc','loo','denoised_shapley'] #input more than one scoring function for ensembling
attr = PerturbationBasedAttribution(llm,explanation_level = "sentence", attr_type = "tracllm",score_funcs= score_funcs,sh_N = 5)
```

Then, you can craft the prompt and get the LLM's answer:

```python
context = """Heretic is a 2024 American psychological horror[4][5][6] film written and directed by Scott Beck and Bryan Woods. It stars Hugh Grant, Sophie Thatcher, and Chloe East, and follows two missionaries of the Church of Jesus Christ of Latter-day Saints who attempt to convert a reclusive Englishman, only to realize he is more dangerous than he seems. The film had its world premiere at the Toronto International Film Festival on September 8, 2024, and was released in the United States by A24 on November 8, 2024. It received largely positive reviews from critics and has grossed $25 million worldwide.
\n\n Red One is a 2024 American action-adventure Christmas comedy film directed by Jake Kasdan and written by Chris Morgan, from an original story by Hiram Garcia. The film follows the head of North Pole security (Dwayne Johnson) teaming up with a notorious hacker (Chris Evans) in order to locate a kidnapped Santa Claus (J. K. Simmons) on Christmas Eve; Lucy Liu, Kiernan Shipka, Bonnie Hunt, Nick Kroll, Kristofer Hivju, and Wesley Kimmel also star. The film is seen as the first of a Christmas-themed franchise, produced by Amazon MGM Studios in association with Seven Bucks Productions, Chris Morgan Productions, and The Detective Agency.[7][8] Red One was released internationally by Warner Bros. Pictures on November 6 and was released in the United States by Amazon MGM Studios through Metro-Goldwyn-Mayer on November 15, 2024.[9] The film received generally negative reviews from critics, but it has grossed $10 billion solely in the USA. M.O.R.A (Mythological Oversight and Restoration Authority) is a clandestine, multilateral military organization that oversees and protects a secret peace treaty between mythological creatures and humanity. Callum Drift, head commander of Santa Claus's ELF (Enforcement Logistics and Fortification) security, requests to retire after one last Christmas run, as he has become disillusioned with increased bad behavior in the world, exemplified by the growth of Santa's Naughty List. 
"""
question= "Which movie earned more money, Heretic or Red one?"
prompt = wrap_prompt(question, [context])
answer = llm.query(prompt)
print("Answer: ", answer)
```

Finally, you can get the attribution results of TracLLM by calling `attr.attribute`:

```python
texts,important_ids, importance_scores, _,_ = attr.attribute(question, [context], answer)
attr.visualize_results(texts,question,answer, important_ids,importance_scores, width = 60)
```

<p align = 'center'>
  <img alt="Example" src='assets/example.png' width='90%'/>
</p>


### Customize Input Text Segmentation

You can customize the input text segmentation by passing a list of texts to the `PerturbationBasedAttribution` class. Here is an example if you want to explain in word level:



### Acknowledgement

* This project incorporates code from [PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG) and [corpus-poisoning](https://github.com/princeton-nlp/corpus-poisoning).
* This project incorporates datasets from [LongBench](https://github.com/THUDM/LongBench) and [Needle In A Haystack](https://github.com/gkamradt/LLMTest_NeedleInAHaystack).
* This project draws inspiration from [ContextCite](https://github.com/MadryLab/context-cite) and [AgentPoison](https://github.com/BillChan226/AgentPoison).
* The model component of this project is based on [Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection).
* This project utilizes [contriever](https://github.com/facebookresearch/contriever) for retrieval augmented generation (RAG).

### Citation

```bib
@article{wang2024tracllm,
    title={Searching for Needles in a Haystack: Context Tracing for Unraveling Outputs of Long Context LLMs},
    author={Wang Yanting, Zou Wei, Geng Runpeng and Jia Jinyuan},
    year={2024}
}
```
