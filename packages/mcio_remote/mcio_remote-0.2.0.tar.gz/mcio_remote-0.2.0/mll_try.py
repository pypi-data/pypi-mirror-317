import subprocess
import minecraft_launcher_lib as mll


def main() -> None:
    mc_dir = "/Users/joe/.mcio/instances/mc1"
    mc_cmd = mll.command.get_minecraft_command(
        "1.21.3", mc_dir, mll.utils.generate_test_options()
    )
    print(" ".join(mc_cmd))
    # subprocess.run(mc_cmd, cwd=mc_dir)


main()
