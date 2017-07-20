from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(
        username="bilke",
        upload="https://ogs.jfrog.io/ogs/api/conan/conan"
    )
    builder.add_common_builds(pure_c=False)
    #builder.add({"arch": "x86_64", "build_type": "Release"}, {"VTK:mpi": True})
    # builder.add({"arch": "x86_64", "build_type": "Release"}, {"VTK:qt": True})
    # builder.add({"arch": "x86_64", "build_type": "Debug"}, {"VTK:qt": True})
    builder.run()
