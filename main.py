
from wifi_lib import conecta
import dht
import machine
import time
import urequests

d = dht.DHT11(machine.Pin(4))
rele = machine.Pin(2, machine.Pin.OUT)

while True:
    
    d.measure()
    temp = d.temperature()
    umid = d.humidity()
    print("Temp={}ºC Umid={}%".format(temp, umid))
    
    try:
        resposta = urequests.get("http://api.thingspeak.com/update?api_key=IAAJV4H0YHK47H61&field1={}&field2={}".format(temp, umid))
        print("Pagina acessada:")
        print(resposta.text)
        resposta.close()
    except Exception as e:
        print("Erro ao enviar dados:", e)
    
    if temp > 31 or umid > 70:
        rele.value(1)
    else:
        rele.value(0)
        
    print("Conectando...")
    station = conecta("sua-rede", "sua-senha")
    if not station.isconnected():
        print("Não conectado!")
    else:
        print("Conectado!")
        
    time.sleep(20)
    