import json

class SecData:
    def __init__(self, input_location):
        sec_input_filename = input_location + "sec.json"
        sec_external_id_type_input_filename = input_location + "sec_external_id_type.json"
        sec_external_input_filename = input_location + "sec_external.json"
        exchange_input_filename = input_location + "exchange.json"
        country_input_filename = input_location + "country.json"
        sec_price_type_input_filename = input_location + "sec_price_type.json"

        sec_input_file = open(sec_input_filename, "r")
        self.sec = []
        for record in sec_input_file:
            self.sec.append(json.loads(record))
        sec_input_file.close()
        
        self.sec_by_country = {}
        for record in self.sec:
            country_id = record["country_id"]
            sec_list = self.sec_by_country.get(country_id, [])
            sec_list.append(record)
            self.sec_by_country[country_id] = sec_list

        sec_external_input_file = open(sec_external_input_filename, "r")
        self.sec_external = []
        for record in sec_external_input_file:
            self.sec_external.append(json.loads(record))
        sec_external_input_file.close()

        self.sec_external_by_sec_id = {}
        for sec_external_info in self.sec_external:
            sec_id = sec_external_info["sec_id"]
            sec_external_list = self.sec_external_by_sec_id.get(sec_id, [])
            sec_external_list.append(sec_external_info)
            self.sec_external_by_sec_id[sec_id] = sec_external_list

        sec_external_id_type_input_file = open(sec_external_id_type_input_filename, "r")
        self.sec_external_id_type_by_id = {}
        for record in sec_external_id_type_input_file:
            sec_external_id_type_info = json.loads(record)
            sec_external_id_type_id = sec_external_id_type_info["sec_external_id_type_id"]
            self.sec_external_id_type_by_id[sec_external_id_type_id] = sec_external_id_type_info
        sec_external_id_type_input_file.close()

        self.sec_external_id_type_by_name = {}
        for record in self.sec_external_id_type_by_id.values():
            name = record["name"]
            self.sec_external_id_type_by_name[name] = record

        country_input_file = open(country_input_filename, "r")
        self.country = []
        for record in country_input_file:
            self.country.append(json.loads(record))
        country_input_file.close()

        self.country_by_country_code = {}
        for record in self.country:
            self.country_by_country_code[record["country_code"]] = record
        
        exchange_input_file = open(exchange_input_filename, "r")
        self.exchange = []
        for record in exchange_input_file:
            self.exchange.append(json.loads(record))
        exchange_input_file.close()

        self.exchange_by_country = {}
        for exchange_info in self.exchange:
            country_id = exchange_info["country_id"]
            exchange_list = self.exchange_by_country.get(country_id, [])
            exchange_list.append(exchange_info)
            self.exchange_by_country[country_id] = exchange_list

        self.exchange_by_exchange_code = {}
        for exchange_info in self.exchange:
            exchange_code = exchange_info["exchange_code"]
            exchange_list = self.exchange_by_exchange_code.get(exchange_code, [])
            exchange_list.append(exchange_info)
            self.exchange_by_exchange_code[exchange_code] = exchange_list

        sec_price_type_input_file = open(sec_price_type_input_filename, "r")
        self.sec_price_type = []
        for record in sec_price_type_input_file:
            self.sec_price_type.append(json.loads(record))
        sec_price_type_input_file.close()
