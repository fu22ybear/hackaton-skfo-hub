import os
from logging import Logger

from injector import Injector
import matplotlib.pyplot as plt
from comtrade import Comtrade

from oscillogram_analyzer.di import DI
from oscillogram_analyzer.config import Config


di = Injector(modules=[DI()])

logger = di.get(Logger)
config = di.get(Config)

oscillograms_dir = os.path.join(os.getcwd(), config.oscillograms_store_dir)
osc = Comtrade(ignore_warnings=True)
osc.load(os.path.join(oscillograms_dir, '02JUL235.cff'))

logger.info("Trigger time = {}s".format(osc.trigger_time))
logger.info(osc.station_name)
logger.info(osc.rec_dev_id)
logger.info(osc.cfg_summary())
logger.info(osc.analog_phases)
logger.info(osc.frequency)

plt.figure()
plt.plot(osc.time, osc.analog[0])
plt.plot(osc.time, osc.analog[1])
plt.plot(osc.time, osc.digital[0])
plt.plot(osc.time, osc.digital[1])
plt.legend([
    osc.analog_channel_ids[0],
    osc.analog_channel_ids[1],
    osc.digital_channel_ids[0],
    osc.digital_channel_ids[1],
])
plt.show()
