# Templates

This repo is a collection of template project structures to get started with popular programming languages and frameworks. These templates are designed to have sane defaults, but with configuration options in plain sight so they're easy to adjust.

# Using a template
```
./init.py <template_name> <target_project_name>
```

- template name -- is one of the available templates to get started with. - target project name -- The `/workspaces` folder to initialize the template in.

# Writing a new template
Add a new folder whose name becomes the template name. Inside the template create a `init_config.json` file. This file defines how the template will be initialized. The json file should have the following shape
```
{
    "merge_json": List[str],
    "merge_list": List[str],
    "append_file": List[str],
    "copy_file": List[str],
    "copy_dir": List[str],
    "init_script": str
}
```

- merge_json - Copy this file to a file of the same path in the target. The json keys will be merged into an existing file if the file already exists.
- merge_list - Copy this file to a file of the same path in the target. Each line will be merged if it doesn't exist in the target file.
- append_file - Append the contents of this file into the target file. Create if it doesn't exist.
- copy_file - Copy the contents of this file to the target. Overwrite if it exists.
- copy_dir - Copy the contents of the directory to the target.
- init_script - Run this script once post init. The first arg is the target_project_root.

See the `python` template for an example.
