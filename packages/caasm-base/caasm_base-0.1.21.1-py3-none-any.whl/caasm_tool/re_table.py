import re

VARIABLE_RE = re.compile(r"([a-z]|\d)([A-Z])")

PASSWORD_RE = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,20}$")

URL_RE = re.compile(r"^(?:([A-Za-z]+):)?(/{0,3})([0-9.\-A-Za-z]+)(?::(\d+))?(?:/([^?#]*))?(?:\?([^#]*))?(?:#(.*))?$")

INT_RE = re.compile(r"^\d+$")

FILE_ID = re.compile(r"^[a-zA-Z\d]{24}$")

TIME_RE = re.compile(r"^(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d$")
