import random
import sys
import json
import datetime

seed = int(sys.argv[1])
random.seed(seed)

words_file = open(sys.argv[2], "rb")
words = words_file.read().split("\n")
if len(words[-1]) == 0:
    words = words[0:-1]
uppercase_words = set([x.upper() for x in words])

output_location = sys.argv[3]
if output_location[-1] != "/":
    output_location += "/"

chars_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-$"
chars = [char for char in chars_string]

country_codes = [
    "AF",
    "AX",
    "AL",
    "DZ",
    "AS",
    "AD",
    "AO",
    "AI",
    "AQ",
    "AG",
    "AR",
    "AM",
    "AW",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BQ",
    "BA",
    "BW",
    "BV",
    "BR",
    "IO",
    "BN",
    "BG",
    "BF",
    "BI",
    "CV",
    "KH",
    "CM",
    "CA",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CC",
    "CO",
    "KM",
    "CD",
    "CG",
    "CK",
    "CR",
    "CI",
    "HR",
    "CU",
    "CW",
    "CY",
    "CZ",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "SZ",
    "ET",
    "FK",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GF",
    "PF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GG",
    "GN",
    "GW",
    "GY",
    "HT",
    "HM",
    "VA",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "JM",
    "JP",
    "JE",
    "JO",
    "KZ",
    "KE",
    "KI",
    "KP",
    "KR",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "ME",
    "MS",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NR",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NU",
    "NF",
    "MP",
    "NO",
    "OM",
    "PK",
    "PW",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PN",
    "PL",
    "PT",
    "PR",
    "QA",
    "RE",
    "RO",
    "RU",
    "RW",
    "BL",
    "SH",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "WS",
    "SM",
    "ST",
    "SA",
    "SN",
    "RS",
    "SC",
    "SL",
    "SG",
    "SX",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "GS",
    "SS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TK",
    "TO",
    "TT",
    "TN",
    "TR",
    "TM",
    "TC",
    "TV",
    "UG",
    "UA",
    "AE",
    "GB",
    "UM",
    "US",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VG",
    "VI",
    "WF",
    "EH",
    "YE",
    "ZM",
    "ZW"
]

country_weights = {}
for country_code in country_codes:
    if country_code == "US":
        weight = 20
    elif country_code in ["GB", "FR", "JP", "DE", "NL", "TW", "CN"]:
        weight = 10
    else:
        weight = 1
    country_weights[country_code] = weight

country_codes_weighted = []
for country_code in country_codes:
    weight = country_weights[country_code]

    for i in xrange(0, weight):
        country_codes_weighted.append(country_code)

countries = []
for i in range(0, len(country_codes)):
    country_code = country_codes[i]
    country_info = {"country_id": i,
                    "country_code": country_code}
    countries.append(country_info)


high_weight_countries = []
for country_info in countries:
    weight = country_weights[country_info["country_code"]]
    if weight >= 10:
        high_weight_countries.append(country_info)

countries_by_code = {}
for country_info in countries:
    country_code = country_info["country_code"]
    countries_by_code[country_code] = country_info

next_exchange_id = 0
exchanges = []
for country_code in country_codes:
    weight = country_weights[country_code]
    country_info = countries_by_code[country_code]
    country_id = country_info["country_id"]
    exchange_count = 0
    if weight == 1:
        exchange_count = random.randint(1, 3)
    elif weight <= 10:
        exchange_count = random.randint(3, 5)
    else:
        exchange_count = 7

    exchange_code_base = 0
        
    for i in range(0, exchange_count):
        exchange_info = {"exchange_id": next_exchange_id,
                         "country_id": country_id,
                         "exchange_code": "%s%02d" % (country_code, exchange_code_base)}
        exchanges.append(exchange_info)
        next_exchange_id += 1
        exchange_code_base += 1
    

exchanges_by_country = {}
for exchange_info in exchanges:
    country_id = exchange_info["country_id"]
    exchanges_for_country = exchanges_by_country.get(country_id, [])
    exchanges_for_country.append(exchange_info)
    exchanges_by_country[country_id] = exchanges_for_country
    
generated_ticker_increment = 0

external_id_type = {
    0: {"name": "sedol", "country_id": countries_by_code["GB"]["country_id"]},
    1: {"name": "cusip", "country_id": countries_by_code["US"]["country_id"]},
    2: {"name": "wkn", "country_id": countries_by_code["DE"]["country_id"]}
}

local_external_id_types = {}
local_external_id_types[countries_by_code["GB"]["country_id"]] = 0
local_external_id_types[countries_by_code["US"]["country_id"]] = 1
local_external_id_types[countries_by_code["DE"]["country_id"]] = 2

next_external_id_type_id = 3
for country_code in country_codes:
    country_id = countries_by_code[country_code]["country_id"]
    if country_code not in ["GB", "US", "DE"]:
        type_info = {"name": "%s-local" % country_code, "country_id": country_id}
        external_id_type[next_external_id_type_id] = type_info
        local_external_id_types[country_id] = next_external_id_type_id
        next_external_id_type_id += 1

    # for each exchange in this country, create an ticker
    country_id = countries_by_code[country_code]["country_id"]
    exchanges_for_country = exchanges_by_country[country_id]
    for exchange_info in exchanges_for_country:
        exchange_code = exchange_info["exchange_code"]
        type_info = {"name": "%s-ticker" % exchange_code, "country_id": country_id}
        external_id_type[next_external_id_type_id] = type_info
        next_external_id_type_id += 1

# add isin
type_info = {"name": "isin", "country_id": -1}
external_id_type[next_external_id_type_id] = type_info
isin_type_id = next_external_id_type_id
next_external_id_type_id += 1

# get the same map, but by country
external_id_type_by_country = {}
for (key, value) in external_id_type.items():
    type_info = value.copy()
    type_info["sec_external_id_type_id"] = key
    country_id = type_info["country_id"]
    if not external_id_type_by_country.has_key(country_id):
        external_id_type_by_country[country_id] = []
    external_id_type_by_country[country_id].append(type_info)



next_sedol = 100000000
def gen_unique_sedol():
    global next_sedol
    result = "%09d" % next_sedol
    next_sedol += 1
    return result

ticker_set = set()
def get_unique_ticker_for_exchange(exchange_code):
    for i in xrange(0, 12):
        candidate = random_string(random.randint(3, 5))
        candidate_with_exchange = "%s:%s" % (exchange_code, candidate)
        if candidate_with_exchange in ticker_set:
            continue
        ticker_set.add(candidate_with_exchange)
        return candidate
    raise Excepion("Ran out of tickers for exchange %s, it seems!" % exchange_code)

def random_string(length):
    result_list = []
    for i in xrange(0, length):
        result_list.append(random.choice(chars))
    return "".join(result_list)
        
def gen_security_name():
    word_count = random.randint(1, 5)
    return " ".join(random.sample(uppercase_words, word_count))


def gen_local_ids_for_sec(sec_id, country_id, start_dt_string, end_dt_string, include_country_id = False):
    sec_external_data = []
    if include_country_id:
        local_id_type_id = local_external_id_types[country_id]
        if local_id_type_id == 0:
            # local_id = gen_unique_sedol()
            # for now, don't generate sedols here
            pass
        else:
            local_id = "%09d" % random.randint(1000000, 999999999)

            sec_external_info = {
                "sec_id": sec_id,
                "sec_external_id_type_id": local_id_type_id,
                "country_id": country_id,
                "sec_external_id": local_id,
                "start_dt": start_dt_string,
                "end_dt": end_dt_string
            }
            sec_external_data.append(sec_external_info)
    
    # get all the local ticker types for this country
    type_list = external_id_type_by_country[country_id]
    for type_info in type_list:
        name = type_info["name"]
        type_id = type_info["sec_external_id_type_id"]
        ticker_index = name.find("-ticker")
        if ticker_index == -1:
            continue

        exchange_code = type_info["name"][0:ticker_index]
        ticker = get_unique_ticker_for_exchange(exchange_code)

        sec_external_info = {
            "sec_id": sec_id,
            "sec_external_id_type_id": type_id,
            "country_id": country_id,
            "sec_external_id": ticker,
            "start_dt": start_dt_string,
            "end_dt": end_dt_string
        }
        sec_external_data.append(sec_external_info)

    return sec_external_data
            
min_start_dt = datetime.date(1900, 1, 1)
max_start_dt = datetime.date(2001, 1, 1)
delta_as_days = (max_start_dt - min_start_dt).days
def gen_external_ids_for_sec(sec_info, start_dt = None):
    start_dt_passed = (start_dt != None)
    sec_external_data = []
    country_id = sec_info["country_id"]
    country_code = countries[country_id]["country_code"]
    local_id_type_id = local_external_id_types[country_id]

    if start_dt == None:
      start_dt = min_start_dt
      if random.randint(0, 9) < 2:
          # pick a new start date, somewhere between 1900-01-01 and 2001-01-01
          offset_as_days = random.randint(0, delta_as_days)
          delta2 = datetime.timedelta(days = offset_as_days)
          start_dt = min_start_dt + delta2

    start_dt_string = start_dt.strftime("%Y-%m-%d")
    
    sec_id = sec_info["sec_id"]
    # generate 9 digit local id
    if local_id_type_id == 0:
        local_id = gen_unique_sedol()
    else:
        local_id = "%09d" % random.randint(1000000, 999999999)
    check_digit = random.randint(0, 9)
    isin = "%s%s%d" % (country_code, local_id, check_digit)
    # if local_id > 99999999:
    #    print isin
    
    sec_external_info = {
        "sec_id": sec_id,
        "sec_external_id_type_id": isin_type_id,
        "country_id": country_id,
        "sec_external_id": isin,
        "start_dt": start_dt_string,
        "end_dt": "2999-01-01"
    }
    sec_external_data.append(sec_external_info)

    sec_external_info = {
        "sec_id": sec_id,
        "sec_external_id_type_id": local_id_type_id,
        "country_id": country_id,
        "sec_external_id": local_id,
        "start_dt": start_dt_string,
        "end_dt": "2999-01-01"
    }
    sec_external_data.append(sec_external_info)

    # roughly 90% of all securities should get a sedol
    if local_id_type_id != 0 and random.randint(0, 9) > 0:
        sec_external_info = {
            "sec_id": sec_id,
            "sec_external_id_type_id": 0,
            "country_id": country_id,
            "sec_external_id": gen_unique_sedol(),
            "start_dt": start_dt_string,
            "end_dt": "2999-01-01"
        }
        sec_external_data.append(sec_external_info)
        
    sec_external_data += gen_local_ids_for_sec(sec_id, country_id, start_dt_string, "2999-01-01", False)

    # expire x% of identifiers and start new ones
    if random.randint(0, 20) < 3:
        print "Expiring ids for sec_id %d" % sec_id
        offset_as_days = random.randint(0, delta_as_days)
        delta2 = datetime.timedelta(days = offset_as_days)
        end_dt = start_dt + delta2
        end_dt_string = end_dt.strftime("%Y-%m-%d")
        for sec_external_info in sec_external_data:
            sec_external_info["end_dt"] = end_dt_string
        if (start_dt_passed):
            print "Interesting!!!"
        # in most cases, start new ids. But sometimes, don't
        if random.randint(0, 19) > 0:
            sec_external_data += gen_external_ids_for_sec(sec_info, end_dt)

    return sec_external_data

# create sec data
sec_data = {}
for sec_id in xrange(0, 20000):
    country_code = random.choice(country_codes_weighted)
    country_id = countries_by_code[country_code]["country_id"]
    name = gen_security_name()
    record = {"sec_id": sec_id, \
              "name": gen_security_name(), \
              "country_id": country_id}
    sec_data[sec_id] = record

# create country to security id type mapping
security_id_types = {}
index = 0
for country_code in country_codes:
    security_id_types[country_code] = index
    index += 1

# every security gets an ISIN for its home country
# some lucky securities will get more than one
sec_external_data = []
for sec_info in sec_data.values():
    ids_for_security = gen_external_ids_for_sec(sec_info)
    sec_external_data += ids_for_security


sec_external_data_by_sec_id = {}
for sec_external_info in sec_external_data:
    sec_id = sec_external_info["sec_id"]
    info_list = sec_external_data_by_sec_id.get(sec_id, [])
    info_list.append(sec_external_info)
    sec_external_data_by_sec_id[sec_id] = info_list
    
# some securities in heavily weighted countries should have
# identifiers on other heavily weighted exchanges and some low weight
# exchanges
additional_sec_external_data = []
for sec_info in sec_data.values():
    country_id = sec_info["country_id"]
    country_code = countries[country_id]["country_code"]
    weight = country_weights[country_code]
    if weight < 10:
        continue

    # not every security from a heavily weighted country
    if random.randint(0, 9) < 2:
        continue
    
    sec_id = sec_info["sec_id"]
    sec_external_list = sec_external_data_by_sec_id[sec_id]
    start_end_pairs = set()
    # get each start_dt, end_dt pair for the home country
    for sec_external_info in sec_external_list:
        start_end_pairs.add((sec_external_info["start_dt"], sec_external_info["end_dt"]))    

    # for each start/end pair, create ids in other weighted countries
    for weighted_country_info in high_weight_countries:
        weighted_country_id = weighted_country_info["country_id"]
        if weighted_country_id == country_id:
            continue
        # only 50% of other heavily weighted countries
        if random.randint(0, 9) > 4:
            continue
        for (start_dt_string, end_dt_string) in start_end_pairs:
            extra_local_ids = gen_local_ids_for_sec(sec_id, weighted_country_id, start_dt_string, end_dt_string, True)
            additional_sec_external_data += extra_local_ids

sec_external_data += additional_sec_external_data

sec_price_type_data = [
    {"sec_price_type_id": 0, "sec_price_type_code": "open"},
    {"sec_price_type_id": 1, "sec_price_type_code": "close"},
    {"sec_price_type_id": 2, "sec_price_type_code": "offer"}, 
    {"sec_price_type_id": 3, "sec_price_type_code": "bid"}
]

sec_output_filename = output_location + "sec.json"
sec_external_id_type_output_filename = output_location + "sec_external_id_type.json"
sec_external_output_filename = output_location + "sec_external.json"
exchange_output_filename = output_location + "exchange.json"
country_output_filename = output_location + "country.json"
sec_price_type_output_filename = output_location + "sec_price_type.json"

sec_output_file = open(sec_output_filename, "wb")
for sec_info in sec_data.values():
    print >> sec_output_file, json.dumps(sec_info)
sec_output_file.close()

sec_external_id_type_output_file = open(sec_external_id_type_output_filename, "wb")
for (id, sec_external_id_type_info) in external_id_type.items():
    sec_external_id_type_info["sec_external_id_type_id"] = id
    print >> sec_external_id_type_output_file, json.dumps(sec_external_id_type_info)
sec_external_id_type_output_file.close()

sec_external_output_file = open(sec_external_output_filename, "wb")
for sec_external_info in sec_external_data:
    print >> sec_external_output_file, json.dumps(sec_external_info)
sec_external_output_file.close()

exchange_output_file = open(exchange_output_filename, "wb")
for exchange_info in exchanges:
    print >> exchange_output_file, json.dumps(exchange_info)
exchange_output_file.close()

country_output_file = open(country_output_filename, "wb")
for country_info in countries:
    print >> country_output_file, json.dumps(country_info)
country_output_file.close()

sec_price_type_output_file = open(sec_price_type_output_filename, "wb")
for sec_price_type_info in sec_price_type_data:
    print >> sec_price_type_output_file, json.dumps(sec_price_type_info)
sec_price_type_output_file.close()
