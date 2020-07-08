hosts = {"dev": "http://10.0.20.125",
         "sandbox": "http://10.0.10.116"}
cacluster = {
    "dev": {
        "username": 'caclient', "password": '6AH7vbrkMWnfK',
        "cluster": ['10.0.20.104', '10.0.20.105', '10.0.20.106']
    },

    "sandbox": {
        "username": 'caclient', "password": 'brT4Kn27RQs',
        "cluster": ['10.0.10.104', '10.0.10.105', '10.0.10.106']
    }
}
bootstrap_servers = {
    "dev": ['10.0.20.107:9092', '10.0.20.108:9092', '10.0.20.109:9092']
}