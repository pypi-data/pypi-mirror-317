import muuusiiik.util as msk
from   pytest import raises

# ============
# MOCK UP ENV
# ============
class MockEnv:
    env_path    = 'tests/_data'
    f_configure = f'{env_path}/system.conf'

    def create_configure(conf):
        msk.configure.save(conf, MockEnv.f_configure)

    def create_contents(contents):
        for k, v in contents.items():
            f = f'{MockEnv.env_path}/{k}'
            msk.data.save(v, f)

    def remove_env():
        msk.data.rm(MockEnv.env_path)


# =============
# CORE TESTING
# =============
def test_mock_content():
    # init env
    contents  = {
                  'file01.vocab': ['f1', 'f2', 'f3'],
                  'file02.vocab': ['v1', 'v2', 'v3', 'v4']
                }
    env_path  = MockEnv.env_path
    configure = {'vocab': [f'{env_path}/{k}' for k, v in contents.items()]}
    MockEnv.create_configure(configure)
    MockEnv.create_contents(contents)
    # assertation
    assert set(msk.data.ls(MockEnv.env_path)) == set(['file01.vocab', 'file02.vocab', 'system.conf'])
    # reset env
    MockEnv.remove_env()
    assert msk.data.exist(MockEnv.env_path) == False


def test_configure_loader_load_content():
    # init env
    contents  = {
                  'file01.vocab': ['f1', 'f2', 'f3'],
                  'file02.vocab': ['v1', 'v2', 'v3', 'v4']
                }
    env_path  = MockEnv.env_path
    configure = {'vocab': [f'{env_path}/{k}' for k, v in contents.items()]}
    MockEnv.create_configure(configure)
    MockEnv.create_contents(contents)
    # load configure
    env_path    = MockEnv.env_path
    f_configure = MockEnv.f_configure
    conf        = msk.configure_loader(f_configure)
    # assertation
    assert conf.path              == f_configure
    assert conf.content           == configure
    assert len(conf.get('vocab')) == 2
    assert [f.split('/')[-1] for f in conf.get('vocab')] == ['file01.vocab', 'file02.vocab']
    # reset env
    MockEnv.remove_env()


def test_configure_loader_load_non_existing_configure():
    f_configure = 'not-existing-file.conf'
    with raises(FileNotFoundError):
        conf = msk.configure_loader(f_configure)


def test_configure_loader_load_none_and_get_empty_class_as_reset():
    f_configure = None
    conf = msk.configure_loader(f_configure)
    assert conf.path    == None
    assert conf.content == {}

