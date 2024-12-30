from ovinc_client.components.base import Component, Endpoint
from ovinc_client.constants import RequestMethodEnum


class Auth(Component):
    """
    Auth
    """

    def __init__(self, client, base_url: str):
        self.verify_ticket = VerifyTicketEndpoint(client, base_url)


class VerifyTicketEndpoint(Endpoint):
    """
    VerifyTicket
    """

    method = RequestMethodEnum.POST.value
    path = "/account/verify_ticket/"
