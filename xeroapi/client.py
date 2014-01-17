"""
Provides a API client module for private XERO Api applications.
"""

from M2Crypto import RSA
import base64
import hashlib
import oauth2
import json
import xml2json
import urllib

class SignatureMethod_RSA(oauth2.SignatureMethod):
    """
    Provides an RSA signature method for oauth2 since there is none.

    PS: Code inherited from:
    https://github.com/simplegeo/python-oauth2/issues/#issue/16
    """
    name = "RSA-SHA1"

    def __init__(self, key_path):
        """
        Instantiates the RSA signature method instance.
        """
        super(oauth2.SignatureMethod, self).__init__()
        self.key_path = key_path
        self.RSA = RSA.load_key(key_path)

    def signing_base(self, request):
        """
        Calculates the string that needs to be signed.
        """
        sig = (oauth2.escape(request.method),
               oauth2.escape(request.normalized_url),
               oauth2.escape(request.get_normalized_parameters()))
        raw = '&'.join(sig)
        return raw

    def sign(self, request, consumer, token):
        """
        Returns the signature for the given request.

        Note: consumer and token are not used, but are there to
        fit in with call in oauth2 module.
        """
        raw = self.signing_base(request)
        digest = hashlib.sha1(raw).digest()
        signature = self.RSA.sign(digest, algo="sha1")
        encoded = base64.b64encode(signature)
        return encoded

class XeroClientRequestException(Exception):
    """
    Indicates that there is a problem with the XERO API client
    request.
    """
    pass

class XeroClientBadRequestException(Exception):
    """
    Indicates that the request has failed Xero validation.
    """
    pass

class XeroClientNotFoundException(Exception):
    """
    Indicates that the reference object (either by ID or Number) does not exist.
    """
    pass

class XeroClientNotImplementedException(Exception):
    """
    Indicates that the endpoint doesn't accept the attempted method.
    """
    pass

class XeroClientUnknownException(Exception):
    """
    Indicates that there occured an unknown exception due to unknown
    status code.
    """
    pass

class Client(oauth2.Client):
    """
    Provides a API client class for private XERO Api applications.
    """

    def __init__(self, access_token, access_secret, cert_filepath, xero_api_url="https://api.xero.com/api.xro/2.0/"):
        """
        Instantiates a API client class instance for private XERO Api applications.
        """
        # Keep the API url for future use:
        if xero_api_url[-1] == "/":
            self._xero_api_url = xero_api_url
        else:
            self._xero_api_url = "%s/" % (xero_api_url)

        # Instantiate the OAuth consumer:
        oauth_consumer = oauth2.Consumer(access_token, access_secret)

        # Instantiate the OAuth token:
        oauth_token = oauth2.Token(access_token, access_secret)

        # Call super constructor:
        oauth2.Client.__init__(self, oauth_consumer, oauth_token)

        # Set the signature method to RSA:
        self.set_signature_method(SignatureMethod_RSA(cert_filepath))

    def get(self, resource_uri):
        """
        ``GET``s a resource by its internal API URI.
        """
        # Attempt to retrieve the response
        try:
            response_header, response_content = self.request("%s%s" % (self._xero_api_url, resource_uri), method="GET")
        except:
            raise XeroClientRequestException

        # Check if there is an error:
        if response_header["status"] == "400":
            raise XeroClientBadRequestException(response_content)
        elif response_header["status"] == "404":
            raise XeroClientNotFoundException(response_content)
        elif response_header["status"] == "501":
            raise XeroClientNotImplementedException(response_content)
        elif response_header["status"] != "200":
            raise XeroClientUnknownException(response_content)

        # Convert the data into a JSON object:
        json_string = xml2json.xml2json(response_content)

        # Convert the json_string to a Python dictionary and return:
        return json.loads(json_string)

    def put(self, resource_uri, content):
        """
        ``PUT``s a resource by its internal API URI and contents.
        """
        # Attempt to retrieve the response
        try:
            response_header, response_content = self.request("%s%s" % (self._xero_api_url, resource_uri), method="PUT", body=content)
        except:
            raise XeroClientRequestException

        # Check if there is an error:
        if response_header["status"] == "400":
            raise XeroClientBadRequestException(response_content)
        elif response_header["status"] == "404":
            raise XeroClientNotFoundException()
        elif response_header["status"] == "501":
            raise XeroClientNotImplementedException(response_content)
        elif response_header["status"] != "200":
            raise XeroClientUnknownException(response_content)

        # Convert the data into a JSON object:
        json_string = xml2json.xml2json(response_content)

        # Convert the json_string to a Python dictionary and return:
        return json.loads(json_string)

    def post(self, resource_uri, content):
        """
        ``POST``s a resource by its internal API URI and contents.
        """
        # Attempt to retrieve the response
        try:
            response_header, response_content = self.request("%s%s" %
                                                             (self._xero_api_url,
                                                              resource_uri),
                                                             method="POST",
                                                             body=urllib.urlencode({"xml": content}))
        except:
            raise XeroClientRequestException

        # Check if there is an error:
        if response_header["status"] == "400":
            raise XeroClientBadRequestException(response_content)
        elif response_header["status"] == "404":
            raise XeroClientNotFoundException()
        elif response_header["status"] == "501":
            raise XeroClientNotImplementedException(response_content)
        elif response_header["status"] != "200":
            raise XeroClientUnknownException(response_content)

        # Convert the data into a JSON object:
        json_string = xml2json.xml2json(response_content)

        # Convert the json_string to a Python dictionary and return:
        return json.loads(json_string)
