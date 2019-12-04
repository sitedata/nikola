"""Check that full archives build and are correct."""

import os
import shutil

import pytest

import nikola.plugins.command.init
from nikola import __main__

from ..base import cd
from .helper import add_post_without_text, patch_config
from .test_empty_build import (  # NOQA
    test_avoid_double_slash_in_rss, test_check_files, test_check_links,
    test_index_in_sitemap)



@pytest.mark.parametrize("path", [
    ['archive.html'],
    ['2012', 'index.html'],
    ['2012', '03', 'index.html'],
    ['2012', '03', '30', 'index.html'],
], ids=["overall", "year", "month", "day"])
def test_full_archive(build, output_dir, path):
    """Check existance of archive pages"""
    expected_path = os.path.join(output_dir, *path)
    assert os.path.isfile(expected_path)


@pytest.fixture(scope="module")
def build(target_dir):
    """Fill the site with demo content and build it."""
    init_command = nikola.plugins.command.init.CommandInit()
    init_command.copy_sample_site(target_dir)
    init_command.create_configuration(target_dir)

    src1 = os.path.join(os.path.dirname(__file__),
                        '..', 'data', '1-nolinks.rst')
    dst1 = os.path.join(target_dir, 'posts', '1.rst')
    shutil.copy(src1, dst1)

    add_post_without_text(os.path.join(target_dir, 'posts'))

    patch_config(target_dir, ('# CREATE_FULL_ARCHIVES = False',
                              'CREATE_FULL_ARCHIVES = True'))

    with cd(target_dir):
        __main__.main(["build"])
