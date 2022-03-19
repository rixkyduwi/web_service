
from werkzeug.security import generate_password_hash, check_password_hash

pswd=generate_password_hash("123")
print(pswd)