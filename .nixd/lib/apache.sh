# Utilities for installations using Apache (apache.org) projects.

locate_apache_mirror() {
    # Print to stdout a full URL matching the closest mirror of given filepath.

    curl https://www.apache.org/dyn/closer.cgi?path=$1 |\
        grep -i -A 10 'we suggest the following' |\
        grep href | head -1 | cut -f 2 -d '"'
}
