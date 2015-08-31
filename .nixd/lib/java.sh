# Utilities for installations using Java/JVM.

check_java_version() {
    # Check if `java` is available and is version 1.7+.

    if ! java_version=$(java -version 2>&1); then
        nixd_error "No java found."
        if [ -n "$java_version" ]; then
            nixd_error $java_version
        fi
        return 1
    fi

    if [ -z "$java_version" ]; then
        nixd_echo '`java -version` is empty.'
        return 1
    elif echo $java_version | grep -q '\bversion "1.7'; then
        nixd_echo "Found Java 1.7."
    elif echo $java_version | grep -q '\bversion "1.8'; then
        nixd_echo "Found Java 1.8."
    else
        nixd_error "Java version is unsupported:"
        nixd_error $java_version
        return 1
    fi
}
