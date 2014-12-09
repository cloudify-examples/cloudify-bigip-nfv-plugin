from cloudify.exceptions import NonRecoverableError
from external import bigsuds
from external.bigsuds import ParseError, MethodNotFound, ArgumentError

import sys

""" Convenience class to proxy calls for BIP. We may externalize this in the future
to support additional BIG-IP functionality.

This class uses bigsuds, which simplifies invoking BIG-IP operations through
BIG-IP's SOAP interface (SOAP communication is done by suds). Currently, bigsuds
doesn't have much documentation but most of it can be figured out by reading this:

https://devcentral.f5.com/articles/getting-started-with-bigsuds-ndasha-new-python-library-for-icontrol

You may have to look at the LocalLB iControl API specification to figure out certain
fields and values required by bigsuds:

https://devcentral.f5.com/wiki/iControl.LocalLB.ashx

Exception handling: by default, all exceptions raised past this module are deemed recoverable
(as per Cloudify's design). Therefore, we'll only dedicate special handling to exceptions that
should be treated as NON-recoverable. """


class BigIpProxy:
    def __init__(self, hn, un, ps):
        self.hostname = hn
        self.username = un
        self.password = ps

    def _get_bip(self):
        return bigsuds.BIGIP(hostname=self.hostname,
                             username=self.username,
                             password=self.password)

    """ Get the LTM canonical pool name from its ID. """

    @staticmethod
    def get_pool_name(pool_id):
        return '/Common/%s' % pool_id

    """ Convenience method to obtain a dictionary represending a pool member. """

    @staticmethod
    def _get_member(address, port):
        return {'address': address,
                'port': port}

    """ Creates a pool.

        pool_id: str
            the pool's identifier
        lb_method: str
            the load balancing method to use; must be one of the enumerated values
            available for 'LBMethod' """

    def create_pool(self, pool_id, lb_method):
        pool_name = self.get_pool_name(pool_id)
        try:
            self._get_bip().LocalLB.Pool.create_v2([pool_name], [lb_method], [[]])
        except (ParseError, MethodNotFound, ArgumentError):
            tpe, value, tb = sys.exc_info()
            raise NonRecoverableError, NonRecoverableError(str(value)), tb

    """ Adds a member to a previously-created pool.

        pool_id: str
            the pool's identifier
        address: str
            the member's address (hostname or IP address)
        port: int
            the member's port """

    def add_member(self, pool_id, address, port):
        pool_name = self.get_pool_name(pool_id)
        try:
            self._get_bip().LocalLB.Pool.add_member_v2([pool_name], [[self._get_member(address, port)]])
        except (ParseError, MethodNotFound, ArgumentError):
            tpe, value, tb = sys.exc_info()
            raise NonRecoverableError, NonRecoverableError(str(value)), tb

    """ Removes a member from a previously-created pool.

        pool_id: str
            the pool's identifier
        address: str
            the member's address (hostname or IP address)
        port: int
            the member's port """

    def remove_member(self, pool_id, address, port):
        pool_name = self.get_pool_name(pool_id)
        try:
            self._get_bip().LocalLB.Pool.remove_member_v2([pool_name], [[self._get_member(address, port)]])
        except (ParseError, MethodNotFound, ArgumentError):
            tpe, value, tb = sys.exc_info()
            raise NonRecoverableError, NonRecoverableError(str(value)), tb

    """ Deletes a pool.

        pool_id: str
            the pool's identifier """

    def delete_pool(self, pool_id):
        pool_name = self.get_pool_name(pool_id)
        try:
            self._get_bip().LocalLB.Pool.delete_pool([pool_name])
        except (ParseError, MethodNotFound, ArgumentError):
            tpe, value, tb = sys.exc_info()
            raise NonRecoverableError, NonRecoverableError(str(value)), tb
