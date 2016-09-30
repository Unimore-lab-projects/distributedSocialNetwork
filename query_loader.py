import os

PATH = os.path.dirname(os.path.abspath(__file__))


def load_query(query_name):
    with open('%s/sql/%s.sql' % (PATH, query_name), 'r') as query:
        return query.read().replace('\n', ' ').replace('\t', ' ')
