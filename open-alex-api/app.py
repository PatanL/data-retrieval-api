import psycopg2
import json
from flask import Flask, request, jsonify, Response
from sqlalchemy import text

app = Flask(__name__)

db_params = "params"

conn = psycopg2.connect(**db_params)

@app.route('/authors', methods=['GET'])
def get_authors():
    cur = conn.cursor()
    # Get arguments
    fields = request.args.get('select', default = "*", type = str)
    select_fields = fields.split(",")
    sample = request.args.get('sample', default = None, type = int)
    per_page = request.args.get('per-page', default = 25, type = int)
    page = request.args.get('page', default = 1, type = int)
    sort_param = request.args.get('sort', default = None, type = str)
    filter_param = request.args.get('filter')
    search_param = request.args.get('search')
    group_by_param = request.args.get('group_by')
    order_clause = ""
    if group_by_param is not None:
        cur.execute(f"SELECT {group_by_param}, COUNT(*) FROM openalex.authors_partition GROUP BY {group_by_param}")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                group_by_param : row[0],
                "count": row[1]
            })
        return jsonify(result)
    if sort_param is not None:
        # Sort
        '''
        You also can sort results with the sort parameter:
        Sort authors by cited by count, descending
        https://api.openalex.org/authors?sort=cited_by_count:desc
        '''
        attribute, order = sort_param.split(":")
        order_clause = "ORDER BY " + attribute + " " + order
    where_clause = "WHERE "
    if filter_param is not None:
        # Intersection (AND)
        # Split by comma to get multiple filters
     
        filters = filter_param.split(',')
        print("filters", filters)
        for filter in filters:
            attr, value = filter.split(':', maxsplit=1)
            # Inequality 
            if value.startswith('<') or value.startswith('>'): 
                where_clause += f"{attr} {value} AND "
            # Negation
            elif value.startswith('!'):
                where_clause += f"{attr} != '{value[1:]}' AND "
            # Addition
            elif '|' in value:
                values = value.split('|')
                where_clause += "("
                for val in values:
                    where_clause += f"{attr} = '{val}' OR "
                # Remove the last OR
                where_clause = where_clause[:-4]
                where_clause += ") AND "
            # If the attribute is a convenience filter, translate it to the appropriate attribute
            elif attr == 'has_orcid':
                if(value.lower() == 'true'):
                    attr = 'orcid IS NOT NULL'
                    where_clause += f"{attr} AND "
                elif(value.lower() == 'false'):
                    attr = 'orcid IS NULL'
                    where_clause += f"{attr} AND "
                else:
                    return jsonify(error="Invalid filter value"), 400
            # TO DO, figure out how to deal with this
            elif 'last_known_insitution' in attr:
                column = attr.split('.')[1]
                #join with institutions table
                query = f"""
                    SELECT {fields} FROM openalex.authors_partition
                    JOIN openalex.institutions
                    ON authors_partition.last_known_institution_id = institutions.id
                    WHERE institutions.{column} = '{value}'
                    LIMIT {per_page} OFFSET {(page - 1) * per_page}
                """
                where_clause += f"insitutions.{column} = '{value}' AND "
            elif attr == 'display_name.search':
                where_clause += f"display_name ILIKE '%{value}%' AND "
            elif attr == 'display_name':
                where_clause += f"md5(display_name) = md5('{value}') AND "
            # Default
            else:
                where_clause += f"{attr} = '{value}' AND "
        # Remove the last AND
        where_clause = where_clause[:-4]
        print("where_clause:", where_clause)
        if where_clause == "WHERE ":
            where_clause = ""
    elif search_param is not None:
        if where_clause != "WHERE ":
            where_clause += f"AND display_name ILIKE '%{search_param}%'"
        else:
            where_clause += f"display_name ILIKE '%{search_param}%'"
    if where_clause == "WHERE ":
        where_clause = ""
 
    if sample is None:
        #rewrite query to use order by clause
        query = f"""
            SELECT {fields} FROM openalex.authors_partition
            {where_clause}
            {order_clause}
            LIMIT {per_page} OFFSET {(page - 1) * per_page}
        """
    else:
        if sample < per_page:
            per_page = sample
        query = f"""
            SELECT {fields} FROM openalex.authors_partition
            TABLESAMPLE SYSTEM ({sample})
            {where_clause}
            {order_clause}
            LIMIT {per_page} OFFSET {(page - 1) * per_page}
        """
    print("query:", query)
    cur.execute(query)
    result = cur.fetchall()
    authors = []
    if fields == "*":
        for row in result:
            print(row)
            authors.append({
                "id": row[0],
                "orcid": row[1],
                "display_name" : row[2],
                "display_name_alternatives": row[3],
                "works_count": row[4],
                "cited_by_count": row[5],
                "last_known_institution" : row[6],
                "works_api_url": row[7],
                "updated_date": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] is not None else None
            })
    else:
        for row in result:
            for i in range(len(select_fields)):
                authors.append({
                    select_fields[i]: row[i]
                })
    cur.close()
    return jsonify(authors)

@app.route('/authors/', methods=['GET'])
@app.route('/authors/<entity_id>', methods=['GET'])
def get_author(entity_id):
    cur = conn.cursor()
    fields = request.args.get('select', default = "*", type = str)
    select_fields = fields.split(",")

    # retrieve data from authors table
    main_query = f"""
        SELECT {fields}
        FROM openalex.authors_partition
        WHERE id = 'https://openalex.org/{entity_id}'
    """
    cur.execute(main_query)
    result = cur.fetchone()
    if entity_id is None:
        return jsonify(error="Author not found"), 404
    
    if fields == "*":
        query = f"""
            SELECT id, ror, display_name, country_code, type 
            FROM openalex.institutions
            WHERE id = '{result[6]}'
        """
        last_known_institution = cur.execute(query)
        last_known_institution_result = cur.fetchone()
        last_known_institution = {
            "id": last_known_institution_result[0],
            "ror": last_known_institution_result[1],
            "display_name": last_known_institution_result[2],
            "country_code": last_known_institution_result[3],
            "type": last_known_institution_result[4]
        }
        authors = {
            "id": result[0],
            "orcid": result[1],
            "display_name" : result[2],
            "display_name_alternatives": result[3],
            "works_count": result[4],
            "cited_by_count": result[5],
            "last_known_institution" : last_known_institution,
            "works_api_url": result[7],
            "updated_date": result[8].strftime("%Y-%m-%d %H:%M:%S") if result[8] is not None else None
        }
    else:
        authors = {}
        for i in range(len(select_fields)):
            if select_fields[i] == "updated_date":
                authors[select_fields[i]] = result[i].strftime("%Y-%m-%d %H:%M:%S") if result[i] is not None else None
            elif(select_fields[i] == "last_known_institution"):
                query = f"""
                    SELECT id, ror, display_name, country_code, type 
                    FROM openalex.institutions
                    WHERE id = '{result[i]}'
                """
                last_known_institution = cur.execute(query)
                last_known_institution_result = cur.fetchone()
                last_known_institution = {
                    "id": last_known_institution_result[0],
                    "ror": last_known_institution_result[1],
                    "display_name": last_known_institution_result[2],
                    "country_code": last_known_institution_result[3],
                    "type": last_known_institution_result[4]
                }
                authors[select_fields[i]] = last_known_institution
            else:
                authors[select_fields[i]] = result[i]

    if result is None:
        return jsonify(error="Author not found"), 404
    
    cur.close()
    return jsonify(authors)                       
@app.route('/concepts/<entity_id>', methods=['GET'])
def get_concept(entity_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM openalex.concepts WHERE id = %s", ("https://openalex.org/" + entity_id,))
    result = cur.fetchone()
    concepts = {
        "id": result[0],
        "wikidata": result[1],
        "display_name": result[2],
        "level": result[3],
        "description": result[4],
        "works_count": result[5],
        "cited_by_count": result[6],
        "image_url": result[7],
        "image_thumbnail_url": result[8],
        "works_api_url": result[9],
        "updated_date": result[10].strftime("%Y-%m-%d %H:%M:%S") if result[10] is not None else None
    }

    if result is None:
        return jsonify(error="Concept not found"), 404
    # Retrieve ancestors from openalex.concepts_ancestors table
    cur.execute("SELECT ancestor_id FROM openalex.concepts_ancestors WHERE concept_id=%s", ("https://openalex.org/" + entity_id,))
    ancestor_concepts = [row[0] for row in cur.fetchall()]
    concepts["concepts_ancestors"] = ancestor_concepts

    # Retrieve related concepts from openalex.concepts_related_concepts table
    cur.execute("SELECT related_concept_id, score FROM openalex.concepts_related_concepts WHERE concept_id=%s", ("https://openalex.org/" + entity_id,))
    related_concepts = []
    for row in cur.fetchall():
        related_concepts.append({
            "id": row[0],
            "score": row[1]
        })
    concepts["related_concepts"] = related_concepts

    # Retrieve counts by year from openalex.concepts_counts_by_year table
    cur.execute("SELECT year, works_count, cited_by_count FROM openalex.concepts_counts_by_year WHERE concept_id=%s", ("https://openalex.org/" + entity_id,))
    counts_by_year = []
    for row in cur.fetchall():
        counts_by_year.append({
            "year": row[0],
            "works_count": row[1],
            "cited_by_count": row[2]
        })
    concepts["counts_by_year"] = counts_by_year

    # Retrieve concept ids from openalex.concepts_ids table
    cur.execute("SELECT openalex, wikidata, wikipedia, umls_aui, umls_cui, mag FROM openalex.concepts_ids WHERE concept_id=%s", ("https://openalex.org/" + entity_id,))
    ids = cur.fetchone()
    concept_ids = {
        "openalex": ids[0],
        "wikidata": ids[1],
        "wikipedia": ids[2],
        "umls_aui": ids[3],
        "umls_cui": ids[4],
        "mag": ids[5]
    }
    concepts["concept_ids"] = concept_ids
    

    # Combine all the data into a single dictionary

    return jsonify(concepts)
@app.route('/works/<work_id>', methods=['GET'])
def get_work(work_id):
    cur = conn.cursor()
    fields = request.args.get('select')
    select_fields = fields.split(",") if fields is not None else None
    query = f"""
    SELECT id, doi, title, display_name, publication_year, publication_date, type, cited_by_count, is_retracted, is_paratext, cited_by_api_url, abstract_inverted_index
    FROM openalex.works_partition_id
    WHERE id = 'https://openalex.org/{work_id}'
    """
    cur.execute(query)
    row = cur.fetchone()
    work = {
        "id": row[0],
        "doi": row[1],
        "title": row[2],
        "display_name": row[3],
        "publication_year": row[4],
        "publication_date": row[5],
        "type": row[6],
        "cited_by_count": row[7],
        "is_retracted": row[8],
        "is_paratext": row[9],
        "cited_by_api_url": row[10],
        "abstract_inverted_index": row[11]
    }
    # print("work:", work)
    if row is None:
        return jsonify(error="Work not found"), 404
    # Retrieve alternate host venues from openalex.works_alternate_host_venues table
    cur.execute("SELECT venue_id, url, is_oa, version, license FROM openalex.works_alternate_host_venues_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    alternate_host_venues = []
    for row in cur.fetchall():
        alternate_host_venues.append({
            "venue_id": row[0],
            "url": row[1],
            "is_oa": row[2],
            "version": row[3],
            "license": row[4]
        })
    work["alternate_host_venues"] = alternate_host_venues
    # Retrieve authors from openalex.works_authorships table
    cur.execute("SELECT author_position, author_id, institution_id, raw_affiliation_string FROM openalex.works_authorships_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    authorships = []
    for row in cur.fetchall():
        authorships.append({
            "author_position": row[0],
            "author_id": row[1],
            "institution_id": row[2],
            "raw_affiliation_string": row[3]
        })
    work["authorships"] = authorships
    # Retrieve bibliographic data from openalex.work_biblio table
    cur.execute("SELECT volume, issue, first_page,  last_page FROM openalex.works_biblio_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    biblio = cur.fetchone()
    work["biblio"] = {
        "volume": biblio[0],
        "issue": biblio[1],
        "first_page": biblio[2],
        "last_page": biblio[3]
    }
    # Retrieve concepts from openalex.works_concepts table
    cur.execute("SELECT concept_id, score FROM openalex.works_concepts_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    concepts = []
    for row in cur.fetchall():
        concepts.append({
            "id": row[0],
            "score": row[1]
        })
    work["concepts"] = concepts
    # Retrieve host venues from openalex.works_host_venues table
    cur.execute("SELECT venue_id, url, is_oa, version, license FROM openalex.works_host_venues_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    host_venues = []
    for row in cur.fetchall():
        host_venues.append({
            "venue_id": row[0],
            "url": row[1],
            "is_oa": row[2],
            "version": row[3],
            "license": row[4]
        })
    work["host_venues"] = host_venues
    # print("work:", work)
    # Retrieve ids from openalex.works_ids table
    cur.execute("SELECT openalex, doi, mag, pmid, pmcid FROM openalex.works_ids_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    ids = cur.fetchone()
    work_ids = {
        "openalex": ids[0],
        "doi": ids[1],
        "mag": ids[2],
        "pmid": ids[3],
        "pmcid": ids[4]
    }
    work["work_ids"] = work_ids
    # Retrieve mesh terms from openalex.works_mesh table
    cur.execute("SELECT descriptor_ui, descriptor_name, qualifier_ui, qualifier_name, is_major_topic FROM openalex.works_mesh_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    mesh = []
    for row in cur.fetchall():
        mesh.append({
            "descriptor_ui": row[0],
            "descriptor_name": row[1],
            "qualifier_ui": row[2],
            "qualifier_name": row[3],
            "is_major_topic": row[4]
        })
    work["mesh"] = mesh
    # Retrieve is open access from openalex.works_open_access table
    cur.execute("SELECT is_oa, oa_status, oa_url FROM openalex.works_open_access_partition WHERE work_id=%s", ("https://openalex.org/" + work_id,))
    oa = cur.fetchone()
    work["open_access"] = {
        "is_oa": oa[0],
        "oa_status": oa[1],
        "oa_url": oa[2]
    }
    response = {}
    if fields is not None:
        for field in select_fields:
            if field in work:
                response[field] = work[field]
            else:
                return jsonify({"error":"Invalid query parameters error.","message":field + " is not a valid select field. Valid fields for select are: id, doi, title, display_name, relevance_score, publication_year, publication_date, ids, language, primary_location, type, open_access, authorships, corresponding_author_ids, corresponding_institution_ids, apc_payment, is_authors_truncated, cited_by_count, biblio, is_retracted, is_paratext, concepts, mesh, locations_count, locations, best_oa_location, grants, referenced_works, related_works, ngrams_url, abstract_inverted_index, cited_by_api_url, counts_by_year, updated_date, created_date."}), 400
        return jsonify(response)
    response = jsonify(work)
   
    return response
@app.route('/works', methods=['GET'])
def get_works():
    cur = conn.cursor()
    # Get arguments
    fields = request.args.get('select', default = "*", type = str)
    select_fields = fields.split(',')
    sample = request.args.get('sample', default=None, type=int)
    per_page = request.args.get('per-page', default=25, type=int)
    page = request.args.get('page', default=1, type=int)
    sort_param = request.args.get('sort')
    filter_param = request.args.get('filter')
    search_param = request.args.get('search')
    group_by_param = request.args.get('group_by')

    if group_by_param is not None:
        query = f"SELECT {group_by_param}, COUNT(*) FROM openalex.works_part_5 GROUP BY {group_by_param}"
        cur.execute(query)
        result = cur.fetchall()
        works = []
        for row in result:
            works.append({
                "id": row[0],
                "count": row[1]
            })
        return jsonify(works)
    where_clause = "WHERE "
    if filter_param is not None:
        # Split by comma
        filters = filter_param.split(',')
        for filter in filters:
            attr, value = filter.split(':', maxsplit=1)
            # Inequality 
            if value.startswith('<') or value.startswith('>'): 
                where_clause += f"w.{attr} {value} AND "
            # Negation
            elif value.startswith('!'):
                where_clause += f"w.{attr} != '{value[1:]}' AND "
            # Addition
            elif '|' in value:
                values = value.split('|')
                where_clause += "("
                for val in values:
                    where_clause += f"w.{attr} = '{val}' OR "
                # Remove the last OR
                where_clause = where_clause[:-4]
                where_clause += ") AND "
            elif 'authorships' in attr:
                # author_id and institution_id
                column = attr.split('.')[1]
                where_clause += f"wa.{column} = '{value}' AND "
            elif 'ids' in attr:
                column = attr.split('.')[1]
                where_clause += f"wi.{column} = '{value}' AND "
            elif attr == 'locations.venue_id':
                column = attr.split('.')[1]
                where_clause += f"wahv.{column} = '{value}' AND "
            elif attr == 'primary_location.venue_id':
                column = attr.split('.')[1]
                where_clause += f"whv.{column} = '{value}' AND "

            # If the attribute is a convenience filter, translate it to the correct column
            elif attr == 'abstract.search':
                # if value is "artificial intelligence" then the where clause would be WHERE abstract_inverted_index @> '{"artificial": [], "intelligence": []}'
                words = value.split(" ")
                where_clause += "abstract_inverted_index @> '{"
                for word in words:
                    where_clause += f'"{word}": [],'
                where_clause = where_clause[:-1]
            elif attr == 'display_name.search' or attr == 'title.search':
                where_clause += f"display_name ILIKE '%{value}%' AND "
            elif attr == 'authors_count':
                if value.startswith('<') or value.startswith('>'):
                    where_clause += f"authors_count {value} AND "
                else:
                    where_clause += f"authors_count = {value} AND "
                query = f"""
                SELECT w.id, COUNT(wa.author_id) AS authors_count
                FROM openalex.works_partition_id w
                JOIN openalex.works_authorships_partition wa ON w.id = wa.work_id
                GROUP BY w.id
                HAVING COUNT(wa.author_id) > 5;
                """
                cur.execute(query)
                result = cur.fetchall()
                works = []
                for row in result:
                    works.append({
                        "id": row[0],
                        "authors_count": row[1]
                    })
                    return jsonify(works)
            elif attr == 'from_publication_date':
                where_clause += f"publication_date >= '{value}' AND "
            elif attr == 'has_abstract':
                if value.lower() == 'true':
                    attr = 'abstract_inverted_index IS NOT NULL'
                    where_clause += f"{attr} AND "
                elif value.lower() == 'false':
                    attr = 'abstract_inverted_index IS NULL'
                    where_clause += f"{attr} AND "
                else:
                    return jsonify(error="Invalid filter value"), 400
            elif attr == 'has_doi':
                if value.lower() == 'true':
                    attr = 'w.doi IS NOT NULL'
                    where_clause += f"{attr} AND "
                elif value.lower() == 'false':
                    attr = 'w.doi IS NULL'
                    where_clause += f"{attr} AND "
                else:
                    return jsonify(error="Invalid filter value"), 400
            elif attr == 'has_oa':
                if value.lower() == 'true':
                    attr = 'wahv.is_oa is TRUE'
                    where_clause += f"{attr} AND "
                elif value.lower() == 'false':
                    attr = 'wahv.is_oa is FALSE'
                    where_clause += f"{attr} AND "
                else:
                    return jsonify(error="Invalid filter value"), 400
            elif attr == 'to_publication_date':
                where_clause += f"publication_date <= '{value}' AND "
            # Default
            else:
                where_clause += f"w.{attr} = '{value}' AND " 
        # Remove the last AND
        where_clause = where_clause[:-4]
        print("where_clause:", where_clause)
        if where_clause == "WHERE ":
            where_clause = ""
    elif search_param is not None:
        if where_clause != "WHERE ":
            where_clause += f"AND display_name ILIKE '%{search_param}%'"
        else:
            where_clause += f"display_name ILIKE '%{search_param}%'"
    order_clause = ""
    if sort_param is not None:
        order_clause = "ORDER BY " + sort_param
    print("order_clause:", order_clause)
    if where_clause == "WHERE ":
        where_clause = ""
    query = get_works_query(where_clause, order_clause, per_page, page, sample)
    cur.execute(query)
    rows = cur.fetchall()
    works = []
    responses = []
    for row in rows:
        works.append({
            "id": row[0],
            "doi": row[1],
            "title": row[2],
            "display_name": row[3],
            "publication_year": row[4],
            "publication_date": row[5],
            "type": row[6],
            "cited_by_count": row[7],
            "is_retracted": row[8],
            "is_paratext": row[9],
            "cited_by_api_url": row[10],
            "alternate_host_venues": {
                "work_id": row[11],
                "venue_id": row[12],
                "url": row[13],
                "is_oa": row[14],
                "version": row[15],
                "license": row[16]
            },
            "authorships": {
                "work_id": row[17],
                "author_position": row[18],
                "author_id": row[19],
                "institution_id": row[20],
                "raw_affiliation_string": row[21]
            },
            "biblio": {
                "work_id": row[22],
                "volume": row[23],
                "issue": row[24],
                "first_page": row[25],
                "last_page": row[26]
            },
            "host_venues": {
                "work_id": row[27],
                "venue_id": row[28],
                "url": row[29],
                "is_oa": row[30],
                "version": row[31],
                "license": row[32]
            },
            "ids": {
                "work_id": row[33],
                "openalex": row[34],
                "doi": row[35],
                "mag": row[36],
                "pmid": row[37],
                "pmcid": row[38]
            },
            "open_access": {
                "work_id": row[39],
                "is_oa": row[40],
                "oa_status": row[41],
                "oa_url": row[42]
            }
        })
        response = {}
        if fields != "*":
            print("select_fields:", select_fields)
            for field in select_fields:
                if field in works[-1]:
                    response[field] = works[-1][field]
                else:
                    return jsonify({"error":"Invalid query parameters error.","message":field + " is not a valid select field. Valid fields for select are: id, doi, title, display_name, relevance_score, publication_year, publication_date, ids, language, primary_location, type, open_access, authorships, corresponding_author_ids, corresponding_institution_ids, apc_payment, is_authors_truncated, cited_by_count, biblio, is_retracted, is_paratext, concepts, mesh, locations_count, locations, best_oa_location, grants, referenced_works, related_works, ngrams_url, abstract_inverted_index, cited_by_api_url, counts_by_year, updated_date, created_date."}), 400
        responses.append(response)
    if fields != "*":
        return jsonify(responses)
    return jsonify(works)
    
    
def get_works_query(where_clause='', order_clause = '', per_page=25, page=1, sample=None):
    with conn.cursor() as cur:
        if sample is None:
            query = f"""
                SELECT w.id, w.doi, w.title, w.display_name, w.publication_year, w.publication_date, w.type, w.cited_by_count,
                    w.is_retracted, w.is_paratext, w.cited_by_api_url, wahv.*, wa.*, wb.*, whv.*, wi.*, woa.*
                FROM openalex.works_partition_id w
                LEFT JOIN openalex.works_alternate_host_venues_partition wahv ON w.id = wahv.work_id
                LEFT JOIN openalex.works_authorships_partition wa ON w.id = wa.work_id
                LEFT JOIN openalex.works_biblio_partition wb ON w.id = wb.work_id
                LEFT JOIN openalex.works_host_venues_partition whv ON w.id = whv.work_id
                LEFT JOIN openalex.works_ids_partition wi ON w.id = wi.work_id
                LEFT JOIN openalex.works_open_access_partition woa ON w.id = woa.work_id
                {where_clause}
                {order_clause}
                LIMIT {per_page} OFFSET {(page - 1) * per_page}
            """
        else:
            if sample < per_page:
                per_page = sample
            query = f"""
            SELECT w.id, w.doi, w.title, w.display_name, w.publication_year, w.publication_date, w.type, w.cited_by_count,
                    w.is_retracted, w.is_paratext, w.cited_by_api_url, wahv.*, wa.*, wb.*, whv.*, wi.*, woa.*
                FROM openalex.works_partition_id w
                LEFT JOIN openalex.works_alternate_host_venues_partition wahv ON w.id = wahv.work_id
                LEFT JOIN openalex.works_authorships_partition wa ON w.id = wa.work_id
                LEFT JOIN openalex.works_biblio_partition wb ON w.id = wb.work_id
                LEFT JOIN openalex.works_host_venues_partition whv ON w.id = whv.work_id
                LEFT JOIN openalex.works_ids_partition wi ON w.id = wi.work_id
                LEFT JOIN openalex.works_open_access_partition woa ON w.id = woa.work_id
                TABLESAMPLE SYSTEM ({sample})
                {where_clause}
                ORDER BY RANDOM()
                LIMIT {sample};
            """

    print("query:", query)
    return query
    

@app.route('/institutions/<institution_id>', methods=['GET'])
def get_institution(institution_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM openalex.institutions WHERE id=%s", ("https://openalex.org/" + institution_id,))
    institution = cur.fetchone()
    if institution is None:
        return jsonify({}), 404
    institution = {
        "id": institution[0],
        "ror": institution[1],
        "display_name": institution[2],
        "country_code": institution[3],
        "type": institution[4],
        "homepage_url": institution[5],
        "image_url": institution[6],
        "image_thumbnail_url": institution[7],
        "display_name_acroynyms": institution[8],
        "display_name_alternatives": institution[9],
        "works_count": institution[10],
        "cited_by_count": institution[11],
        "works_api_url": institution[12],
        "updated_date": institution[13]
    }
    # Retrieve associated institutions from openalex.institutions_associated_institutions table
    cur.execute("SELECT associated_institution_id, relationship FROM openalex.institutions_associated_institutions WHERE institution_id=%s", ("https://openalex.org/" + institution_id,))
    associated_institutions = []
    for row in cur.fetchall():
        associated_institutions.append({
            "associated_institution_id": row[0],
            "relationship": row[1]
        })
    institution["associated_institutions"] = associated_institutions
    # Retrieve geo from openalex.institutions_geo table
    cur.execute("SELECT city, geonames_city_id, region, country_code, country, latitude, longitude FROM openalex.institutions_geo WHERE institution_id=%s", ("https://openalex.org/" + institution_id,))
    geo = cur.fetchone()
    institution["geo"] = {
        "city": geo[0],
        "geonames_city_id": geo[1],
        "region": geo[2],
        "country_code": geo[3],
        "country": geo[4],
        "latitude": geo[5],
        "longitude": geo[6]
    }
    # Retrieve ids from openalex.institutions_ids table
    cur.execute("SELECT openalex, ror, grid, wikipedia, wikidata, mag FROM openalex.institutions_ids WHERE institution_id=%s", ("https://openalex.org/" + institution_id,))
    ids = cur.fetchone()
    institution["ids"] = {
        "openalex": ids[0],
        "ror": ids[1],
        "grid": ids[2],
        "wikipedia": ids[3],
        "wikidata": ids[4],
        "mag": ids[5]
    }
    # Retrieve works counts by year from openalex.institutions_counts_by_year table
    cur.execute("SELECT year, works_count, cited_by_count FROM openalex.institutions_counts_by_year WHERE institution_id=%s", ("https://openalex.org/" + institution_id,))
    counts_by_year = []
    for row in cur.fetchall():
        counts_by_year.append({
            "year": row[0],
            "works_count": row[1],
            "cited_by_count": row[2]
        })
    institution["counts_by_year"] = counts_by_year
    cur.close()
    return jsonify(institution)

def get_institutions_query(where_clause='', order_clause = '', per_page=25, page=1, sample=None):
    with conn.cursor() as cur:
        query = f"""
            SELECT i.id, i.ror, i.display_name, i.country_code, i.type, i.homepage_url, i.image_url, 
                    i.image_thumbnail_url, i.works_count, 
                    i.cited_by_count, works_api_url, i.updated_date,
                COALESCE(ARRAY_AGG(DISTINCT iai.associated_institution_id), '{{}}') AS associated_institution_ids,
                JSON_AGG(DISTINCT
                 (SELECT x FROM (SELECT ic.year, ic.works_count, ic.cited_by_count) x)) AS years,
                JSON_AGG(DISTINCT (SELECT x FROM (SELECT ig.city, ig.geonames_city_id, ig.region, ig.country_code, ig.country, ig.latitude, ig.longitude) x)) AS geo,
                JSON_AGG(DISTINCT (SELECT x FROM (SELECT iid.openalex, iid.wikipedia, iid.wikidata, iid.mag) x)) AS ids
            FROM openalex.institutions i
            LEFT JOIN openalex.institutions_associated_institutions iai ON i.id = iai.institution_id
            LEFT JOIN openalex.institutions_counts_by_year ic ON i.id = ic.institution_id
            LEFT JOIN openalex.institutions_geo ig ON i.id = ig.institution_id
            LEFT JOIN openalex.institutions_ids iid ON i.id = iid.institution_id
            {where_clause}
            GROUP BY i.id, i.ror, i.display_name, i.country_code, i.type, i.homepage_url, i.image_url,
                    i.image_thumbnail_url, i.works_count,
                    i.cited_by_count, works_api_url, i.updated_date
            {order_clause}
            LIMIT {per_page} OFFSET {(page - 1) * per_page};
        """
        print("query:", query)
        cur.execute(query)
        rows = cur.fetchall()
    institutions = []
    for row in rows:
        institutions.append({
            "id": row[0],
            "ror": row[1],
            "display_name": row[2],
            "country_code": row[3],
            "type": row[4],
            "homepage_url": row[5],
            "image_url": row[6],
            "image_thumbnail_url": row[7],
            "works_count": row[8],
            "cited_by_count": row[9],
            "works_api_url": row[10],
            "updated_date": row[11],
            "associated_institutions": row[12],
            "counts_by_years": row[13],
            "geo": row[14],
            "ids": row[15]
        })
    return jsonify(institutions)



def get_concepts_query(where_clause='', order_clause='', per_page=25, page=1, sample=None):
    with conn.cursor() as cur:
        if sample is None:
            query = f"""
                SELECT c.id, c.level, c.description, c.wikidata,
                    c.image_url, c.image_thumbnail_url, c.works_api_url, c.updated_date,
                    COALESCE(SUM(cc.works_count), 0) AS works_count,
                    COALESCE(SUM(cc.cited_by_count), 0) AS cited_by_count,
                    ARRAY_AGG(DISTINCT ac.ancestor_id) AS ancestors,
                    ARRAY_AGG(DISTINCT rc.related_concept_id) AS related_concepts
                FROM openalex.concepts c
                LEFT JOIN openalex.concepts_counts_by_year cc
                    ON c.id = cc.concept_id
                LEFT JOIN openalex.concepts_ancestors ac
                    ON c.id = ac.concept_id
                LEFT JOIN openalex.concepts_related_concepts rc
                    ON c.id = rc.concept_id
                {where_clause}
                GROUP BY c.id, c.level, c.description, c.wikidata,
                        c.image_url, c.image_thumbnail_url, c.works_api_url, c.updated_date
                {order_clause}
                LIMIT {per_page} OFFSET {(page - 1) * per_page};
            """
        else:
            if sample < per_page:
                sample = per_page
            query = f"""
                SELECT c.id, c.level, c.description, c.wikidata,
                    c.image_url, c.image_thumbnail_url, c.works_api_url, c.updated_date,
                    COALESCE(SUM(cc.works_count), 0) AS works_count,
                    COALESCE(SUM(cc.cited_by_count), 0) AS cited_by_count,
                    ARRAY_AGG(DISTINCT ac.ancestor_id) AS ancestors,
                    ARRAY_AGG(DISTINCT rc.related_concept_id) AS related_concepts
                FROM openalex.concepts c
                LEFT JOIN openalex.concepts_counts_by_year cc
                    ON c.id = cc.concept_id
                LEFT JOIN openalex.concepts_ancestors ac
                    ON c.id = ac.concept_id
                LEFT JOIN openalex.concepts_related_concepts rc
                    ON c.id = rc.concept_id
                {where_clause}
                GROUP BY c.id, c.level, c.description, c.wikidata,
                        c.image_url, c.image_thumbnail_url, c.works_api_url, c.updated_date
                ORDER BY RANDOM()
                LIMIT {sample};
            """
        print("query:", query)
        cur.execute(query)
        results = cur.fetchall()
    concepts = []
    for result in results:
        ancestors = result[10] if result[10] is not None else []
        related_concepts = result[11] if result[11] is not None else []
        concept = {
                "id": result[0],
                "level": result[1],
                "description": result[2],
                "wikidata": result[3],
                "image_url": result[4],
                "image_thumbnail_url": result[5],
                "works_api_url": result[6],
                "updated_date": result[7].strftime("%Y-%m-%d %H:%M:%S") if result[7] is not None else None,
                "works_count": result[8],
                "cited_by_count": result[9],
                "ancestors": ancestors,
                "related_concepts": related_concepts
            }
        concepts.append(concept)

    return jsonify(concepts)
@app.route('/concepts')
def get_concepts():
    cur = conn.cursor()
    where_clause = ''
    fields = request.args.get('select', default = "*", type = str)
    select_fields = fields.split(",")
    sample = request.args.get('sample', default = None, type = int)
    per_page = request.args.get('per-page', default = 25, type = int)
    page = request.args.get('page', default = 1, type = int)
    sort_param = request.args.get('sort', default = None, type = str)
    filter_param = request.args.get('filter')
    search_param = request.args.get('search')
    group_by_param = request.args.get('group_by')
    where_clause = "WHERE "
    if filter_param is not None:
        # Split by comma
        filters = filter_param.split(',')
        for filter in filters:
            # Split the filter string into attribute and value
            attr, value = filter_param.split(':', maxsplit=1)
            # Inequality 
            if value.startswith('<') or value.startswith('>'): 
                where_clause += f"w.{attr} {value} AND "
            # Negation
            elif value.startswith('!'):
                where_clause += f"w.{attr} != '{value[1:]}' AND "
            # Addition
            elif '|' in value:
                values = value.split('|')
                where_clause += "("
                for val in values:
                    where_clause += f"w.{attr} = '{val}' OR "
                # Remove the last OR
                where_clause = where_clause[:-4]
                where_clause += ") AND "
            # If the attribute is a convenience filter, translate it to the appropriate attribute
            if attr == 'has_wikidata':
                attr = 'wikidata IS NOT NULL'
                where_clause += f"WHERE {attr} = '{value}' AND "
            elif attr == 'display_name.search':
                where_clause += f"WHERE display_name ILIKE '%%{value}%%' AND "
                return get_concepts_query(where_clause)
            # Build the WHERE clause using the attribute and value
            else:
                where_clause += f"{attr} = '{value}' AND " 
        # Remove the last AND
        where_clause = where_clause[:-4]
        print("where_clause:", where_clause) 
    if where_clause == "WHERE ":
        where_clause = ""
    if search_param is not None:
        if where_clause:
            where_clause += f" AND display_name ILIKE '%%{search_param}%%'"
        else:
            where_clause = f"WHERE display_name ILIKE '%%{search_param}%%'"
    if group_by_param:
        # if group_by_param not in ['cited_by_count', 'continent', 'country_code', 'is_global_south', 'has_ror', 'type', 'works_count']:
        #     return jsonify({"error": "Invalid group_by parameter"}), 400
        cur.execute(f"SELECT {group_by_param}, COUNT(*) FROM openalex.concepts GROUP BY {group_by_param} ORDER BY {group_by_param} ASC")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({group_by_param: row[0], "count": row[1]})
        return jsonify(result)
    order_clause = ''
    if sort_param:
        if sort_param not in ['works_count', 'cited_by_count']:
            return jsonify({"error": "Invalid sort parameter"}), 400
        order_clause = f"ORDER BY {sort_param} DESC"
    return get_concepts_query(where_clause, order_clause, per_page, page, sample)

@app.route('/institutions', methods=['GET'])
def get_institutions():
    cur = conn.cursor()
    fields = request.args.get('select', default = "*", type = str)
    select_fields = fields.split(",")
    sample = request.args.get('sample', default = None, type = int)
    per_page = request.args.get('per-page', default = 25, type = int)
    page = request.args.get('page', default = 1, type = int)
    sort_param = request.args.get('sort', default = None, type = str)
    filter_param = request.args.get('filter')
    search_param = request.args.get('search')
    group_by_param = request.args.get('group_by')
    where_clause = 'WHERE '
    if filter_param:
        # Split by comma to get multiple filters
        filters = filter_param.split(',')
        print("filters", filters)
        for filter in filters:
            # Split the filter string into attribute and value
            attr, value = filter_param.split(':', maxsplit=1)
            # Inequality 
            if value.startswith('<') or value.startswith('>'): 
                where_clause += f"i.{attr} {value} AND "
            # Negation
            elif value.startswith('!'):
                if attr == 'country_code':
                    # capitalization
                    value = value.upper()
                where_clause += f"i.{attr} != '{value[1:]}' AND "
            # Addition
            elif '|' in value:
                values = value.split('|')
                where_clause += "("
                for val in values:
                    if attr == 'country_code':
                        # capitalization
                        val = val.upper()
                    where_clause += f"i.{attr} = '{val}' OR "
                # Remove the last OR
                where_clause = where_clause[:-4]
                where_clause += ") AND "
            # If the attribute is a convenience filter, translate it to the appropriate attribute
            elif attr == 'has_ror':
                if value.lower() == 'true':
                    where_clause += f"i.ror IS NOT NULL AND "
                else:
                    where_clause += f"i.ror IS NULL AND "
                # return jsonify(institutions)
            elif attr == 'is_global_south':
                attr = 'country_code IN (\'AF\', \'AO\', \'BD\', \'BF\', \'BI\', \'BJ\', \'BO\', \'BR\', \'BT\', \'BW\', \'CD\', \'CF\', \'CG\', \'CI\', \'CM\', \'CO\', \'CR\', \'CU\', \'DJ\', \'DO\', \'EC\', \'EG\', \'ER\', \'ET\', \'GA\', \'GH\', \'GT\', \'GW\', \'HN\', \'HT\', \'ID\', \'IN\', \'KE\', \'KH\', \'KP\', \'KR\', \'LA\', \'LK\', \'LR\', \'LS\', \'LY\', \'MA\', \'MD\', \'MG\', \'ML\', \'MM\', \'MN\', \'MZ\', \'NA\', \'NE\', \'NG\', \'NI\', \'NP\', \'PA\', \'PE\', \'PG\', \'PH\', \'PK\', \'PR\', \'PY\', \'RW\', \'SA\', \'SB\', \'SD\', \'SL\', \'SN\', \'SO\', \'SS\', \'SV\', \'SY\', \'TD\', \'TG\', \'TH\', \'TJ\', \'TL\', \'TM\', \'TN\', \'TR\', \'TZ\', \'UG\', \'UZ\', \'VE\', \'VN\', \'VU\', \'WS\', \'YE\', \'ZA\', \'ZM\', \'ZW\')'
                where_clause += f"i.{attr} = '{value}' AND "
            # elif attr == 'continent':
            #     attr = f'country_code IN (\'{CONTINENTS[value]}\')'
            elif attr == 'display_name.search':
                where_clause += f"display_name ILIKE '%%{value}%%' AND "
            # Build the WHERE clause using the attribute and value
            else:
                if attr == 'country_code':
                    value = value.upper()
                where_clause += f"i.{attr} = '{value}' AND " 
        # Remove the last AND
        where_clause = where_clause[:-4]
        print("where_clause:", where_clause)
    if search_param:
        if where_clause:
            where_clause += f" AND display_name ILIKE '%%{search_param}%%'"
        else:
            where_clause = f"WHERE display_name ILIKE '%%{search_param}%%'"
    if group_by_param:
        if group_by_param not in ['cited_by_count', 'continent', 'country_code', 'is_global_south', 'has_ror', 'type', 'works_count']:
            return jsonify({"error": "Invalid group_by parameter"}), 400
        cur.execute(f"SELECT {group_by_param}, COUNT(*) FROM openalex.institutions GROUP BY {group_by_param} ORDER BY {group_by_param} ASC")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({group_by_param: row[0], "count": row[1]})
        return jsonify(result)
    order_clause = ""
    if sort_param:
        if sort_param not in ['cited_by_count', 'country_code', 'display_name', 'is_global_south', 'type', 'works_count']:
            return jsonify({"error": "Invalid sort parameter"}), 400
        order_clause = f"ORDER BY {sort_param} ASC"
    if where_clause == "WHERE ":
        where_clause = ""

    return get_institutions_query(where_clause, order_clause, per_page, page, sample)

# get: {could not identify a comparison function for type json}, error when I include issn in the query
def get_sources_query(where_clause = ''):
    with conn.cursor() as cur:
        query = f"""
            SELECT v.id, v.issn_l, v.display_name, v.publisher, v.works_count, v.cited_by_count, v.is_oa, v.is_in_doaj, v.homepage_url, v.works_api_url, v.updated_date, COUNT(*) AS publication_count 
            FROM openalex.venues v 
            JOIN openalex.works_alternate_host_venues wahv ON v.id = wahv.venue_id 
            JOIN openalex.works_partition_id w ON wahv.work_id = w.id 
            GROUP BY v.id, v.issn_l, v.display_name, v.publisher, v.works_count, v.cited_by_count, v.is_oa, v.is_in_doaj, v.homepage_url, v.works_api_url, v.updated_date
            ORDER BY publication_count 
            DESC LIMIT 10;
            """
        cur.execute(query)
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "issn_l": row[1],
                "display_name": row[2],
                "publisher": row[3],
                "works_count": row[4],
                "cited_by_count": row[5],
                "is_oa": row[6],
                "is_in_doaj": row[7],
                "homepage_url": row[8],
                "works_api_url": row[9],
                "updated_date": row[10],
                "counts_by_year": row[11],
                "ids": row[12]
            })
        return jsonify(result)


@app.route('/sources', methods=['GET'])
def get_sources():
    cur = conn.cursor()
    filter_param = request.args.get('filter')
    search_param = request.args.get('search')
    where_clause = ''
    if filter_param:
        # Split the filter string into attribute and value
        attr, value = filter_param.split(':', maxsplit=1)
        # If the attribute is a convenience filter, translate it to the appropriate attribute
        if attr == 'display_name.search':
            where_clause = f"WHERE display_name ILIKE '%{value}%'"
            return get_sources_query(where_clause)
        elif attr == 'continent':
            # TO DO: Add continent filter
            pass
        elif attr == 'has_issn':
            if(value.lower() == 'true'):
                where_clause = f"WHERE v.issn_l IS NOT NULL"
            else:
                where_clause = f"WHERE v.issn_l IS NULL"
            get_sources_query(where_clause)
        elif attr == 'is_global_south':
            # TO DO: Add is_global_south filter
            pass
        # Build the WHERE clause using the attribute and value
        else:
            where_clause = f"WHERE {attr} = '{value}'"
    if search_param:
        if where_clause:
            where_clause += f" AND display_name ILIKE '%%{search_param}%%'"
        else:
            where_clause = f"WHERE display_name ILIKE '%%{search_param}%%'"
    return get_sources_query(where_clause)

# Returns differennt autocomplete results than openalex

@app.route('/autocomplete/institutions')
def autocomplete_institutions():
    search_query = request.args.get('q')
    cur = conn.cursor()
    cur.execute("SELECT i.id, i.display_name, g.city, g.country_code, i.cited_by_count, i.works_count FROM openalex.institutions i JOIN openalex.institutions_geo g ON i.id = g.institution_id WHERE i.display_name ILIKE %s LIMIT 10", (f'{search_query}%',))
    rows = cur.fetchall()
    institutions = []
    for row in rows:
        institution = {
            "id": row[0],
            "display_name": row[1],
            "hint": f"{row[2]}, {row[3]}",
            "cited_by_count": row[4],
            "works_count": row[5],
            "entity_type": "institution"
        }
        institutions.append(institution)
    return jsonify({"results": institutions})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
