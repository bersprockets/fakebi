import random
import sys
import json
import datetime
import sec_data

seed = int(sys.argv[1])

data_date_string = sys.argv[2]
seed_enhance = int(data_date_string.replace("-", ""))

random.seed(seed + seed_enhance)

input_location = sys.argv[3]
if input_location[-1] != "/":
    input_location += "/"

output_location = sys.argv[4]
if output_location[-1] != "/":
    output_location += "/"

data_date = datetime.datetime.strptime(data_date_string, "%Y-%m-%d")

sd = sec_data.SecData(input_location)

country_id = sd.country_by_country_code["US"]["country_id"]
cusip_type_id = sd.sec_external_id_type_by_name["cusip"]["sec_external_id_type_id"]

# find max end_dts on all US-based security ids
sec_max_end_dt = {}
for record in sd.sec_external:
    if record["sec_external_id_type_id"] != cusip_type_id:
        continue
    sec_id = record["sec_id"]
    end_dt = record["end_dt"]
    if not sec_max_end_dt.has_key(sec_id):
        sec_max_end_dt[sec_id] = end_dt
    current_max_end_dt = sec_max_end_dt[sec_id]
    if end_dt > current_max_end_dt:
        sec_max_end_dt[sec_id] = end_dt

# find some sec_ids where the max end_dt is less than data date
expired_sec_list = [item for item in sec_max_end_dt.items()]
interesting_expired_sec_list = [item for item in expired_sec_list if item[1] < data_date_string]
print "There are", len(interesting_expired_sec_list), "interesting expired securties. Among them are:"
loop_count = int(min(len(interesting_expired_sec_list), 10))
for i in range(0, loop_count):
    print interesting_expired_sec_list[i]
    

cusip_set = set()
for record in sd.sec_external:
    id_type_id = record["sec_external_id_type_id"]
    start_dt = record["start_dt"]
    end_dt = record["end_dt"]
    if id_type_id != cusip_type_id:
        continue
    if start_dt > data_date_string or end_dt < data_date_string:
        continue

    # only about 60%
    if random.randint(0, 9) > 3:
        cusip_set.add((record["sec_id"], record["sec_external_id"]))


for (sec_id, max_end_dt) in interesting_expired_sec_list:
    if (random.randint(0, 9)) > 4:
        sec_external_list = sd.sec_external_by_sec_id[sec_id]
        for record in sec_external_list:
            if record["sec_external_id_type_id"] == cusip_type_id and record["end_dt"] == max_end_dt:
                print "Including expired id", record["sec_external_id"], "in the data"
                cusip_set.add((sec_id, record["sec_external_id"]))

prices_output_filename = output_location + "prices_us_%s.csv" % data_date_string
prices_output_file = open(prices_output_filename, "wb")

big_exchanges = ["US00", "US01"]
record_count = 0
for (sec_id, cusip) in cusip_set:
   exchanges = sd.exchange_by_country[country_id]
   for exchange_info in exchanges:
       exchange_code = exchange_info["exchange_code"]
       if exchange_code not in big_exchanges and random.randint(0, 9) < 4:
           continue
       feed_exchange_code = int(exchange_code[2:4])
       magnitude = float(10**random.randint(0, 8))
       open_raw = (random.randint(1, 100000))
       open_cooked = open_raw / magnitude
       close = max(0.0, (open_raw + random.randint(-100, 100))/magnitude)
       offer = max(0.0, (open_raw + random.randint(-100, 100))//magnitude)
       bid = max(0.0, (open_raw + random.randint(-100, 100))//magnitude)
       output_record = "%s,%d,%s,%f,%f,%f,%f" % (cusip, feed_exchange_code, data_date_string, open_cooked, close, offer, bid)
       print >> prices_output_file, output_record


prices_output_file.close()
