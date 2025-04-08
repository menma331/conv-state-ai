class Config:
    CPM = 20  # $ за 1000 просмотров

    MIN_VIEWS = 50000
    MAX_VIEWS = 100000

    TARGET_FIXED = ((CPM * ((MIN_VIEWS + MAX_VIEWS) / 2 + MAX_VIEWS) / 2) / 1000)
    MIN_FIXED = (CPM * MIN_VIEWS) / 1000


config = Config()