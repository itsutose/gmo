response_data = {'status': 5, 
                 'messages': [{'message_code': 'ERR-5201', 
                               'message_string': 'MAINTENANCE. Please wait for a while'}]
                }

print(response_data['messages'][0]['message_code'])
print(response_data['messages'][0]['message_string'])