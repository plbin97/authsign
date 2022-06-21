from appFactory import createApp

appInst = None

def getApp():
    """
    Get app
    :return:
    """
    if appInst is None:
        refreshApp()
    return appInst

def refreshApp():
    """
    create a new app that cover the original one
    :return:
    """
    global appInst
    appInst = createApp()
    appInst.config.update({
        "TESTING": True,
    })
    appInst.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    appInst.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    return appInst

