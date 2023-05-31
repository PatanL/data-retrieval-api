# Academic Search (Strucutred Data, Relational Database)

## Overview

This module is responsible for creating a relational database using Postgresql to store scholarly data from OpenAlex dataset and providing an API to access the database.

## Setup

Relational database:

1. [Download the data to your machine](https://docs.openalex.org/download-all-data/download-to-your-machine)
2. [Load the data to a relational database (PostgreSQL)](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database)
3. Insert the new data into partitioned tables
3. Reindex existing tables and create indexes on new tables. 

API: 

1. Install the required dependencies by running pip install -r requirements.txt.
2. Run the provided script to start the API server.
```
pip install -r requirements.txt 
```

3. Additionally, list any other setup required to run your module such as installing MySQL or downloading data files that you module relies on. 

4. Include instructions on how to run any tests you have written to verify your module is working properly. 

It is very important to also include an overall breakdown of your repo's file structure. Let people know what is in each directory and where to look if they need something specific. This will also let users know how your repo needs to structured so that your module can work properly

```
patrick-liu-academic-search/
    - requirements.txt
    - app.py 
    - scripts/
        -- create_partitioned_table.py
    - tests/
        -- functional/
            -- test_authors.py
            -- test_concepts.py
            -- test_group_by.py
            -- test_institutions.py
            -- test_sample.py
            -- test_sort.py
            -- test_sources.py
            -- test_works.py
```

Include text description of all the important files / componenets in your repo. 
* `src/create_train_data/`: fetches and pre-processes articles
* `src/train.py`: trains model from pre-processed data
* `src/classify_articles/`: runs trained model on input data
* `data/eval_artcles.csv`: articles to be classified (each row should include an 'id', and 'title')

### Important 
Go to [our shared google Drive space](https://drive.google.com/drive/folders/1rxPAdGTVcl-Xo6uuFovdKcCw5_FEaXIC?usp=sharing) and create a folder with the format `FirstnameLastName-Projectname` (e.g. `AshutoshUkey-KeywordTrie`). In here, make sure to include a zipped copy of any data files related to your module (including `.sql` dumps of necessary databases) as well as a backup zipped copy of your Github repo (i.e. all the files you upload to Github).



## Functional Design (Usage)
Describe all functions / classes that will be available to users of your module. This section should be oriented towards users who want to _apply_ your module! This means that you should **not** include internal functions that won't be useful to the user in this section. You can think of this section as a documentation for the functions of your package. Be sure to also include a short description of what task each function is responsible for if it is not apparent. You only need to provide the outline of what your function will input and output. You do not need to write the pseudo code of the body of the functions. 

### Get a single entity, based on an ID
To get a single entity object from from the API:/<entity_name>/<entity_id>. Here's an example:
Get the work with the OpenAlex ID W2741809807: http://hawk5.csl.illinois.edu:5000/works/W3127800895

#### Select fields
You can use select to choose top-level fields you want to see in a result.
Display id and display_name for a work.

http://hawk5.csl.illinois.edu:5000/works/W3127800895?select=id,display_name
```

{
    "display_name":"Impact of COVID-19 pandemic on mobility in ten countries and associated perceived risk for all transport modes",
    "id":"https://openalex.org/W3127800895"
}
```

### Get lists of entities

To get a list of entity objects from the API:`/<entity_name>`:
http://hawk5.csl.illinois.edu:5000/concepts.
This query returns a list of `Concept` objects.

<details>
  <summary>Paging</summary>
    Use the page query parameter to control which page of results you want (eg page=1, page=2, etc). By default there are 25 results per page; you can use the
    per-page parameter to change that to any number between 1 and 200.
    Get the 2nd page of a list:
    http://hawk5.csl.illinois.edu:5000/authors?page=2
    Get 200 results on the second page:
    http://hawk5.csl.illinois.edu:5000/authors?page=2&per-page=200
</details>

<details>
    <summary>Filter entity lists</summary>
Filters narrow the list down to just entities that meet a particular condition--specifically, a particular value for a particular attribute.
A list of filters are set using the filter parameter, formatted like this: filter=attribute:value,attribute2:value2. Examples: Get the authors whose name is John Smith:
http://hawk5.csl.illinois.edu:5000/authors?filter=display_name.search:einstein

Filters are case-insensitive.
    
    ### Logical expressions
    
    #### Inequality
    For numerical filters, use the less-than (<) and greater-than (>) symbols to filter by inequalities. Example:
    
    Get authors that have more than 10000 citations:
    http://hawk5.csl.illinois.edu:5000/authors?filter=cited_by_count:>10000
    
    Some attributes have special filters that act as syntactic sugar around commonly-expressed inequalities: for example, the from_publication_date filter on works. See the endpoint-specific documentation below for more information. Example:
    
    Get all works published after 2022-01-01 (inclusive):
    http://hawk5.csl.illinois.edu:5000/works?filter=from_publication_date:2022-01-01
    
    #### Negation (NOT)
    You can negate any filter, numerical or otherwise, by prepending the exclamation mark symbol (!) to the filter value. Example:
    Get all institutions except for ones located in the US:
    http://hawk5.csl.illinois.edu:5000/institutions?filter=country_code:!us``
    
    #### Intersection (AND)
    By default, the returned result set includes only records that satisfy all the supplied filters. In other words, filters are combined as an AND query. Example:
    Get all works that have been cited more than once and are free to read:
    http://hawk5.csl.illinois.edu:5000/works?filter=cited_by_count:>1
    Get all the works that have an author from France and an author from the UK:
    
    You can repeat a filter to create an AND query within a single attribute. Example:
    Get all works that have concepts "Medicine" and "Artificial Intelligence":
    
    
    #### Addition (OR)
    Use the pipe symbol (|) to input lists of values such that any of the values can be satisfied--in other words, when you separate filter values with a pipe, they'll be combined as an OR query. Example:
    Get all the works that have an author from France or an author from the UK:
    
    This is particularly useful when you want to retrieve a many records by ID all at once. Instead of making a whole bunch of singleton calls in a loop, you can make one call, like this:
    Get the works with DOI 10.1371/journal.pone.0266781 or with DOI 10.1371/journal.pone.0267149 (note the pipe separator between the two DOIs):
    http://hawk5.csl.illinois.edu:5000/works?filter=doi:https://doi.org/10.1371/journal.pone.0266781|https://doi.org/10.1371/journal.pone.0267149
    #### Available filters
</details>

<details>
  <summary>Search entities</summary>
    ### The search parameter
    
    The search query parameter finds results that match a given text search. Example:
    
    Get works with search term "dna" in the title or abstract:
    
    http://hawk5.csl.illinois.edu:5000/works?search=dna
    
    When you search works, the API looks for matches in titles, abstracts, and fulltext. When you search concepts, we look in each concept's display_name and
    description fields. When you search sources, we look at the display_name, alternate_titles, and abbreviated_title fields. Searching authors or institutions will looks for matches
    within each entities' display_name field.
</details>
    
<details>
  <summary>Sort entities</summary>
    ### Sort entity lists
    
    Use the ?sort parameter to specify the property you want your list sorted by. You can sort by these properties, where they exist:
    
    display_name
    
    cited_by_count
    
    works_count
    
    publication_date
    By default, sort direction is ascending. You can reverse this by appending :desc to the sort key like works_count:desc. You can sort by multiple properties by providing multiple sort keys, separated by commas. Examples:
    * All works, sorted by cited_by_count (highest counts first)
    http://hawk5.csl.illinois.edu:5000/works?sort=cited_by_count
    
    * All sources, in alphabetical order by title:
    http://hawk5.csl.illinois.edu:5000/works?sort=display_name
</details>



## Demo video
Make sure to include a video showing your module in action and how to use it in this section. Github Pages doesn't support this so I am unable to do this here. However, this can be done in your README.md files of your own repo. Follow instructions [here](https://stackoverflow.com/questions/4279611/how-to-embed-a-video-into-github-readme-md) of the accepted answer 


## Issues and Future Work

In this section, please list all know issues, limitations, and possible areas for future improvement. For example:

* Add multi-column indexes to improve query performance. 
* Update the schema of the database to reflect changes in the OpenAlex dataset. The previous version of the OpenAlex schema can be accessed at this link: https://gist.github.com/richard-orr/4c30f52cf5481ac68dc0b282f46f1905. The updated version of the OpenAlex schema is available at this link: https://github.com/ourresearch/openalex-documentation-scripts/blob/main/openalex-pg-schema.sql. 
* Another area of future work that I plan to explore is the use of n-grams for full-text search on works. N-grams are groups of sequential words that occur in the text of a work and can be used to enable full-text searches on the works that have them.



## Change log

Use this section to list the _major_ changes made to the module if this is not the first iteration of the module. Include an entry for each semester and name of person working on the module. For example 

Fall 2021 (Student 1)
* Week of 04/11/2022: added two new functions responsible for ...
* Week of 03/14/2022: fixed bug and added support for ...

Spring 2021 (Student 2)
...

Fall 2020 (Student 3)
...


## References 
include links related to datasets and papers describing any of the methodologies models you used. E.g. 

* OpenAlex Dataset: https://docs.openalex.org
