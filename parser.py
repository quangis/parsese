#!/usr/bin/env python

import json
import re
import csv


# q390 is not in the parsed list


def question_sequence_to_string(question_sequence, separator='::', brackets=('<', '>')):
    """Returns the shorthand notation of the semantically encoded question."""
    return "".join([f"{brackets[0]}{token['tag']}{separator}{token['value']}{brackets[1]}" for token in question_sequence])


def complex_spatial_extent():
    # 9 <1trnot><1::Where><::are><::5-star><t::hotels><r::in><n::the Happy Valley><o::ski><t::resort>
    # 50 <1ptopo><1::Where><::is><::a><p::suitable><t::site><::for><::the><o::disposal><::of><p::radioactive><o::waste><::in><::UK>
    # 155 <2oorotrnqqot><2::What><::is><o::population><o::density><r::by><o::census><t::block><r::in><::the><n::Dallas><::/><::Fort><q::Worth><q::metropolitan><o::service><t::area>
    # 161 <2oooo><2::What><::is><::the><o::density><::of><o::elms><::and><::crape><o::myrtles><::in><o::Oleander>
    # 188  <6tartoaoor><6::How much of the city><t::city><::is><a::affected><r::by><t::street><o::noise><a::given><::the><o::noise><o::coefficients><r::for><::each><::street><::in><::the><::city>
    # 192 <2ootrtrot><2::What><::are><::the><o::noise><o::mitigation><t::zones><r::around><::each><t::runway><r::in><o::Schiphol><t::airport>
    # 239 <2tqrtrno><2::What><::are><::the><t::sites><q::suitable><r::for><t::metro stations><r::in><n::Karbala><::,><o::Iraqi>
    # 242 <2oopooorn><2::To what extent><o::extent><::are><o::there><p::regional><o::differences><::in><o::population><o::distribution><r::in><::the><::Yunnan><::province><::,><n::China>
    # 258 <1tpoornno><1::Where><::are><::the><t::sites><::that><::are><::most><p::suitable><::for><o::marina><o::construction><r::in><n::Istanbul><::â€™s><n::Marmara Sea><o::shoreline>
    # 267, 268, 269, 278, 422-425, 418, 403, 400, 398, 387

    # [SC] incorrectly classified as an extent: 110 What is the pattern of accidents on ski pistes?
    # [SC] 214 What is the bikeability in the Metro Vancouver region of Canada?
    #       <2ornntrn><2::What><::is><o::bikeability><r::in><n::the Metro Vancouver><n::the Metro Vancouver><t::region><r::of><n::Canada>

    # 421 <2ortrnpoooooo><2::What><::is><::the><o::accessibility><r::of><t::residential units><r::in><n::Utrecht city><::to><p::public><o::waste><o::collectors><::for><o::glass><::,><o::paper><o::plastic><::and><o::textile>
    # 426 <rn1tpoooot><r::Within><n::Riverside - San Bernardino><1::where><t::areas><p::high><o::population><o::density><o::health><o::care><t::facilities>
    # 279 <5popornod><5::How><::did><::the><p::spatial><o::distribution><::of><p::domestic><o::tourism><r::in><n::South Korea><o::change><d::between 1989 and 2011>
    # 275 <2orootooornrnd><2::What><::are><::the><o::changes><r::in><::the><o::environment><::,><o::climate><t::land><::and><o::use><::land><o::cover><o::types><r::for><n::Jiangsu Province><r::of><n::China><d::between 1980 - 2012>
    # 273 <5sosrnnntrnrpoooort><5::How><::can><::individual><::-><s::based><o::rurality><::be><s::measured><r::in><n::Levy><::,><n::Lafayette><::and><n::Suwannee><t::counties><r::of><::the><n::US><r::on><p::individual><o::activity><o::space><::and><o::rurality><o::degree><r::of><t::places>
    # 251 <2pooooooornnn><2::What><::is><::the><p::geographic><o::accessibility><::to><o::family><o::physician><::and><o::nurse><o::practitioner><o::services><::for><o::seniors><r::in><n::Saskatchewan><::and><n::Alberta><::,><n::Canada>
    # 241 <2oorrnsno><2::What><::is><::the><o::population><o::density><r::in><::the><::Banten><::province><::,><r::in><n::Indonesia><s::based><::on><n::IndoPop><o::data>
    # 233 <2poorooooootoo><2::What><::is><::the><p::urban><o::population><::in><o::China><::estimated><r::from><o::radiance><::corrected><o::DMSP><::-><o::OLS><o::night><o::time><o::light><::and><t::land><o::cover><o::data>
    # 232 <opopotortrnoo><::Are><o::there><::urban><::-><p::suburban><o::differences><::in><p::spatial><o::clustering><::and><t::neighborhood><o::characteristics><r::of><t::residential sites><r::of><n::Pennsylvania><::for><o::people><::with><::ID><::and><o::people><::with><::PD>
    # 231 <troostrnrqqposto><::Are><t::residential sites><r::for><o::people><::with><::ID><::and><o::people><::with><::PD><s::located><::in><t::neighborhoods><r::of><n::Pennsylvania><r::with><q::similar><::or><q::different><p::sociodemographic><o::characteristics><::that><s::affect><t::community><o::inclusion>
    # 190 <trtattoo><::How><::lit><::are><::the><t::areas><r::of><::the><t::city><a::given><t::locations><::of><t::street><o::lights><::and><::their><o::wattage>
    # 184 <2ortooroto><2::What><::is><::the><o::percentage><r::of><::each><t::land><::-><o::use><o::type><r::inside><::the><o::notification><t::zone><::for><::zoning><o::change>
    # 183 <3oosrtoo><3::Which property owners><o::property><o::owners><::do><s::need><::to><::be><::notified><r::around><::the><t::area><::of><::proposed><o::zoning><o::change>
    # 167 <2ororntooo><2::What><::is><::the><o::relationship><r::between><o::clusters><r::of><n::West Nile Virus><::and><::the><t::locations><::of><o::food><::and><o::water><o::sources>
    # 147 <2oortrnaooo><2::What><::is><::the><o::construction><o::trend><r::in><::the><t::city><r::of><n::Oleander><a::given><o::construction><o::years><::of><::dwelling><o::units>
    # 113 <2poopoo><2::What><::will><::be><::the><p::long><::-><o::term><o::consequences><::of><::continuing><p::recreational><o::activity><::for><::the><o::landscape>
    # 130 <1otaqooo><1::Where><::does><::the><::Fort><::Worth><o::police><t::department><a::assign><::a><q::specific><o::task><o::force><::to><::deal><::with><::the><::most><::dangerous><o::crimes>

    expression = (""
        + "<r?::(of|in|at|within|for|by|per|between|from|on|to|around|among|along|over)>" # relation
        + "("
        +       "(<::the>)?<n::[^>]+>(<t::[^>]+>)?" # spatial extent is a named entity; t if the named entity also has an explicit type specified
        +       "|<::the><t::[^>]+>" # spatial extent is a specific instance of a type
        + ")"
        # + "(" # spatial extent locators
        # +       "(<::,>|<r?::(of|in|at|within|for|by|per|from|on|around|along|over)>)"
        # +       "("
        # +           "(<::the>)?<n::[^>]+>"
        # +           "|<::the><t::[^>]+>"
        # +       ")"
        # + ")*"
        # + "(" # optional date
        # +       "<r?::(of|in|at|within|for|by|from|on|to|around|over)><d?::[^>]+>" # [relation] [d]
        # +       "|<r?::from><d?::[^>]+><r?::to><d?::[^>]+>" # from [d] to [d]
        # +       "|<r?::between><d?::[^>]+><::and><d?::[^>]+>" # between [d] and [d]
        # + ")?"
        # + "$"
    )
    matcher = re.compile(expression, re.IGNORECASE)
    print(expression)

    counter = 0
    for q in questions:
        result = matcher.search(q['shorthand'])
        if result:
            counter += 1
            print(f"\tQuestion {q['id']} matched: {q['question']}?")
            print(f"\t\tMatching pattern: {result.group(0)}")
            print(f"\t\tMatching pattern: {result.group(1, 2)}")
            # print(f"\t\tWhole string: {q['shorthand']}")
        # else:
        #     print(f"\tQuestion {q['id']} mismatched: {q['question']}?")
        #     print(f"\t\tWhole string: {q['shorthand']}")
    print(counter)

    # [statistical aggregation][spatial extent],[spatial extent locator]

    # 426 <rn1tpoooot><r::Within><n::Riverside - San Bernardino><1::where><t::areas><p::high><o::population><o::density><o::health><o::care><t::facilities>
    # 428 <2trtrn><2::What parcels><t::parcels><::are><r::within><::the><::100-year><t::floodplain><r::in><::the><n::Netherlands>
    # 177 <6ttrtrn><6::How many land parcels><t::land><t::parcels><::are><r::in><::the><t::floodplain><r::in><n::Oleander>
    # 178 <2qtrtrtrn><2::What><::the><q::total><t::area><r::of><t::land><::is><r::inside><::the><t::floodplain><r::in><n::Oleander>
    # 179 <2ortrtortrn><2::What><::is><::a><o::breakdown><r::of><::the><t::area><r::of><t::land><o::use><r::inside><::the><t::floodplain><r::in><n::Oleander>
    # 59 <2oooorn><2::What><::is><::the><o::condition><::of><::the><o::water><o::treatment><o::plant><r::at><n::270 Fleet>
    # 62 What is the pattern of public spending in areas where the majority of residents are African American?
    # 65 What would be the economic impact if development were restricted within 100 yards of the river?
    # 82 What is the flow of traffic along A28 motorway?
    # 119 What are the areas covered by cameras in Salford, England?
    # 123 What political parties are favored in different counties of the United States?
    # 124 What is the crime distribution in Amsterdam in 2018?
    # 145 What is the population distribution in Tarrant County, Texas
    # 150 How does tractor traffic compare to auto traffic on Texas roads?
    # 152 What are the crime rates for this and last years in each police district of Texas?
    # 154 What are the portions of energy coming from oil, natural gas, and nuclear power in each state of the United States?
    # 155 What is population density by census block in the Dallas/Fort Worth metropolitan service area?
    # 156 What is the density of robberies for each police beat in Dallas/Fort Worth metropolitan service area?
    # 159 What is the dot density of registered voters relative to the total population of voting age per precinct in Dallas?
    # 160 What is the density of trees in parks in Oleander?
    # 169 Are fire calls randomly distributed among city blocks in Fort Worth?
    # 174 What is acreage for each land-use type in a region of Oleander?
    # 180 How many poll workers do each precinct need given the number of households that fall within each precinct?
    # 192 What are the noise mitigation zones around each runway in Schiphol airport?
    # 195 What areas are not within the 3 minutes of driving time for a fire truck given a road network in Oleander?
    # 421 What is the accessibility of residential units in Utrecht city to public waste collectors for glass, paper, plastic, and textile?
    # 419 What is the walkability of Utrecht?
    # 416 What areas do have high water levels near A27 road in Utrecht?
    # 417 What are the land cover types within 1km of A27 road in Utrecht?
    # 409 Where are the areas with a high concentration of NO2 in Vancouver and Seattle?
    # 401 What are the water and land use changes in Original-stream Zone of the Tarim River from 1994 to 2005?
    # 397 What is the urban growth potential in the area Islamabad Zone IV of Islamabad, Pakistan?
    #   <5spootnnrnn><5::How><::to><s::identify><p::urban><o::growth><o::potential><::in><::the><t::area><n::Islamabad><n::Islamabad Zone IV><r::of><n::Islamabad><::,><n::Pakistan>
    # 394 What is the conversion pattern of rural-urban land use in Nanjing, China from 2000 to 2004?
    #   <2ooqtonn><2::What><::is><::the><o::conversion><o::pattern><::of><::rural><::-><q::urban><t::land><o::use><::in><n::Nanjing><::,><n::China><::from><::2000><::to><::2004>
    # 392 What are the spatial-temporal variations of hotspots for thefts and robberies in Shanghai in 2009?
    #   <1pooornd><1::Where><::are><::the><p::monthly><o::hotspots><::of><o::thefts><::and><o::robberies><r::in><n::Shanghai><::in><d::2009>
    # 384 What industries are concentrated in the suburbs of Shanghai?

    # 396 373 393
    # 9 <r::in><n::the Happy Valley> => the Happy Valley ski resort
    # Question 134 matched: What is the distribution of West Nile Virus in US? => <::of><n::West Nile>
    # Question 143 matched: What is the relationship between the locations of stores and the population income levels in Amsterdam? => <r::between><::the><t::locations>
    # Question 147 matched: What is the construction trend in the city of Oleander given construction years of dwelling units? => <r::in><::the><t::city>
    # Question 155 matched: What is population density by census block in the Dallas/Fort Worth metropolitan service area? => Matching pattern: <r::in><::the><n::Dallas>
    # Question 219 matched: What is the destination density for cyclists in the Metro Vancouver region of Canada? => <r::of><n::Canada>
    # Question 218 matched: What is the topography of bicycle-friendly streets the Metro Vancouver region of Canada?
    # Question 244 matched: Which are the determinant factors in the land-use change in the urban area of Yogyakarta in Indonesia? => <r::in><::the><t::land>
    # Question 258 matched: Where are the sites that are most suitable for marina construction in Istanbulâ€™s Marmara Sea shoreline? => <r::in><n::Istanbul>
    # Question 262 matched: What are the impact of land use and population density on seasonal surface water quality in the Wen-Rui Tang River watershed in China? => <r::in><n::China>
    # Question 267 matched: What are the spatiotemporal patterns of relative healthy food access in the Region of Waterloo, Canada, from 2011 to 2014? => <r::in><::the><t::Region>
    # Question 278 matched: What is the impact of High-Speed Rail on land cover change in the area of Atocha railway station in Madrid, Spain, between 1990 and 2006? => <::in><::the><t::area>
    # Question 303 matched: Are there significant patterns of clustering of obesity and moderate physical activity in the neighborhoods of Metro Vancouver, Canada? => <r::of><n::Metro Vancouver>
    # Question 304 matched: Is there an association between obesity and moderate physical activity and the built urban environment in the neighborhoods of Metro Vancouver, Canada? => <::in><::the><t::neighborhoods>
    # Question 311 matched: Which factors influence the location choice of business establishments in the city of Hamilton, Canada? => <r::in><::the><t::city>
    # Question 314 matched: What are the spatial trends of school and housing segregation on the South of US between 1990 and 2010? => <r::of><n::US>
    # Question 335 matched: What are the changes of landuse categories distribution in the district of Kefalos for the years 1981, 1995 and 2002? => r::in><::the><t::district>
    # Question 373 matched: How to measure and monitor urban sprawl and carbon footprint in Phoenix metropolitan area? => <r::in><n::Phoenix>

    # not extent
    # 197 What is the spread of plumes over time from a fire in a match factory?
    # 204 Which buildings were affected by the changing tornado?

def search_for_spatial_extent(relation_instance, token_code='n', print_details=False):
    # ><r::in><t::region>
    expression = f'><r::{relation_instance}><{token_code}::[^>]+>$' # matches any question where relation is "in" in the relation noun pair at the end
    matcher = re.compile(expression, re.IGNORECASE)

    counter = 0
    for q in questions:
        result = matcher.search(q['shorthand'])
        if result:
            counter += 1
            if print_details:
                print(f"\tQuestion {q['id']} matched: {q['question']}?")
                print(f"\t\tMatching pattern: {result.group()}")
                #print(f"\t\tWhole string: {q['shorthand']}")

    if counter:
        print(f"{counter} results for spatial extent expression {expression}\n")
    # else:
    #     print(f"No results for spatial extent expression {expression}")

    return counter


def explore_spatial_extent():
    with open('spatial_extent.csv', 'w', newline='') as csvfile:
        fieldnames = ['relation', 'code', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for relation in ['of', 'in', 'within', 'for', 'by', 'per', 'between', 'from', 'on', 'to', 'around', 'among', 'along']:
            for code in codes:
                count = search_for_spatial_extent(relation, code, False)
                writer.writerow({'relation': relation, 'code': code, 'count': count})


def search_for_relation(relation_instance, token_code='n', print_details=False):
    expression = f'><r::{relation_instance}><{token_code}::[^>]+><'
    matcher = re.compile(expression, re.IGNORECASE)

    counter = 0
    for q in questions:
        result = matcher.search(q['shorthand'])
        if result:
            counter += 1
            if print_details:
                print(f"\tQuestion {q['id']} matched: {q['question']}?")
                print(f"\t\tMatching pattern: {result.group()}")
                #print(f"\t\tWhole string: {q['shorthand']}")

    if counter:
        print(f"{counter} results for relation expression {expression}\n")
    # else:
    #     print(f"No results for relation expression {expression}\n")

    return counter


def explore_relation():
    with open('relation.csv', 'w', newline='') as csvfile:
        fieldnames = ['relation', 'code', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for relation in ['of', 'in', 'within', 'for', 'by', 'per']:
            for code in codes:
                count = search_for_relation(relation, code, True)
                writer.writerow({'relation': relation, 'code': code, 'count': count})


def extract_what_codes():
    with open('what_codes.csv', 'w', newline='') as csvfile:
        fieldnames = ['code', 'qid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        counter = 0
        counterT = 0
        for q in questions:
            if q['intent_code'].startswith('2'):
                writer.writerow({'code': q['intent_code'], 'qid': q['id']})
                counter += 1
                if q['intent_code'].find("t") != -1:
                    counterT += 1
        print(f"Total: {counter}; Objects: {counter - counterT}; Place types: {counterT}")


def what_intents():
    # [TODO]
    # <2qtoornt><2::What><::is><q::predominant><t::land><o::use><o::type><r::in><n::the Happy Valley><t::resort>
    # What houses do/does
    # <2oatoo><2::What><::would><::be><::the><o::time><::saving><::if><::we><a::delivered><::our><t::parcels><::using><::this><o::route><::,><::rather><::than><::an><o::alternative>
    # <2poooorotrn><2::What><::will><::be><::the><p::long><::-><o::term><o::consequences><::of><o::farming><::and><o::forestry><r::for><::the><o::conservation><t::area><r::in><n::Zdarske Vrchy>
    # <2orpot><2::What><::is><::the><::predicted><o::snowfall><r::for><::the><p::new><o::ski><t::piste>

    # 392 <2ppoooornd><2::What><::are><::the><p::spatial><::-><p::temporal><o::variations><::of><o::hotspots><::for><o::thefts><::and><o::robberies><r::in><n::Shanghai><::in><d::2009>
    # 399 <2oooorotorn><2::What><::are><::the><::in><o::interactions><::between><o::population><o::growth><::and><o::changes><r::in> ..
    # 418 <2oooaoo><2::To what extent><o::extent><::does><o::traffic><o::congestion><a::reduce><::because><::of><o::expansion><::of><o::A27>

    # [SC] mis-identified intent words
    # 138 <2orn><2::What><::are><::the><::zoning><o::categories><r::in><n::Utrecht>
    # 400 <2otoo><2::What><::are><::the><o::water><::and><t::land><o::use><o::changes><::in><::Original><::-><::stream><::Zone><::of><::the><::Tarim><::River><::from><::1994><::to><::2005>

    with open('what_intents.csv', 'w', newline='') as csvfile:
        fieldnames = ['intent', 'qid', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><::of>' where n4 is the object intent
        # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><n::n5>' where n4 is the object intent
        expression = (""
            + "<2::What[^>]*>"  # what question
            + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
            + "(<::be>)?"
            + "(<::the>|<::a>)?"  # 'the' is optional
            + "((<::and>)?(<::->)?<[otnqaspd]::(?P<adjective>[^>]+)>)*"  # zero or more non-object and non-type code value pairs
            + "<o::(?P<intent>[^>]+)>"  # one object value pair assumed to be the goal attribute
            + "("
            # + "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among)>"  # followed by an unannotated relation
            + "<::"  # a quick fix
            + "|<[1-9rnqaspd]"  # or followed by non-object and non-type code
            + ")"
        )
        matcher = re.compile(expression, re.IGNORECASE)
        print(expression)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                writer.writerow({'intent': result.group('intent'), 'qid': q['id'], 'code': 'o'})
                counter += 1

                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group('intent')}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")
        print(counter)

        # '<2::What><o::n1><t::n2><o::n3><::is>' where n3 is the object intent that occurs before 'is' or 'are'
        expression = (""
            + "<2::What[^>]*>"  # what question
            + "((<::and>)?(<::->)?<[ntoqaspd]::(?P<adjective>[^>]+)>)*" # zero or more non-relation code and value pair
            + "<o::(?P<intent>[^>]+)>" # object value pair
            + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
            + "(<::be>)?"
        )
        matcher = re.compile(expression, re.IGNORECASE)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                writer.writerow({'intent': result.group('intent'), 'qid': q['id'], 'code': 'o'})
                counter += 1

                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group('intent')}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")
        print(counter)

        ####################################################

        # '<2::What><::is><::the><o::n1><p::n2><t::n3><t::n4><::of>' where n4 is the type intent
        # '<2::What><::is><::the><o::n1><p::n2><t::n3><t::n4><n::n5>' where n4 is the type intent
        expression = (""
                      + "<2::What[^>]*>"  # what question
                      + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
                      + "(<::be>)?"
                      + "(<::the>|<::a>)?"  # 'the' is optional
                      + "((<::and>)?(<::->)?<[otnqaspd]::(?P<adjective>[^>]+)>)*"  # zero or more non-object and non-type code value pairs
                      + "<t::(?P<intent>[^>]+)>"  # one type value pair assumed to be the goal attribute
                      + "("
                      #+ "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among)>"  # followed by an unannotated relation
                      + "<::"
                      + "|<[1-9rnqaspd]"  # or followed by non-object and non-type code
                      + ")"
                      )
        matcher = re.compile(expression, re.IGNORECASE)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                writer.writerow({'intent': result.group('intent'), 'qid': q['id'], 'code': 't'})
                counter += 1
                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group('intent')}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")
        print(counter)

        # '<2::What><o::n1><t::n2><t::n3><::is>' where n3 is the type intent that occurs before 'is' or 'are'
        expression = (""
                      + "<2::What[^>]*>"  # what question
                      + "((<::and>)?(<::->)?<[ntoqaspd]::(?P<adjective>[^>]+)>)*"  # zero or more non-relation code and value pair
                      + "<t::(?P<intent>[^>]+)>"  # type value pair
                      + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
                      + "(<::be>)?"
                      )
        matcher = re.compile(expression, re.IGNORECASE)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                writer.writerow({'intent': result.group('intent'), 'qid': q['id'], 'code': 't'})
                counter += 1

                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group('intent')}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")
        print(counter)

        print("End what_intents")


def what_adjectives():
    with open('what_adjectives.csv', 'w', newline='') as csvfile:
        fieldnames = ['intent', 'adjective', 'distance', 'qid', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for intentCode in ['o', 't']:
            for adjectives in [1, 2, 3, 4]:
                # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><::of>' where n4 is the object intent
                # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><n::n5>' where n4 is the object intent
                expression = (""
                    + "<2::What[^>]*>"  # what question
                    + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
                    + "(<::be>)?"
                    + "(<::the>|<::a>)?"  # 'the' is optional
                )

                for adjectiveCount in range(adjectives):
                    expression += f"(<::and>)?(<::->)?<[otnqaspd]::(?P<adjective{adjectiveCount}>[^>]+)>"

                expression += (""
                    + f"<{intentCode}::(?P<intent>[^>]+)>"
                    + "("
                    # + "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among)>"  # followed by an unannotated relation
                    + "<::"  # a quick fix
                    + "|<[1-9rnqaspd]"  # or followed by non-object and non-type code
                    + ")"
                )
                # print(expression)

                matcher = re.compile(expression, re.IGNORECASE)

                counter = 0
                for q in questions:
                    result = matcher.search(q['shorthand'])
                    if result:
                        # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                        # print(f"\t\tThe intent is {result.group('intent')}")
                        for adjectiveCount in range(adjectives):
                            writer.writerow({
                                'intent': result.group('intent')
                                , 'adjective': result.group(f"adjective{adjectiveCount}")
                                , 'distance': adjectives - adjectiveCount
                                , 'qid': q['id']
                                , 'code': intentCode
                            })
                            # temp = f"adjective{adjectiveCount}"
                            # print(f"\t\tThe adjective is {result.group(temp)}")
                        counter += 1
                        # print(f"\t\tMatching shorthand: {q['shorthand']}")
                        # print("")
                print(counter)

                ###################################################

                # '<2::What><o::n1><t::n2><o::n3><::is>' where n3 is the object intent that occurs before 'is' or 'are'
                expression = "<2::What[^>]*>"  # what question

                for adjectiveCount in range(adjectives):
                    expression += f"(<::and>)?(<::->)?<[otnqaspd]::(?P<adjective{adjectiveCount}>[^>]+)>"

                expression += (""
                    + f"<{intentCode}::(?P<intent>[^>]+)>"
                    + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
                    + "(<::be>)?"
                )
                # print(expression)

                matcher = re.compile(expression, re.IGNORECASE)

                counter = 0
                for q in questions:
                    result = matcher.search(q['shorthand'])
                    if result:
                        # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                        # print(f"\t\tThe intent is {result.group('intent')}")
                        for adjectiveCount in range(adjectives):
                            writer.writerow({
                                'intent': result.group('intent')
                                , 'adjective': result.group(f"adjective{adjectiveCount}")
                                , 'distance': adjectives - adjectiveCount
                                , 'qid': q['id']
                                , 'code': intentCode
                            })
                            temp = f"adjective{adjectiveCount}"
                            # print(f"\t\tThe adjective is {result.group(temp)}")
                        counter += 1
                        # print(f"\t\tMatching shorthand: {q['shorthand']}")
                        # print("")
                print(counter)

# def what_objects():
#     with open('what_objects.csv', 'w', newline='') as csvfile:
#         fieldnames = ['intent', 'relation', 'object', 'distance', 'qid', 'code']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#
#         for intentCode in ['o', 't']:
#             for objects in [1, 2, 3]:
#                 # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><::of>' where n4 is the object intent
#                 # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><n::n5>' where n4 is the object intent
#                 expression = (""
#                     + "<2::What[^>]*>"  # what question
#                     + "(<::(is|are|were|was|do|does|did|have|has|should|could|will)>|<::(would|will)><::be>)"  # either 'is' or 'are'
#                     + "(<::the>|<::a>)?"  # 'the' is optional
#                     + "(<[otnqaspd]::[^>]+>)*" # zero or more non-object and non-type code value pairs
#                     + f"<{intentCode}::(?P<intent>[^>]+)>"
#                     + "(<r::|<::)(?P<relation>of|in|at|for|by|within|per|between|on|from|to|around|among)>"
#                 )
#
#                 for objectCount in range(objects):
#                     expression += f"<[otnqasp]::(?P<object{objectCount}>[^>]+)>"
#
#                 expression += (""
#                     + "(<r::|<::)(of|in|at|for|by|within|per|between|on|from|to|around|if|among)>"
#                     + "<[1-9rnqaspd]::[^>]+>"
#                 )
#
#                 print(expression)
#
#                 matcher = re.compile(expression, re.IGNORECASE)
#
#                 counter = 0
#                 for q in questions:
#                     result = matcher.search(q['shorthand'])
#                     if result:
#                         print(f"\tQuestion {q['id']} matched: {q['question']}?")
#                         print(f"\t\tThe intent is {result.group('intent')}")
#                         print(f"\t\tThe relation is {result.group('relation')}")
#                         for objectCount in range(objects):
#                             writer.writerow({
#                                 'intent': result.group('intent')
#                                 , 'relation': result.group('relation')
#                                 , 'object': result.group(f"object{objectCount}")
#                                 , 'distance': objectCount
#                                 , 'qid': q['id']
#                                 , 'code': intentCode
#                             })
#                             temp = f"object{objectCount}"
#                             print(f"\t\tThe object is {result.group(temp)}")
#                         counter += 1
#                         print(f"\t\tMatching shorthand: {q['shorthand']}")
#                         print("")
#                 print(counter)
#
#                 ###################################################
#
#                 # # '<2::What><o::n1><t::n2><o::n3><::is>' where n3 is the object intent that occurs before 'is' or 'are'
#                 # expression = "<2::What[^>]*>"  # what question
#                 #
#                 # for adjectiveCount in range(adjectives):
#                 #     expression += f"<[otnqaspd]::(?P<adjective{adjectiveCount}>[^>]+)>"
#                 #
#                 # expression += (""
#                 #     + f"<{intentCode}::(?P<intent>[^>]+)>"
#                 #     + "(<::(is|are|were|was|do|does|did|have|has|should|could|will)>|<::(would|will)><::be>)"
#                 # )
#                 # # print(expression)
#                 #
#                 # matcher = re.compile(expression, re.IGNORECASE)
#                 #
#                 # counter = 0
#                 # for q in questions:
#                 #     result = matcher.search(q['shorthand'])
#                 #     if result:
#                 #         # print(f"\tQuestion {q['id']} matched: {q['question']}?")
#                 #         # print(f"\t\tThe concept is {result.group('intent')}")
#                 #         for adjectiveCount in range(adjectives):
#                 #             writer.writerow({
#                 #                 'intent': result.group('intent')
#                 #                 , 'adjective': result.group(f"adjective{adjectiveCount}")
#                 #                 , 'distance': adjectives - adjectiveCount
#                 #                 , 'qid': q['id']
#                 #                 , 'code': intentCode
#                 #             })
#                 #             temp = f"adjective{adjectiveCount}"
#                 #             # print(f"\t\tThe adjective is {result.group(temp)}")
#                 #         counter += 1
#                 #         # print(f"\t\tMatching shorthand: {q['shorthand']}")
#                 #         # print("")
#                 # print(counter)

def what_objects():
    nonobjects = ('and', ',', '-', 'a', 'the', ')', '(')

    subExpress = "<[otnqaspd]*::([^>]+)>"
    subMatcher = re.compile(subExpress, re.IGNORECASE)

    with open('what_objects.csv', 'w', newline='') as csvfile:
        fieldnames = ['intent', 'relation', 'object', 'distance', 'qid', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for intentCode in ['o', 't']:
            # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><::of>' where n4 is the object intent
            # '<2::What><::is><::the><o::n1><p::n2><t::n3><o::n4><n::n5>' where n4 is the object intent
            expression = (""
                + "<2::What[^>]*>"  # what question
                + "<::(is|are|were|was|do|does|did|have|has|should|could|would|will)>"  # either 'is' or 'are'
                + "(<::be>)?"
                + "(<::the>|<::a>)?"  # 'the' is optional
                + "((<::and>)?(<::->)?<[otnqaspd]::[^>]+>)*" # zero or more non-object and non-type code value pairs
                + f"<{intentCode}::(?P<intent>[^>]+)>"
                + "(<r::|<::)(?P<relation>of|in|at|for|by|within|per|between|on|from|to|around|among|along|over)>"
                + "(?!<(n|d)::)"
                + "(?P<object>(.*?))"
                + "(?="
                +    "("
                +        "(<r::|<::)(of|in|at|for|by|within|per|between|on|from|to|around|if|among|along|that|over)>"
                +        "|<[1-9]::"
                +    ")"
                + ")"
            )
            print(expression)
            matcher = re.compile(expression, re.IGNORECASE)

            counter = 0
            for q in questions:
                result = matcher.search(q['shorthand'])
                if result:
                    subResults = subMatcher.findall(result.group('object'))
                    for objectCount in range(len(subResults)):
                        if subResults[objectCount] not in nonobjects:
                            writer.writerow({
                                'intent': result.group('intent')
                                , 'relation': result.group('relation')
                                , 'object': subResults[objectCount]
                                , 'distance': len(subResults) - objectCount
                                , 'qid': q['id']
                                , 'code': intentCode
                            })
                    counter += 1

                    # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                    # print(f"\t\tThe intent is {result.group('intent')}")
                    # print(f"\t\tThe relation is {result.group('relation')}")
                    # print(f"\t\tThe object is {result.group('object')}")
                    # print(f"\t\tThe object is {subResults}")
                    # print(f"\t\tMatching shorthand: {q['shorthand']}")
                    # print("")
            print(counter)

            #########################################################


def explore_what():
    extract_what_codes()
    what_intents()
    what_adjectives()
    what_objects()


def extract_how_codes():
    with open('how_codes.csv', 'w', newline='') as csvfile:
        fieldnames = ['code', 'type', 'qid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for q in questions:
            if q['intent_code'].startswith('6'):
                writer.writerow({'code': q['intent_code'], 'type': '6', 'qid': q['id']})
            elif q['intent_code'].startswith('5'):
                 writer.writerow({'code': q['intent_code'], 'type': '5', 'qid': q['id']})


def complex_how_patterns():
    with open('how_amount.csv', 'w', newline='') as csvfile:
        fieldnames = ['wh', 'amount', 'qid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        expression = "(how many )(.*?)(?=is |are |was |were |does |do |have been |has been )"
        matcher = re.compile(expression, re.IGNORECASE)
        counter = 0
        for q in questions:
            result = matcher.search(q['question'])
            if result:
                counter += 1
                writer.writerow({'wh': result.group(1), 'amount': result.group(2), 'qid': q['id']})
                # print(f"{q['id']}-{q['question']}")
                # print(result.group(1))
                # print(result.group(2))
        print(counter)

        expression = "(how much )(.*?)(?=is\s|are |was |were |does |do |have been |has been )"
        matcher = re.compile(expression, re.IGNORECASE)
        counter = 0
        for q in questions:
            result = matcher.search(q['question'])
            if result:
                counter += 1
                writer.writerow({'wh': result.group(1), 'amount': result.group(2), 'qid': q['id']})
                # print(f"{q['id']}-{q['question']}")
                # print(result.group(1))
                # print(result.group(2))
        print(counter)


def explore_how():
    extract_how_codes()
    complex_how_patterns()


def extract_where_codes():
    with open('where_codes.csv', 'w', newline='') as csvfile:
        fieldnames = ['intent_code', 'all_code', 'qid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for q in questions:
            if q['intent_code'].startswith('1'):
                writer.writerow({'intent_code': q['intent_code'], 'all_code': q['all_code'], 'qid': q['id']})


def complex_where_patterns():
    # incorrectly parsed: 9, 13, 31, 79, 85, 332, 339, 426
    # unconventional structure: 80, 93, 106, 173, 375

    with open('where_intents.csv', 'w', newline='') as csvfile:
        fieldnames = ['intent', 'qid', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # '<1::Where><::is><::the><o::n1><p::n2><t::n3><o::n4><::of>' where n4 is the object intent
        # '<1::Where><::is><::the><o::n1><p::n2><t::n3><o::n4><n::n5>' where n4 is the object intent
        expression = (""
            + "<1::Where[^>]*>"  # where question
            + "(<::(is|are|were|was|do|does|did|have|has|should|could|will)>|<::(would|will)><::be>)"  # either 'is' or 'are'
            + "(<::the>|<::a>)?"  # 'the' is optional
            + "(<[otnqaspd]::[^>]+>)*"  # zero or more non-object and non-type code value pairs
            + "<o::[^>]+>"  # one object value pair assumed to be the goal attribute
            + "("
            #+ "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among|with)>"  # followed by an unannotated relation
            + "<::" # a quick fix
            + "|<[1-9rnqaspd]"  # or followed by non-object and non-type code
            + ")"
        )
        matcher = re.compile(expression, re.IGNORECASE)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                start_index = result.group().rindex("<o::")
                end_index = result.group().index(">", start_index)
                writer.writerow({'intent': result.group()[start_index + 4:end_index], 'qid': q['id'], 'code': 'o'})

                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group()[start_index + 4:end_index]}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")

                counter += 1
        print(counter)

        ####################################################

        # '<1::Where><::is><::the><o::n1><p::n2><t::n3><t::n4><::of>' where n4 is the type intent
        # '<1::Where><::is><::the><o::n1><p::n2><t::n3><t::n4><n::n5>' where n4 is the type intent
        expression = (""
                      + "<1::Where[^>]*>"  # where question
                      + "(<::(is|are|were|was|do|does|did|have|has|should|could|will)>|<::(would|will)><::be>)"  # either 'is' or 'are'
                      + "(<::the>|<::a>)?"  # 'the' is optional
                      + "(<[otnqaspd]::[^>]+>)*"  # zero or more non-object and non-type code value pairs
                      + "<t::[^>]+>"  # one type value pair assumed to be the goal attribute
                      + "("
                      #+ "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among|with)>"  # followed by an unannotated relation
                      + "<::"
                      + "|<[1-9rnqaspd]"  # or followed by non-object and non-type code
                      + ")"
                      )
        matcher = re.compile(expression, re.IGNORECASE)

        counter = 0
        for q in questions:
            result = matcher.search(q['shorthand'])
            if result:
                start_index = result.group().rindex("<t::")
                end_index = result.group().index(">", start_index)
                writer.writerow({'intent': result.group()[start_index + 4:end_index], 'qid': q['id'], 'code': 't'})

                # print(f"\tQuestion {q['id']} matched: {q['question']}?")
                # print(f"\t\tMatching pattern: {result.group()}")
                # print(f"\t\tThe concept is {result.group()[start_index + 4:end_index]}")
                # print(f"\t\tMatching shorthand: {q['shorthand']}")

                counter += 1
        print(counter)


def explore_where():
    extract_where_codes()
    complex_where_patterns()


if __name__ == '__main__':
    with open('./analyzed_question.json') as f:
        codes = list('ntoqasrpd')

        questions = json.load(f)

        # [SC] add shorthand string
        for q in questions:
            q['shorthand'] = f"<{q['all_code']}>{question_sequence_to_string(q['all_info'])}"
            q['intent_shorthand'] = f"<{q['intent_code']}>{question_sequence_to_string(q['intent_info'])}"

        # explore_spatial_extent()
        complex_spatial_extent()
        #
        # explore_relation()
        #
        # explore_what()
        #
        # explore_how()
        #
        # explore_where()

    # '<2::What><o::n1><t::n2><o::n3><::of>' where n3 is the object intent that occurs before 'is' or 'are'
    # expression = (""
    #               + "<2::What[^>]*>"  # what question
    #               + "(<[ntoqaspd]::[^>]+>)*"  # non-relation code and value pair
    #               + "<o::[^>]+>"  # object value pair
    #               + "<::(of|in|at|for|by|within|per|between|on|from|to|around|if|among)>"
    #               # followed by an unannotated relation
    #               )
    # matcher = re.compile(expression, re.IGNORECASE)
    #
    # counter = 0
    # for q in questions:
    #     result = matcher.search(q['shorthand'])
    #     if result:
    #         start_index = result.group().rindex("<o::")
    #         end_index = result.group().index(">", start_index)
    #         writer.writerow({'intent': result.group()[start_index + 4:end_index], 'qid': q['id'], 'code': 'o'})
    #
    #         # print(f"\tQuestion {q['id']} matched: {q['question']}?")
    #         # print(f"\t\tMatching pattern: {result.group()}")
    #         # print(f"\t\tThe concept is {result.group()[start_index + 4:end_index]}")
    #         # print(f"\t\tMatching shorthand: {q['shorthand']}")
    #
    #         counter += 1
    # print(counter)

    # [TEMP]
    # expression = (""
    #     + "<2::What[^>]*>"      # what question
    #     + "(<::is>|<::are>)"    # either 'is' or 'are'
    #     + "(<::the>)?"          # 'the' is optional
    #     + "(<[rnqaspd]::[^>]+>)*" # zero or more non-object and non-type code value pairs
    #     + "(<o::[^>]+>)+"       # one or more object value pairs, it is assumed that the last pair is the goal attribute
    #     + "("
    #     + "<::(of|in|for|by|within|per|between|on|from|to|around|if)>"   # followed by an unannotated relation
    #     + "|<[rnqaspd]"    # or followed by non-object and non-type code
    #     + ")"
    # )

    # [TEMP]
    # expression = (""
    #               + "<2::What[^>]*>"  # what question
    #               + "(<::is>|<::are>)"  # either 'is' or 'are'
    #               + "(<::the>)?"  # 'the' is optional
    #               + "<[rnqaspd]"  # one or more object value pairs, it is assumed that the last pair is the goal attribute
    #               )

    # [TEMP]
    # expression = (""
    #               + "<2::What[^>]*>"  # what question
    #               + "(<::is>|<::are>)"  # either is or are
    #               + "(<::the>)?"  # the is optional
    #               + "(<o::[^>]+>)+"  # one or more object value pairs, the last pair is the goal attribute
    #               + "<[rnqaspd]"  # followed by an unannotated relation
    #               )