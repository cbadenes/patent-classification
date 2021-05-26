# patent-classification

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v3+-blue.svg)
![Python](https://img.shields.io/badge/python-v3+-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/cbadenes/patent-classification.svg)](https://github.com/cbadenes/patent-classification/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Basic Overview
Patent IPC class prediction and analysis


## Quick Start

1. Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
1. Clone this repo

	```
	git clone https://github.com/cbadenes/patent-classification.git
	```
1. Move into the root folder
	```
	cd patent-classification/
	```
1. Run the librAIry platform (the first time it may take a few minutes to download the Docker images)
    ````
    docker-compose up -d
    ````  
1. Create a virtual environment
    ```
    python -m venv custom-env
    ```
1. Activate the environment
    ```
    source custom-env/bin/activate
    ```
1. Install dependencies
    ```
    pip install -r requirements.txt
    ```
1. Download [XML patents](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/) (Patent Application Full Text Data (No Images)): 
    ````
    wget 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/ipg210105.zip'
    ````
1. Extract the ziped file: *.xml
    ````
    unzip ipg210105.zip
    ````
1. Parse Patents
    ```
    python parser.py ipg210105.xml
    ```  
1. Train a topic model based on the IPC sections (Docker-Hub credentials are required)
    ```
    python modeler.py
    ```  
1. Deploy the model as a web service
    ```
    docker run -p 8585:7777 --name model -e NLP_ENDPOINT=http://nlp/parse --network patent-classification_net cbadenes/uspto-ipc-sections:latest
    ```  
1. REST web api is available at: http://localhost:8585

## Local Resources

|               service                                                   |            description                                      |
|-------------------------------------------------------------------------|-------------------------------------------------------------|
|    [/nlp](http://localhost:8082/parse)                  				  |    NLP Tasks                                                |
|    [/repo](http://localhost:8983)                          			  |    SOLR repository                                          |
|    [/dashboard](http://localhost:8983/solr/banana/#/dashboard)          |    Banana dashboard                                         |
|    [/api](http://localhost:8081)                              		  |    librAIry API (credentials in `docker-compose.yml` file)  |
|    [/explorer](http://localhost:8080)                              	  |    librAIry Browser                                         |
|    [/model](http://localhost:8585)                                      |    International Patent Classification codes as Topic Model |

## Evaluation

1. Infers categories in documents not used during training and compares the results with those assigned manually
    ````
	python evaluator.py
	````
	A `results.jsonl` file will be created
1. Calculates precision, recall and f-measurement values from the results obtained
    ````
    python reporter.py
	````
	
## Results


| Strategy |  Sample | Precision |   Recall | F-Measure |
|----------|---------|-----------|----------|-----------|
|   Top1   |  1000   | 0.46      | 0.27     |   0.31    |
|   Top2   |  1000   | 0.33      | 0.62     |   0.39    |
|   Top3   |  1000   | 0.25      | 0.85     |   0.34    |
 