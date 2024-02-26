import re
import urllib.request
from urllib.error import URLError

from bs4 import BeautifulSoup

from src.custom_logging import setup_logger
from src.logic.language import ProviderError, get_href_by_language

logger = setup_logger(__name__)

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
cache_url_attempts = 0

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
VOE_PATTERN = re.compile(r"'hls': '(?P<url>.+)'")
STREAMTAPE_PATTERN = re.compile(r'get_video\?id=[^&\'\s]+&expires=[^&\'\s]+&ip=[^&\'\s]+&token=[^&\'\s]+\'')
# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_redirect_link_by_provider(site_url, internal_link, language):
    """
    Sets the priority in which downloads are attempted.
    First -> VOE download, if not available...
    Second -> Streamtape download, if not available...
    Third -> Vidoza download

    Parameters:
        site_url (String): serie or anime site.
        internal_link (String): link of the html page of the episode.
        language (String): desired language to download the video file in.

    Returns:
        get_redirect_link(): returns link_to_redirect and provider.
    """
    try:
        return get_redirect_link(site_url, internal_link, language, "Streamtape")
    except ProviderError:
        try:
            return get_redirect_link(site_url, internal_link, language, "Vidoza")
        except ProviderError:
            return get_redirect_link(site_url, internal_link, language, "VOE")


def get_redirect_link(site_url, html_link, language, provider):
    # if you encounter issues with captchas use this line below
    # html_link = open_captcha_window(html_link)
    html_response = urllib.request.urlopen(html_link)
    href_value = get_href_by_language(html_response, language, provider)
    link_to_redirect = site_url + href_value
    logger.debug("Link to redirect is: " + link_to_redirect)
    return link_to_redirect, provider
     

def find_cache_url(url, provider):
    global cache_url_attempts
    logger.debug("Enterd {} to cache".format(provider))
    try:
        html_page = urllib.request.urlopen(url)
    except URLError as e:
        logger.warning(f"{e}")
        logger.info("Trying again to read HTML Element...")
        if cache_url_attempts < 5:
            return find_cache_url(url, provider)
        else:
            logger.error("Could not find cache url HTML for {}.".format(provider))
            return 0
    try:
        if provider == "Vidoza":
            soup = BeautifulSoup(html_page, features="html.parser")
            cache_link = soup.find("source").get("src")
        elif provider == "VOE":
            cache_link = VOE_PATTERN.search(html_page.read().decode('utf-8')).group("url")
        elif provider == "Streamtape":
            cache_link = STREAMTAPE_PATTERN.search(html_page.read().decode('utf-8'))
            if cache_link is None:
                return find_cache_url(url, provider)
            cache_link = "https://" + provider + ".com/" + cache_link.group()[:-1]
            logger.debug(f"This is the found video link of {provider}: {cache_link}")
    except AttributeError as e:
        logger.error(f"ERROR: {e}")
        logger.info("Trying again...")
        if cache_url_attempts < 5:
            cache_url_attempts += 1
            return find_cache_url(url, provider)
        else:
            logger.error("Could not find cache url for {}.".format(provider))
            return 0
        
    logger.debug("Exiting {} to Cache".format(provider))
    return cache_link

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

