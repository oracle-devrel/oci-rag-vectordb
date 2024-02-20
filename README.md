# OCI Retrieval-Augmented Generations (RAG) with Generative AI Agents Service

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_oci-rag-vectordb)](https://sonarcloud.io/dashboard?id=oracle-devrel_oci-rag-vectordb)

## Introduction

RAG is one of the most coveted use cases nowadays for AI. The great thing about RAG is that it allows you to augment the knowledge of an LLM without having to retrain it. How, you may ask? Well, it's a way for the LLM to extract information (like a database) and present this information to the user very quickly.

This allows LLMs to acquire up-to-date knowledge, for example, the results of this year's SuperBowl, regardless of when the LLM you're running inference against has been trained. Therefore, you can make your LLM more intelligent and provide it with updated data with little to no effort.

Luckily, OCI GenAI Agents Service allows us to do just that: we will be able to upload our documents, process this data, put it into a Vector Store (OCI OpenSearch), create a Redis cluster for caching purposes, and provide users with a way to **consume** this data through a chatbot!

Oracle Cloud Infrastructure Generative AI Agents (Beta) is a fully managed service that combines the power of large language models with an intelligent retrieval system to create contextually relevant answers by searching your knowledge base, making your AI applications smart and efficient.

To use this service, index your data in OCI Search with OpenSearch and set up a cluster in OCI Cache with Redis for the cached user prompts and responses. Then you create an agent and attach your data source. Finally, you test your agent and allow it to generate insights and answer questions. We will see how to do all these steps in this application pattern.

### Use Cases

Use the OCI Generative AI Agents service for the following types of use cases:

- Chatbot for FAQs: Index FAQ and documentation so that users can easily access relevant topics and find answers to their questions through a chatbot or through the current documentation.
- Chatbot for policies: Index policy documents, such as human resources, insurance, or finance documents. When users ask specific questions about these policies, they can get answers relevant answers from those documents through a chatbot interface.

### Available Regions in OCI with the Generative AI Agents Service

Oracle hosts its OCI services in regions and availability domains. A region is a localized geographic area, and an availability domain is one or more data centers in that region. OCI Generative AI Agents is hosted in the following region:

- Region name: US Midwest (Chicago)
- Region identifier: `us-chicago-1`

## 0. Prerequisites and setup

- Oracle Cloud Infrastructure (OCI) Account with available credits to spend
- [Appropriate policies for the GenAI Agents Service](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/iam-policies.htm#policies) set up properly within your tenancy
- [Oracle Cloud Infrastructure Documentation - Generative AI Agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm#overview)
- [Oracle Cloud Infrastructure (OCI) Generative AI - Getting Started](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/getting-started.htm#get-started)
- [Oracle Cloud Infrastructure (OCI) Generative AI - API](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-agents/20240331/)
- [Python 3.10](https://www.python.org/downloads/release/python-3100/)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)
- You must have the Chicago region in your tenancy. Generative AI Agents is only available in Chicago.
- You must have an Identity Domain before you create an agent. [Follow the steps here](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/getting-started.htm#prereq-domain) to create an Identity Domain within your OCI Account.

Instead of doing the whole infrastructure deployment manually (which includes Cache with Redis and OCI Search with OpenSearch) you can deploy both things with the following [Terraform stack](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/create-stack.htm#create-stack):

1. Download the [prerequisite stack zip file](https://idem3zoqc0ti.objectstorage.us-ashburn-1.oci.customer-oci.com/p/MmUQVkbQKVfQT8V2ItM5Y3wqaM0uzRzpbI6RnFAXYLTL4sjxMcvZGrHtNTp3plKn/n/idem3zoqc0ti/b/genaiagent-service-stack/o/genaiagent-solution-accelerator-quickstart.zip) to your local machine.
2. In the navigation bar of the Console, choose a region that hosts Generative AI Agents, for example, US Midwest (Chicago). If you don't know which region to choose, see [Regions with Generative AI Agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm#regions).
3. Open the navigation menu and click Developer Services. Under Resource Manager, click Stacks.
4. Choose a compartment that you have permission to work in.
5. Click Create stack.
6. For the origin of the Terraform configuration, click My Configuration.
7. Under Stack Configuration, click .Zip file and then browse to or drop the prerequisite zip file from step 1 into the provided area.
8. Keep Custom providers unselected.
9. (Optional) Give the stack a name and description.
10. Choose Terraform version 1.2.x.
11. Click Next.
12. For openid_url, enter [your identity domain URL](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/getting-started.htm#prereq-domain). Example URL: `https://idcs-xxxxxxx.identity.oraclecloud.com`.
13. Keep the rest of the defaults and click Next.
14. Click Run apply.
15. Click Create.

Finally, we will generate some data points for our use case: we want to have **healthcare patient records** with some information from their previous visits. This is information we will give our LLM access to, through our Generative AI Agent, and ask the Agent questions about our patient records - this shows that even if the LLM hasn't trained for solving a specific type of prompt or query, RAG can facilitate this data *instantaneously* to the agent.

To generate data, we will go into our Conda environment and install Python dependencies to produce this data:

```bash
pip install -r requirements.txt
```

After, we can run `data_generator.py`: 

```bash
cd scripts/
python data_generator.py
```

The console will ask for how many synthetic users' data you want. For testing purposes, this can be any small value that will let us test; for your own use case in practice, your only job is to select which data will go into the vector database, and in which form (JSON, structured data, raw text... and their properties (if any)).

## 1. Create data sources

## 2. Create endpoint to consume data

## 3. Create agent to point to data source and identity domain

## 4. Talk to your new agent




Finally, we install Python dependencies:

```sh
pip install -r requirements.txt
```

Then, we will create a Bucket in our OCI tenancy, and upload the pictures we want to analyze over there. This will ultimately depend on your use case, if you're trying to count the number of objects in an image (for traffic management), count people (for access management)... You will have to decide.

## 1. Create OCI Bucket

Let's create the Bucket:

1. Open the **Navigation** menu in the Oracle Cloud console and click **Storage**. Under **Object Storage & Archive Storage**, click **Buckets**.

2. On the **Buckets** page, select the compartment where you want to create the bucket from the **Compartment** drop-down list in the **List Scope** section. Make sure you are in the region where you want to create your bucket.

3. Click **Create Bucket**.

4. In the **Create Bucket** panel, specify the following:
    - **Bucket Name:** Enter a meaningful name for the bucket.
    - **Default Storage Tier:** Accept the default **Standard** storage tier. Use this tier for storing frequently accessed data that requires fast and immediate access. For infrequent access, choose the **Archive** storage tier.
    - **Encryption:** Accept the default **Encrypt using Oracle managed keys**.

5. Click **Create** to create the bucket.

  ![The completed Create Bucket panel is displayed.](./img/create-bucket-panel.png)

The new bucket is displayed on the **Buckets** page.

  ![The new bucket is displayed on the Buckets page.](./img/bucket-created.png)

## 1. (Optional) Running Image Classification with Object Storage

We will run `scripts/image_classification.py`, but before, we need to obtain some info from our OCI Bucket and replace it in our script, line 37:

![Information needed from bucket](./img/info_needed_bucket.PNG)

Then, we can just run the following command:

```bash
python image_classification.py
```

To run OCI Vision's image classification against that image. These results will be in JSON format.

## 2. (Optional) Running Object Detection with Object Storage

We will repeat the steps to obtain the information as in step 1 above:

![Information needed from bucket for Object Detection](./img/info_needed_bucket_object_detection.PNG)

Then we can proceed and run the following command:

```bash
python object_detection.py
```

And we'll obtain a JSON object detailing detections.

Optionally, you can uncomment the block starting in line 107, to visualize these results. Note that you must have the file locally and reference it in order to draw detections on top of the local image:

![Uncomment this code block](./img/codeblock_uncomment.PNG)

## 3. Batch processing any video with OCI Vision

We have prepared two different scripts for you:

- One script will generate an output MP4 file with results inserted into it.
- The other script will process the video frame-by-frame, process detections into a single `.json` file, but won't produce an output file. It's a way to learn how to invoke the service and aggregate results.

### Run Detector

```bash
python detector_video.py [-h] --video-file VIDEO_FILE [--model-id MODEL_ID] 
    [--output-frame-rate OUTPUT_FRAME_RATE] [--confidence-threshold CONFIDENCE_THRESHOLD] [-v]
```

For example, in my case, where I want only to draw objects above 80% model confidence, 30 frames per second (in my output video), and using the standard OCI Vision model (not a custom one), I would run:

```bash
python detector_video.py --video-file="H:/Downloads/my_video.mp4" --output-frame-rate="30" --confidence-threshold="80" -v
```

### Create Output Video (CPU-intensive)

```bash
python video_processer.py --file FILE_PATH
```

For example:

```bash
python video_processer.py --file="H:/Downloads/my_video.mp4" --mode="moderate"
```

## Demo

[OCI Vision Overview - Exploring the Service](https://www.youtube.com/watch?v=eyJm7OlaRBk&list=PLPIzp-E1msraY9To-BB-vVzPsK08s4tQD&index=4)

## Tutorial

Here’s an use case being solved with OCI Vision + Python:

[App Pattern: OCI Vision Customized Object Detector in Python](https://www.youtube.com/watch?v=B9EmMkqnoGQ&list=PLPIzp-E1msraY9To-BB-vVzPsK08s4tQD&index=2)

## Physical Architecture

![arch](./img/arch.PNG)

## Contributing

This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License

Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK.
