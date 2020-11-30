""""
SQL Injection Example
This function is the only one you are permitted
to modify for the lab assignment.

Note: if you aren't familiar with str.format, here
is a link to the docs:
https://docs.python.org/3/library/stdtypes.html#str.format
"""


def query(query_term: str) -> str:
    """
    Creation of SQL query that has injection vulnerability.
    You should be able to
        1) explain why this is vulnerable,
        2) demonstrate how to exploit this vulnerability, and
        3) modify this code to prevent SQL injection attack
    :param query_term:
    :return: str (the query)
    """
    # Never do this in the real world...
    if '%' in query_term:
        query_term = query_term.replace('%', '')
    if '"' in query_term:
        query_term = query_term.replace('"', '')
    q = 'SELECT * FROM account ' \
        'WHERE account.query_term = {} ' \
        'AND ' \
        'account.pw_hash LIKE "%{}%"'.format(query_term)
    return q
