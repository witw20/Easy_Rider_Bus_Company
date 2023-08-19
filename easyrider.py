import re
import json


def main():
    json_str = input()
    bus_data = json.loads(json_str)
    # validate(bus_data)
    # bus_info(bus_data)
    # check_stop(bus_data)
    # check_time(bus_data)
    check_od_stop(bus_data)


def check_od_stop(bus_data):
    start_finish_stops = set()
    stops_info = dict()
    transfer_stops = set()
    od_stops = set()

    for bus in bus_data:
        stops_info.setdefault(bus["stop_name"], 0)
        stops_info[bus["stop_name"]] += 1
        if bus["stop_type"] == "S" or bus["stop_type"] == "F":
            start_finish_stops.add(bus["stop_name"])
        if bus["stop_type"] == "O":
            od_stops.add(bus["stop_name"])

    for stop, bus_count in stops_info.items():
        if bus_count > 1:
            transfer_stops.add(stop)

    print("On demand stops test:")
    wrong_stops = (od_stops & start_finish_stops) | (od_stops & transfer_stops)
    if wrong_stops:
        print("Wrong stop type:", sorted(list(wrong_stops)))
    else:
        print("OK")


def check_time(bus_data):
    print("Arrival time test:")
    time_errors = dict()
    error_flag = False
    for bus in bus_data:
        time_errors.setdefault(bus["bus_id"], {"time": "00:00", "flag": False})
        if if_later(time_errors[bus["bus_id"]]["time"], bus["a_time"]):
            time_errors[bus["bus_id"]]["time"] = bus["a_time"]
        elif time_errors[bus["bus_id"]]["flag"] is False:
            print(f'bus_id line {bus["bus_id"]}: wrong time on {bus["stop_name"]}')
            time_errors[bus["bus_id"]]["flag"] = True
            error_flag = True
    if error_flag is False:
        print("OK")


def if_later(time1, time2):
    hour1, min1 = list(map(int, time1.split(":")))
    hour2, min2 = list(map(int, time2.split(":")))
    if hour2 > hour1 or (hour2 == hour1 and min2 > min1):
        return True
    else:
        return False


def check_stop(bus_data):
    route_info = dict()
    start_stops = set()
    stops_info = dict()
    finish_stops = set()

    for bus in bus_data:
        route_info.setdefault(bus["bus_id"], {"start_stop": None, "finish_stop": None})
        stops_info.setdefault(bus["stop_name"], 0)
        stops_info[bus["stop_name"]] += 1
        if bus["stop_type"] == "S":
            route_info[bus["bus_id"]]["start_stop"] = bus["stop_name"]
            start_stops.add(bus["stop_name"])
        if bus["stop_type"] == "F":
            route_info[bus["bus_id"]]["finish_stop"] = bus["stop_name"]
            finish_stops.add(bus["stop_name"])

    for route, info in route_info.items():
        if info["start_stop"] is None or info["finish_stop"] is None:
            print(f"There is no start or end stop for the line: {route}.")
            quit()

    print(f"Start stops: {len(start_stops)}", sorted(start_stops))
    transfer_stops = list()
    for stop, bus_count in stops_info.items():
        if bus_count > 1:
            transfer_stops.append(stop)
    print(f"Transfer stops: {len(transfer_stops)}", sorted(transfer_stops))
    print(f"Finish stops: {len(finish_stops)}", sorted(finish_stops))


def bus_info(bus_data):
    info_dict = dict()
    for bus in bus_data:
        info_dict.setdefault(bus["bus_id"], 0)
        info_dict[bus["bus_id"]] += 1
    print("Line names and number of stops:")
    for k, v in info_dict.items():
        print(f"bus_id: {k}, stops: {v}")


def validate(bus_data):
    validation = {'stop_name': {'type': str,
                                'format': r'^([A-Z]\w+ ?)+(Road|Avenue|Boulevard|Street)$'},
                  'stop_type': {'type': str, 'format': r'^[SOF]?$'},
                  'a_time': {'type': str,
                             'format': r'^([01]\d|2[0-3]):([0-5]\d)$'}}
    error_dict = {'stop_name': 0, 'stop_type': 0, 'a_time': 0}

    # check for each data type
    for bus in bus_data:
        for error in error_dict:
            if isinstance(bus[error], validation[error]['type']) is False \
                    or not re.match(validation[error]['format'], bus[error]):
                error_dict[error] += 1

    print(f'Format validation: {sum(error_dict.values())} errors')

    for k, v in error_dict.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
