import pkg_resources

ignore = {"pyngrok"}  # pacotes que você quer ignorar

with open("requirements.txt", "w") as f:
    for dist in pkg_resources.working_set:
        if dist.project_name not in ignore:
            f.write(f"{dist.project_name}=={dist.version}\n")
