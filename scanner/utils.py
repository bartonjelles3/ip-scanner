import enum

NGINX_FLAGGED_VERSIONS = ('1.2',)
IIS_FLAGGED_VERSIONS = ('7.0',)

class WebSrvEnum(str, enum.Enum):
    nginx = 'nginx'
    iis = 'Microsoft IIS'
    other = 'Unflagged'
    none = 'None listed'
    err = 'Error occurred while checking this server for web server'
    disabled = 'Web server check disabled',

def get_flagged_versions() -> dict[WebSrvEnum, tuple[str]]:
    return {WebSrvEnum.nginx: NGINX_FLAGGED_VERSIONS, 
            WebSrvEnum.iis: IIS_FLAGGED_VERSIONS}

class DirListEnum(str, enum.Enum):
    available = 'Available'
    unavailable = 'Unavailable'
    err = 'Error occurred while checking this server for dir listing'
    disabled = 'Dir listing check disabled'
    
class StatusEnum(str, enum.Enum):
    """Enum class for statuses. Format ruins enums so use another field for more detail."""
    good = 'Good'
    bad_ip = 'Bad IP given'
    response_err = 'Failure in response, see logs or status...'