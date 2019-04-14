def site2name(site):
    # 深股（海信是港股）

    if 'sz002668' in site:
        return 'aoma'
    elif 'sh600690' in site:
        return 'haier'
    elif 'sz002242' in site:
        return 'jiuyang'
    elif 'sh603726' in site:
        return 'langdi'
    elif 'sz002032' in site:
        return 'suboer'
    elif 'sz002759' in site:
        return 'tianji'
    elif 'sh603996' in site:
        return 'zhongxin'
    elif 'sz000651' in site:
        return 'geli'
    elif 'sz002508' in site:
        return 'laoban'
    elif 'sz000100' in site:
        return 'TCL'
    elif 'sz000333' in site:
        return 'meidi'
    elif 'sh600839' in site:
        return 'changhong'
    elif 'sz000921' in site:
        return 'haixing'
