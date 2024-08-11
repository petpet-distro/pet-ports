import os
import json
import re

json_path = 'packages.json'
petbuild_folder = 'main'

def load_json(path):
    try:
        with open(path, 'r') as file:
            content = file.read()
            if not content:
                return {"repositoryName": "ports", "packages": []}
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: The file {path} contains invalid JSON.")
        return {"repositoryName": "ports", "packages": []}
    except FileNotFoundError:
        print(f"Error: The file {path} does not exist.")
        return {"repositoryName": "ports", "packages": []}

def save_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def extract_info_from_petbuild(file_path):
    info = {}
    with open(file_path, 'r') as file:
        content = file.read()

        pkgname_pattern = re.compile(r'pkgname="([^"]+)"')
        pkgver_pattern = re.compile(r'pkgver="([^"]+)"')
        pkgrdeps_pattern = re.compile(r'pkgrdeps="([^"]+)"')
        pkgbdeps_pattern = re.compile(r'pkgbdeps="([^"]+)"')

        pkgname_match = pkgname_pattern.search(content)
        pkgver_match = pkgver_pattern.search(content)
        pkgrdeps_match = pkgrdeps_pattern.search(content)
        pkgbdeps_match = pkgbdeps_pattern.search(content)

        if pkgname_match:
            info['pkgname'] = pkgname_match.group(1)
        if pkgver_match:
            info['pkgver'] = pkgver_match.group(1)
        if pkgrdeps_match:
            info['pkgdeps'] = pkgrdeps_match.group(1)
        else:
            info['pkgdeps'] = 'none'
        if pkgbdeps_match:
            info['pkgdeps'] += ' ' + pkgbdeps_match.group(1)
    return info

def update_packages_json(json_data, petbuild_folder):
    packages = json_data.get('packages', [])
    petbuild_folders = [f for f in os.listdir(petbuild_folder) if os.path.isdir(os.path.join(petbuild_folder, f))]

    for folder in petbuild_folders:
        petbuild_path = os.path.join(petbuild_folder, folder, 'PETBUILD')
        if os.path.isfile(petbuild_path):
            info = extract_info_from_petbuild(petbuild_path)

            existing_pkg = next((pkg for pkg in packages if pkg['pkgname'] == info['pkgname']), None)
            if existing_pkg:
                existing_pkg.update(info)
            else:
                packages.append(info)

    json_data['packages'] = packages

def main():
    json_data = load_json(json_path)

    update_packages_json(json_data, petbuild_folder)

    save_json(json_data, json_path)
    print(f'Updated {json_path} successfully.')

if __name__ == '__main__':
    main()
