import pytest

test_data = [("10FA0E00", {'field1': 'Low',
                           'field2': '00',
                           'field3': '01',
                           'field4': '00',
                           'field5': '00',
                           'field6': '01',
                           'field7': '00',
                           'field8': 'Very High',
                           'field9': '00',
                           'field10': '00'}),
             ("00162B64", {'field1': 'Low',
                           'field2': '00',
                           'field3': '00',
                           'field4': '00',
                           'field5': '00',
                           'field6': '01',
                           'field7': '01',
                           'field8': 'Low',
                           'field9': '01',
                           'field10': '01'})
             ]

# Format_settings = array [sett_byte1 as dict {bit: [size, 'field_name']}, sett_byte2, sett_byte3, sett_byte4]
device_settings = [{0: [3, 'field1'],
                    3: [1, 'field2'],
                    4: [1, 'field3'],
                    5: [3, 'field4']},

                   {0: [1, 'field5'],
                    1: [1, 'field6'],
                    2: [1, 'field7'],
                    3: [3, 'field8'], },

                   {0: [1, 'field9'],
                    5: [1, 'field10']},
                   {}]

FORMAT_RULES = dict(
    field1={'0': 'Low',
            '1': 'reserved',
            '2': 'reserved',
            '3': 'reserved',
            '4': 'Medium',
            '5': 'reserved',
            '6': 'reserved',
            '7': 'High',
            },
    field4={'0': '00',
            '1': '10',
            '2': '20',
            '3': '30',
            '4': '40',
            '5': '50',
            '6': '60',
            '7': '70',
            },
    field8={'0': 'Very Low',
            '1': 'reserved',
            '2': 'Low',
            '3': 'reserved',
            '4': 'Medium',
            '5': 'High',
            '6': 'reserved',
            '7': 'Very High',
            }
)


def payload_to_list(payload: str) -> list[str]:
    bytes_list = []
    for i in range(0, len(payload), 2):
        byte_str = payload[i: i + 2]
        bit_str = "{:08b}".format(int(byte_str, base=16))
        bytes_list.append(bit_str[::-1])
    return bytes_list


def get_data_from_payload(payload: str) -> dict:
    # for big endian, reverse every second byte with first
    payload_big = payload_to_list(payload)
    # format payload to bits
    parsed_data = {}
    # for each byte in the payload get the bits and the corresponding field with settings for fields
    for sett_byte, current_byte in zip(device_settings, payload_big):
        for offset, (field_length, field_name) in sett_byte.items():
            bits_form = current_byte[offset: offset + field_length]
            # get the value with format rules
            if field_name in FORMAT_RULES:
                rule = FORMAT_RULES[field_name]
                parsed_data[field_name] = rule[str(int(bits_form, 2))]
            else:
                # if no format rule
                parsed_data[field_name] = '{:02x}'.format(int(bits_form, 2))

    return parsed_data


@pytest.mark.parametrize("payload, expected", test_data)
def test_get_data_from_payload(payload, expected):
    assert get_data_from_payload(payload) == expected
