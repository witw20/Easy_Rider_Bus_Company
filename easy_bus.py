import json


def main():
    error_dict = {'bus_id': 0, 'stop_id': 0, 'stop_name': 0, 'next_stop': 0,\
                    'stop_type': 0, 'a_time': 0}
    total_error = 0
    json_str = input()
    bus_data = json.loads(json_str)

    # check for each data type
    for bus in bus_data:
        if isinstance(bus['bus_id'], int) == False:
            error_dict['bus_id'] += 1
        if isinstance(bus['stop_id'], int) == False:
            error_dict['stop_id'] += 1
        if isinstance(bus['stop_name'], str) == False:
            error_dict['stop_name'] += 1
        if isinstance(bus['next_stop'], int) == False:
            error_dict['next_stop'] += 1
        if isinstance(bus['stop_type'], str) == False or \
            len(str(bus['stop_type'])) != 1: # should be a char
            error_dict['stop_type'] += 1
        if isinstance(bus['a_time'], str) == False:
            error_dict['a_time'] += 1

    # sum up all the errors
    for i in error_dict.values():
        total_error += i

    print(f'Type and required field validation: {total_error} errors')
    if total_error > 0:
        for k, v in error_dict.items():
            print(f'{k}: {v}')


if __name__ == '__main__':
    main()
