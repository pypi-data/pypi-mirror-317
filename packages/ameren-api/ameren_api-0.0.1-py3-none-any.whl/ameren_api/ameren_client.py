"""Ameren API Client."""
import logging

import httpx
import json
import datetime
from bs4 import BeautifulSoup
from types import SimpleNamespace
from urllib.parse import urlparse,parse_qs

from .errors import AmerenError
#from .models.base import 

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.StreamHandler())
_LOGGER.setLevel(logging.INFO)

def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)

class AmerenClient():
    """Ameren API Client"""
    def __init__(
        self,
        username,
        password,
        debug=False,
    ):
        if debug:
            _enable_debug_logging()
        
        self._username = username
        self._password = password
        self._client_id = '86e63c1f-eefb-46d3-b2e2-1ac54af179fb'
        self._redirect_uri = 'https://www.ameren.com'
        self._scope = 'openid profile ismemberof registration imp_role imp_username imp_email outage payment stop_start_service programs alerts account_mgmt READ:ENRICHMENT:ADDRESS READ:CUSTOMER:PREMISES READ:CUSTOMER:PARTY READ:CUSTOMER:OUTAGE WRITE:CUSTOMER:OUTAGE READ:CUSTOMER:BILLACCOUNT'
        self._response_mode = 'form_post'
        self._arc_values = 'amerenrestlogin'
        self._xclient_sku = 'ID_NET461'
        self._xclient_ver = '5.3.0.0'
        self._headers = None
        self._login_provider = 'https://login.eiam.ece.ameren.com'
        self._api_provider = 'https://naapi2-read.bidgely.com/v2.0/dashboard/users/'

    def get_unix_timestamp_for_date(self,date_str):
        """Gets the start and end Unix timestamps for a given date string."""

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        start_timestamp = int(datetime.datetime.combine(date, datetime.time.min).timestamp())
        end_timestamp = int(datetime.datetime.combine(date, datetime.time.max).timestamp())

        return start_timestamp, end_timestamp

    async def _init_authentication(self, session):
        """Initialize Authentication with Ameren"""
        try:
            request_url = f'{self._login_provider}/json/realms/root/realms/ameren/authenticate?authIndexType=service&authIndexValue=amerenrestlogin'
            headers = {
                'Content-Type': 'application/json'
            }
            
            _LOGGER.debug("Getting Cookies From Ameren (URL): https://www.ameren.com/missouri/residential/manage-my-energy-use")
            getcookies = await session.get('https://www.ameren.com/missouri/residential/manage-my-energy-use')

            _LOGGER.debug("Getting Authentication Initiation from Ameren (URL): "+request_url)
            authinit = await session.post(request_url,headers=headers)
            authinittext = authinit.text
            _LOGGER.debug("Auth Init JSON: "+authinittext)
            authinitjson = json.loads(authinittext)
            authinitjson['callbacks'][1]['input'][0]['value'] = self._username
            authinitjson['callbacks'][2]['input'][0]['value'] = self._password
            return authinitjson
        except Exception as error:
            raise AmerenError(400, error)

    async def _authenticate(self, session, authinitjson):
        """Authenticate with Ameren"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Origin': 'https://www.ameren.com',
                'Referer': 'https://www.ameren.com/',
                'Accept-Api-Version': 'resource=2.0, protocol=1.0'
            }
            _LOGGER.debug("Authenticating with Ameren (URL): "+f'{self._login_provider}/json/realms/root/realms/ameren/authenticate?authIndexType=service&authIndexValue=amerenrestlogin')
            _LOGGER.debug("Authenticating with Ameren (Data): "+json.dumps(authinitjson))
            auth = await session.post(f'{self._login_provider}/json/realms/root/realms/ameren/authenticate?authIndexType=service&authIndexValue=amerenrestlogin',data=json.dumps(authinitjson),headers=headers)
            _LOGGER.debug("Auth Response: "+auth.text)
            return auth
        except Exception as error:
            raise AmerenError(400, error)

    async def _initiate_fr_login(self, session):
        """Initiate ForgeRock Login"""
        try:
            request_url = 'https://www.ameren.com/api/ameren/login/initiatefrlogin'
            _LOGGER.debug("Initiating ForgeRock Login (URL): "+request_url)
            initiatefr = await session.get(request_url)
            frtext = BeautifulSoup(initiatefr.text, "html.parser")
            form = frtext.find("form")  # Find the first form on the page
            action_url = form.get("action")  # Extract the "action" attribute
            _LOGGER.debug("Action URL: "+action_url)
            return action_url
        except Exception as error:
            raise AmerenError(400, error)

    async def _external_login(self, session, action_url):
        """External Login"""
        try:
            _LOGGER.debug("External Login (URL): "+f'https://www.ameren.com{action_url}')
            externalauth = await session.post(f'https://www.ameren.com{action_url}')
            redirect = externalauth.headers['Location']
            _LOGGER.debug("Redirect URL: "+redirect)
            authorize = await session.get(redirect)
            authtext = authorize.text
            authsoup = BeautifulSoup(authtext, 'html.parser')
            #_LOGGER.debug("Auth Soup: "+str(authsoup))
            params = {
                'iss' : authsoup.find_all("input",{"name":"iss"})[0]['value'],
                'code': authsoup.find_all("input",{"name":"code"})[0]['value'],
                'state': authsoup.find_all("input",{"name":"state"})[0]['value'],
                'client_id' : self._client_id
            }

            initcallback = await session.post('https://www.ameren.com/',data=params)
            redirect = initcallback.headers['Location']

            callback = await session.get('https://www.ameren.com'+redirect)
            redirect = callback.headers['Location']

            home = await session.get('https://www.ameren.com/account/prot/dashboard/home?')
            homesoup = BeautifulSoup(home.text,'html.parser')

            requestverificationtoken = homesoup.find_all("input",{"name":"__RequestVerificationToken"})[0]['value']
            _LOGGER.debug("Request Verification Token: "+requestverificationtoken)
            return requestverificationtoken
        except Exception as error:
            raise AmerenError(400, error)

    async def _bidgely_login(self, session, requestverificationtoken):
        """Login to Bidgely"""
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.ameren.com',
                'Referer':'https://www.ameren.com/account/prot/dashboard/home?',
            }
            params = {
                '__RequestVerificationToken' : requestverificationtoken
            }
            bidgelysaml = await session.post('https://www.ameren.com/api/ameren/AccountSummaryStatus/PostSAMLToBidgely?requestPath=dashboard/home',data=params,headers=headers)
            samlresponse = BeautifulSoup(bidgelysaml.text,'html.parser')
            #_LOGGER.debug("SAML Response: "+str(samlresponse))
            #for input in samlresponse.find_all("input"):
            #    _LOGGER.debug("Input: "+str(input))
            params = {
                'SAMLResponse': samlresponse.find_all("input",{"name":"SAMLResponse"})[0]['value'],
                'RelayState': samlresponse.find_all("input",{"name":"RelayState"})[0]['value']
            }

            postsaml = await session.post('https://login.eiam.ece.ameren.com/Consumer/metaAlias/ameren/sp',data=params)
            redirect = postsaml.headers['Location']

            idpsso = await session.get(redirect)
            samlresponse = BeautifulSoup(idpsso.text,'html.parser')

            params = {
                'SAMLResponse': samlresponse.find_all("input",{"name":"SAMLResponse"})[0]['value']
            }

            bidgelyauth = await session.post('https://ssoprod.bidgely.com/prod-na/10057/saml/acs',data=params)
            redirect = bidgelyauth.headers['Location']
            _LOGGER.debug("Bidgely Auth Redirect URL: "+redirect)

            bidgelyuuid = urlparse(redirect)
            uuid = parse_qs(bidgelyuuid.query)['uuid'][0]
            _LOGGER.debug("Bidgely UUID: "+uuid)

            bidgelysso = await session.get(redirect)

            bidgelysession = await session.get('https://naapi2-read.bidgely.com/v2.0/web/web-session/1615791583919v1kR7AA9cu3_pV0jGqgMFLqSPVllGlrbp8c2w5wdXHJHJXuuqpc37K1EThkyH_6pCtrs_fAimxtb7Wp1rUElCyqQ==?pilotId=10057&clientId=ameren-dashboard')
            token = bidgelysession.json()['payload']['tokenDetails']['accessToken']                                                                 
            return token,uuid
        except Exception as error:
            raise AmerenError(400, error)

    async def _get_token(self,session) -> str:
        """Get a token from the Ameren/Bidgely API"""
        try:
            authinitjson = await self._init_authentication(session)
            auth = await self._authenticate(session, authinitjson)
            action_url = await self._initiate_fr_login(session)
            requestverificationtoken = await self._external_login(session, action_url)
            token = await self._bidgely_login(session, requestverificationtoken)
            return token

        except Exception as error:
            raise AmerenError(400, error)
        
    async def _get_request(self, end_url: str) -> dict:
        """Perform GET request to API endpoint."""

        async with httpx.AsyncClient() as session:
            token,uuid = await self._get_token(session)
            _LOGGER.debug("Getting Request URL (BASE): "+self._api_provider)
            _LOGGER.debug("Getting Request URL (ENDPOINT): "+end_url)
            _LOGGER.debug("Getting Request URL (UUID): "+uuid)
            request_url = f"{self._api_provider}{uuid}{end_url}"
            if token:
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                _LOGGER.debug("Request URL: "+request_url)
                resp = await session.get(f"{request_url}", headers=headers)
                response = resp
                responsetext = resp.text
                response_json = json.loads(resp.text,object_hook=lambda d: SimpleNamespace(**d))
                if response.status_code >= 400:
                    raise AmerenError(response.status_code, responsetext)
                return response_json
            raise AmerenError(400, "Bad Credentials")
        
    async def get_daily_usage(self,date_str) -> dict:
        """Get daily usage for an account."""
        start,end = self.get_unix_timestamp_for_date(date_str)
        end_url = f"/usage-chart-details?measurement-type=ELECTRIC&mode=day&start={start}&end={end}&date-format=DATE_TIME&locale=en_US&next-bill-cycle=false&show-at-granularity=true&skip-ongoing-cycle=false"
        return await self._get_request(end_url)
    
    async def get_monthly_usage(self,date_str) -> dict:
        """Get monthly usage for an account based on END date of month."""
        start,end = self.get_unix_timestamp_for_date(date_str)
        end_url = f"/usage-chart-details?measurement-type=ELECTRIC&mode=month&start=0&end={end}&date-format=DATE_TIME&locale=en_US&next-bill-cycle=false&show-at-granularity=true&skip-ongoing-cycle=false"
        return await self._get_request(end_url)
    
    async def get_yearly_usage(self,date_str) -> dict:
        """Get yearly usage for an account based on END date of year."""
        start,end = self.get_unix_timestamp_for_date(date_str)
        end_url = f"/usage-chart-details?measurement-type=ELECTRIC&mode=year&start=0&end={end}&date-format=DATE_TIME&locale=en_US&next-bill-cycle=false&show-at-granularity=true&skip-ongoing-cycle=false"
        return await self._get_request(end_url)