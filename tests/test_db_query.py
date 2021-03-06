from tdmq.db import list_descriptions_in_table
from tdmq.db import get_object
from tdmq.db import list_sensors_in_db
from tdmq.db import get_scalar_timeseries_data

from datetime import datetime, timedelta
import json
import os
root = os.path.dirname(os.path.abspath(__file__))


def test_db_list_sensor_types(db):
    sensor_types = json.load(
        open(os.path.join(root, 'data/sensor_types.json')))['sensor_types']
    data = list_descriptions_in_table(db, 'sensor_types')
    assert len(sensor_types) == len(data)
    assert data == sensor_types


def test_list_sensors(db):
    sensors = json.load(
        open(os.path.join(root, 'data/sensors.json')))['sensors']
    data = list_descriptions_in_table(db, 'sensors')
    assert len(sensors) == len(data)
    assert data == sensors


def test_db_get_sensor(db):
    sensors = json.load(
        open(os.path.join(root, 'data/sensors.json')))['sensors']
    for s in sensors:
        assert s == get_object(db, 'sensors', s['code'])


def test_db_get_sensor_type(db):
    sensor_types = json.load(
        open(os.path.join(root, 'data/sensor_types.json')))['sensor_types']
    for s in sensor_types:
        assert s == get_object(db, 'sensor_types', s['code'])


def test_list_sensors_with_args(db):
    sensors = json.load(
        open(os.path.join(root, 'data/sensors.json')))['sensors']
    sensors_by_code = dict((s['code'], s) for s in sensors)
    args = {}
    args['footprint'] = {'type': 'circle',
                         'center':  {'type': 'Point',
                                     'coordinates': [9.2215, 30.0015]},
                         'radius': 100000}
    args['after'] = '2019-05-02T11:00:00Z'
    args['before'] = '2019-05-02T11:50:25Z'
    data = list_sensors_in_db(db, args)
    for d in data:
        assert d['code'] in sensors_by_code
        assert d['stypecode'] == sensors_by_code[d['code']]['stypecode']


def test_get_scalar_timeseries_data(db):
    def to_dt(s):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    args = {}
    args['bucket'] = timedelta(seconds=1)
    args['op'] = 'sum'
    args['after'] = '2019-05-02T11:00:00Z'
    args['before'] = '2019-05-02T11:50:35Z'
    sensors = json.load(
        open(os.path.join(root, 'data/sensors.json')))['sensors']
    measures = json.load(
        open(os.path.join(root, 'data/measures.json')))['measures']
    sensors_by_code = dict((s['code'], s) for s in sensors)
    timebase = to_dt(args['after'])
    deltas_by_code = {}
    values_by_code = {}
    for m in measures:
        deltas_by_code.setdefault(m['sensorcode'], []).append(
            (to_dt(m['time']) - timebase).total_seconds())
        values_by_code.setdefault(m['sensorcode'], []).append(
            m['measure']['value'])
    for code in sensors_by_code:
        args['code'] = code
        result = get_scalar_timeseries_data(db, args)
        assert result['timebase'] == args['after']
        assert result['timedelta'] == deltas_by_code[code]
        assert result['data'] == values_by_code[code]


def test_get_scalar_timeseries_data_empty(db):
    sensors = json.load(
        open(os.path.join(root, 'data/sensors.json')))['sensors']
    sensors_by_code = dict((s['code'], s) for s in sensors)
    args = {}
    args['bucket'] = timedelta(seconds=3)
    args['op'] = 'sum'
    args['after'] = '2010-05-02T11:00:00Z'
    args['before'] = '2010-05-02T11:50:25Z'
    for code in sensors_by_code:
        args['code'] = code
        result = get_scalar_timeseries_data(db, args)
        assert result['timebase'] == args['after']
        assert result['timedelta'] == []
        assert result['data'] == []
