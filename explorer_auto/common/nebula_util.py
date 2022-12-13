from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

from explorer_auto.common.yaml_util import read_yaml_by_key,generate_random_csv


"""
    :param ngql: 需要执行的nGQL
    :return: 返回执行结果
"""
def execute_nebula_query(ngql):
    # define a config
    config = Config()
    config.max_connection_pool_size = 10
    # init connection pool
    connection_pool = ConnectionPool()
    # if the given servers are ok, return true, else return false
    nebula_server = read_yaml_by_key("graphd_ip").split(":")
    ok = connection_pool.init([(nebula_server[0], nebula_server[1])], config)

    # option 2 with session_context, session will be released automatically
    with connection_pool.session_context(read_yaml_by_key("graphd_username"), read_yaml_by_key("graphd_plaintext_password")) as session:
        session.execute('USE {}'.format(read_yaml_by_key("result_database")))
        result = session.execute(ngql)
        return result
        

    # close the pool
    connection_pool.close()


