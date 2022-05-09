from pyModbusTCP.client import ModbusClient
import time

c = ModbusClient(host="challenges.france-cybersecurity-challenge.fr", port=502, unit_id=1, auto_open=True)
h_token = 0
regs = c.read_holding_registers(h_token, 32)

if regs:
    print("Token : ", ''.join( chr(_) for _ in regs))
else:
    print("read error")

time.sleep(7)

print("Sending commands")

r = 32
g = 126
b = 42

c_r = 0
c_g = 1
c_b = 2
c_m_b = 3

h_deb_r = 32
h_deb_g = 33
h_deb_b = 34
h_deb_m = 35


# remplir M avec 20 r / 50 g / 30 b
# augmenter le debit r g b
c.write_single_register(h_deb_r, 2)
c.write_single_register(h_deb_g, 5)
c.write_single_register(h_deb_b, 3)

count = 10

while( count > 0):
    c.write_single_coil(c_m_b, 0)
    c.write_single_coil(c_r ,1)
    c.write_single_coil(c_g ,1)
    c.write_single_coil(c_b ,1)
    time.sleep(1)
    count -= 1

# fermeture des vannes
c.write_single_coil(c_r, 0)
c.write_single_coil(c_g, 0)
c.write_single_coil(c_b, 0)
# remise a zero des debit
c.write_single_register(h_deb_r, 0)
c.write_single_register(h_deb_g, 0)
c.write_single_register(h_deb_b, 0)

time.sleep(1)

# augmenter debit de M
c.write_single_register(h_deb_m, 5)

# ouvrir vanne M
count = 20
while( count > 0):
    #c.write_single_coil(c_m_h, 0)
    c.write_single_coil(c_r, 0)
    c.write_single_coil(c_g, 0)
    c.write_single_coil(c_b, 0)
    c.write_single_coil(c_m_b, 1)
    time.sleep(1)
    count -= 1

# fermer M bas
c.write_single_coil(c_m_b, 0)


# remplir avec 12 r / 76 g / 12 b
# regler les debits

c.write_single_register(h_deb_r, 4)
c.write_single_register(h_deb_g, 4)
c.write_single_register(h_deb_b, 4)

count = 19
while( count > 0 ):
    c.write_single_coil(c_m_b, 0)
    if count > 16:
        c.write_single_coil(c_r, 1)
        c.write_single_coil(c_b, 1)
    else:
        c.write_single_coil(c_r, 0)
        c.write_single_coil(c_b, 0)

    c.write_single_coil(c_g, 1)

    time.sleep(1)
    count -= 1


# fermeture des vannes
c.write_single_coil(c_r, 0)
c.write_single_coil(c_g, 0)
c.write_single_coil(c_b, 0)
# remise a zero des debit
c.write_single_register(h_deb_r, 0)
c.write_single_register(h_deb_g, 0)
c.write_single_register(h_deb_b, 0)

time.sleep(1)


# augmenter debit de M
c.write_single_register(h_deb_m, 5)

# ouvrir vanne M
count = 20
while( count > 0):
#c.write_single_coil(c_m_h, 0)
    c.write_single_coil(c_r, 0)
    c.write_single_coil(c_g, 0)
    c.write_single_coil(c_b, 0)
    c.write_single_coil(c_m_b, 1)
    time.sleep(1)
    count -= 1

# fermer M bas
c.write_single_coil(c_m_b, 0)
