import time, logging
from flask import Flask, request

'''
This class will have a flask server to handle the APIs and keep 
track of all the queues. Server is set to run on localhost.
All queue data is stored in queue_data.
'''
localhost = __name__
app = Flask(localhost)
queue_data = {}
    
'''
This function will create a queue.
If it is there, it will return false since it was already created.
Otherwise, it will return True
'''
@app.route('/CreateQueue', methods=['POST'])
def CreateQueue() -> dict:
    queueName = request.form['queueName']
    if queueName not in queue_data:
        queue_data[queueName] = {'messages': []}
        return {'created': True}
    return {'created': False}
    # returns the created queue


'''
This function will send a message to the queue.
Based on delay, it will delay the system from sending the message.
If queue was created, it will return the 0-based index of message
inside the queue.
Otherwise, it returns an error.
'''
@app.route('/SendMessage', methods=['POST'])
def SendMessage() -> dict:
    d = request.form
    queueName=d['queueName']
    delayInMS=d['delayInMS']
    message=d['message']
    if queueName in queue_data:
        # Unsure what MS meant so assumed it was microservice
        # Assumed delay is in second units
        # Also need to cast because delay becomes a string
        time.sleep(int(delayInMS))
        # Add message to queue
        q = queue_data[queueName]['messages']
        if q:
            index = q[-1][0]+1
        else:
            index = 0
        q.append((index, message))
        return {'messageId': index}
    return {'error': 'Queue not found'}

'''
This function looks for the queue based on queueName.
If found, it returns the oldest message.
Otherwise, it returns an error that no message was received.
'''
@app.route('/ReceiveMessage', methods=['GET','POST'])
def ReceiveMessage() -> dict:
    queueName = request.form['queueName']
    if queueName in queue_data:
        q = queue_data[queueName]['messages']
        if q:
            return {'messageId': q[0][0], 'message': q[0][1]}
        else:
            return {'error': 'No messages in Queue'}
    return {'error': 'Queue not found.'}

'''
This function looks for the q where the messageId is found in the queue.
If not, it returns false as it was not deleted.
'''
@app.route('/DeleteMessage', methods=['DELETE'])
def DeleteMessage() -> dict:
    queueName = request.form['queueName']
    messageId = request.form['messageId']
    if queueName in queue_data:
        q = queue_data[queueName]['messages']
        query = list(filter(lambda x: x[0] == int(messageId), q))
        if query:
            if len(query) > 1:
                logging.debug('found multiple message id in deleting')
            target_id, target_msg = query[0]
            queue_data[queueName]['messages'].remove((target_id, target_msg))
            return {'wasDeleted': True}
    return {'wasDeleted': False}


if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
