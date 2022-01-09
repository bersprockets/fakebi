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

interesting_country_codes = ['VE', 'CO', 'EC', 'PE', 'BR', 'BO', 'CL']


def is_interesting(record):
    id_type_id = record["sec_external_id_type_id"]
    sec_external_id_type = sd.sec_external_id_type_by_id[id_type_id]
    id_type_name = sec_external_id_type["name"]
    
    if len(id_type_name) < 2:
        # print record, "too small"
        return False

    if id_type_name.find("-ticker") == -1:
        # print record, "not a ticker"
        return False

    maybe_country_code = id_type_name[0:2]
    
    if maybe_country_code not in interesting_country_codes:
        # print record, "not in interesting country"
        return False

    country_id = sd.country_by_country_code[maybe_country_code]["country_id"]

    if sec_external_id_type["country_id"] != country_id:
        # print record, "does not have expected country_id"
        return False

    # print record, "got one"
    return True


# find max end_dts on all US-based security ids
sec_max_end_dt = {}
for record in sd.sec_external:
    if not is_interesting(record):
        continue
    id_type_id = record["sec_external_id_type_id"]
    sec_id = record["sec_id"]
    end_dt = record["end_dt"]
    if not sec_max_end_dt.has_key(sec_id):
        sec_max_end_dt[(sec_id, id_type_id)] = end_dt
    current_max_end_dt = sec_max_end_dt[(sec_id, id_type_id)]
    if end_dt > current_max_end_dt:
        sec_max_end_dt[(sec_id, id_type_id)] = end_dt

# find some sec_ids where the max end_dt is less than data date
expired_sec_list = [item for item in sec_max_end_dt.items()]
interesting_expired_sec_list = [item for item in expired_sec_list if item[1] < data_date_string]
print "There are", len(interesting_expired_sec_list), "interesting expired securties. Among them are:"
loop_count = int(min(len(interesting_expired_sec_list), 10))
for i in range(0, loop_count):
    print interesting_expired_sec_list[i]

ticker_set = set()
for record in sd.sec_external:
    if not is_interesting(record):
        continue
    
    id_type_id = record["sec_external_id_type_id"]
    start_dt = record["start_dt"]
    end_dt = record["end_dt"]
    if start_dt > data_date_string or end_dt < data_date_string:
        continue

    # only about 60%
    if random.randint(0, 9) > 3:
        ticker_set.add((record["sec_id"], record["sec_external_id"], id_type_id))


for ((sec_id, id_type_id), max_end_dt) in interesting_expired_sec_list:
    if (random.randint(0, 9)) > 4:
        sec_external_list = sd.sec_external_by_sec_id[sec_id]
        for record in sec_external_list:
            if record["sec_external_id_type_id"] == id_type_id and record["end_dt"] == max_end_dt:
                print "Including expired id", record["sec_external_id"], "in the data"
                ticker_set.add((sec_id, record["sec_external_id"], id_type_id))

prices_output_filename = output_location + "prices_emerging_%s.csv" % data_date_string
prices_output_file = open(prices_output_filename, "wb")


# we need to produce trades throughout the day
open_time = data_date + datetime.timedelta(hours = 9)
close_time = data_date + datetime.timedelta(hours = 16)

print open_time, close_time
price_types = ["trade", "bid", "offer"]
entries = []

for (sec_id, ticker, id_type_id) in ticker_set:
    sec_external_id_type = sd.sec_external_id_type_by_id[id_type_id]
    id_type_name = sec_external_id_type["name"]
    exchange_code = id_type_name[0:4]
    magnitude = float(10**random.randint(0, 8))
    baseline = random.randint(1, 100000)
    current_time = open_time
    while current_time < close_time:
        offset_minutes = random.randint(0, 60)
        current_time = current_time + datetime.timedelta(minutes = offset_minutes)
        current_time_string = current_time.strftime("%H:%M:%S")
        price_type = random.choice(price_types)
        price = max(0.0, (baseline + random.randint(-100, 100))/magnitude)

        entries.append((ticker, exchange_code, price_type, current_time_string, price))

cmp_func = lambda x,y: cmp(x[3], y[3])
sorted_entries = sorted(entries, cmp_func)

for entry in sorted_entries:
    output_record = "%s,%s,%s,%s,%f" % entry
    print >> prices_output_file, output_record

prices_output_file.close()
