# coding:utf-8
import os

import platform

from cosmos.env.core import EnvOperationSetter, EnvOperationList

from cosmos.util.log import get_logger

logger = get_logger(__name__)
logger.debug('loading module {0} at {1}'.format(__name__, __file__))

bundle_dir = os.path.dirname(os.path.abspath(__file__))
platform_name = platform.system().lower()

environ_data = [
    ('LXDCC_GUI_BASE', '{root}', 'set'),
    #
    ('PYTHONPATH', '{root}/script/python', 'append_to_path'),
]

environ_data_linux = []

environ_data_windows = []

environ_variants = dict(
    root=bundle_dir
)

ops = EnvOperationList()

for i_key, i_value, i_opt_type in environ_data:
    ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))

if platform_name == 'linux':
    for i_key, i_value, i_opt_type in environ_data_linux:
        ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))
elif platform_name == 'windows':
    for i_key, i_value, i_opt_type in environ_data_windows:
        ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))

ops.export_for_config_base()
