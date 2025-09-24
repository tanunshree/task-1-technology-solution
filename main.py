import json
import unittest
import datetime
from datetime import datetime, timezone, timedelta

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def iso_to_unix_ms(iso_timestamp_str):
    try:
        dt_object = datetime.strptime(iso_timestamp_str, ISO_FORMAT)
    except ValueError:
        return None

    dt_object = dt_object.replace(tzinfo=timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    time_diff = dt_object - epoch
    total_seconds = time_diff.total_seconds()
    unix_ms = int(total_seconds * 1000)

    return unix_ms


with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):

    location_parts = jsonObject.get('location', '').split('/')

    location_block = {
        'country': location_parts[0],
        'city': location_parts[1],
        'area': location_parts[2],
        'factory': location_parts[3],
        'section': location_parts[4]
    }

    data_block = {
        'status': jsonObject.get('operationStatus'),
        'temperature': jsonObject.get('temp')
    }

    transformed_record = {
        'deviceID': jsonObject.get('deviceID'),
        'deviceType': jsonObject.get('deviceType'),
        'timestamp': jsonObject.get('timestamp'),
        'location': location_block,
        'data': data_block,
    }

    return transformed_record


def convertFromFormat2(jsonObject):

    iso_ts_str = jsonObject.get('timestamp')
    unix_ms_ts = iso_to_unix_ms(iso_ts_str)

    device_info = jsonObject.get('device', {})
    data_source = jsonObject.get('data', {})

    location_block = {
        'country': jsonObject.get('country'),
        'city': jsonObject.get('city'),
        'area': jsonObject.get('area'),
        'factory': jsonObject.get('factory'),
        'section': jsonObject.get('section')
    }

    transformed_record = {
        'deviceID': device_info.get('id'),
        'deviceType': device_info.get('type'),
        'timestamp': unix_ms_ts,
        'location': location_block,
        'data': data_source,
    }

    return transformed_record


def main(jsonObject):

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 1 failed')

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 2 failed')


if __name__ == '__main__':
    unittest.main()
