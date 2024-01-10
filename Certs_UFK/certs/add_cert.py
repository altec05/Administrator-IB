import fsb795
from pathlib import Path
from .models import Cerificate
from django.core.exceptions import ValidationError


def get_cert(cert_path):
    data = {}
    # Получаем сертификат
    # path = str(Path(cert_path).absolute())
    path = cert_path
    print('path abs =', path)
    cert = fsb795.Certificate(path)

    # Получаем атрибуты сертификата в читаемом виде
    cert_data = get_name(cert)
    cert_data_date = get_date(cert)

    data['name'] = cert_data[0]
    data['job'] = cert_data[1]
    data['start'] = cert_data_date[0]
    data['stop'] = cert_data_date[1]

    if get_sn(cert) != '':
        data['serial_number'] = get_sn(cert)
    else:
        data['serial_number'] = '0'

    try:
        if Cerificate.objects.get(serial_number=data['serial_number']):
            raise ValidationError('Серийный номер уже зарегистрирован!')
    except Exception as e:
        pass


    data['uc'] = get_uc(cert)
    data['snils'] = str(cert_data[2])
    data['inn'] = str(cert_data[3])
    data['ogrn'] = str(cert_data[4])
    data['city'] = str(get_city(cert))

    return data


# Получение реквизитов сертификата
def get_name(cert):
    cn = ''
    job = ''
    snils = ''
    inn = ''
    ogrn = ''

    sub, vlad_sub = cert.subjectCert()
    for key in sub.keys():

        if key == 'CN':
            cn = sub[key]
            try:
                cn = cn.encode().decode('utf-16-be')
            except:
                print(cn)
            finally:
                if not str(cn)[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                    cn = sub[key]
        if key == 'title' or key == 'T':
            temp = sub[key]
            try:
                temp = temp.encode().decode('utf-16-be')
            except:
                print(temp)
            finally:
                print(f'temp: {temp}')
            if temp == '':
                continue
            else:
                job = sub[key]
                try:
                    job = job.encode().decode('utf-16-be')
                except:
                    print(job)
                finally:
                    if not str(job)[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                        job = sub[key]
        if key == 'SNILS':
            snils = sub[key]
            try:
                snils = snils.encode().decode('utf-16-be')
            except:
                print(snils)
            finally:
                if not str(snils)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    snils = sub[key]
        if key == 'INN':
            inn = sub[key]
            try:
                inn = inn.encode().decode('utf-16-be')
            except:
                print(inn)
            finally:
                if not str(inn)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    inn = sub[key]
        if key == 'OGRN':
            ogrn = sub[key]
            try:
                ogrn = ogrn.encode().decode('utf-16-be')
            except:
                print(ogrn)
            finally:
                if not str(ogrn)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    ogrn = sub[key]
    return cn, job, snils, inn, ogrn


# Получение даты сертификата
def get_date(cert):
    valid = cert.validityCert()
    start = valid["not_before"].date()
    end = valid["not_after"].date()
    return start, end


# Получение серийного номера сертификата
def get_sn(cert):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                        5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                        13: 'D', 14: 'E', 15: 'F'}

    def decimal_to_hexadecimal(decimal):
        hexadecimal = ''
        while (decimal > 0):
            remainder = decimal % 16
            hexadecimal = conversion_table[remainder] + hexadecimal
            decimal = decimal // 16

        return hexadecimal

    hex_output = decimal_to_hexadecimal(cert.serialNumber())
    return hex_output


# Получение удостоверяющего центра сертификата
def get_uc(cert):
    uc = ''
    iss, vlad_is = cert.issuerCert()
    for key in iss.keys():
        if key == 'CN':
            uc = iss[key]
            try:
                return uc.encode().decode('utf-16-be')
            except:
                return uc


# Получение города сертификата
def get_city(cert):
    city = ''
    sub, vlad_sub = cert.subjectCert()
    for key in sub.keys():
        if key == 'L':
            city = sub[key]
            try:
                city = city.encode().decode('utf-16-be')
            except Exception as e:
                # mes.error('Получение города сертификата', f'При получении сведений о городе произошла ошибка конвертации!\n\nОшибка:\n[{e}]')
                city = sub[key]
            if not city[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                city = sub[key]
        if key == 'serialNumber':
            print(key, sub[key])
    return city