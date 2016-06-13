__author__ = 'Dmitriy Korsakov'
__doc__ = 'Server management'
import copy
from scalrctl import commands
from scalrctl import click


class RebootServer(commands.Action):

    epilog = "Example: scalr-ctl server reboot --serverId <ID> --hard"

    post_template = {
        "serverRebootOptions": {"hard": True}
    }

    def get_options(self):
        hlp = "Reboot type. By default it does soft reboot unless this \
        option is set to true. Beware that some types of the instances do \
        not support soft reboot."
        hard_reboot = click.Option(('--hard', 'hard'), is_flag=True, default=False, help=hlp)
        options = super(RebootServer, self).get_options()
        options.append(hard_reboot)
        return options


    def pre(self, *args, **kwargs):
        """
        before request is made
        """
        hard = kwargs.pop("hard", None)
        post_data = copy.deepcopy(self.post_template)
        post_data["serverRebootOptions"]["hard"] = hard
        kv = {"import-data": post_data}
        kv.update(kwargs)
        arguments, kw = super(RebootServer, self).pre(*args, **kv)
        return arguments, kw


class ResumeServer(commands.Action):

    epilog = "Example: scalr-ctl server resume --serverId <ID>"
    post_template = {}

    def pre(self, *args, **kwargs):
        """
        before request is made
        """
        kv = {"import-data": {}}
        kv.update(kwargs)
        arguments, kw = super(ResumeServer, self).pre(*args, **kv)
        return arguments, kw


class SuspendServer(commands.Action):

    epilog = "Example: scalr-ctl server suspend  --serverId <ID>"
    post_template = {}

    def pre(self, *args, **kwargs):
        """
        before request is made
        """
        kv = {"import-data": {}}
        kv.update(kwargs)
        arguments, kw = super(SuspendServer, self).pre(*args, **kv)
        return arguments, kw


class TerminateServer(commands.Action):

    epilog = "Example: scalr-ctl server terminate --serverId <ID> --force"
    post_template = {
        "serverTerminationOptions": {"hard": True}
    }

    def get_options(self):
        hlp = "It is used to terminate the Server immediately ignoring scalr.system.server_terminate_timeout."
        hard_terminate = click.Option(('--force', 'hard'), is_flag=True, default=False, help=hlp)
        options = super(TerminateServer, self).get_options()
        options.append(hard_terminate)
        return options


    def pre(self, *args, **kwargs):
        """
        before request is made
        """
        hard = kwargs.pop("hard", None)
        post_data = copy.deepcopy(self.post_template)
        post_data["serverTerminationOptions"]["hard"] = hard
        kv = {"import-data": post_data}
        kv.update(kwargs)
        arguments, kw = super(TerminateServer, self).pre(*args, **kv)
        return arguments, kw
