# Academic Search (Strucutred Data, Relational Database)

## Overview

This module is responsible for creating a relational database using Postgresql to store scholarly data from OpenAlex dataset and providing an API to access the database.

## Setup

1.  Connect to the Illinois VPN
2.  Go to http://hawk5.csl.illinois.edu:5000/api/docs/

It is very important to also include an overall breakdown of your repo's file structure. Let people know what is in each directory and where to look if they need something specific. This will also let users know how your repo needs to structured so that your module can work properly

```
patrick-liu-academic-search/
    - requirements.txt
    - app.py 
    - static/
        -- swagger.json
```

Include text description of all the important files / componenets in your repo. 
* `static/swagger.json`: json file that describes the strucutre of the swagger front end

### Important 
Go to [our shared google Drive space](https://drive.google.com/drive/folders/1rxPAdGTVcl-Xo6uuFovdKcCw5_FEaXIC?usp=sharing) and create a folder with the format `FirstnameLastName-Projectname` (e.g. `AshutoshUkey-KeywordTrie`). In here, make sure to include a zipped copy of any data files related to your module (including `.sql` dumps of necessary databases) as well as a backup zipped copy of your Github repo (i.e. all the files you upload to Github).



## Functional Design (Usage)
Describe all functions / classes that will be available to users of your module. This section should be oriented towards users who want to _apply_ your module! This means that you should **not** include internal functions that won't be useful to the user in this section. You can think of this section as a documentation for the functions of your package. Be sure to also include a short description of what task each function is responsible for if it is not apparent. You only need to provide the outline of what your function will input and output. You do not need to write the pseudo code of the body of the functions. 

### Get a single entity, based on an ID
To get a single entity object from from the API:
Go to the /<entity_name>/<entity_id> route. Thenn input a valid entity id. 


#### Select fields
You can use select to choose top-level fields you want to see in a result.
Go to the /<entity_name> route. Ex. /authors
Then input the fields you want to select in the "select" parameter. Ex. Fields to select (comma-separated): id,display_name

### Get lists of entities

To get a list of entity objects from the API: go to the `/<entity_name>` route.
Ex. /authors, then click "Try it out" and "Execute". 

<details>
  <summary>Paging</summary>
    Use the page query parameter to control which page of results you want (eg page=1, page=2, etc). By default there are 25 results per page; you can use the
    per-page parameter to change that to any number between 1 and 200.
    Get the 2nd page of a list:
    Find the "page" parameter and enter 2. 
    Get 200 results on the second page:
    Find the "per-page" parameter and enter 200.
</details>

<details>
    <summary>Filter entity lists</summary>
Filters narrow the list down to just entities that meet a particular condition--specifically, a particular value for a particular attribute.
A list of filters are set using the filter parameter, formatted like this: attribute:value,attribute2:value2                                                                            Examples: Get the authors whose name is John Smith:
Go to the /authors route. Then in the "filter" parameter, type "display_name:John Smith"

Filters are case-insensitive.
### Logical expressions

#### Inequality
For numerical filters, use the less-than (<) and greater-than (>) symbols to filter by inequalities. Example:

Get authors that have more than 10000 citations:
Go to the /authors route. Then in the "filter" parameter, type "cited_by_count:>10000"

Some attributes have special filters that act as syntactic sugar around commonly-expressed inequalities: for example, the from_publication_date filter on works. See the endpoint-specific documentation below for more information. Example:

Get all works published after 2022-01-01 (inclusive):
Go to the /works route. Then in the "filter parameter", type "from_publication_date:2022-01-01"

#### Negation (NOT)
You can negate any filter, numerical or otherwise, by prepending the exclamation mark symbol (!) to the filter value. Example:
Get all institutions except for ones located in the US:
Go to the /institutions route. Then in the "filter parameter", type "country_code:!us"

#### Intersection (AND)
By default, the returned result set includes only records that satisfy all the supplied filters. In other words, filters are combined as an AND query. Example:
Get all authors with a display name have are cited more than a number:
Go to the /authors route. Then in the "filter" parameter, type "cited_by_count:>100,display_name:Kevin Chen-Chuan Chang"


#### Addition (OR)
Use the pipe symbol (|) to input lists of values such that any of the values can be satisfied--in other words, when you separate filter values with a pipe, they'll be combined as an OR query. Example:
Get all the works that have an author from France or an author from the UK:

This is particularly useful when you want to retrieve a many records by ID all at once. Instead of making a whole bunch of singleton calls in a loop, you can make one call, like this:
Get the works with DOI 10.1371/journal.pone.0266781 or with DOI 10.1371/journal.pone.0267149 (note the pipe separator between the two DOIs):
Go to the /works route. Then in the "filter" parameter, type "doi:https://doi.org/10.1371/journal.pone.0266781|https://doi.org/10.1371/journal.pone.0267149"
    
</details>

<details>
  <summary>Search entities</summary>
### The search parameter

The search query parameter finds results that match a given text search. Example:

Get works with search term "dna" in the title or abstract:

Go to the /works route. Then in the "search" parameter, type "dna"

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
Go to the /works route. Then in the "sort" parameter, type "cited_by_count"

* All sources, in alphabetical order by title:
Go to the /works route, then in the "sort" parameter, type "display_name"
</details>



## Change log

## References 
include links related to datasets and papers describing any of the methodologies models you used. E.g. 

* OpenAlex Dataset: https://docs.openalex.org
