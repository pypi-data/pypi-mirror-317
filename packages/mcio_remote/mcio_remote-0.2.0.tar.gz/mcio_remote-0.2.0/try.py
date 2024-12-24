import sys
from typing import Any
from pathlib import Path

import minecraft_launcher_lib as mll

from mcio_remote import instance
from mcio_remote import server
from mcio_remote import world


def gen() -> None:
    world = world.World("test")
    world.generate("HelloWorld", "1.21.3")


def java() -> None:
    jvm_ver = "java-runtime-delta"
    inst_dir = "/Users/joe/.mcio/instances/mc1"
    c = mll.command.get_minecraft_command(
        "1.21.3", inst_dir, mll.utils.generate_test_options()
    )
    print(c)
    print(1, mll.runtime.get_executable_path(jvm_ver, inst_dir))
    # 1 /Users/joe/.mcio/instances/mc1/runtime/java-runtime-delta/mac-os-arm64/java-runtime-delta/jre.bundle/Contents/Home/bin/java
    print(2, mll.runtime.get_jvm_runtimes())
    # 2 ['java-runtime-alpha', 'java-runtime-beta', 'java-runtime-delta', 'java-runtime-gamma', 'java-runtime-gamma-snapshot', 'jre-legacy', 'minecraft-java-exe']
    print(3, mll.runtime.get_installed_jvm_runtimes(inst_dir))
    # 3 ['java-runtime-delta']
    print(4, mll.runtime.get_jvm_runtime_information(jvm_ver))
    # 4 {'name': '21.0.3', 'released': datetime.datetime(2024, 4, 23, 9, 46, 27, tzinfo=datetime.timezone.utc)}
    print(5, mll.runtime.get_version_runtime_information("1.21.3", inst_dir))
    # 5 {'name': 'java-runtime-delta', 'javaMajorVersion': 21}


def server_test() -> None:
    s = server.Server()
    s.install_server()
    s.run()
    s.send_command("help")
    s.stop()


def main() -> None:
    fn_name = sys.argv[1]
    globals()[fn_name]()


main()
