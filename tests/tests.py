import requests
import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://hawk5.csl.illinois.edu:5000"

    def test_get_single_entity(self):
        url = f"{self.base_url}/works/W3127800895"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_data = {'abstract_inverted_index': {'(N': [105], '(walk,': [35], '100,000': [198], '2020': [104], '9,394).': [107], '=': [106], 'According': [164], 'Africa': [71], 'Australia,': [62], 'Brazil,': [63], 'COVID-19': [8, 196, 240], 'COVID-19.': [94], 'China,': [64], 'Findings': [95], 'Ghana,': [65], 'Gini': [186], 'In': [136], 'India,': [66], 'Iran,': [67], 'Italy,': [68], 'May': [103], 'Motivation': [168], 'Norway,': [69], 'Protection': [167], 'South': [70], 'States.': [75], 'The': [0, 108], 'Theory,': [169], 'These': [232], 'This': [24, 76, 203], 'United': [74], 'across': [161], 'actual': [216], 'adopted': [55], 'aggravate': [200], 'aims': [80], 'airplane)': [49], 'airplanes': [142], 'all': [20, 32, 127, 134], 'alone,': [40], 'also': [79, 227], 'an': [98], 'and': [51, 72, 93, 117, 131, 143, 188, 209], 'are': [145, 211], 'around': [21], 'as': [185, 219, 242, 244], 'at': [81], 'avoidance': [154], 'be': [148], 'before': [50], 'behaviors': [17, 87], 'bicycle,': [36], 'both': [115], 'bus,': [45], 'buses': [144], 'but': [226], 'car': [38, 41], 'changes': [14], 'commuting': [116], 'company,': [44], 'conducted': [101], 'consistently': [159], 'continents:': [61], 'countries': [58], 'countries.': [163], 'crisis': [241], 'cross-country': [77], 'deaths': [193], 'developing': [251], 'disruptions': [113], 'document': [234], 'documented': [221], 'driven': [39, 42], 'due': [194], 'during': [52], 'empirical': [109], 'examines': [26], 'expressed': [184], 'fact': [177], 'findings': [233], 'for': [31, 114, 247], 'found': [160], 'frequency': [125], 'future': [252], 'global': [236], 'guidance': [246], 'have': [10], 'health': [217], 'highlighting': [120], 'hinge': [96], 'impact': [237], 'implemented': [3], 'in': [4, 43, 56, 102, 123, 222, 250], 'income': [182], 'index,': [187], 'indicates': [205], 'indicators,': [180], 'individual': [28], 'inequality': [208], 'inequality,': [183], 'inhabitants,': [199], 'is': [158], 'light': [174], 'literature,': [225], 'massive': [13], 'measures': [2], 'mobility': [29], 'modes': [34], 'modes,': [152], 'modes.': [135], 'morbidity': [210], 'motorcycle,': [37], 'namely': [181], 'new': [173], 'non-commuting': [118], 'not': [212], 'number': [191], 'of': [18, 85, 126, 129, 133, 138, 155, 192, 238], 'on': [59, 175], 'online': [99], 'only': [213], 'pandemic': [9], 'patterns': [30], 'people': [19], 'per': [197], 'perceived': [146, 230], 'perceptions.': [202], 'potential': [139], 'practitioners': [249], 'predictors': [84], 'protective': [86], 'provide': [245], 'public': [156], 'quantify': [111], 'reductions': [122], 'related': [88, 214], 'relevant': [224], 'reported': [190], 'research': [204], 'respondents’': [201], 'response': [5], 'restrictions': [54], 'restrictive': [1], 'results': [110], 'riskiest': [150], 'risks,': [218], 'risks.': [231], 'sector': [92], 'sheds': [172], 'six': [60], 'socio-economic': [207], 'spread,': [141], 'strategies.': [253], 'study': [25, 78, 171], 'substantial': [121], 'subway,': [46], 'sudden': [12], 'survey': [100], 'ten': [57], 'terms': [137], 'that': [178, 206], 'the': [7, 22, 27, 53, 73, 83, 90, 124, 149, 162, 166, 170, 176, 189, 223, 229, 235, 239], 'to': [6, 15, 89, 147, 165, 195, 215, 228], 'train,': [48], 'tram,': [47], 'transport': [33, 91, 151, 157], 'transportation': [248], 'travel': [16], 'travels,': [119], 'tremendous': [112], 'triggered': [11], 'trips': [130], 'two': [179], 'types': [128], 'understanding': [82], 'upon': [97], 'use': [132], 'virus': [140], 'well': [220, 243], 'while': [153], 'world.': [23]}, 'alternate_host_venues': [{'is_oa': True, 'license': 'cc-by', 'url': 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0245886&type=printable', 'venue_id': 'https://openalex.org/V202381698', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://europepmc.org/articles/pmc7850470?pdf=render', 'venue_id': 'https://openalex.org/V4306400806', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://cris.unibo.it/bitstream/11585/808752/1/journal.pone.0245886.pdf', 'venue_id': 'https://openalex.org/V4306402579', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://opus.lib.uts.edu.au/bitstream/10453/145723/2/2021_PLOS1_Impact%20of%20COVID-10%20pandemic%20on%20mobility_DMB...KPW...THR.pdf', 'venue_id': 'https://openalex.org/V4306401629', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://scholar.sun.ac.za:443/bitstream/10019.1/109534/1/barbieri_impact_2021.pdf', 'venue_id': 'https://openalex.org/V4306400300', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://researchonline.federation.edu.au/vital/access/services/Download/vital:15094/SOURCE1', 'venue_id': 'https://openalex.org/V4306400234', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/11250/2778866/1/journal.pone.0245886.pdf', 'venue_id': 'https://openalex.org/V4306401716', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'https://vtechworks.lib.vt.edu/bitstream/10919/103486/1/journal.pone.0245886.pdf', 'venue_id': 'https://openalex.org/V4306400248', 'version': 'publishedVersion'}, {'is_oa': True, 'license': None, 'url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7850470', 'venue_id': 'https://openalex.org/V2764455111', 'version': 'publishedVersion'}, {'is_oa': True, 'license': 'cc-by', 'url': 'http://eprints.iisc.ac.in/68103/1/plo_one_16-02_2021.pdf', 'venue_id': 'https://openalex.org/V4306401429', 'version': 'acceptedVersion'}], 'authorships': [{'author_id': 'https://openalex.org/A2735223019', 'author_position': 'first', 'institution_id': 'https://openalex.org/I204778367', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, Norwegian University of Science and Technology, Trondheim, Trøndelag, Norway'}, {'author_id': 'https://openalex.org/A2969870756', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I25355098', 'raw_affiliation_string': "School of Highway, Chang'an University , Xi'an , Shaanxi , China."}, {'author_id': 'https://openalex.org/A3048773702', 'author_position': 'middle', 'institution_id': None, 'raw_affiliation_string': 'Italian Society of Cognitive Behavioral Therapy (CBT-Italy), Firenze, Toscana, Italy.'}, {'author_id': 'https://openalex.org/A1985884011', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I148561064', 'raw_affiliation_string': 'Biodiversity Informatics Unit, African Institute for Mathematical Sciences, Cape Town, South Africa; Centre for Invasion Biology, Dept of Mathematical Sciences, Stellenbosch Univ. Matieland South Africa'}, {'author_id': 'https://openalex.org/A1985884011', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I26092322', 'raw_affiliation_string': 'Biodiversity Informatics Unit, African Institute for Mathematical Sciences, Cape Town, South Africa; Centre for Invasion Biology, Dept of Mathematical Sciences, Stellenbosch Univ. Matieland South Africa'}, {'author_id': 'https://openalex.org/A1846896739', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I204778367', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, Norwegian University of Science and Technology, Trondheim, Trøndelag, Norway'}, {'author_id': 'https://openalex.org/A3048370475', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I10824318', 'raw_affiliation_string': 'Department of Civil Engineering, Federal University of Ouro Preto, Ouro Preto, Minas Gerais, Brazil'}, {'author_id': 'https://openalex.org/A3048916912', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I3130357712', 'raw_affiliation_string': 'Department of Geography, Lalit Narayan Mithila University, Darbhanga, Bihar, India.'}, {'author_id': 'https://openalex.org/A2145696301', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I155093810', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, University of Idaho, Moscow, Idaho, United States of America'}, {'author_id': 'https://openalex.org/A2427376554', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I154851008', 'raw_affiliation_string': 'Indian Institute of Technology Roorkee Department of Civil Engineering, Transportation Engineering Group, Roorkee, Uttarakhand, India.'}, {'author_id': 'https://openalex.org/A2098760026', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I158011677', 'raw_affiliation_string': 'Department of Geography, Environment, and Planning, Sonoma State University, Rohnert Park, California, United States of America'}, {'author_id': 'https://openalex.org/A2883695540', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I1317621060', 'raw_affiliation_string': 'Dept of Civil Engineering, Indian Institute of Technology Guwahati, Guwahati, Assam, India'}, {'author_id': 'https://openalex.org/A1956356266', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I95023434', 'raw_affiliation_string': 'Department of Geography, University of KwaZulu-Natal, Durban, KwaZulu, South Africa'}, {'author_id': 'https://openalex.org/A2527962065', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I149672521', 'raw_affiliation_string': 'School of Health, Federation University Australia, Berwick, Victoria, Australia'}, {'author_id': 'https://openalex.org/A2979599145', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I9360294', 'raw_affiliation_string': 'Department of Civil Chemical Environmental and Materials Engineering, University of Bologna, Bologna, Emilia-Romagna, Italy'}, {'author_id': 'https://openalex.org/A2143610888', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I22759111', 'raw_affiliation_string': 'Department of Civil Engineering/Russ College of Engineering & Technology, Ohio University, Athens, Ohio, United States of America.'}, {'author_id': 'https://openalex.org/A3024866434', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I196699116', 'raw_affiliation_string': 'State Key Laboratory of Silicate Materials for Architectures; Wuhan University of Technology; Wuhan Hubei China'}, {'author_id': 'https://openalex.org/A2789994199', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I204778367', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, Norwegian University of Science and Technology, Trondheim, Trøndelag, Norway'}, {'author_id': 'https://openalex.org/A3048546563', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I4210121477', 'raw_affiliation_string': 'School of Medicine, Bam University of Medical Sciences, Bam, Kerman, Iran.'}, {'author_id': 'https://openalex.org/A2735223019', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I25355098', 'raw_affiliation_string': "School of Highway, Chang'an University , Xi'an , Shaanxi , China."}, {'author_id': 'https://openalex.org/A2105876965', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I25757504', 'raw_affiliation_string': 'School of Mechanics and Civil Engineering, China University of Mining and Technology, Jiangsu, China.'}, {'author_id': 'https://openalex.org/A2164805560', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I140172145', 'raw_affiliation_string': 'Connecticut Transportation Safety Research Center, University of Connecticut, Storrs, Connecticut, United States of America'}, {'author_id': 'https://openalex.org/A1827990080', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I114017466', 'raw_affiliation_string': 'School of Civil & Environmental Engineering, University of Technology Sydney, Ultimo, New South Wales, Australia;'}, {'author_id': 'https://openalex.org/A2593576855', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I31746571', 'raw_affiliation_string': 'Department of Social Policy Research Centre, University of New South Wales, Sydney, New South Wales, Australia'}, {'author_id': 'https://openalex.org/A3048586673', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I200650556', 'raw_affiliation_string': 'Department of Engineering and Science, University of Agder, Grimstad, Agder, Norway.'}, {'author_id': 'https://openalex.org/A3174641537', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I157773358', 'raw_affiliation_string': 'School of Civil Engineering, Sun Yat-sen University, Guangzhou, Guangdong, China.'}, {'author_id': 'https://openalex.org/A3048891594', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I59270414', 'raw_affiliation_string': 'Department of Civil Engineering, Indian Institute of Science Bangalore, Bangalore, Karnataka, India.'}, {'author_id': 'https://openalex.org/A3119881690', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I204778367', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, Norwegian University of Science and Technology, Trondheim, Trøndelag, Norway'}, {'author_id': 'https://openalex.org/A2607317792', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I14894300', 'raw_affiliation_string': 'Foshan Transportation Science and Technology Co. Ltd., Foshan, Guangdong, China.'}, {'author_id': 'https://openalex.org/A2944003332', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I181414168', 'raw_affiliation_string': 'Department of Civil and Architectural Engineering, Texas A&M University-Kingsville, Kingsville, Texas, United States of America.'}, {'author_id': 'https://openalex.org/A2111756778', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I859038795', 'raw_affiliation_string': 'Department of Civil and Environmental Engineering, Virginia Tech, Blacksburg, Virginia, United States of America'}, {'author_id': 'https://openalex.org/A2944111737', 'author_position': 'middle', 'institution_id': 'https://openalex.org/I33213144', 'raw_affiliation_string': 'Department of Civil & Coastal Engineering, University of Florida, Gainesville, Florida, United States of America'}, {'author_id': 'https://openalex.org/A1938701650', 'author_position': 'last', 'institution_id': 'https://openalex.org/I114017466', 'raw_affiliation_string': 'School of Civil & Environmental Engineering, University of Technology Sydney, Ultimo, New South Wales, Australia;'}], 'biblio': {'first_page': 'e0245886', 'issue': '2', 'last_page': 'e0245886', 'volume': '16'}, 'cited_by_api_url': 'https://api.openalex.org/works?filter=cites:W3127800895', 'cited_by_count': 85, 'concepts': [{'id': 'https://openalex.org/C157085824', 'score': 0.7068153}, {'id': 'https://openalex.org/C89623803', 'score': 0.7006862}, {'id': 'https://openalex.org/C3008058167', 'score': 0.62425596}, {'id': 'https://openalex.org/C539828613', 'score': 0.532903}, {'id': 'https://openalex.org/C45555294', 'score': 0.48366842}, {'id': 'https://openalex.org/C205649164', 'score': 0.46559486}, {'id': 'https://openalex.org/C99454951', 'score': 0.411155}, {'id': 'https://openalex.org/C45355965', 'score': 0.3902169}, {'id': 'https://openalex.org/C4249254', 'score': 0.38615042}, {'id': 'https://openalex.org/C144133560', 'score': 0.37869132}, {'id': 'https://openalex.org/C47768531', 'score': 0.32098132}, {'id': 'https://openalex.org/C71924100', 'score': 0.2791521}, {'id': 'https://openalex.org/C162324750', 'score': 0.19277003}, {'id': 'https://openalex.org/C22212356', 'score': 0.1785352}, {'id': 'https://openalex.org/C127413603', 'score': 0.12856498}, {'id': 'https://openalex.org/C134306372', 'score': 0.0}, {'id': 'https://openalex.org/C33923547', 'score': 0.0}, {'id': 'https://openalex.org/C2779134260', 'score': 0.0}, {'id': 'https://openalex.org/C142724271', 'score': 0.0}, {'id': 'https://openalex.org/C524204448', 'score': 0.0}], 'display_name': 'Impact of COVID-19 pandemic on mobility in ten countries and associated perceived risk for all transport modes', 'doi': 'https://doi.org/10.1371/journal.pone.0245886', 'host_venues': [{'is_oa': True, 'license': 'cc-by', 'url': 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0245886&type=printable', 'venue_id': 'https://openalex.org/V202381698', 'version': 'publishedVersion'}], 'id': 'https://openalex.org/W3127800895', 'is_paratext': False, 'is_retracted': False, 'mesh': [], 'open_access': {'is_oa': True, 'oa_status': 'gold', 'oa_url': 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0245886&type=printable'}, 'publication_date': '2021-02-01', 'publication_year': 2021, 'title': 'Impact of COVID-19 pandemic on mobility in ten countries and associated perceived risk for all transport modes', 'type': 'journal-article', 'work_ids': {'doi': 'https://doi.org/10.1371/journal.pone.0245886', 'mag': 3127800895, 'openalex': 'https://openalex.org/W3127800895', 'pmcid': 'https://www.ncbi.nlm.nih.gov/pmc/articles/7850470', 'pmid': 'https://pubmed.ncbi.nlm.nih.gov/33524042'}}
        self.assertDictEqual(data, expected_data)

    def test_select_fields(self):
        url = f"{self.base_url}/works/W3127800895?select=id,display_name"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "https://openalex.org/W3127800895")
        self.assertEqual(data["display_name"], "Impact of COVID-19 pandemic on mobility in ten countries and associated perceived risk for all transport modes")

    def test_get_list_of_entities(self):
        url = f"{self.base_url}/concepts"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_paging(self):
        url = f"{self.base_url}/authors?page=2"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_entity_lists(self):
        url = f"{self.base_url}/authors?filter=display_name:John%20Smith"
        response = requests.get(url)
        data = response.json()
        for author in data:
            self.assertEqual(author["display_name"], "John Smith")
        self.assertEqual(response.status_code, 200)

    def test_get_list_of_entities(self):
        url = f"{self.base_url}/concepts"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_200_results_on_second_page(self):
        url = f"{self.base_url}/authors?page=2&per-page=200"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 200)

    def test_inequality_filter(self):
        url = f"{self.base_url}/authors?filter=cited_by_count:>10000"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for author in data:
            self.assertGreater(author["cited_by_count"], 10000)

    def test_from_publication_date_filter(self):
        url = f"{self.base_url}/works?filter=from_publication_date:2022-01-01"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for work in data:
            self.assertGreaterEqual(work["publication_date"], "2022-01-01")

    def test_negation_filter(self):
        url = f"{self.base_url}/institutions?filter=country_code:!us"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for institution in data:
            self.assertNotEqual(institution["country_code"], "US")

    def test_intersection_filter(self):
        url = f"{self.base_url}/authors?filter=cited_by_count:%3E100,display_name:Kevin%20Chen-Chuan%20Chang"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for author in data:
            self.assertGreater(author["cited_by_count"], 100)
            self.assertEqual(author["display_name"], "Kevin Chen-Chuan Chang")

    def test_or_filter(self):
        url = f"{self.base_url}/works?filter=doi:https://doi.org/10.1371/journal.pone.0266781|https://doi.org/10.1371/journal.pone.0267149"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        dois = [work["doi"] for work in data]
        self.assertIn("https://doi.org/10.1371/journal.pone.0266781", dois)
        self.assertIn("https://doi.org/10.1371/journal.pone.0267149", dois)
    def test_search_entities(self):
        url = f"{self.base_url}/works?search=dna"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for work in data:
            self.assertTrue("dna" in work["title"].lower() or "dna" in work["abstract"].lower())

    def test_sort_entities(self):
        url = f"{self.base_url}/works?sort=cited_by_count"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        cited_by_counts = [work["cited_by_count"] for work in data]
        self.assertEqual(cited_by_counts, sorted(cited_by_counts))

if __name__ == "__main__":
    unittest.main()
