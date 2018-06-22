import os
from scrapy.utils.conf import closest_scrapy_cfg


def get_prot_root():
    '''get project root dir url

    Returns:
        proj_root_dir: project root dir

    '''
    return os.path.dirname(closest_scrapy_cfg())


def get_abs_url(rel_url):
    '''

    Args:
        rel_url: relative url

    Returns:
        url: absolute url

    '''
    return os.path.normpath(os.path.join(get_prot_root(), rel_url))
