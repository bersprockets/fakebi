import random
import sys
import json
import datetime

seed = int(sys.argv[1])
random.seed(seed)

data_dt_string = sys.argv[2]
min_price_dt_string = sys.argv[3]
max_price_dt_string = sys.argv[4]

input_location = sys.argv[5]
if input_location[-1] != "/":
    input_location += "/"
    
output_location = sys.argv[6]
if output_location[-1] != "/":
    output_location += "/"

sec_input_filename = input_location + "sec.json"
sec_external_id_type_input_filename = input_location + "sec_external_id_type.json"
sec_external_input_filename = input_location + "sec_external.json"
exchange_input_filename = input_location + "exchange.json"
country_input_filename = input_location + "country.json"
sec_price_type_input_filename = input_location + "sec_price_type.json"

sec_input_file = open(sec_input_filename, "r")
sec = []
for record in sec_input_file:
    sec.append(json.loads(record))
sec_input_file.close()

sec_external_input_file = open(sec_external_input_filename, "r")
sec_external = []
for record in sec_external_input_file:
    sec_external.append(json.loads(record))
sec_external_input_file.close()


sec_external_by_sec_id = {}
for sec_external_info in sec_external:
    sec_id = sec_external_info["sec_id"]
    sec_external_list = sec_external_by_sec_id.get(sec_id, [])
    sec_external_list.append(sec_external_info)
    sec_external_by_sec_id[sec_id] = sec_external_list


sec_external_id_type_input_file = open(sec_external_id_type_input_filename, "r")
sec_external_id_type_by_id = {}
for record in sec_external_id_type_input_file:
    sec_external_id_type_info = json.loads(record)
    sec_external_id_type_id = sec_external_id_type_info["sec_external_id_type_id"]
    sec_external_id_type_by_id[sec_external_id_type_id] = sec_external_id_type_info
sec_external_id_type_input_file.close()

# find the isin type id
isin_type_id = -1
for record in sec_external_id_type_by_id.values():
    if record["name"] == "isin":
        isin_type_id = record["sec_external_id_type_id"]
        break

if isin_type_id == -1:
    raise Exception("Couldn't find isin type id")
    
exchange_input_file = open(exchange_input_filename, "r")
exchange = []
for record in exchange_input_file:
    exchange.append(json.loads(record))
exchange_input_file.close()


exchange_by_country = {}
for exchange_info in exchange:
    country_id = exchange_info["country_id"]
    exchange_list = exchange_by_country.get(country_id, [])
    exchange_list.append(exchange_info)
    exchange_by_country[country_id] = exchange_list


exchange_by_exchange_code = {}
for exchange_info in exchange:
    exchange_code = exchange_info["exchange_code"]
    exchange_list = exchange_by_exchange_code.get(exchange_code, [])
    exchange_list.append(exchange_info)
    exchange_by_exchange_code[exchange_code] = exchange_list

sec_price_type_input_file = open(sec_price_type_input_filename, "r")
sec_price_type = []
for record in sec_price_type_input_file:
    sec_price_type.append(json.loads(record))
sec_price_type_input_file.close()

prices_output_filename = output_location + "prices_ex_%s.json" % (data_dt_string)
prices_output_file = open(prices_output_filename, "wb")

min_price_dt = datetime.datetime.strptime(min_price_dt_string, "%Y-%m-%d")
max_price_dt = datetime.datetime.strptime(max_price_dt_string, "%Y-%m-%d")
for sec_info in sec:
    sec_id = sec_info["sec_id"]
    sec_external_list = sec_external_by_sec_id[sec_id]
    isin_list = [item for item in sec_external_list if item["sec_external_id_type_id"] == isin_type_id]
    start_dates = [item["start_dt"] for item in isin_list]

    # get the min start date from this list

    min_start_dt = reduce(lambda x, y: min(x, y), start_dates, "2999-01-01")
    if sec_id == 4858:
        print "min start date is", min_start_dt


    isin_sec_external_info = isin_list[random.randint(0, len(isin_list) - 1)]
    isin = isin_sec_external_info["sec_external_id"]

    isin_start_dt_string = isin_sec_external_info["start_dt"]
    isin_start_dt = datetime.datetime.strptime(isin_start_dt_string, "%Y-%m-%d")
    isin_end_dt_string = isin_sec_external_info["end_dt"]
    isin_end_dt = datetime.datetime.strptime(isin_end_dt_string, "%Y-%m-%d")
    delta_as_days = (isin_start_dt - isin_end_dt).days
    
    # find all tickers with same start date
    def is_interesting_ticker(sec_external_info, expected_start_dt):
        sec_external_id_type_id = sec_external_info["sec_external_id_type_id"]
        start_dt = sec_external_info["start_dt"]
        if start_dt != expected_start_dt:
            return False
        name = sec_external_id_type_by_id[sec_external_id_type_id]["name"]
        
        if name.find("-ticker") != -1:
            return True
        return False
            
    interesting_tickers = [item for item in sec_external_list if is_interesting_ticker(item, isin_start_dt_string)]
    # get the exchanges associated with the tickers
    interesting_exchange_codes = []
    for sec_external_info in interesting_tickers:
        sec_external_id_type_id = sec_external_info["sec_external_id_type_id"]
        name = sec_external_id_type_by_id[sec_external_id_type_id]["name"]
        interesting_exchange_codes.append(name[0:4])
        
    interesting_exchanges = []
    for interesting_exchange_code in interesting_exchange_codes:
        interesting_exchanges += exchange_by_exchange_code[interesting_exchange_code]


    candidate_start_dt = isin_start_dt
    if candidate_start_dt > datetime.datetime(1900, 1, 1):
        # possibly create some prices before the isin's start date
        if random.randint(0, 9) < 1:
            candidate_start_dt = candidate_start_dt - datetime.timedelta(days = random.randint(12, 120))
        
    price_curr_dt = candidate_start_dt
    if price_curr_dt < min_price_dt:
        price_curr_dt = min_price_dt


    candidate_end_dt = isin_end_dt
    if candidate_end_dt < max_price_dt:
        # possibly create some prices on or after the isin's end date
        if random.randint(0, 9) < 1:
            candidate_end_dt = candidate_end_dt + datetime.timedelta(days = random.randint(1, 120))
        
    last_price_dt = candidate_end_dt
    if last_price_dt > max_price_dt:
        last_price_dt = max_price_dt

    increment = datetime.timedelta(days = 40)
    
    sec_price = []
    # get some dates in the range of this isin's life

    while price_curr_dt < last_price_dt:
        # create some prices on these exchanges, using the isin as the identifier
        for interesting_exchange in interesting_exchanges:
            magnitude = float(10**random.randint(0, 8))
            open_raw = (random.randint(1, 100000))
            open_cooked = open_raw / magnitude
            close = max(0.0, (open_raw + random.randint(-100, 100))/magnitude)
            offer = max(0.0, (open_raw + random.randint(-100, 100))//magnitude)
            bid = max(0.0, (open_raw + random.randint(-100, 100))//magnitude)
            record = {"isin": isin,
                      "exchange": interesting_exchange["exchange_code"],
                      "date": price_curr_dt.strftime("%Y-%m-%d"),
                      "open": open_cooked,
                      "close": close,
                      "offer": offer,
                      "bid": bid
            }
            sec_price.append(record)

        price_curr_dt += increment
        

    # output prices
    for record in sec_price:
        print >> prices_output_file, json.dumps(record)
    
prices_output_file.close()

