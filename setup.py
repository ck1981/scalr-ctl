from distutils.core import setup
from distutils.command.install import install


try:
    from post_setup import main as post_install
except ImportError:
    post_install = lambda: None


class _install(install):
    def run(self):
        install.run(self)
        post_install()


if __name__ == '__main__':

    setup(
        name='scalr-ctl',
        version='1.0',
        packages = [
            "scalrctl",
            "scalrctl.commands",
        ],
        include_package_data=True,
        install_requires=[
            'Click',
            'prettytable',
            'pyyaml',
            'requests'
        ],
        entry_points='''
            [console_scripts]
            scalr-ctl=scalrctl.app:cli
        ''',
        #cmdclass=dict(install=_install)
    )


# pip install PyYAML --global-option='--without-libyaml'