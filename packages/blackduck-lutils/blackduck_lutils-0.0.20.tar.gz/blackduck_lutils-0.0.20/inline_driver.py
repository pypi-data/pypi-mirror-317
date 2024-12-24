import argparse
from blackduck import Client
from blackduck_lutils import license_conflicts
import sys
import json

def parse_command_args():

    parser = argparse.ArgumentParser("license_conflicts")
    parser.add_argument("-u", "--base-url",     required=False, help="Hub server URL e.g. https://your.blackduck.url")
    parser.add_argument("-t", "--token-file",   required=False, help="File containing access token")
    parser.add_argument("-nv", "--no-verify",   action='store_false', help="Disable TLS certificate verification")
    mux = parser.add_mutually_exclusive_group()
    mux.add_argument("-ldd", "--license-data-download", action='store_true', help="Download license data into a file specified with -ld/--license-data parameter")
    mux.add_argument("-pn", "--project-name", required=False, help="Project Name")
    parser.add_argument("-pv", "--project-version-name", required=False, help="Project Version Name")
    mux.add_argument("-sbom", required=False, help="SBOM File to process")
    parser.add_argument("-ld", "--license-data", required=False, default='license_data.json', help="Local license data storage")
    parser.add_argument("-o", "--output-file", required=False, default=None, help="Output file name for license conflict report output")
    parser.add_argument("--fail-unknown-licenses", required=False, action='store_true', help="Stop processing if Unknown licenses are present")
    parser.add_argument("--skip-terms", required=False, default=None, help="License terms to exclude from analysis, Comma separated list")
    parser.add_argument("--print-defined-terms", required=False, action='store_true', help="Print all defined license terms and exit")
    parser.add_argument("--xls", required=False, action='store_true', help="Use EXCEL format instead of CSV")
    return parser.parse_args()

def main():
    args = parse_command_args()

    with open(args.token_file) as tf:
        token = tf.readline().strip()

    bd = Client(base_url=args.base_url, token=token, verify=args.no_verify, timeout=60.0, retries=4)

    license_conflict_data = license_conflicts.generate_license_conflict_report(bd=bd,
                                                project_name=args.project_name,
                                                project_version_name=args.project_version_name,
                                                license_data_file=args.license_data)
                                                
    # Note that if output file is not specified, it will be generated automatically as
    # ProjectName_Version_YYYY-MM-DD_HHMMSS.(csv|xlsx)
    # print (json.dumps(license_conflict_data, indent=2))
    print (f"data array length {len(license_conflict_data)}")

if __name__ == "__main__":
    sys.exit(main())