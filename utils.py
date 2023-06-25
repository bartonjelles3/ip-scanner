import enum

NGINX_FLAGGED_VERSIONS = ('1.2',)
IIS_FLAGGED_VERSIONS = ('7.0',)

class WebSrvEnum(enum.Enum):
    nginx = 'nginx'
    iis = 'Microsoft IIS'
    other = 'Unsupported web server.'
    none = 'No web server listed.'
    err = 'Web server software: An error occurred while checking this server.'
    disabled = 'Web server software not checked.',

def get_flagged_versions() -> dict[WebSrvEnum, tuple[str]]:
    return {WebSrvEnum.nginx: NGINX_FLAGGED_VERSIONS, 
            WebSrvEnum.iis: IIS_FLAGGED_VERSIONS}

class DirListEnum(enum.Enum):
    available = 'Directory listing: available at /'
    unavailable = 'Directory listing: unavailable at /'
    err = 'Directory listing: An error occurred while checking this server.'
    disabled = 'Directory listing not checked.'
    
class StatusEnum(enum.Enum):
    """Enum class for statuses. Format ruins enums so use another field for more detail."""
    good = 'Status: Good.'
    bad_ip = 'Status: Failed. Bad IP given.'
    response_err = 'Status: Failed. Failure in response. See logs or status...'