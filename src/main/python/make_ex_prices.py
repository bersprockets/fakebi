import random
import sys
import json
import datetime
import sec_data

seed = int(sys.argv[1])

data_dt_string = sys.argv[2]
seed_enhance = int(data_dt_string.replace("-", ""))

random.seed(seed + seed_enhance)

start_price_dt_string = sys.argv[3]
end_price_dt_string = sys.argv[4]

input_location = sys.argv[5]
if input_location[-1] != "/":
    input_location += "/"
    
output_location = sys.argv[6]
if output_location[-1] != "/":
    output_location += "/"

sd = sec_data.SecData(input_location)

# find the isin type id
isin_type_id = sd.sec_external_id_type_by_name["isin"]["sec_external_id_type_id"]

prices_output_filename = output_location + "prices_ex_%s.json" % (data_dt_string)
prices_output_file = open(prices_output_filename, "wb")

start_price_dt = datetime.datetime.strptime(start_price_dt_string, "%Y-%m-%d")
end_price_dt = datetime.datetime.strptime(end_price_dt_string, "%Y-%m-%d")
for sec_info in sd.sec:
    # let's not do every security
    if random.randint(0, 9) > 5:
        continue
    
    sec_id = sec_info["sec_id"]
    sec_external_list = sd.sec_external_by_sec_id[sec_id]
    isin_list = [item for item in sec_external_list if item["sec_external_id_type_id"] == isin_type_id]
    if len(isin_list) == 0:
        print "Empty isin list for sec_id", sec_id, "using type id", isin_type_id
    
    # randomly select an isin from the list. Purposefully might not be active for the price date
    isin_sec_external_info = isin_list[random.randint(0, len(isin_list) - 1)]
    isin = isin_sec_external_info["sec_external_id"]

    isin_start_dt_string = isin_sec_external_info["start_dt"]
    isin_start_dt = datetime.datetime.strptime(isin_start_dt_string, "%Y-%m-%d")
    isin_end_dt_string = isin_sec_external_info["end_dt"]
    isin_end_dt = datetime.datetime.strptime(isin_end_dt_string, "%Y-%m-%d")
    
    # find all tickers with same start date
    def is_interesting_ticker(sec_external_info, expected_start_dt):
        sec_external_id_type_id = sec_external_info["sec_external_id_type_id"]
        start_dt = sec_external_info["start_dt"]
        if start_dt != expected_start_dt:
            return False
        name = sd.sec_external_id_type_by_id[sec_external_id_type_id]["name"]
        
        if name.find("-ticker") != -1:
            return True
        return False
            
    interesting_tickers = [item for item in sec_external_list if is_interesting_ticker(item, isin_start_dt_string)]
    # get the exchanges associated with the tickers
    interesting_exchange_codes = []
    for sec_external_info in interesting_tickers:
        sec_external_id_type_id = sec_external_info["sec_external_id_type_id"]
        name = sd.sec_external_id_type_by_id[sec_external_id_type_id]["name"]
        interesting_exchange_codes.append(name[0:4])
        
    interesting_exchanges = []
    for interesting_exchange_code in interesting_exchange_codes:
        # if a US-based exchange, don't be too eager to include
        if interesting_exchange_code[0:2] == "US" and random.randint(0, 9) > 1:
            continue
        interesting_exchanges += sd.exchange_by_exchange_code[interesting_exchange_code]

    increment = datetime.timedelta(days = 1)
    
    sec_price = []

    price_curr_dt = start_price_dt
    while price_curr_dt < end_price_dt:
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

