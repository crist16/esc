from datetime import datetime

mesesDic = {
    "01":'ENERO',
    "02":'FEBRERO',
    "03":'MARZO',
    "04":'ABRIL',
    "05":'MAYO',
    "06":'JUNIO',
    "07":'JULIO',
    "08":'AGOSTO',
    "09":'SEPTIEMBRE',
    "10":'OCTUBRE',
    "11":'NOVIEMBRE',
    "12":'DICIEMBRE'
}



def fecha_de_hoy():
    fecha_actual = datetime.now()
    fecha = fecha_actual.date()
    fecha_actual = fecha.strftime('%d/%m/%Y')

    mes_actual = fecha_actual.split("/")[1]
    for mes in  mesesDic:
        if mes == mes_actual:
            mes = mesesDic[mes]
            mesdehoy = mes

    fecha_diccionario = {
        "dia" : fecha_actual.split("/")[0],
        "mes" : mesdehoy,
        "year" : fecha_actual.split("/")[2]
    }
    return fecha_diccionario


