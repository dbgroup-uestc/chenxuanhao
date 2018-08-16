# -*- coding: gbk -*
from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS = 6371  #����ƽ���뾶��6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    "��haversine��ʽ�������������ľ��롣"
    # ��γ��ת���ɻ���
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance

EARTH_REDIUS = 6378.137


lat1, lon1 = (22.599578, 113.973129)  # ����Ұ������԰(��㣩
lat2, lon2 = (22.6986848, 114.3311032)  # ����ƺɽվ (�ٶȵ�ͼ��ࣺ38.3km)
d2 = get_distance_hav(lat1, lon1, lat2, lon2)
print(d2)

lat2, lon2 = (39.9087202, 116.3974799)  # �����찲��(1938.4KM)
d2 = get_distance_hav(lat1, lon1, lat2, lon2)
print(d2)

lat2, lon2 = (34.0522342, -118.2436849)  # ��ɼ�(11625.7KM)
d2 = get_distance_hav(lat1, lon1, lat2, lon2)
print(d2)
