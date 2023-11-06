#!/usr/bin/env bash

install_main() {
    sudo cp etc/systemd/system/hallowdonna.service /etc/systemd/system

    sudo cp -a knocker.py /usr/bin/

    sudo systemctl enable hallowdonna

    sudo systemctl start hallowdonna
}
export -f install_main

if [ "${BASH_SOURCE[0]}" = "${0}" ] || [ "${BASH_SOURCE[0]}" = '--' ]; then
    set -o errexit
    set -o pipefail
    set -o nounset

    if [ "${1:-}" = '-v' ]; then
        printf '%s\n' "INFO: $(basename "$0")::${LINENO}: Verbose output enabled" 1>&2
        shift
        set -o xtrace
    fi

    install_main "$@"
fi
