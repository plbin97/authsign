from app import app, create_app

appInst = app


def getApp():
    """
    Get app
    :return:
    """
    return appInst


def refreshApp():
    """
    create a new app that cover the original one
    :return:
    """
    global appInst
    appInst = create_app()
    appInst.config.update({
        "TESTING": True,
    })
    appInst.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    appInst.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    return appInst


refreshApp()
