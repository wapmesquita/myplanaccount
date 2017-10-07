from oauth2client import client
import constants

def getFlow(redirect_path):
    return client.flow_from_clientsecrets(constants.KEY, scope=constants.SCOPE, redirect_uri=redirect_path + constants.AUTH_PATH_NAME)
