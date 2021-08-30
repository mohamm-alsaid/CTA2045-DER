#! /bin/python3
from pycta2045 import cta2045device as device
import pycta2045.models as models
import time
import matplotlib.pyplot as plt
from rich import pretty
pretty.install()

port = '/dev/ttyS7'
figsize = (50,50) # (w,h)
version = '40kw' # experiment version
ev = models.EV(max_cap=40,verbose=True,decay_rate=.08)
t_end = ev.t_end
dev = device.CTA2045Device(mode="DER",model=ev,comport=port)
log = dev.run()
print("LOG: ")
print(log)
log.to_csv('logs/DER_log.csv')
log = ev.get_all_records()

assert log is not None, "log is None"
log.to_csv("logs/ev_records_soc.csv")
log = log[['soc','power']]
x = log['soc']
y = log['power']
print('plotting soc...')
# log.plot(subplots=True,figsize=figsize)
log.plot(subplots=True)
plt.savefig(fname=f'figs/ev_records_soc_{version}.png')
plt.close()

plt.plot(x,y)
plt.savefig(f'figs/power_vs_soc_{version}.png')
plt.close()

log = ev.get_commodity_log()
assert log is not None, "log is None"
log.set_index('time',inplace=True)

log.to_csv("logs/ev_record_commodity.csv")
CAs = log[['Elect. Consumed - Cumulative (Wh)','EnergyTake - Cumulative (Wh)']]
IRs = log[['Elect. Consumed - Inst. Rate (W)']]

print('plotting time vs CA...')
# CAs.plot(figsize=figsize) # plot CA
CAs.plot() # plot CA
plt.savefig(fname=f'figs/ev_records_commodity_CA_{version}.png')
plt.close()

print('plotting time vs IR...')
# IRs.plot(figsize=figsize) # plot IR
IRs.plot() # plot IR
plt.savefig(fname=f'figs/ev_records_commodity_IR_{version}.png')
print('closing..')
plt.close()

