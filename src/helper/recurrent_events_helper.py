import logging

def filterRecurrentEvent(m, y, events):
    logging.debug("$$$$ Filtering recurrent events (%s): %s-%s", len(events), m, y)
    list = []
    delta = y*100 + m
    for s in events:
        delta_begin = None
        delta_end = None
        fm = s['firstMonth']
        fy = s['firstYear']
        lm = s['lastMonth']
        ly = s['lastYear']

        if fm is None:
            fm = m - 1

        if fy is None:
            fy = y

        delta_begin = fy*100 + fm

        if delta_begin > delta and lm is None:
            continue

        if lm is None:
            lm = m + 1

        if ly is None:
            ly = y

        delta_end = ly*100 + lm

        if (delta_begin > delta_end):
            if (lm < fm) and (m >= lm):
                ly = y + 1
            if (m <= lm):
                fy = y - 1

        delta_begin = fy*100 + fm
        delta_end = ly*100 + lm

        if (delta_begin <= delta) and (delta_end >= delta):
            logging.debug('$$$$ Adding event %s', s['name'])
            list.append(s)
    return list
