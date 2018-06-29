from conan.packager import ConanMultiPackager
import copy
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(archs = ["x86_64"])
    builder.add_common_builds(pure_c=False)
    items = []
    for item in builder.items:
        if item.settings["compiler"] == "Visual Studio":
            if item.settings["compiler.runtime"] == "MT" or item.settings["compiler.runtime"] == "MTd":
                # Ignore MT runtime
                continue
        new_options = copy.copy(item.options)
        new_options["VTK:qt"] = True
        items.append([item.settings, new_options, item.env_vars, item.build_requires])
    builder.items = items
    builder.run()
