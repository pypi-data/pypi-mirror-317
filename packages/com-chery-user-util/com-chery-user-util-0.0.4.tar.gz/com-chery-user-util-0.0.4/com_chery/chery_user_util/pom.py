PROJECT_PKG_VERSION = '0.0.4'

INCLUDE_FILES = [
    'user_util.py',
]

PROJECT_PKG_NAME = 'chery_user_util'
PYPI_PKG_NAME = ('com_' + PROJECT_PKG_NAME).replace('_', '-')
CHERY_POM_ROOT_REQUIRED_VERSION = '0.0.1'


if __name__ == '__main__':
    import chery_pom_tool
    chery_pom_tool.build_and_upload(
        PROJECT_PKG_NAME,
        PYPI_PKG_NAME,
        CHERY_POM_ROOT_REQUIRED_VERSION,
        PROJECT_PKG_VERSION,
        INCLUDE_FILES,
    )
