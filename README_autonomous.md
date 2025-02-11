# Build with GenAI and RAG with Autonomous Database

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_oci-rag-vectordb)](https://sonarcloud.io/dashboard?id=oracle-devrel_oci-rag-vectordb)

## Introduction

RAG (Retrieval-Augmented Generation) is revolutionizing the way we interact with AI by seamlessly enhancing the capabilities of large language models (LLMs). Imagine an AI that not only generates text but also pulls in real-time information from vast databases, providing you with accurate and up-to-date responses instantly.

With RAG, your LLM can access the latest knowledge —like the results of this year's Super Bowl (yesterday, at the time of writing) — regardless of its training cut-off date. This means you can empower your AI to deliver intelligent, context-aware answers with minimal effort.

Thanks to the OCI GenAI Agents Service, harnessing the power of Oracle Autonomous Database 23AI's advanced vector search capabilities is easier than ever. This service enables you to efficiently process and store documents, allowing users to **interact** with this wealth of information through an intuitive chatbot experience!

![chat with model - autonomous 1](./img/chat_autonomous_1.png)

![chat with model - autonomous 2](./img/chat_autonomous_2.png)

Here's a list of the most prominent features of the service:

- Supports several data on-boarding methods and interaction channels (chat interface or API)
- Creates contextually relevant answers by searching your knowledge base
- Provides source attribution for every answer
- Leverages Oracle Autonomous Database 23AI's vector search capabilities for accurate semantic search
- Includes content moderation options for input and output to ensure a safe and respectful chat experience
- Supports multi-turn conversations, where users can ask follow-up questions and receive answers that consider the context of previous questions and answers
- Can interpret data from two-axis charts and reference tables in a PDF, without needing explicit descriptions of the visual elements

For the infrastructure, we have the following OCI Services present:

- **Oracle Autonomous Database 23AI** for vector search, tokenization, and embeddings storage - providing a fully managed solution for RAG applications
- **OCI Generative AI Agents** for communicating and interacting with the data in our Autonomous Database
- **OCI Object Storage** to temporarily store PDF documents to later extract their text and embeddings with Autonomous Database
In this specific solution, we will use **Oracle Autonomous Database 23AI** as our storage and vector search mechanism. The 23AI version of Autonomous Database comes with **built-in vector search** capabilities, making it ideal for RAG applications. It handles all the data processing, tokenization, and embedding storage, providing a simpler and more integrated solution compared to other approaches.
**OCI Vault** to securely store database connection details

OCI Generative AI Agents is a fully managed service that combines the power of large language models (LLMs) with an intelligent retrieval system to create contextually relevant answers by searching your knowledge base, making your AI applications smart and efficient.

To use this service, we'll follow these five steps:

1. Create the necessary infrastructure and OCI resources
2. Upload and embed your data
3. Create a knowledge base
4. Create an agent
5. Start chatting

### Use Cases

Use the OCI Generative AI Agents service for the following types of use cases:

- Customer Support: In the customer service industry, RAG agents can retrieve information from a company's knowledge base to provide correct and contextually relevant answers to customer inquiries, reducing response times and improving customer satisfaction.
- Legal Research: Legal professionals can use RAG agents to quickly find precedents and relevant case law from vast legal databases, streamlining the research process and ensuring thorough consideration of relevant legal texts.
- Healthcare and Medical Guidance: In healthcare, RAG agents can help doctors and medical staff by providing diagnostic support, retrieving medical literature, treatment protocols, and patient history to suggest potential diagnoses and treatments.
- Financial Analysis: In finance, RAG agents can analyze large volumes of financial data, reports, and news to provide analysis and recommendations for traders and analysts, helping them make informed investment decisions.
- Educational Tutoring: RAG agents can function as personal tutors, providing students with explanations, resources, and answers to questions by accessing educational content and tailoring explanations to the student's current level of understanding.
- Content Creation: In media and content creation, RAG agents can help writers and journalists by pulling information on specific topics, suggesting content ideas, and even drafting sections of articles based on the latest data and trends.
- Technical Support and Troubleshooting: RAG agents can guide users through technical troubleshooting processes by accessing and synthesizing technical manuals and support forums to offer step-by-step help.
- Supply Chain Management: In supply chain and logistics, RAG agents can provide insights by retrieving and synthesizing information on inventory levels, supplier data, and logistic metrics to optimize operations and predict potential disruptions.
- Real Estate Market Analysis: RAG agents can help real estate professionals by aggregating and analyzing data from several sources, including market trends, property listings, and regulatory changes, to provide comprehensive market analyses.
- Travel Planning and Help: In the travel industry, RAG agents can serve as interactive travel guides, pulling information on destinations, weather, local attractions, and regulations to provide personalized travel advice and itineraries.

### Available Regions in OCI with the Generative AI Agents Service

Oracle hosts its OCI services in regions and availability domains. A region is a localized geographic area, and an availability domain is one or more data centers in that region.

OCI Generative AI Agents is hosted in the following region:

- Region name: US Midwest (Chicago)
- Region identifier: `us-chicago-1`

## 0. Prerequisites and setup

### Prerequisites

- Oracle Cloud Infrastructure (OCI) Account with available credits to spend
- [Appropriate policies for the GenAI Agents Service](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/iam-policies.htm#policies) set up properly within your tenancy
- [Oracle Cloud Infrastructure Documentation - Generative AI Agents](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/home.htm)
- You must be subscribed to the `Chicago` region in your tenancy.
- You must have an Identity Domain before you create an agent. [Follow the steps here](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/getting-started.htm#prereq-domain) to create an Identity Domain within your OCI Account.

### Docs

- [OCI Object Storage Guidelines in Generative AI Agents](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/data-requirements.htm#data-requirements)
- [OCI Search with OpenSearch Guidelines for Generative AI Agents](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/opensearch-guidelines.htm#opensearch-guide)
- [Oracle Database Guidelines for Generative AI Agents](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/oracle-db-guidelines.htm)
- [Oracle Cloud Infrastructure (OCI) Generative AI - Getting Started](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/getting-started.htm#get-started)
- [Oracle Cloud Infrastructure (OCI) Generative AI - API](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-agents/20240531/)
- [OCI GenAI Agents - Concepts](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/concepts.htm#concepts)

### Setup

In the navigation bar of the Console, choose a region that hosts Generative AI Agents - for example, US Midwest (Chicago). If you don't know which region to choose, see [Regions with Generative AI Agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm#regions).

#### Task 1: Create Dynamic Group and Policies

First, we will need to ensure that we have access to the service. For this, let's create a *dynamic group* and some *policies* to allow access to the service.

1. Go to your dynamic groups and create a new dynamic group:

  ![create dynamic group](./img/dynamic_group_create.png)

  Create a dynamic group with the following name and the following matching rule:

  ![dynamic group name](./img/dg_details.png)

  This will ensure all Generative AI Agent resources are allowed to be accessed by this dynamic group.


2. Add the following policies to the dynamic group:

  ![policy details](./img/policy_details.png)

  Replace `genaiagentdg` with the name of your dynamic group, and `<genai-agent-administrators>` with the name of the group which you are part of:

  ```bash
  allow dynamic-group genaiagentdg to manage database-tools-family in tenancy
  allow dynamic-group genaiagentdg to manage secret-bundle in tenancy
  allow group <genai-agent-administrators> to manage object-family in tenancy
  allow group <genai-agent-administrators> to manage genai-agent-family in tenancy
  # if you aren't in the Default domain, you'll need to prepend the domain name to the group name like this:
  # allow dynamic-group OracleIdentityCloudService/genaiagentdg to manage secret-bundle in tenancy
  # also for the group policies:
  # allow group OracleIdentityCloudService/<genai-agent-administrators> to manage genai-agent-family in tenancy
  ```

  The four permissions are: `object-family`, `genai-agent-family`, `secret-bundle`, and `database-tools-family`. Ensure the user's that will make the requests is a member of the mentioned group and has the mentioned permissions (preferrably in the whole tenancy, although if you want to configure it per compartment or be more careful with your permissions, you can do so by following [this guide](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/iam-policies.htm)).

  > **Note**: if you are working on an identity provider other than Oracle Identity Cloud Service to authenticate to your OCI tenancy, you'll need to *prepend* the name of your identity provider in the policies and dynamic group definitions. For example, if you're using 'OracleIdentityCloudService', your policy shall be set like 'OracleIdentityCloudService/<genai-agent-administrators>' instead of '<genai-agent-administrators>'.

#### Task 2: Create VCN and Private Subnet

We need to create a VCN and private subnet to host our Autonomous database securely in a private network. Then, we will use a Database Connection to act as a bastion. This will help our database be more secure and isolated from the public internet.

1. Create Virtual Cloud Network (VCN):
  - Navigate to Networking -> Virtual cloud networks 
  - Click "Create VCN"
  - Provide IPv4 CIDR Block: `10.0.0.0/16`

![create vcn](./img/create_vcn.png)

2. Create Private Subnet:
   - In the newly created VCN, click "Create Subnet"
   - Configure:
     - IPv4 CIDR Block: `10.0.1.0/24`
     - Select "Private Subnet"
     - Leave other settings as default

![create subnet](./img/create_subnet.png)

3. Configure Security List:
   - Go to the new subnet
   - Navigate to Security List
   - Add ingress rules including:
     - Database access ports 1521-1522
     - Other required ingress rules

![ingress rules](./img/vcn_creation.png)

#### Task 3: Create Vault for Database Secrets

1. Create Vault:
   - Navigate to Key Management & Secret Management -> Vault
   - Provide Name
   - Click Create Vault

![vault creation](./img/vault_creation.png)

2. Create Encryption Key:
   - In the new vault, click "Create Key"
   - Configure:
     - Provide Name
     - Protection Mode: HSM
     - Leave other settings as default
   - Click Create Key

![key creation](./img/key_creation.png)

> **Note**: set your protection mode to `HSM`.

#### Task 4: Create Autonomous Database

Now, we need to create the Autonomous Database that will be used by the Generative AI Agents service to store and retrieve data in the form of *embeddings*.

![databases_menu](./img/databases_menu.png)

1. Create Database:
   - Navigate to Oracle Databases -> Autonomous Databases
   - Click "Create Autonomous Database"
   - Configure:
     - Select Compartment
     - Provide Display name and Database name
     - Workload type: Data Warehouse
     - Deployment type: Serverless
     - Database version: `23ai`
     - Set a password
     - Network Access: `Private Endpoint access` only
     - Select the VCN and subnets that we created in task 2
     - **Uncheck** "Require mutual TLS (mTLS) authentication"
     - Provide valid email ID
   - Click Create Autonomous Database

![database_config](./img/database_config.png)

#### Task 5: Create Database Tools Connection

Now, we'll create a database connection to act as a bastion to our database. This will help us connect to the database securely and isolate it from the public internet. Additionally, this connection will be used by the Generative AI Agents service to retrieve data from the database.

Go to the Database Tools Connections menu:
![connections_menu](./img/connections_menu.png)

Before, let's make sure we have the private IP address and connection strings of our Autonomous Database. Go to your Autonomous Database details page:

![database_details](./img/database_details.png)

Now, we can get the private IP address and connection strings from the details page:

![private_db_ip](./img/private_db_ip.png)

![connection_strings](./img/connection_strings.png)

Your connection string should look something like this:

```bash
(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=lpne8zzr.adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gc3dd18cc561e12_agents_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=no)))
```

Let's make the necessary changes to the connection string:

- Change `retry_count` from `20` to `3`
- Replace `host` with your database'sprivate IP address

Your connection string should look like this:

```bash
(description= (retry_count=3)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=10.0.1.76))(connect_data=(service_name=agents_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=no)))
```

Let's save this info for later use. Now, we can create the database connection with this information:

- Navigate to Developer Services -> Database Tools Connections
- Click "Create connection"
- Configure:
  - Provide Name and Compartment
  - Database cloud service: Oracle Autonomous Database
  - Username: `ADMIN`
  - Create a password secret:
    - Provide Name
    - Select the vault and keys from Task 3
    - Use the same password you used when creating the Autonomous Database
  - Copy the connection string from Task 5
  - Create private endpoint:
    - Provide Name
    - Select the private subnet from Task 2
  - In SSL details, select the wallet format: `None`

Finally, let's validate the connection we just created:
  - Go to new Database Tools connection
  - Click `Validate` to verify setup

![validate connection](./img/validate_connection.png)

If everything is correct, you should see the following message:

![validate connection - success](./img/validate_result.png)

As a recap, we have created the following resources:

- **Policies and dynamic group**, to allow access to the service
- **VCN** with private subnet and security list, to protect the Autonomous Database
- **Autonomous Database**, in a private subnet of a VCN
- **Database Tools Connection**, to connect to the Autonomous Database
- **Vault**, to store the database password
- **Encryption Key**, to encrypt the database password

If you have followed every step, the infrastructure setup is complete. Now, we can start using this infrastructure to create the knowledge base for our RAG agent.

#### Task 6: Set up the Autonomous Database

To work with the Oracle Generative AI Agents service, we need to set up the Autonomous Database to conform to some requirements. 

To launch this SQL worksheet, go to the Autonomous Database details page and click on the `SQL worksheet` button:

![sql_worksheet](./img/sql_worksheet.png)

Now, we can proceed to run some SQL code:

1. First, we'll run an Access Control List rule to allow the database user to access the embedding model, amongst other things:

```sql
-- ACL to let user go out everywhere (host =>'*'), it's not required for Oracle Base Database.
begin
 -- Allow all hosts for HTTP/HTTP_PROXY
 dbms_network_acl_admin.append_host_ace(
     host =>'*',
     lower_port => 443,
     upper_port => 443,
     ace => xs$ace_type(
     privilege_list => xs$name_list('http', 'http_proxy'),
     principal_name => upper('admin'),
     principal_type => xs_acl.ptype_db)
 );
 end;
 /
```

2. We'll now create some credentials to access the OCI GenAI Agents service. For this, we'll need to add a new API key to our OCI user, and then use this API key with the `DBMS_CLOUD` plugin to authenticate. For this, go to your user's OCI page and click on the `API Keys` tab. Once generated (or uploaded), save it in your local computer as you will need to use the fingerprint and private keys in the following steps:

![generate_api_key](./img/generate_api_key.png)

3. Let's use this API key and the `DBMS_CLOUD` plugin to authenticate. You will need your user, compartment and tenancy OCIDs, as well as your private key and fingerprint. In the following SQL code, replace the strings with your own values, and run the code:

```sql
-- DBMS_CLOUD credentials
-- Some examples are based on DBMS_CLOUD, that is included in Autonomous DB.
-- If you need to install it (for example on Base Database) you can refer to: https://support.oracle.com/knowledge/Oracle%20Cloud/2748362_1.html
begin
     DBMS_CLOUD.CREATE_CREDENTIAL (
         credential_name => 'OCI_CRED_BUCKET',
         user_ocid       => 'ocid1.user.oc1..aaaaaaaaa2...',
         tenancy_ocid    => 'ocid1.tenancy.oc1..aaaaaaaa...',
         private_key     => 'MIIEvgI...RpV',
         fingerprint     => '0f:df...1d:88:d6'
     );
 end;
 /
```

> **Note**: the private key shall not begin with `-----BEGIN PRIVATE KEY-----` or `-----END PRIVATE KEY-----`, it shall only have the key's content. You can also retrieve the key's fingerprint from the API key details page.

4. Let's create credentials for the Generative AI Agents service:

```sql
declare
     jo json_object_t;
begin
     jo := json_object_t();
     jo.put('user_ocid','ocid1.user.oc1..aaaaaaaaa2...');
     jo.put('tenancy_ocid','ocid1.tenancy.oc1..aaaaaaaa...');
     jo.put('compartment_ocid','ocid1.tenancy.oc1..aaaaaaaa...');
     jo.put('private_key','MIIEvgI...RpV');
     jo.put('fingerprint','0f:df...1d:88:d6');
     dbms_vector.create_credential(
         credential_name   => 'OCI_CRED',
         params            => json(jo.to_string)
     );
 end;
 /
```

If the setup has been properly executed, you can run this SQL query as a test, to embed the word "hello" with the `cohere.embed-multilingual-v3.0` model:

```sql
SELECT
     dbms_vector.utl_to_embedding(
         'hello',
         json('{
             "provider": "OCIGenAI",
             "credential_name": "OCI_CRED",
             "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText",
             "model": "cohere.embed-multilingual-v3.0"
         }')
     )
 FROM dual;
```

#### Task 7: Upload & embed your data

Now that our setup is done and we can already generate embeddings, we can upload a test PDF file to an OCI Object Storage bucket. From there, we'll use the `DBMS_CLOUD.GET_OBJECT` function to embed the file and save the embeddings in the Autonomous Database, in chunks of 75 tokens.

1. Create an OCI Object Storage bucket:

  ![create bucket](./img/create_bucket.png)

2. Upload your PDF file to your bucket

  ![uploaded_pdf](./img/uploaded_pdf.png)

3. From this PDF, create a Pre-Authenticated Request (PAR) to access the file:

  ![create par](./img/create_par.png)

4. Copy the PAR URL:

  ![create_par_output](./img/create_par_output.png)

5. Use the `DBMS_CLOUD.GET_OBJECT` function to embed the file and save the embeddings in the Autonomous Database, in chunks of 75 tokens. For your data, make sure to replace that `https` PAR with your own PAR URL, and execute it:

  ```sql
  CREATE TABLE ai_extracted_data AS
  SELECT
      j.chunk_id,
      j.chunk_offset,
      j.chunk_length,
      j.chunk_data
  FROM
      -- divide a blob into chunks (utl_to_chunks):
      (select * from dbms_vector_chain.utl_to_chunks(
          dbms_vector_chain.utl_to_text(
              to_blob(
                  DBMS_CLOUD.GET_OBJECT('OCI_CRED_BUCKET', 'https://objectstorage.us-chicago-1.oraclecloud.com/p/Aaklz9CEuOdwhdWbV-bLcDTvML4DNlRtTw7z6dMuSMh1gn2toBnmE1airTA-ZhkW/n/axk4z7krhqfx/b/AI_Vector_Search/o/oracle-ai-vector-search-users-guide.pdf')
              )
          ), json('{"max":"75", "normalize":"all", "overlap":"15"}')
      )),
      JSON_TABLE(column_value, '$'
          COLUMNS (
              chunk_id NUMBER PATH '$.chunk_id',
              chunk_offset NUMBER PATH '$.chunk_offset',
              chunk_length NUMBER PATH '$.chunk_length',
              chunk_data CLOB PATH '$.chunk_data'
          )
      ) j;
  ```

6. If everything went well, you can check the table's contents: 

  ![table_contents](./img/table_contents.png)

  You can run the command yourself:

  ```sql
  SELECT * FROM ai_extracted_data;
  select COUNT(*) from ai_extracted_data
  ```

7. Now, remember that, even though we already have some data in this table, it's in cleartext (not in its numerical embeddings form). To generate the embeddings from these cleartext chunks, let's first create the vector table:

  ```sql
  -- Create vector table from an existing table
  -- In the following table ai_extracted_data, chunk_id is the record id while chunk_data is the content column.
  create table ai_extracted_data_vector as (
      select chunk_id as docid, to_char(chunk_data) as body, dbms_vector.utl_to_embedding(
          chunk_data,
          json('{
              "provider": "OCIGenAI",
              "credential_name": "OCI_CRED",
              "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText",
              "model": "cohere.embed-multilingual-v3.0"
          }')
      ) as text_vec
      from ai_extracted_data
      where chunk_id <= 400
  )
  ```

  > **Note**: there's a quota limit for running the embedding model. For datasets with more than 400 records, we can repeatedly load the data or write a script to load data in batches.

  > **Note**: if your existing data hasn't been processed into chunks yet, your chunk size might exceed 512, which would prevent embedding generation. If you run into this issue, refer to [Custom Chunking Specifications](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/custom-chunking-specifications.htm) to convert content to chunks.

8. If you have more than 400 chunks/records in the table, you can repeat the process for the next batch of data with this script:

  ```sql
  insert into ai_extracted_data_vector
  select chunk_id as docid, to_char(chunk_data) as body, dbms_vector.utl_to_embedding(
      chunk_data,
      json('{
          "provider": "OCIGenAI",
          "credential_name": "OCI_CRED",
          "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText",
          "model": "cohere.embed-multilingual-v3.0"
      }')
      ) as text_vec
  from ai_extracted_data
  where chunk_id > 400
  ```

  If you just have **too many** chunks/records in the table, you can repeat the process for the next batch of data sequentially by editing the SQL above, or through some additional programming logic (automating it). Just know that for now the limit is 400 chunks per data load.


9. Finally, create the function that will return `top_k` results when calling the function (by default, 5):

```sql
-- Create function from vector table
-- When returning the results, rename (alias) the record ID as 'DOCID', the content column as 'BODY', and the VECTOR_DISTANCE between text_vec and query_vec as 'SCORE'. These 3 columns are required. If the vector table includes 'URL' and 'Title' columns, rename them (alias) as 'URL' and 'TITLE' respectively.
create or replace FUNCTION retrieval_func_ai (
     p_query IN VARCHAR2,
     top_k IN NUMBER
) RETURN SYS_REFCURSOR IS
     v_results SYS_REFCURSOR;
     query_vec VECTOR;
BEGIN
     query_vec := dbms_vector.utl_to_embedding(
         p_query,
         json('{
             "provider": "OCIGenAI",
             "credential_name": "OCI_CRED",
             "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText",
             "model": "cohere.embed-multilingual-v3.0"
         }')
     );

     OPEN v_results FOR
         SELECT DOCID, BODY, VECTOR_DISTANCE(text_vec, query_vec) as SCORE
         FROM ai_extracted_data_vector
         ORDER BY SCORE
         FETCH FIRST top_k ROWS ONLY;

     RETURN v_results;
 END;
```

10. You can now run this function to retrieve the top `n` results:

  ```sql
  -- Run & check the function
  -- Display the DOCID and SCORE
  DECLARE
      v_results SYS_REFCURSOR;
      v_docid VARCHAR2(100);
      v_body VARCHAR2(4000);
      v_score NUMBER;
      p_query VARCHAR2(100) := 'What is self-instruct?';
      top_k NUMBER := 10;
  BEGIN
      v_results := retrieval_func_ai(p_query, top_k);

      DBMS_OUTPUT.PUT_LINE('DOCID | SCORE');
      DBMS_OUTPUT.PUT_LINE('--------|------');

      LOOP
          FETCH v_results INTO v_docid, v_body, v_score;
          EXIT WHEN v_results%NOTFOUND;

          DBMS_OUTPUT.PUT_LINE(v_docid || ' | ' || v_score);
      END LOOP;

      CLOSE v_results;
  END;
  ```

  You should see something like this, with a ranking of the most relevant chunks (and their IDs), together with the similarity score:
  
  ![embeddings_result](./img/embeddings_result.png)

  Even though we were able to communicate with our embeddings directly (and you're perfectly fine if you wanted to create a system like this), we'll use the Generative AI Agents service to create an agent that can answer questions about our data through the OCI Console interface.


## 1. Create a knowledge base

To associate every step we've done in the setup so far with the Generative AI Agents service, we'll need to create a knowledge base. This will let the agent know about our data and be able to answer questions about it.

1. Go to the Generative AI Agents service and click on the *Knowledge Bases* tab:

  ![knowledge bases](./img/knowledge_bases.png)

2. Click on *Create knowledge base* and enter the following information:

  [knowledge base - autonomous](./img/knowledge_base_autonomous.png)

  Make sure to select `Oracle AI Vector Search` as the data store type, and the connection that you created in Task 5.

> **Note**: after creating a knowledge base, and since the purpose of having used Autonomous Database is to have an updateable, searchable, in-real time vector database, we can now see one of the advantages of using Autonomous over Object Storage: after we upload some more data and vectorize it (can be automated), the knowledge base will be updated in real time, and will not require any additional human intervention, as the knowledge base only needs to know which retrieval function to use, and doesn't care how much data actually exists in the database.

## 2. Create an agent

1. Now, let's create an Agent in a similar fashion:

  ![new agent](./img/agents_autonomous.png)

2. Click on *Create agent* and enter the following information:

  [new_agent_autonomous](./img/new_agent_autonomous.png)

  Make sure to select the knowledge base that you just created. Make sure to select the *Automatically create an endpoint for this agent* option to avoid later having to manually setup the endpoint.

  > **Note**: you can customize the welcome message when interacting with the user through chat, as well as providing some additional instructions to the RAG agent for it to follow during generations.

In a few minutes, your agent will be ready to use!

## 3. Chat with your new agent

We can now access our agent's chat and start talking to it - and query about our data:

![chat_autonomous_1](./img/chat_autonomous_1.png)

The `traces` system will also retrieve the embeddings used for the responses (and their document IDs in the database), so you can verify the sources that contributed to the generated response by the agent:

![chat_autonomous_2](./img/chat_autonomous_2.png)

This can be applied to any domain: if you follow the instructions in this AI solution to process & upload your own data, you'll receive accurate responses from the agent (as well as some references so you can check the veracity of the model's responses).

## Demo

[Watch the demo here](https://www.youtube.com/watch?v=JqF6Bc9am4s&list=PLPIzp-E1msraY9To-BB-vVzPsK08s4tQD&index=15)

## Physical Architecture

![arch](./img/arch.PNG)

## Contributing

This project is open source. Please submit your contributions by forking this repository and submitting a pull request! Oracle appreciates any contributions that are made by the open source community.

## License

Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK.
