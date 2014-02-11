import win32service

from oslo.config import cfg

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.plugins import base

LOG = logging.getLogger(__name__)

class CmfIntegrationPlugin(base.BasePlugin):
  def _start_cmf_agent(self):
    scm = win32service.OpenSCManager(None, None,  win32service.SC_MANAGER_ALL_ACCESS)
    cmfsvc = win32service.OpenService(scm, "CMFAgent", win32service.SC_MANAGER_ALL_ACCESS)
    LOG.info('Changing CMF service startup type to automatic')
    win32service.ChangeServiceConfig(cmfsvc, win32service.SERVICE_NO_CHANGE,
                                     win32service.SERVICE_AUTO_START,
                                     win32service.SERVICE_NO_CHANGE,
                                     None, None, 0, None, None, None, None)
    LOG.info('Starting CMF service')
    win32service.StartService(cmfsvc, None)
    win32service.CloseServiceHandle(cmfsvc)

  def execute(self, service, shared_data):
    LOG.info('Starting CMF Integration Plugin...')
    try:
      self._start_cmf_agent()
    except Exception as ex:
      LOG.error('Exception during CMF activation: %s', ex)
 
    return (base.PLUGIN_EXECUTION_DONE, False)
