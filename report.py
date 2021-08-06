from github import Github
import csv
import argparse


languages = set()
name = set()


def github_connection(token):
    try:
        github_auth = Github(token)
        login = github_auth.get_user().login
        email = github_auth.get_user().email
    except Exception:
        print("Invalid Token")
        return False
    return github_auth


def validate_arguments(args_parser):
    args_parser.add_argument('--organization')
    args_parser.add_argument('--token')
    args = args_parser.parse_args()
    is_valid = args.organization is not None and args.token is not None
    return is_valid, args


def data_assemble(git_object, organization):
    userdata = {}
    org = git_object.get_organization(organization)
    repos = org.get_repos()
    for repo in repos:
        for contributor in repo.get_contributors():
            if contributor.name is not None:
                if contributor.login in userdata:
                    userdata[contributor.login]["repos"].add(repo.name)
                    for key in repo.get_languages().keys():
                        userdata[contributor.login]["languages"].add(key)
                else:
                    userdata[contributor.login] = {}
                    userdata[contributor.login]['name'] = contributor.name
                    userdata[contributor.login]['email'] = contributor.email
                    userdata[contributor.login]["repos"] = set()
                    userdata[contributor.login]["repos"].add(repo.name)
                    userdata[contributor.login]["languages"] = set()
                    for key in repo.get_languages().keys():
                        userdata[contributor.login]["languages"].add(key)
    return userdata


def data_export(userdata):
    csv_columns = ['Login', 'Name', 'Email', 'Repositories', 'Languages']
    with open("report.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for key, values in userdata.items():
            login = key
            for key, value in values.items():
                if key == 'name':
                    name = value
                if key == 'email':
                    email = value
                if key == 'repos':
                    repos = " "
                    for repo in value:
                        repos = repos + " " + repo
                if key == 'languages':
                    languages = " "
                    for language in value:
                        languages = languages + " " + language
            writer.writerow(
                {'Login': login, 'Name': name, 'Email': email, 'Repositories': repos, 'Languages': languages})


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    is_arg_valid, args = validate_arguments(args_parser)
    if is_arg_valid:
        git_object = github_connection(str(args.token))
        organization = str(args.organization)
        org = git_object.get_organization(organization)
        repos = org.get_repos()
        data = data_assemble(git_object, organization)
        data_export(data)
    else:
        print("Missing Argument")
