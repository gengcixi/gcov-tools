#! /usr/bin/env python3
"""A util to parse gcov visual coverage html reports."""

import argparse
import json
import os
import sys

_BASH_RESET_CODE = '\033[0m'
_ERROR_CODE = '\033[1;31m'
_SUCCEED_CODE = '\033[1;32m'

_COVERAGE_JSON_FILE = 'kernel-coverage-data.json'


def _ParArgs(argv):
    """Parse command line arguments.

    :param argv: A list of arguments.
    :return: An argspace.Namespace class instance holding parsed args.
    """
    global parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-c",
                        '--coverage-dir',
                        type=str,
                        default=None,
                        help="Directory of coverage report.")

    parser.add_argument(
        "-j",
        '--json-file',
        type=str,
        default=_COVERAGE_JSON_FILE,
        help=
        "Generated JSON file of coverage data. (Default is 'kernel-coverage-data.json')"
    )

    parser.add_argument('-f',
                        '--filter',
                        type=str,
                        default=None,
                        help="Filter of modules to generate coverage data.")

    return parser.parse_args(argv)


def GenerateJsonResult(coverage_result_dir, coverage_json_file):
    """
    Parse all modules' html reports under drivers directory, write lines and functions coverage data into a JSON file.

    Example:

        "nvmem": {
            "Line_coverPreLo": "41.6 %",
            "Line_coverNumLo": "348 / 837",
            "Functions_coverPreLo": "40.8 %",
            "Functions_coverNumLo": "31 / 76",
            "module_type": "drivers",
            "report_index": "coverage_result/drivers/nvmem/index.html"
        },

    :param kernel_coverage_dir: kernel coverage result directory
    "param json_out_dir: out directory of the JSON file
    :return: path of JSON file
    """

    results = dict()
    index_html = os.path.join(coverage_result_dir, 'index.html')

    if not os.path.exists(index_html):
        raise Exception('{} is missing!'.format(index_html))

    results = _AnalyzeCoverageData(index_html, 'drivers')

    if results:
        with open(coverage_json_file, 'w') as j_file:
            json.dump(results,
                      j_file,
                      indent=2,
                      sort_keys=True,
                      ensure_ascii=False)
        return True
    return False


def _AnalyzeCoverageData(index_html, module_type):
    """Use ``BeautifulSoup`` to parse the html file of the report and return the coverage statistic data.

    The format of coverage data is as follows:
        <center>
        <table width="80%" cellpadding=1 cellspacing=1 border=0>
            <tr>
                <td class="coverFile"><a href="drivers/nvmem/index.html">drivers/nvmem</a></td>
                <td align="center" class="coverBar"><table border="0" cellpadding="1" cellspacing="0">...</table></td>
                <td class="coverPerLo">41.6 %</td>
                <td class="coverNumLo">348 / 837</td>
                <td class="coverPerLo">40.8 %</td>
                <td class="coverNumLo">31 / 76</td>
            </tr>
        </table>
        </center>
    """
    from bs4 import BeautifulSoup

    coverage_dict = {}
    with open(index_html, 'r') as html:
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

        module_tags = [
            item.parent for item in soup.find_all(**{'class': "coverFile"})
        ]

        for module in module_tags:
            module_path = ''
            report_index = ''
            data_list = []
            coverage_tds = [
                child for child in module.find_all('td', recursive=False)
                if not 'coverBar' in child['class']
            ]
            for c_td in coverage_tds:
                if 'coverFile' in c_td['class']:
                    module_path = c_td.a.string
                    report_index = os.path.join(os.path.dirname(index_html),
                                                c_td.a['href'])
                else:
                    # Replace &nbsp;
                    data_list.append(c_td.string.replace(u'\xa0', u' '))

            class_list = [
                'Line_coverPreLo', 'Line_coverNumLo', 'Functions_coverPreLo',
                'Functions_coverNumLo'
            ]

            module_cov_data = dict(zip(class_list, data_list))
            module_cov_data.update({
                'module_type': module_type,
                'report_index': report_index
            })

            if args.filter and not module_path.startswith(args.filter):
                continue

            coverage_dict.setdefault(
                module_path[module_path.find('/') + 1:].replace('/', '_'),
                module_cov_data)

    return coverage_dict


if __name__ == "__main__":
    global args
    args = _ParArgs(sys.argv[1:])
    if not args.coverage_dir:
        print('{}Missing coverage directory!{}'.format(_ERROR_CODE,
                                                       _BASH_RESET_CODE))
        parser.print_usage()
        exit(1)

    if GenerateJsonResult(args.coverage_dir, args.json_file):
        print('Coverage JSON file:',
              '{}{}{}'.format(_SUCCEED_CODE, args.json_file, _BASH_RESET_CODE))
    else:
        print('{}Failed to generate JSON file!{}'.format(
            _ERROR_CODE, _BASH_RESET_CODE))
