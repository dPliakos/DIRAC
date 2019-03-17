from DIRAC import S_OK, S_ERROR, gLogger, gConfig

def checkCAOfUser(user, CA):
    """ user, and CA are string.
    """

    userCA = gConfig.getValue('/Registry/Users/{}/CA'.format(user))

    gLogger.notice(userCA)

    if userCA is None:
        return S_ERROR("Not found")

    if userCA != CA:
        return S_ERROR("User CA not match the user's CA")

    return S_OK(True)
