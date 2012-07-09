import os
import time


'''
Library to get a systems average load
'''
class check():

    '''
    Init the lib
    '''
    def __init_x_(self, params=None):
        self.params = params

    '''
    Check system requirements
    Should return True if requirements pass
    of a List of messages of any errors
    '''
    def requirements(self):
        messages = []
        if hasattr(os, 'getloadavg') and callable(getattr(os, 'getloadavg')):
            return True;
        else:
            messages.append('getloadavg() method not found in package os')
            return messages

    '''
    Run the script and return the data to be serialized
    Data should be ready to pass right into the Json handler
    '''
    def run(self):
        load = os.getloadavg()
        data = {'time': int(time.time()), '1_min': load[0], '5_min': load[1], '15_min': load[2]}
        return data


    '''
    Supplied funciton used to validate the output from the script
    Should return True if data passes validation or a list of errors
    if data fails validation
    '''
    def validate(self, data):
        messages = []
        if len(data) is not 4:
            messages.append('Data length was not expected, expected 4, got ' + str(len(data)))
        
        #for i in data:
        if data["time"] > int(time.time()) + 5 or data["time"] < int(time.time()) - 5:
            messages.append('Time appears to be wrong')
        
        if float(data["1_min"]) < 0.0 or float(data["1_min"]) > 9999:
            messages.append('The value of 1 minute load average appears wrong')
        
        if float(data["5_min"]) < 0.0 or float(data["5_min"]) > 9999:
            messages.append('The value of 5 minute load average appears wrong')
        
        if float(data["15_min"]) < 0.0 or float(data["15_min"]) > 9999:
            messages.append('The value of 15 minute load average appears wrong')
        
        if len(messages) is 0:
            return True
        else:
            return messages