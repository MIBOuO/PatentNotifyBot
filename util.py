from datetime import date, timedelta
from random import sample
from database import Database
import crawler_api

class Preference:
    def __init__(self, pref_string = '') -> None:
        self.count = 0
        self.section = []
        self._class = []
        self.subclass = []
        self.group = []
        self.subgroup = []
        
        if pref_string:
            for pref in pref_string.split('&'):
                ipc, count = pref.split('=')
                self.add(ipc, int(count))
                self.count += int(count)
        
    def add(self, ipc: str, times = 1):
        ipc_len = len(ipc)
        if ipc_len > 0:
            self.__add_helper(self.section, ipc[0], times)
        if ipc_len >= 3:
            self.__add_helper(self._class, ipc[:3], times)
        if ipc_len >= 4:
            self.__add_helper(self.subclass, ipc[:4], times)
        if ipc_len > 4:
            sep = ipc.find('/')
            self.__add_helper(self.subclass, ipc[:sep], times)
            if sep != -1:
                self.__add_helper(self.subgroup, ipc, times)

    def __add_helper(self, layer, item, times):
        prev_count = 0
        target_index = 0
        for i in range(len(layer)):
            ipc, count = layer[i]
            if item == ipc:
                layer[i][1] = count = count + times
                if i > 0 and count > prev_count:
                    layer[i-1], layer[i] = layer[i], layer[i-1]
                break
            if count >= times:
                target_index = i + 1
            prev_count = count
        else:
            layer.insert(target_index, times)

    def __str__(self) -> str:
        return '&'.join((f"{ipc}={count}" for ipc, count in self.subgroup))

def notify_all_users():
    targets = zip(
        [
            lambda pref: pref.subgroup,
            lambda pref: pref.group,
            lambda pref: pref.subclass,
            lambda pref: pref.section,
        ],
        [
            [0, 0.3, 0.6, 0.8],
            [0, 0.4, 0.7],
            [0],
            [0, 0.6]
        ]
    )
    database = Database()
    for id, pref in database.get_users():
        pref = Preference(pref)
        rec = []
        rand_num = 1
        for layer, tile in targets:
            index = 0
            acc_ipc_count = 0
            tile_len = len(tile)
            for ipc, ipc_count in layer(pref):
                acc_ipc_count += ipc_count
                patent_count = 0
                while index < tile_len and acc_ipc_count / pref.count >= tile[index]:
                    patent_count += 1
                    index += 1
                if patent_count == 0:
                    continue
                num, patents = database.get_patents(date.today() - timedelta(days=7), ipc = ipc, limit = 50)
                if num >= patent_count:
                    rec.extend(patents[:patent_count])
                else:
                    rec.extend(patents[:num])
                    patent_count = patent_count - num
                    num, patents = crawler_api.get_patents(date.today() - timedelta(days=7), ipc = ipc, limit = 50)
                    if num >= patent_count:
                        rec.extend(patents[:patent_count])
                    else:
                        rec.extend(patents[:num])
                        rand_num += patent_count - num
                    database.add_patents(patents)

                if index >= tile_len:
                    break
        num, patents = database.get_patents(date.today() - timedelta(days=7), limit = rand_num)
        rec.extend(patents[:rand_num])
        send_recommandation(id, rec)

def add_preference(id, ipcs):
    database = Database()
    _, pref = database.get_user(id)
    pref = Preference(pref)
    for ipc in ipcs:
        pref.add(ipc)
    database.add_user(id, str(pref))

def send_recommandation(id, rec):
    pass

        
