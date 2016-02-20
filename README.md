# Bee.i

## Description
A shell client for fetching beer data.

## Licensing information
The software licensed under MIT.

## Querying

Once data has been fetch querying is possible with `jq` and `grep`.


    # Find all product names
    ls . | xargs cat ./logs/ | grep ProductName | awk '{print $2}' | sort | uniq

    # With seek ahead and behind
    ls . | xargs cat ./logs/ | grep -A 50 -B 50 brewery
    
    # Mulitple expressions
    ls . | xargs cat ./logs/ | grep 'ProductName\|"ibu"'


## Useful docs to play around with..
+ SocketIO https://github.com/miguelgrinberg/python-socketio
+ Setting up *wheels* and *virtualenv* http://python-packaging-user-guide.readthedocs.org/en/latest/installing/
+ ChartJS http://www.chartjs.org/docs/
+ https://github.com/hotzenklotz/Flask-React-Webpack-Server/
+ https://github.com/foreverjs/forever
+ http://socket.io/get-started/chat/
+ http://preshing.com/20110920/the-python-with-statement-by-example/
