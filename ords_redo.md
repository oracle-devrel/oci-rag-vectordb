
## 1. Create/Use data

We will generate some data points for our use case: we want to have **healthcare patient records** with some information from their previous visits. This is information we will give our LLM access to, through our Generative AI Agent, and ask the Agent questions about our patient records - this shows that even if the LLM hasn't trained for solving a specific type of prompt or query, RAG can facilitate this data *instantaneously* to the agent.

To generate data, we will go into our Conda environment and install Python dependencies to produce this data:

```bash
pip install -r requirements.txt
```

After, we can run `data_generator.py`:

```bash
cd scripts/
python data_generator.py
```

The console will ask for how many synthetic users' data you want. For testing purposes, this can be any small value that will let us test; for your own use case in practice, your only job is to select which data will go into the vector store database, and in which form (JSON, structured data, raw text... and their properties (if any)).

Finally, we need to run `data_converter.py` to convert the data source into expected OCI OpenSearch format. From the docs, [this is the expected format](https://opensearch.org/docs/latest/im-plugin/) for a JSON Object being inserted in OpenSearch:

```json
{ "index": { "_index": "<index>", "_id": "<id>" } }
{ "A JSON": "document" }
```

For that, we just have to execute the following script, making sure that there's a file called `data/generated_data.json` in your `data/` directory:

```bash
python data_converter.py
```

This will generate `data/opensearch_data.json`, in the proper format for OCI OpenSearch. Now that we have our data properly-formatted, we can use the data to create our knowlegde base.

TODO We need to connect to the VM in the same private subnet as our deployed OpenSearch and Redis cluster; through this VM, we will push the generated data into the OpenSearch cluster: