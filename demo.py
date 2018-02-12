from classification import Classification
from pprint import pprint


client_id = 'id'
client_secret = 'secret'

c = Classification(client_id, client_secret)

pprint(c.find_student_classification('MI-PYT', 'laskobor'))
