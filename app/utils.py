from flask import jsonify
import pickle
import numpy as np
from .models import *

list_table_names = [
    'khoadaotao',
    'chuyennganh',
    'chuongtrinhdaotao',
    'sinhvien',
    'diemsinhvien',
    'chitietmonhoctheochuyennganh',
    'diemtuvan',
    'nguoidung'
]

list_table_objects = [
    KhoaDaoTao,
    ChuyenNganh,
    ChuongTrinhDaoTao,
    SinhVien,
    DiemSinhVien,
    ChiTietMonHocTheoChuyenNganh,
    DiemTuVan,
    NguoiDung
]

map_table = dict(zip(list_table_names, list_table_objects))


def make_response(data={}, status=200):
    '''
        - Make a resionable response with header
        - status default is 200 mean ok
    '''
    res = jsonify(data)
    # res.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5502')
    res.headers.add('Content-Type', 'application/json')
    res.headers.add('Accept', 'application/json')
    return res

def get_model(major, scores_dict):
    assert major in ['mmt', 'cnpm', 'khptdl', 'httt'], "Major not found."
    
    if major == 'khptdl':
        subj = ['nmlt', 'trr', 'ktdl', 'csdl']
    elif major == 'httt':
        subj = ['csdl', 'hqtcsdl', 'nmlt', 'ctdlgt']
    elif major == 'cnpm':
        subj = ['nmlt', 'lthdt', 'csdl']
    else:
        subj = ['ktmt', 'mmt', 'nmlt', 'hdh']
    
    scores = np.array([[np.nan if isinstance(scores_dict[i], str) else scores_dict[i] for i in subj]])

    with open(f'models/{major}.model', 'rb') as f:
        model = pickle.load(f)
        print(f"Load model {major} successfully!")

    probability = model.soft_predict(scores).reshape(-1)[1] * 100
    return round(probability, 2)

def make_data(data: dict = dict(), msg: str = "", status: str = "SUCCESS") -> dict:
    ret_data = dict(data=data, msg=msg, status_code=status_code[status])
    return ret_data