import enum

NGINX_FLAGGED_VERSIONS = ('1.2',)
IIS_FLAGGED_VERSIONS = ('7.0',)

class WebSrvEnum(enum.Enum):
    nginx = 'nginx'
    iis = 'Microsoft IIS'
    other = 'unflagged'
    none = 'none listed'
    err = 'error occurred while checking this server for web server'
    disabled = 'web server check disabled',

def get_flagged_versions() -> dict[WebSrvEnum, tuple[str]]:
    return {WebSrvEnum.nginx: NGINX_FLAGGED_VERSIONS, 
            WebSrvEnum.iis: IIS_FLAGGED_VERSIONS}

class DirListEnum(enum.Enum):
    available = 'available'
    unavailable = 'unavailable'
    err = 'error occurred while checking this server for dir listing'
    disabled = 'dir listing check disabled'
    
class StatusEnum(enum.Enum):
    """Enum class for statuses. Format ruins enums so use another field for more detail."""
    good = 'good'
    bad_ip = 'bad IP given'
    response_err = 'failure in response, see logs or status'