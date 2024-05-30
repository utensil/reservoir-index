import pathlib
import json
import matplotlib.pyplot as plt

# use pathlib to walk each directory recursively to get a file named builds.json, and get the relative path, use a generator to yield the relative path
def get_builds_json_files(root_dir):
    root_dir = pathlib.Path(root_dir)
    for path in root_dir.rglob('builds.json'):
        yield path.relative_to(root_dir)

# parse the json as an array, for each element, if "outcome" is "success", adds 1 to the resulting dict with key which has the value of key "toolchain" of the element
def get_successful_builds_by_toolchain(builds_json_files):
    result = {}
    count = 0
    for file in builds_json_files:
        with open(file) as f:
            builds = json.load(f)
            for build in builds:
                if build['outcome'] == 'success':
                    toolchain = build['toolchain']
                    result[toolchain] = result.get(toolchain, 0) + 1
        count += 1
    return result, count


# write the main function to use the functions above to get the result and plot it using matplotlib
def main(root_dir):
    builds_json_files = get_builds_json_files(root_dir)
    successful_builds_by_toolchain, total_repos = get_successful_builds_by_toolchain(builds_json_files)

    # set the title of the plot to be the total number of repositories
    plt.title(f'Total Repositories: {total_repos}')

    # the x-axis should rotate 90 degrees to make it readable
    plt.xticks(rotation=90)
    plt.bar(successful_builds_by_toolchain.keys(), successful_builds_by_toolchain.values())
    plt.show()

if __name__ == '__main__':
    main('.')
