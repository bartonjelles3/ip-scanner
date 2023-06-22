import enum

class WebServerSoftwareEnum(enum.Enum):
    nginx = 'nginx'
    iis = 'Microsoft IIS'
    other = 'Unsupported web server.'
    none = 'No web server listed.'
    err = 'Web server software: An error occured while checking this server.'
    disabled = 'Web server software not checked.'

class DirListingEnum(enum.Enum):
    available = 'Directory listing: available at /'
    unavailable = 'Directory listing: unavailable at /'
    err = 'Directory listing: An error occured while checking this server.'
    disabled = 'Directory listing not checked.'
    
class StatusEnum(enum.Enum):
    """Enum class for statuses. Format ruins enums so use another field for more detail."""
    good = 'Status: Good.'
    bad_ip = 'Status: Failed. Bad IP given.'
    bad_response_code = 'Status: Failed. Bad response code, see logs or status...'
    bad_request = 'Status: Failed. Error occured while sending request, see logs or status...'
