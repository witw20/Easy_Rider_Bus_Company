import re
import json


def main():
    validation = {'stop_name': {'type': str,
                                'format': r'^([A-Z]\w+ ?)+(Road|Avenue|Boulevard|Street)$'},
                  'stop_type': {'type': str, 'format': r'^[SOF]?$'},
                  'a_time': {'type': str,
                             'format': r'^([01]\d|2[0-3]):([0-5]\d)$'}}
    error_dict = {'stop_name': 0, 'stop_type': 0, 'a_time': 0}
    json_str = input()
    bus_data = json.loads(json_str)

    # check for each data type
    for bus in bus_data:
        for error in error_dict:
            if isinstance(bus[error], validation[error]['type']) is False \
                    or not re.match(validation[error]['format'], bus[error]):
                error_dict[error] += 1

    print(f'Format validation: {sum(error_dict.values())} errors')

    # if sum(error_dict.values()) > 0:
    #     for k, v in error_dict.items():
    #         print(f'{k}: {v}')
    for k, v in error_dict.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
